# 🎨 AI Prompt Architect Pro

> **Fikirlerinizi profesyonel AI prompt'larına dönüştürün — Türkçe veya İngilizce.**

Bir Streamlit uygulaması olarak çalışan bu proje; kullanıcının girdiği metni Ollama (LLaMA 3.2) ile geliştirilmiş bir prompt'a çevirir, ardından Stability AI API'si üzerinden yüksek kaliteli görsel oluşturur.

---

## ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| 🌐 **Otomatik Çeviri** | Türkçe girdi otomatik olarak İngilizce'ye çevrilir |
| 🤖 **LLM Prompt Geliştirme** | Ollama (LLaMA 3.2) ile kısa fikir → detaylı profesyonel prompt |
| 🖼️ **3 Farklı Model** | Stability AI Ultra, Core ve SD3 Large |
| 🎭 **17 Stil Seçeneği** | Anime, Cinematic, Photographic, Pixel Art ve daha fazlası |
| 📐 **9 En-Boy Oranı** | 1:1'den 21:9'a, story formatından ultra geniş ekrana |
| 📚 **Görsel Kütüphanesi** | Oluşturulan görseller otomatik kaydedilir, filtrelenebilir |
| 💾 **PNG İndirme** | Her görsel tek tıkla indirilebilir |

---

## 🏗️ Proje Yapısı

```
ai-prompt-architect/
│
├── main.py           # Streamlit arayüzü ve uygulama akışı
├── ai_engine.py      # Ollama & Stability AI entegrasyonları
├── utils.py          # Çeviri, kütüphane kayıt/yükleme işlemleri
├── config.py         # API ayarları, model/stil/oran seçenekleri, system prompt
│
├── ai_image_library/ # Oluşturulan görseller ve metadata (otomatik oluşur)
│   ├── 20250101_120000.png
│   └── 20250101_120000.json
│
├── .env              # API anahtarları (Git'e ekleme!)
└── requirements.txt
```

---

## ⚙️ Kurulum

### 1. Repoyu klonla

```bash
git clone https://github.com/kullanici-adi/ai-prompt-architect.git
cd ai-prompt-architect
```

### 2. Bağımlılıkları yükle

```bash
pip install -r requirements.txt
```

### 3. `.env` dosyasını oluştur

```env
STABILITY_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> API anahtarını [Stability AI Platform](https://platform.stability.ai/account/credits) üzerinden alabilirsiniz.

### 4. Ollama'yı kur ve çalıştır

```bash
# Ollama kurulumu: https://ollama.com
ollama pull llama3.2
ollama serve
```

### 5. Uygulamayı başlat

```bash
streamlit run main.py
```

---

## 🚀 Kullanım

```
1. Fikrinizi yazın  →  Türkçe veya İngilizce, kısa veya uzun
2. Stil seçin       →  Photographic, Anime, Cinematic...
3. En-boy seçin     →  Instagram, YouTube, Story...
4. Model seçin      →  Ultra (en kaliteli), Core (dengeli), SD3 (hızlı)
5. "Prompt Geliştir" →  LLaMA 3.2 prompt'u profesyonelleştirir
6. "Görsel Oluştur" →  Stability AI görseli üretir ve kütüphaneye kaydeder
```

---

## 💡 Model & Kredi Karşılaştırması

| Model | Kredi | En İyi Kullanım |
|---|---|---|
| **Ultra** | 8 kredi | En yüksek kalite, detaylı sanat eserleri |
| **Core** | 3 kredi | Günlük kullanım, hızlı prototipleme |
| **SD3 Large** | 6.5 kredi | Metin içeren görseller, yaratıcı çalışmalar |

---

## 🛠️ Kullanılan Teknolojiler

- **[Streamlit](https://streamlit.io/)** — Web arayüzü
- **[Ollama + LLaMA 3.2](https://ollama.com/)** — Yerel LLM ile prompt geliştirme
- **[Stability AI API](https://stability.ai/)** — Görsel üretimi
- **[deep-translator](https://github.com/nidhaloff/deep-translator)** — Türkçe → İngilizce çeviri
- **[Pillow](https://python-pillow.org/)** — Görsel işleme

---

## 📋 Gereksinimler

```
streamlit
requests
Pillow
deep-translator
python-dotenv
```

---

## ⚠️ Bilinen Sorunlar & Çözümler

**Ollama bağlantı hatası?**
```bash
# Ollama'nın çalışıp çalışmadığını kontrol et
ollama serve
```

**Stability API hatası?**
- `.env` dosyasındaki API anahtarını kontrol edin
- [Kredi durumunuzu](https://platform.stability.ai/account/credits) kontrol edin
- Rate limit'e takılmış olabilirsiniz, birkaç dakika bekleyin

---

<div align="center">
  <sub>Built with ❤️ using Streamlit + Ollama + Stability AI</sub>
</div>