
import json
import ollama
from typing import Any


# class Engine:
#     def __init__(self, 

#                  backend:str="ollama",
#                  model_id:str="qwen2.5:3b",
#                  api_key:str=""):
        
#         self.backend = backend
#         self.api_key = api_key
#         self.model_id = model_id
        
#         if self.backend == 'gemini' and api_key:
#             # Use Gemini
#             print("gemini not implemented yet")
#             return
#             from google import genai
            
            
#             self.client = genai.Client(api_key=api_key)
#             self.llm = 'gemini-2.5-flash'
            
#             print(f"✓ Gemini Backend Initialized: {self.client}")
            
#         else:
#             # Use Ollama
            
#             self.backend = 'ollama'
#             self.ollama_model = self.model_id 
            
#             # Check if Ollama is available
#             try:
#                 import ollama
#                 ollama.show(self.ollama_model)
#                 print(f"✓ Using Ollama ({self.ollama_model})")
                
#             except:
#                 print(f"⚠ Ollama model '{self.ollama_model}' not found")
#                 print("  Run: ollama pull qwen3:0.6b")
                
             
#     def _generate(self,_identity:str, prompt:Any,_use_ollama:bool=True, send_json:bool=False) -> str:
#         """Generate response from AI backend with persistent ROSA persona."""
    
#     # Construct the message history with the system prompt at the top
#         messages = [
#         {'role': 'system', 'content': _identity},
#         {'role': 'user', 'content': f"{prompt}"}
#     ] 
        
#         if self.backend == 'gemini' and not _use_ollama:
#             try:
#                 from google.genai import types

#                 print("BEFORE RESPONSES:", messages[:8])
#                 response = self.client.models.generate_content(
#                     model=self.llm, 
#                     contents=prompt, # or whole history depends
#                     config=types.GenerateContentConfig( 
#                         system_instruction=_identity,
#                         #response_mime_type="application/json"
#                     )
#                 )
                
                
#                 return response.text or '[]'
#             except Exception as e:
#                 print(f"[engine.generate gemini] ⚠️ Gemini error: {e}")
#                 if "503" in str(e):
#                     print("⚠️ Gemini service unavailable, switching to ollama, please hold...")
#                     self.backend = 'ollama'
#                     return self._generate(_identity, prompt, _use_ollama=True)  # Retry with Ollama
#                 return '[]'
        
#         else:  # Ollama

#             client = ollama.Client(timeout=60.0)
#             kwargs = {
#     'model': self.ollama_model,
#     'messages': messages,
#     'options': {'temperature': 0.2}
# }

#             if send_json:
#                 kwargs['format'] = 'json'
#                 messages[0]['content'] += "\nRespond ONLY with valid JSON."

#             response = client.chat(**kwargs)

#             content = response['message']['content']

#             if send_json:
#                 try:
#                     return json.loads(content)
#                 except Exception as e:
#                     print("JSON parse failed:", e)
#                     print(content)
#                     return {}

#             return content
                
    
#     def _parse_json(self, text: str, default: Any = None) -> Any:
#         """Robust JSON parsing."""
#         if not text or text.strip() == '':
#             return default if default is not None else []
        
#         text = text.strip()
        
#         if "```json" in text:
#             text = text.split("```json")[1].split("```")[0].strip()
#         elif "```" in text:
#             text = text.split("```")[1].split("```")[0].strip()
        
#         # Try to parse
#         try:
#             parsed = json.loads(text)
#             return parsed
#         except json.JSONDecodeError as e:
#             print(f"⚠ JSON parse error: {e}")
#             print(f"  Raw text: {text[:200]}...")
#             return default if default is not None else []
        

class Engine:
    def __init__(
        self,
        backend: str = "ollama",
        model_id: str = "qwen2.5:3b",
        api_key: str = ""
    ):

        self.backend = backend
        self.api_key = api_key
        self.model_id = model_id

        if self.backend == 'gemini' and api_key:
            print("gemini not implemented yet")

        else:
            self.backend = 'ollama'
            self.ollama_model = self.model_id

            try:
                ollama.show(self.ollama_model)
                print(f"✓ Using Ollama ({self.ollama_model})")

            except Exception:
                print(f"⚠ Ollama model '{self.ollama_model}' not found")
                print(f"Run: ollama pull {self.ollama_model}")

    def _generate(
        self,
        _identity: str,
        prompt: Any,
        _use_ollama: bool = True,
        send_json: bool = False
    ) -> Any:

        messages = [
            {
                'role': 'system',
                'content': _identity
            },
            {
                'role': 'user',
                'content': str(prompt)
            }
        ]

        # GEMINI
        if self.backend == 'gemini' and not _use_ollama:
            print("Gemini not implemented")
            return None

        # OLLAMA
        try:
            client = ollama.Client(timeout=60.0)

            if send_json:
                messages[0]['content'] += (
                    "\nRespond ONLY with valid JSON."
                )

            kwargs = {
                'model': self.ollama_model,
                'messages': messages,
                'options': {
                    'temperature': 0.2
                }
            }

            if send_json:
                kwargs['format'] = 'json'

            response = client.chat(**kwargs)

            content = response['message']['content']

            if send_json:
                return self._parse_json(content, default={})

            return content

        except Exception as e:
            print(f"⚠ Ollama generation error: {e}")

            return {} if send_json else ""

    def _parse_json(
        self,
        text: str,
        default: Any = None
    ) -> Any:

        if not text or text.strip() == '':
            return default if default is not None else {}

        text = text.strip()

        # Remove markdown fences
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()

        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        try:
            return json.loads(text)

        except json.JSONDecodeError as e:
            print(f"⚠ JSON parse error: {e}")
            print(f"Raw response:\n{text}")

            return default if default is not None else {}