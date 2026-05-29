
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
            from google import genai
            
            
            self.client = genai.Client(api_key=api_key)
            self.llm = 'gemini-2.5-flash'
            
            print(f"✓ Gemini Backend Initialized: {self.client}")

        else:
            self.backend = 'ollama'
            self.ollama_model = self.model_id

            try:
                ollama.show(self.ollama_model)
                print(f"✓ Using Ollama ({self.ollama_model})")
            except:
                try:
                    self.ollama_model = "qwen3:0.6b"
                    ollama.show(self.ollama_model)
                    print(f"✓ Using Ollama ({self.ollama_model})")

                except Exception:
                    print(f"⚠ Ollama model '{self.ollama_model}' not found")
                    print(f"Run: ollama pull {self.ollama_model}")
    def old_generate(
        self,
        _identity: str,
        prompt: Any,
        _use_ollama: bool = False,
        send_json: bool = False
    ) -> Any:

        # 1. Normalize prompt logic so both Ollama and Gemini handle histories/strings
        # If it's a string representation of a dict/list, safely evaluate it
        if isinstance(prompt, str) and (prompt.startswith('{') or prompt.startswith('[')):
            try:
                import ast
                prompt = ast.literal_eval(prompt)
            except Exception:
                pass  # Keep as string if parsing fails

        # Build standard messages list for Ollama
        messages = [
            {'role': 'system', 'content': _identity}
        ]
        
        if isinstance(prompt, list):
            for turn in prompt:
                # Map custom keys ('user'/'response') to what LLMs expect
                role = 'user' if 'user' in turn else 'assistant'
                content = turn.get('user') or turn.get('response') or turn.get('content', '')
                messages.append({'role': role, 'content': str(content)})
        elif isinstance(prompt, dict):
            # If it's a single dict turn like {'user': '...', 'response': '...'}
            user_text = prompt.get('user', '')
            response_text = prompt.get('response', '')
            if user_text: messages.append({'role': 'user', 'content': str(user_text)})
            if response_text: messages.append({'role': 'assistant', 'content': str(response_text)})
        else:
            messages.append({'role': 'user', 'content': str(prompt)})

        # GEMINI BRANCH
        if self.backend == 'gemini' and not _use_ollama:
            try:
                from google.genai import types

                # Translate our cleaned messages list into Gemini SDK types.Content structures
                gemini_contents = []
                for msg in messages:
                    if msg['role'] == 'system':
                        continue # System instructions belong in the config, not contents
                    
                    # Convert 'assistant' back to Gemini's expected role string: 'model'
                    gemini_role = 'model' if msg['role'] == 'assistant' else 'user'
                    
                    gemini_contents.append(
                        types.Content(
                            role=gemini_role,
                            parts=[types.Part.from_text(text=msg['content'])]
                        )
                    )

                print("BEFORE RESPONSES:", messages[:8])
                response = self.client.models.generate_content(
                    model=self.llm, 
                    contents=gemini_contents, # Safely mapped objects!
                    config=types.GenerateContentConfig( 
                        system_instruction=_identity,
                        response_mime_type="application/json" if send_json else None
                    )
                )
                
                return response.text or '[]'
                
            except Exception as e:
                print(f"[engine.generate gemini] ⚠️ Gemini error: {e}")
                if "503" in str(e):
                    print("⚠️ Gemini service unavailable, switching to ollama, please hold...")
                    self.backend = 'ollama'
                    return self._generate(_identity, prompt, _use_ollama=True, send_json=send_json) 
                return '[]'
        
        # OLLAMA BRANCH
        else:
            try:
                import ollama
                client = ollama.Client(timeout=60.0)

                if send_json:
                    messages[0]['content'] += "\nRespond ONLY with valid JSON."

                # Convert roles to match what Ollama expects ('assistant', not 'model')
                ollama_messages = []
                for m in messages:
                    role = 'assistant' if m['role'] == 'model' else m['role']
                    ollama_messages.append({'role': role, 'content': m['content']})

                kwargs = {
                    'model': self.ollama_model,
                    'messages': ollama_messages,
                    'options': {'temperature': 0.2}
                }

                if send_json:
                    kwargs['format'] = 'json'

                response = client.chat(**kwargs)
                content = response['message']['content']

                if send_json:
                    return self._parse_json(content, default={})

                return content

            except Exception as e:
                print(f"⚠️ Ollama generation error: {e}")
                return {} if send_json else ""
    def _generate(
        self,
        _identity: str,
        prompt: Any,
        _use_ollama: bool = False,
        send_json: bool = False
    ) -> Any:
        #print(f"INSIDE _GENERATE _identity: {_identity}")
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

        # GEMINI BRANCH
        
        if self.backend == 'gemini' and not _use_ollama:
            try:
                from google.genai import types

                # 1. Transform raw prompt history structures into Gemini SDK native types
                gemini_contents = []

                # Handle a list of historical turns
                if isinstance(prompt, list):
                    for turn in prompt:
                        role = 'model' if 'response' in turn or turn.get('role') == 'assistant' else 'user'
                        text_content = turn.get('user') or turn.get('response') or turn.get('content', '')
                        if text_content:
                            gemini_contents.append(
                                types.Content(role=role, parts=[types.Part.from_text(text=str(text_content))])
                            )
                
                # Handle a single turn dict: {'user': 'hi', 'response': '...'}
                elif isinstance(prompt, dict):
                    if 'user' in prompt:
                        gemini_contents.append(
                            types.Content(role='user', parts=[types.Part.from_text(text=str(prompt['user']))])
                        )
                    if 'response' in prompt:
                        gemini_contents.append(
                            types.Content(role='model', parts=[types.Part.from_text(text=str(prompt['response']))])
                        )
                
                # Handle basic text strings
                else:
                    gemini_contents.append(
                        types.Content(role='user', parts=[types.Part.from_text(text=str(prompt))])
                    )

                print("BEFORE RESPONSES: Cleaned and structured contents successfully.")

                # 2. Fire the generation call with explicit configs
                response = self.client.models.generate_content(
                    model=self.llm, 
                    contents=gemini_contents,  # No more raw dicts!
                    config=types.GenerateContentConfig( 
                        system_instruction=_identity,
                        # None completely omits the key so Gemini defaults to raw text
                        response_mime_type="application/json" if send_json else None
                    )
                )
                
                return response.text or '[]'

            except Exception as e:
                print(f"[engine.generate gemini] ⚠️ Gemini error: {e}")
                if "503" in str(e):
                    print("⚠️ Gemini service unavailable, switching to ollama...")
                    self.backend = 'ollama'
                    return self._generate(_identity, prompt, _use_ollama=True, send_json=send_json)
                return '[]'
        else:
            # OLLAMA
            try:
             
                client = ollama.Client(timeout=60.0)

                if send_json:
                    messages[0]['content'] += (
                        "\nRespond ONLY with valid JSON."
                    )
                    print("Sending JSON")
                
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
                print("Response and content are created successfully")
                if send_json:
                
                    return self._parse_json(content, default={})
                print(f'\n\n\t\u2022CONTENT: {content}')
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