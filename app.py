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
            data = json.loads(body)
            text = data.get("text", "")
            model = data.get("mode", "encode").lower() # Varsayılan olarak encode modu kullanılır

            if model == "encode": # Encode modu kullanılır
                base64_content = base64.b64encode(text.encode("utf-8")).decode("utf-8")
                response = {"success": True, "base64Content": base64_content}
            elif model == "decode": # Decode modu kullanılır
                decoded_text = base64.b64decode(text).decode("utf-8")
                response = {"success": True, "decodedText": decoded_text}
            else: # Hatalı mod kullanılırsa hata mesajı döndürülür
                response = {"success": False, "error": "Invalid model"}

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
