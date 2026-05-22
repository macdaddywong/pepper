import urllib2
import json
# 10.2.166.8
# pepper ip: 172.17.10.113
# Use the IP that worked in your ping
pc_ip = "10.2.166.8" 
url = "http://" + pc_ip + ":11434/api/generate"

def call_ollama(prompt):
    # Data formatted for Ollama's API
    data = json.dumps({
        "model": "qwen2.5-coder:7b",
        "prompt": prompt,
        "stream": False
    })
    
    try:
        # Note: headers are important for Ollama to accept the JSON
        req = urllib2.Request(url, data=data)
        req.add_header('Content-Type', 'application/json')
        
        response = urllib2.urlopen(req, timeout=120) # 10 second timeout
        body = response.read()
        return json.loads(body)['response']
    except Exception as e:
        return "Error: " + str(e)

print "--- Contacting Ollama at " + pc_ip + " ---"
print call_ollama("Say 'Hello Leroy, I am online' in one short sentence.")