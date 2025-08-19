from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64
from urllib.parse import urlparse, parse_qs

class Base64API(BaseHTTPRequestHandler):
    def _send_response(self, response):
        self.send_response(200) # HTTP 200 OK
        self.send_header("Content-Type", "application/json") # İçerik tipi olarak JSON belirtiyoruz
        self.end_headers() # headers'ı bitiriyoruz
        self.wfile.write(json.dumps(response).encode("utf-8")) # JSON'u byte çevirip gönderiyoruz

    def process_text(self, text, mode): # Metni işleme fonksiyonu
        try:
            mode = mode.lower()
            if mode == "encode": # Encode modu kullanılır
                result = base64.b64encode(text.encode("utf-8")).decode("utf-8")
            elif mode == "decode": # Decode modu kullanılır
                result = base64.b64decode(text).decode("utf-8")
            else: # Hatalı mod kullanılırsa hata mesajı döndürülür
                result = {"success": False, "error": f"Unknown mode: {mode}"}
            return {"success": True, "result": result}
        except Exception as e: # Hata durumunda hata mesajı döndürülür
            return {"success": False, "error": str(e)}


    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0)) # POST body'nin uzunluğunu alıyoruz
        body = self.rfile.read(content_length) # POST body'ni okuyoruz
        try:
            data = json.loads(body) # POST body'yi JSON'a çeviriyoruz
            text = data.get("text", "") # JSON'dan "text" alanını alıyoruz
            mode = data.get("mode", "encode").lower() # JSON'dan "mode" alanını alıyoruz ve küçük harfe çeviriyoruz
            result = self.process_text(text, mode)
        except Exception as e: # Hata durumunda hata mesajı döndürülür
            result = {"success": False, "error": str(e)}
            self._send_response(result)

    def do_GET(self):
        parsed_url = urlparse(self.path) # URL'yi ayrıştırıyoruz
        query_params = parse_qs(parsed_url.query) # URL'deki query parametrelerini alıyoruz
        text = query_params.get("text", [""])[0] # Query parametresinden "text" alanını alıyoruz
        mode = query_params.get("mode", ["encode"])[0].lower() # Query parametresinden "mode" alanını alıyoruz ve küçük harfe çeviriyoruz
        result = self.process_text(text, mode) # Metni işleme fonksiyonunu çağırıyoruz
        self._send_response(result) # Yanıtı gönderiyoruz

# Serveri başlat
def run(server_class=HTTPServer, handler_class=Base64API, port=8080): # Port numarasını 8080 olarak belirledik
    server_address = ("0.0.0.0", port) # Sunucu adresini ve portunu belirliyoruz
    httpd = server_class(server_address, handler_class) # HTTPServer'ı başlatıyoruz
    print(f"🚀 Server running on port {port}...") 
    httpd.serve_forever() # Sunucuyu sonsuz döngüde çalıştırıyoruz

if __name__ == "__main__":
    run()
