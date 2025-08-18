from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import base64

class Base64API(BaseHTTPRequestHandler):
    def _send_response(self, response):
        self.send_response(200) # HTTP 200 OK
        self.send_header("Content-Type", "application/json") # İçerik tipi olarak JSON belirtiyoruz
        self.end_headers() # headers'ı bitiriyoruz
        self.wfile.write(json.dumps(response).encode("utf-8")) # JSON'u byte çevirip gönderiyoruz

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) # POST body'ni okuyoruz
        try:
            data = json.loads(body) # POST edilen JSON'u dictionary'ye çeviriyoruz
            text = data.get("text", "") # JSON'dan "text" alanını alıyoruz
            base64Content = base64.b64encode(text.encode("utf-8")).decode("utf-8") # Metni base64'e çeviriyoruz
            success = True if base64Content else False # Başarılı bir dönüş olup olmadığını kontrol ediyoruz

            response = {
                "success": success,
                "base64Content": base64Content
            }
        except Exception as e:
            response = {"success": False, "error": str(e)} # Hata durumunda hata mesajını döndürüyoruz

        self._send_response(response) # JSON yanıtını gönderiyoruz

# Serveri başlat
def run(server_class=HTTPServer, handler_class=Base64API, port=8080): # Port numarasını 8080 olarak belirledik
    server_address = ("0.0.0.0", port) # Sunucu adresini ve portunu belirliyoruz
    httpd = server_class(server_address, handler_class) # HTTPServer'ı başlatıyoruz
    print(f"🚀 Server running on port {port}...") 
    httpd.serve_forever() # Sunucuyu sonsuz döngüde çalıştırıyoruz

if __name__ == "__main__":
    run()
