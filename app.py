from http.server import BaseHTTPRequestHandler, HTTPServer
import json, base64
from urllib.parse import urlparse, parse_qs
import socketserver

class Base64API(BaseHTTPRequestHandler): # BaseHTTPRequestHandler sınıfını kullanarak HTTP isteklerini işlemek için bir sınıf oluşturuyoruz
    def _send(self, r): # Yanıtı göndermek için bir fonksiyon oluşturuyoruz
        self.send_response(200) # HTTP 200 OK yanıtı gönderiyoruz
        self.send_header("Content-Type", "application/json") # İçerik tipi olarak JSON belirtiyoruz
        self.end_headers() # Yanıtın başlıklarını gönderiyoruz
        self.wfile.write(json.dumps(r, ensure_ascii=False).encode()) # JSON'u byte çevirip gönderiyoruz
    
    def process(self, t, m): # Metni işleme fonksiyonu
        try:
            if m == "encode": return {"success": True, "result": base64.b64encode(t.encode()).decode()} # Encode modu kullanılır
            elif m == "decode": return {"success": True, "result": base64.b64decode(t).decode()} # Decode modu kullanılır
            else: return {"success": False, "error": f"Unknown mode: {m}"} # Hatalı mod kullanılırsa hata mesajı döndürülür
        except Exception as e: return {"success": False, "error": str(e)} # Hata durumunda hata mesajı döndürülür
    
    def do_POST(self):
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0)))) # POST body'yi JSON'a çeviriyoruz
            self._send(self.process(data.get("text", ""), data.get("mode", "encode").lower())) # Metni işleme fonksiyonunu çağırıyoruz
        except json.JSONDecodeError as e: # JSON decode hatası için özel kontrol
            self._send({"success": False, "error": f"Invalid JSON: {e}"})

    def do_GET(self): # GET isteklerini işlemek için bir fonksiyon oluşturuyoruz
        params = parse_qs(urlparse(self.path).query) # URL'deki query parametrelerini alıyoruz
        self._send(self.process(params.get("text", [""])[0], params.get("mode", ["encode"])[0].lower())) # Metni işleme fonksiyonunu çağırıyoruz

# Multi-threaded HTTP Server sınıfı
class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    server = ThreadedHTTPServer(("0.0.0.0", 8080), Base64API)
    print("🚀 Multi-threaded server running on port 8080...")
    server.serve_forever()
