# Base64 API (HTTPServer)

Saf Python ile geliştirilmiş minimal Base64 kodlama/çözme API'si. GET ve POST metodlarını destekler.

## Özellikler

- ✅ **Base64 Encode/Decode**: Metinleri Base64 formatına çevirme ve çözme
- ✅ **GET/POST Desteği**: Query parametreleri ve JSON body
- ✅ **Hata Yönetimi**: Kapsamlı hata yanıtları
- ✅ **Hafif**: Sadece 25 satır kod!

## Hızlı Başlangıç

```bash
python app.py
```

## Kullanım

### POST Metodu (JSON Body)

**Encode:**
```bash
curl -X POST http://localhost:8080 \
     -H "Content-Type: application/json" \
     -d '{"text":"Merhaba Dünya","mode":"encode"}'
```

**Yanıt:**
```json
{
  "success": true,
  "result": "TWVyaGFiYSBEw7xueWE="
}
```

**Decode:**
```bash
curl -X POST http://localhost:8080 \
     -H "Content-Type: application/json" \
     -d '{"text":"TWVyaGFiYSBEw7xueWE=","mode":"decode"}'
```

**Yanıt:**
```json
{
  "success": true,
  "result": "Merhaba Dünya"
}
```

### GET Metodu (Query Parametreleri)

**Encode:**
```bash
curl "http://localhost:8080/?text=Merhaba%20Dünya&mode=encode"
```

**Decode:**
```bash
curl "http://localhost:8080/?text=TWVyaGFiYSBEw7xueWE%3D&mode=decode"
```

## API Parametreleri

### POST Request Body
```json
{
  "text": "İşlenecek metin",
  "mode": "encode|decode"
}
```

### GET Query Parametreleri
- `text`: İşlenecek metin (URL encoded)
- `mode`: İşlem modu (`encode` veya `decode`)

## Hata Yanıtları

### Geçersiz Mod
```json
{
  "success": false,
  "error": "Unknown mode: invalid"
}
```

### Geçersiz Base64
```json
{
  "success": false,
  "error": "Incorrect padding"
}
```

### Geçersiz JSON
```json
{
  "success": false,
  "error": "Invalid JSON: Expecting value: line 1 column 1 (char 0)"
}
```

## Kod Örnekleri

### JavaScript
```javascript
// Encode
const response = await fetch('http://localhost:8080', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: 'Merhaba!', mode: 'encode'})
});
const data = await response.json();
console.log(data.result);
```

### Python
```python
import requests

# Encode
response = requests.post('http://localhost:8080', 
    json={'text': 'Merhaba!', 'mode': 'encode'})
print(response.json()['result'])

# Decode
response = requests.post('http://localhost:8080', 
    json={'text': 'TWVyaGFiYSgh', 'mode': 'decode'})
print(response.json()['result'])
```

### cURL Örnekleri
```bash
# Encode
curl -X POST http://localhost:8080 \
     -H "Content-Type: application/json" \
     -d '{"text":"Test","mode":"encode"}'

# Decode
curl -X POST http://localhost:8080 \
     -H "Content-Type: application/json" \
     -d '{"text":"VGVzdA==","mode":"decode"}'

# GET encode
curl "http://localhost:8080/?text=Test&mode=encode"
```

## Sunucu Bilgileri

- **Port**: 8080
- **Host**: 0.0.0.0
- **Metodlar**: GET, POST
- **Yanıt Formatı**: JSON

## Kod Yapısı

API sadece 25 satır kod ile geliştirilmiştir:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, base64
from urllib.parse import urlparse, parse_qs

class Base64API(BaseHTTPRequestHandler):
    def _send(self, response):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode())

    def process(self, text, mode):
        try:
            if mode == "encode":
                return {"success": True, "result": base64.b64encode(text.encode()).decode()}
            elif mode == "decode":
                return {"success": True, "result": base64.b64decode(text).decode()}
            else:
                return {"success": False, "error": f"Unknown mode: {mode}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def do_POST(self):
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            self._send(self.process(data.get("text", ""), data.get("mode", "encode").lower()))
        except json.JSONDecodeError as e:
            self._send({"success": False, "error": f"Invalid JSON: {e}"})

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        self._send(self.process(params.get("text", [""])[0], params.get("mode", ["encode"])[0].lower()))

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8080), Base64API)
    print("🚀 Server running on port 8080...")
    server.serve_forever()
```

## Lisans

MIT Lisansı - Açık kaynak ve ücretsiz kullanım.

