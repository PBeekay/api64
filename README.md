# Base64 API 🚀

Saf Python ile geliştirilmiş Base64 kodlama/çözme API'si. Multi-threading desteği ile hızlı çalışır.

## Özellikler

- ✅ Base64 encode/decode
- ✅ GET ve POST desteği
- ✅ Multi-threading
- ✅ 30 satır kod

## Kullanım

```bash
python app.py
```

### POST İstekleri

**Encode:**
```bash
curl -X POST http://localhost:8080 \
     -H "Content-Type: application/json" \
     -d '{"text":"Merhaba","mode":"encode"}'
```

**Decode:**
```bash
curl -X POST http://localhost:8080 \
     -H "Content-Type: application/json" \
     -d '{"text":"TWVyaGFiYQ==","mode":"decode"}'
```

### GET İstekleri

**Encode:**
```bash
curl "http://localhost:8080/?text=Merhaba&mode=encode"
```

**Decode:**
```bash
curl "http://localhost:8080/?text=TWVyaGFiYQ%3D%3D&mode=decode"
```

## Yanıt Formatı

```json
{
  "success": true,
  "result": "TWVyaGFiYQ=="
}
```

## Hata Örneği

```json
{
  "success": false,
  "error": "Unknown mode: invalid"
}
```

## Kod Örnekleri

### JavaScript
```javascript
const response = await fetch('http://localhost:8080', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: 'Hello', mode: 'encode'})
});
const data = await response.json();
console.log(data.result);
```

### Python
```python
import requests

response = requests.post('http://localhost:8080', 
    json={'text': 'Hello', 'mode': 'encode'})
print(response.json()['result'])
```

## Lisans

MIT Lisansı