from http.server import BaseHTTPRequestHandler, HTTPServer
import json, base64
from urllib.parse import urlparse, parse_qs
import socketserver
import logging
from datetime import datetime

# Logging konfigürasyonu
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s', # Log formatı
    handlers=[
        logging.FileHandler('api.log'), # Log dosyası
        logging.StreamHandler() # Konsola log yazdırır
    ]
)
logger = logging.getLogger(__name__)

class Base64API(BaseHTTPRequestHandler): # BaseHTTPRequestHandler sınıfını kullanarak HTTP isteklerini işlemek için bir sınıf oluşturuyoruz
    def _send(self, r): # Yanıtı göndermek için bir fonksiyon oluşturuyoruz
        self.send_response(200) # HTTP 200 OK yanıtı gönderiyoruz
        self.send_header("Content-Type", "text/plain; charset=utf-8") # İçerik tipi olarak text belirtiyoruz
        self.end_headers() # Yanıtın başlıklarını gönderiyoruz
        self.wfile.write(str(r).encode("utf-8")) # Text'i byte çevirip gönderiyoruz
    
    def custom_log_request(self, method, path, status_code, mode):
        """İstek loglarını kaydet"""
        client_ip = self.client_address[0]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        log_message = f"[{timestamp}] {method} {path} - IP: {client_ip} - Status: {status_code} - Mode: {mode}"
        logger.info(log_message)
    
    def process(self, t, m): # Metni işleme fonksiyonu
        try:
            if m == "encode": 
                result = base64.b64encode(t.encode()).decode() # Encode modu kullanılır
            elif m == "decode": 
                result = base64.b64decode(t).decode() # Decode modu kullanılır
            else: 
                result = f"Error: Unknown mode: {m}" # Hatalı mod kullanılırsa hata mesajı döndürülür
            return result
        except Exception as e: 
            return f"Error: {str(e)}" # Hata durumunda hata mesajı döndürülür
    
    def do_POST(self):
        try:
            # POST body'den text'i al (JSON yerine düz text)
            text = self.rfile.read(int(self.headers.get("Content-Length", 0))).decode("utf-8")
            # URL'den mode parametresini al
            params = parse_qs(urlparse(self.path).query)
            mode = params.get("mode", ["encode"])[0].lower()
            
            response = self.process(text, mode) # Metni işleme fonksiyonunu çağırıyoruz
            self._send(response) # Yanıtı gönderiyoruz
            self.custom_log_request("POST", self.path, 200, mode) # Log kaydı
        except Exception as e: # Hata durumunda hata mesajı döndürülür
            error_response = f"Error: {str(e)}"
            self._send(error_response)
            self.custom_log_request("POST", self.path, 400, "error") # Hata log kaydı

    def do_GET(self): # GET isteklerini işlemek için bir fonksiyon oluşturuyoruz
        params = parse_qs(urlparse(self.path).query) # URL'deki query parametrelerini alıyoruz
        response = self.process(params.get("text", [""])[0], params.get("mode", ["encode"])[0].lower()) # Metni işleme fonksiyonunu çağırıyoruz
        self._send(response) # Yanıtı gönderiyoruz
        self.custom_log_request("GET", self.path, 200, params.get("mode", ["encode"])[0]) # Log kaydı

# Multi-threaded HTTP Server sınıfı
class ThreadedHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

if __name__ == "__main__":
    server = ThreadedHTTPServer(("0.0.0.0", 8080), Base64API)
    print("🚀 Multi-threaded server running on port 8080...")
    print("📝 Logs will be saved to 'api.log' file")
    server.serve_forever()
