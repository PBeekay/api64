# Base64 API 🚀

Saf Python ile geliştirilmiş Base64 kodlama/çözme API'si. Multi-threading desteği ve detaylı loglama ile hızlı çalışır.

## ✨ Özellikler

- ✅ Base64 encode/decode
- ✅ GET ve POST desteği
- ✅ Multi-threading
- ✅ Detaylı loglama (api.log dosyası)
- ✅ Plain text POST istekleri
- ✅ Hata yönetimi

## 🚀 Kullanım

```bash
python app.py
```

Server başlatıldığında:
- Port: 8080
- Log dosyası: api.log
- Multi-threaded çalışır

## 📤 POST İstekleri

**Encode:**
```bash
curl -X POST "http://localhost:8080?mode=encode" \
     -H "Content-Type: text/plain" \
     -d "Merhaba Dünya"
```

**Decode:**
```bash
curl -X POST "http://localhost:8080?mode=decode" \
     -H "Content-Type: text/plain" \
     -d "TWVyaGFiYSBEw7xueWE="
```

## 📥 GET İstekleri

**Encode:**
```bash
curl "http://localhost:8080/?text=Merhaba&mode=encode"
```

**Decode:**
```bash
curl "http://localhost:8080/?text=TWVyaGFiYQ%3D%3D&mode=decode"
```

## 📋 Yanıt Formatı

API düz metin (plain text) formatında yanıt verir:

**Başarılı yanıt:**
```
TWVyaGFiYSBEw7xueWE=
```

**Hata durumu:**
```
Error: Invalid base64 string
```

## 📊 Loglama

Tüm istekler `api.log` dosyasına kaydedilir:

```
2024-01-15 10:30:45 - INFO - [2024-01-15 10:30:45] POST /?mode=encode - IP: 127.0.0.1 - Status: 200 - Mode: encode
2024-01-15 10:30:46 - INFO - [2024-01-15 10:30:46] GET /?text=Hello&mode=encode - IP: 127.0.0.1 - Status: 200 - Mode: encode
```

## 💻 Kod Örneği

```python
import requests

# POST isteği (plain text)
response = requests.post('http://localhost:8080?mode=encode', 
    data='Hello World',
    headers={'Content-Type': 'text/plain'})
print(response.text)  # SGVsbG8gV29ybGQ=

# GET isteği
response = requests.get('http://localhost:8080/?text=Hello&mode=encode')
print(response.text)  # SGVsbG8=
```

## 🔧 Parametreler

- `mode`: `encode` veya `decode` (varsayılan: `encode`)
- `text`: GET isteklerinde kodlanacak/çözülecek metin

## 📄 Lisans

MIT Lisansı