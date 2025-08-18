# Base64 API (HTTPServer)

Bu proje, saf Python kullanarak POST ile gönderilen metni Base64’e çeviren minimal bir API sağlar. 

## Kurulum

1. Python 3 yüklü olmalı.
2. `api.py` dosyasını çalıştır:
```bash
python api.py

Kullanım

curl -X POST http://127.0.0.1:8080 \
     -H "Content-Type: application/json" \
     -d "{\"text\":\"merhaba\"}"

Cevap

{
  "success": true,
  "base64Content": "bWVySGFiYQ=="
}

