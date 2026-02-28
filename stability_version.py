import streamlit as st
import requests
import json
import io
import base64
from PIL import Image
import time
from deep_translator import GoogleTranslator
import os
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:3b"

# API KEY GOMULU
STABILITY_API_KEY = "sk-khpr85prAoCnffP8jdDIdKy4nOW1PXr9k7SLMuExILadCSxL"

# Stable Image Ultra endpoint
STABILITY_API_URL = "https://api.stability.ai/v2beta/stable-image/generate/ultra"

# Kütüphane klasörü
LIBRARY_FOLDER = "ai_image_library"
if not os.path.exists(LIBRARY_FOLDER):
    os.makedirs(LIBRARY_FOLDER)

# ============================================================================
# MODEL OPTIONS
# ============================================================================

MODEL_OPTIONS = {
    "Ultra (En Kaliteli - 8 kredi)": {
        "endpoint": "https://api.stability.ai/v2beta/stable-image/generate/ultra",
        "credits": 8
    },
    "Core (Dengeli - 3 kredi)": {
        "endpoint": "https://api.stability.ai/v2beta/stable-image/generate/core",
        "credits": 3
    },
    "SD3 Large (Hızlı - 6.5 kredi)": {
        "endpoint": "https://api.stability.ai/v2beta/stable-image/generate/sd3",
        "credits": 6.5
    }
}

# ============================================================================
# STYLE & ASPECT RATIO OPTIONS
# ============================================================================

STYLE_OPTIONS = {
    "Yok (Doğal)": None,
    "3D Model": "3d-model",
    "Analog Film": "analog-film",
    "Anime": "anime",
    "Cinematic": "cinematic",
    "Comic Book": "comic-book",
    "Digital Art": "digital-art",
    "Enhance": "enhance",
    "Fantasy Art": "fantasy-art",
    "Isometric": "isometric",
    "Line Art": "line-art",
    "Low Poly": "low-poly",
    "Modeling Compound": "modeling-compound",
    "Neon Punk": "neon-punk",
    "Origami": "origami",
    "Photographic": "photographic",
    "Pixel Art": "pixel-art",
    "Tile Texture": "tile-texture"
}




ASPECT_RATIOS = {
    "16:9 (Yatay - Video)": "16:9",
    "1:1 (Kare - Instagram)": "1:1",
    "21:9 (Ultra Geniş)": "21:9",
    "2:3 (Dikey - Portre)": "2:3",
    "3:2 (Klasik Fotoğraf)": "3:2",
    "4:5 (Instagram Portre)": "4:5",
    "5:4 (Klasik Monitör)": "5:4",
    "9:16 (Dikey - Story)": "9:16",
    "9:21 (Ultra Dikey)": "9:21"
}

# ============================================================================
# IMPROVED SYSTEM PROMPT
# ============================================================================

SYSTEM_PROMPT = """You are an expert AI image prompt engineer. Your job is to take an English description and enhance it into a detailed, professional image generation prompt.

CRITICAL RULES:
1. Input is ALREADY in English - just enhance it
2. Consider the user's selected STYLE and ASPECT RATIO
3. Output ONLY valid JSON - no explanations, no markdown

JSON STRUCTURE:
{
  "original_idea": "brief summary of what user wants",
  "enhanced_prompt": "detailed professional prompt in English (150-200 words)",
  "negative_prompt": "things to avoid in the image",
  "style_tags": ["tag1", "tag2", "tag3"],
  "quality_score": 8
}

STYLE-BASED ENHANCEMENT:
- photographic/realistic: "photorealistic, DSLR camera, 85mm lens, professional photography, RAW photo, ultra realistic, natural lighting"
- anime: "anime style, manga art, cel shading, vibrant colors, Japanese animation, detailed linework"
- 3d-model: "3D render, octane render, high detail, perfect topology, clean geometry"
- cinematic: "cinematic lighting, film grain, anamorphic lens, color grading, dramatic shadows"
- digital-art: "digital painting, concept art, highly detailed, artstation trending"

NEGATIVE PROMPT STRATEGY:
- FOR PHOTOGRAPHIC: "cartoon, anime, illustration, painting, drawing, sketch, 3D render, CGI, artificial, blurry, low quality, distorted, bad anatomy, watermark, text"
- FOR ANIME: "photorealistic, 3D, photograph, realistic, blurry, low quality, bad anatomy, extra limbs, watermark, text"
- FOR 3D: "2D, flat, cartoon, anime, photograph, blurry, low quality, bad topology, watermark, text"
- ALWAYS ADD: "ugly, deformed, noisy, blurry, low contrast, distorted"

QUALITY SCORING RULES:
- Basic description (5-6): Simple prompt, minimal details
- Good description (7-8): Technical terms, lighting mentioned
- Excellent description (9-10): Professional terms, composition, style details, mood
Score based on: word count (min 150 words = higher score), technical terms, style integration

Now process the input and return ONLY the JSON."""

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def translate_to_english(text: str) -> str:
    """Türkçe metni İngilizce'ye çevir"""
    try:
        turkish_chars = ['ç', 'ğ', 'ı', 'ö', 'ş', 'ü', 'Ç', 'Ğ', 'İ', 'Ö', 'Ş', 'Ü']
        has_turkish = any(char in text for char in turkish_chars)
        
        if not has_turkish and text.isascii():
            return text
        
        translated = GoogleTranslator(source='tr', target='en').translate(text)
        print("-"*100)
        print(translated)
        return translated
        
    except Exception as e:
        st.warning(f"⚠️ Çeviri hatası: {e}")
        return text


def call_ollama(user_input: str, style: str, aspect_ratio: str) -> dict:
    """Ollama ile prompt geliştirme"""
    try:
        full_prompt = f"{SYSTEM_PROMPT}\n\nUSER INPUT: {user_input}\nSTYLE: {style}\nASPECT RATIO: {aspect_ratio}\n\nJSON OUTPUT:"
        
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": full_prompt,
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            },
            timeout=60
        )
        
        response.raise_for_status()
        data = response.json()
        raw_response = data.get("response", "{}")
        
        cleaned = raw_response.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        
        result = json.loads(cleaned)
        return result
        
    except json.JSONDecodeError as e:
        st.error(f"JSON Parse Hatası: {e}")
        return {
            "error": "JSON parsing failed",
            "raw_response": raw_response[:500]
        }
    except Exception as e:
        st.error(f"Ollama Hatası: {e}")
        return {"error": str(e)}


def generate_image_stability(
    prompt: str,
    model_endpoint: str,
    aspect_ratio: str = "1:1",
    style: str = None,
    output_format: str = "png"
) -> Image.Image:
    """Stability AI ile görsel oluşturma"""
    try:
        headers = {
            "Authorization": f"Bearer {STABILITY_API_KEY}",
            "Accept": "image/*"
        }
        
        # Form data hazırlama
        files = {
            "prompt": (None, prompt),
            "output_format": (None, output_format),
            "aspect_ratio": (None, aspect_ratio)
        }
        
        # Style preset ekle (eğer varsa)
        if style:
            files["style_preset"] = (None, style)
        
        response = requests.post(
            model_endpoint,
            headers=headers,
            files=files,
            timeout=120
        )
        
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            return image
        else:
            st.error(f"API Hatası: {response.status_code}")
            st.error(response.text)
            return None
            
    except Exception as e:
        st.error(f"Görsel oluşturma hatası: {e}")
        return None


def save_to_library(image: Image.Image, prompt: str, metadata: dict):
    """Görseli ve prompt'u kütüphaneye kaydet"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Görsel kaydet
        image_filename = f"{timestamp}.png"
        image_path = os.path.join(LIBRARY_FOLDER, image_filename)
        image.save(image_path)
        
        # Metadata kaydet (JSON)
        metadata_filename = f"{timestamp}.json"
        metadata_path = os.path.join(LIBRARY_FOLDER, metadata_filename)
        
        data = {
            "timestamp": timestamp,
            "prompt": prompt,
            "model": metadata.get("model", "Unknown"),
            "style": metadata.get("style", "None"),
            "aspect_ratio": metadata.get("aspect_ratio", "Unknown"),
            "image_file": image_filename
        }
        
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
        
    except Exception as e:
        st.error(f"Kütüphaneye kayıt hatası: {e}")
        return False


def load_library():
    """Kütüphaneden tüm görselleri yükle"""
    try:
        library_items = []
        
        # Tüm JSON dosyalarını bul
        json_files = [f for f in os.listdir(LIBRARY_FOLDER) if f.endswith('.json')]
        json_files.sort(reverse=True)  # En yeniler önce
        
        for json_file in json_files:
            json_path = os.path.join(LIBRARY_FOLDER, json_file)
            
            with open(json_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Görsel dosyasını kontrol et
            image_path = os.path.join(LIBRARY_FOLDER, metadata['image_file'])
            if os.path.exists(image_path):
                library_items.append({
                    'metadata': metadata,
                    'image_path': image_path
                })
        
        return library_items
        
    except Exception as e:
        st.error(f"Kütüphane yükleme hatası: {e}")
        return []


# ============================================================================
# MODERN STREAMLIT UI
# ============================================================================

def main():
    st.set_page_config(
        page_title="AI Prompt Architect Pro",
        page_icon="🎨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Updated CSS - Siyah Tema
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
        
        * {
            font-family: 'Poppins', sans-serif;
        }
        
        /* Main Background */
        .main {
            background-color: #0a0a0a;
        }
        
        /* Main Header */
        .main-header {
            text-align: center;
            padding: 40px 20px;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border-radius: 20px;
            margin-bottom: 40px;
            box-shadow: 0 10px 40px rgba(15, 52, 96, 0.4);
            animation: fadeInDown 0.8s ease;
        }
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 3em;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .main-header p {
            color: #b8c6db;
            margin: 10px 0 0 0;
            font-size: 1.2em;
            font-weight: 300;
        }
        
        /* Prompt Box */
        .prompt-box {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            padding: 25px;
            border-radius: 15px;
            border-left: 5px solid #0f3460;
            margin: 15px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            transition: transform 0.3s ease;
        }
        
        .prompt-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 20px rgba(15, 52, 96, 0.4);
        }
        
        /* Style Tags */
        .style-tag {
            display: inline-block;
            background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            margin: 5px;
            font-size: 0.9em;
            font-weight: 600;
            box-shadow: 0 2px 10px rgba(15, 52, 96, 0.4);
        }
        
        /* Info Cards */
        .info-card {
            background: #1a1a2e;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            margin: 15px 0;
            border-top: 4px solid #0f3460;
            color: #b8c6db;
        }
        
        .info-card h4 {
            color: white;
        }
        
        /* Animations */
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Button Styling */
        .stButton > button {
            background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 15px 30px;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(15, 52, 96, 0.4);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(15, 52, 96, 0.5);
            background: linear-gradient(135deg, #16213e 0%, #0f3460 100%);
        }
        
        /* Progress Bar */
        .stProgress > div > div {
            background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
        }
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background: #0a0a0a;
            border-right: 1px solid #1a1a2e;
        }
        
        /* Text Input Styling */
        .stTextArea > div > div > textarea {
            border-radius: 10px;
            border: 2px solid #1a1a2e;
            padding: 15px;
            background-color: #0f0f0f;
            color: white;
        }
        
        .stTextArea > div > div > textarea:focus {
            border-color: #0f3460;
            box-shadow: 0 0 0 0.2rem rgba(15, 52, 96, 0.25);
        }
        
        /* Selectbox Styling */
        .stSelectbox > div > div {
            background-color: #0f0f0f;
            border: 2px solid #1a1a2e;
            border-radius: 10px;
        }
        
        /* Metric Styling */
        [data-testid="stMetricValue"] {
            color: white;
        }
        
        /* Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: #0a0a0a;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #1a1a2e;
            color: white;
            border-radius: 10px 10px 0 0;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #0f3460;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🎨 AI Prompt Architect Pro</h1>
            <p>Fikirlerinizi profesyonel prompta dönüştürün • Muhteşem görseller oluşturun</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - Sadeleştirilmiş
    with st.sidebar:
        st.markdown("## ⚙ Ayarlar")
        
        st.markdown("---")
        st.markdown("### 📊 İstatistikler")
        
        if 'generated_count' not in st.session_state:
            st.session_state.generated_count = 0
        
        st.metric("Oluşturulan Prompt", st.session_state.generated_count)
        
        st.markdown("---")
        st.caption("Yapay Zeka Dersi Projesi 2025")
    
    # Main Tabs
    tab1, tab2, tab3 = st.tabs(["Prompt Oluştur", "Kütüphane", " Hakkında"])
    
    with tab1:
        # ===== 1. ADIM: Fikir Girişi =====
        st.markdown("## 📝 1. Adım: Fikrinizi Girin")
        
        user_input = st.text_area(
            "Görsel Fikriniz",
            height=150,
            placeholder="Örnek: Gün batımında sahilde yürüyen romantik bir çift, gerçekçi fotoğraf",
            help="Türkçe veya İngilizce yazabilirsiniz",
            key="user_input"
        )
        
        st.markdown("---")
        
        # ===== 2. ADIM: Görsel Ayarları =====
        st.markdown("## 🎨 2. Adım: Görsel Ayarları")
        
        col_model, col_style, col_aspect = st.columns(3, gap="large")
        
        with col_model:
            selected_model = st.selectbox(
                "🤖 Model Seçin",
                options=list(MODEL_OPTIONS.keys()),
                index=0,  # "Ultra" default
                help="Görsel oluşturma modeli"
            )
        
        with col_style:
            selected_style = st.selectbox(
                "🎭 Stil Seçin",
                options=list(STYLE_OPTIONS.keys()),
                index=0,  # "Yok (Doğal)" default
                help="Görselin genel stili"
            )
        
        with col_aspect:
            selected_aspect = st.selectbox(
                "📐 En-Boy Oranı",
                options=list(ASPECT_RATIOS.keys()),
                index=0,  # "16:9" default
                help="Görselin boyutu"
            )
        
        st.markdown("---")
        
        # Generate button
        generate_btn = st.button(
            "✨ Promptu Geliştir",
            use_container_width=True,
            type="primary"
        )
        
        if generate_btn and user_input:
            # Önceki sonuçları temizle
            if 'prompt_result' in st.session_state:
                del st.session_state['prompt_result']
            if 'confirmed' in st.session_state:
                del st.session_state['confirmed']
            
            with st.spinner("🔄 Türkçe → İngilizce çevriliyor..."):
                english_text = translate_to_english(user_input)
                st.session_state['english_translation'] = english_text
                time.sleep(0.3)
            
            with st.spinner("🤖 AI promptunuzu optimize ediyor..."):
                style_value = STYLE_OPTIONS[selected_style]
                aspect_value = ASPECT_RATIOS[selected_aspect]
                
                result = call_ollama(english_text, selected_style, selected_aspect)
                
                # Sonuçları kaydet
                st.session_state['prompt_result'] = result
                st.session_state['selected_style_key'] = selected_style
                st.session_state['selected_aspect_key'] = selected_aspect
                st.session_state['selected_model_key'] = selected_model
                st.session_state.generated_count += 1
                
                time.sleep(0.5)
        
        elif generate_btn and not user_input:
            st.warning("⚠ Lütfen bir fikir yazın!")
        
        # ===== 3. ADIM: Prompt Düzenleme =====
        if 'prompt_result' in st.session_state:
            result = st.session_state['prompt_result']
            
            if "error" not in result:
                st.markdown("---")
                st.markdown("## ✏ 3. Adım: Prompt'u Düzenleyin")
                
                # Çeviri göster
                if 'english_translation' in st.session_state:
                    st.info(f"🌐 *İngilizce Çeviri:* {st.session_state['english_translation']}")
                
                st.markdown("### Geliştirilmiş Prompt")
                st.caption("Görselde olmasını istediğiniz özellikler (düzenleyebilirsiniz)")
                
                # BU KISMI DEĞİŞTİR - Key'i dinamik yap
                enhanced_prompt = st.text_area(
                    "",
                    value=result.get('enhanced_prompt', ''),
                    height=300,
                    key=f"enhanced_prompt_edit_{st.session_state.generated_count}",  # Dinamik key
                    help="İstediğiniz değişiklikleri yapın",
                    label_visibility="collapsed"
                )
                
                # Style tags
                if 'style_tags' in result:
                    st.markdown("### Stil Etiketleri")
                    tags_html = "".join([f'<span class="style-tag">{tag}</span>' for tag in result['style_tags']])
                    st.markdown(tags_html, unsafe_allow_html=True)
                
                # Quality score
                if 'quality_score' in result:
                    st.markdown("### ⭐ Kalite Skoru")
                    score = result['quality_score']
                    st.progress(score / 10)
                    col_score1, col_score2, col_score3 = st.columns(3)
                    col_score1.metric("Puan", f"{score}/10")
                    col_score2.metric("Karmaşıklık", "Yüksek" if score > 7 else "Orta")
                    col_score3.metric("Detay", "Bol" if score > 8 else "İyi")
                
                st.markdown("---")
                
                # ===== 4. ADIM: Görsel Oluştur =====
                st.markdown("## 🎨 4. Adım: Görseli Oluşturun")
                
                col_info1, col_info2, col_info3, col_info4 = st.columns(4)
                
                with col_info1:
                    st.metric("🤖 Model", st.session_state.get('selected_model_key', 'N/A').split('(')[0].strip())
                
                with col_info2:
                    st.metric("🎭 Stil", st.session_state.get('selected_style_key', 'N/A').split('(')[0].strip())
                
                with col_info3:
                    st.metric("📐 En-Boy", st.session_state.get('selected_aspect_key', 'N/A').split('(')[0].strip())
                
                with col_info4:
                    model_key = st.session_state.get('selected_model_key', 'Ultra (En Kaliteli - 8 kredi)')
                    credits = MODEL_OPTIONS[model_key]['credits']
                    st.metric("💳 Kredi", f"{credits}")
                
                if st.button("🚀 Görseli Oluştur!", use_container_width=True, type="primary"):
                    st.session_state['confirmed'] = True
                    st.session_state['final_positive'] = enhanced_prompt
                    st.rerun()
    
    with tab3:
        st.markdown("## AI Prompt Architect Pro Hakkında")
        
        col_info1, col_info2 = st.columns(2)
        
        with col_info1:
            st.markdown("""
            ### 🎯 Özellikler
            
            ✅ *Akıllı Çeviri*
            - Google Translate ile doğru çeviri
            
            ✅ *Düzenlenebilir Promptlar*
            - Pozitif promptu istediğiniz gibi düzenleyin
            
            ✅ *3 Farklı Model*
            - Ultra, Core, SD3 Large
            
            ✅ *17 Farklı Stil*
            - Photographic, Anime, 3D, Cinematic...
            
            ✅ *9 En-Boy Oranı*
            - Instagram, YouTube, Story formatları
            """)
        
        with col_info2:
            st.markdown("""
            ### 🛠 Kullanılan Teknolojiler
            
            - *Streamlit* - Modern UI
            - *Ollama (Llama 3.2)* - Lokal AI
            - *Stability AI* - Görsel oluşturma
            - *Deep Translator* - Çeviri
            - *Python* - Backend
            
            ### 📊 Model Bilgileri
            
            - *Ultra:* 8 kredi (En kaliteli)
            - *Core:* 3 kredi (Dengeli)
            - *SD3 Large:* 6.5 kredi (Hızlı)
            """)
    
    # ===== GÖRSEL OLUŞTURMA =====
    if st.session_state.get('confirmed', False):
        st.markdown("---")
        st.markdown("## 🎨 Görsel Oluşturuluyor...")
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        model_key = st.session_state.get('selected_model_key', 'Ultra (En Kaliteli - 8 kredi)')
        model_endpoint = MODEL_OPTIONS[model_key]['endpoint']
        
        status_text.text(f"📤 {model_key.split('(')[0].strip()} modeline gönderiliyor...")
        progress_bar.progress(20)
        time.sleep(0.5)
        
        status_text.text("🎨 Görsel oluşturuluyor (30-60 saniye)...")
        progress_bar.progress(50)
        
        final_prompt = st.session_state.get('final_positive', '')
        style_key = st.session_state.get('selected_style_key', 'Yok (Doğal)')
        aspect_key = st.session_state.get('selected_aspect_key', '16:9 (Yatay - Video)')
        
        style_value = STYLE_OPTIONS[style_key]
        aspect_value = ASPECT_RATIOS[aspect_key]
        
        image = generate_image_stability(
            final_prompt,
            model_endpoint,
            aspect_ratio=aspect_value,
            style=style_value
        )
        
        progress_bar.progress(100)
        status_text.text("✅ Tamamlandı!")
        time.sleep(0.5)
        status_text.empty()
        progress_bar.empty()
        
        if image:
            st.success("🎉 Görsel başarıyla oluşturuldu!")
            
            # Kütüphaneye kaydet
            save_metadata = {
                "model": model_key.split('(')[0].strip(),
                "style": style_key.split('(')[0].strip(),
                "aspect_ratio": aspect_key.split('(')[0].strip()
            }
            
            if save_to_library(image, final_prompt, save_metadata):
                st.info("✅ Görsel kütüphaneye kaydedildi!")
            
            col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
            with col_img2:
                st.image(image, caption="🎨 AI Tarafından Oluşturulan Görsel", use_container_width=True)
            
            # Download
            col_dl1, col_dl2, col_dl3 = st.columns(3)
            
            with col_dl1:
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                st.download_button(
                    label="💾 Görseli İndir (PNG)",
                    data=img_byte_arr,
                    file_name="ai_generated_image.png",
                    mime="image/png",
                    use_container_width=True
                )
            
            with col_dl2:
                st.metric("📐 En-Boy", aspect_key.split('(')[0].strip())
            
            with col_dl3:
                st.metric("🎨 Format", "PNG")
            
            # Detaylar
            st.markdown("---")
            st.markdown("### 📊 Görsel Detayları")
            
            col_detail1, col_detail2 = st.columns(2)
            
            with col_detail1:
                st.markdown(f"""
                <div class="info-card">
                    <h4>🎯 Kullanılan Prompt</h4>
                    <p style="font-size: 0.9em;">
                        {final_prompt[:200]}...
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col_detail2:
                st.markdown(f"""
                <div class="info-card">
                    <h4>🎨 Ayarlar</h4>
                    <p style="font-size: 0.9em;">
                        <b>Model:</b> {model_key.split('(')[0].strip()}<br>
                        <b>Stil:</b> {style_key.split('(')[0].strip()}<br>
                        <b>En-Boy:</b> {aspect_key.split('(')[0].strip()}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Reset
            st.markdown("---")
            col_reset1, col_reset2 = st.columns(2)
            
            with col_reset1:
                if st.button("🔄 Aynı Prompt ile Yeniden Oluştur", use_container_width=True):
                    st.session_state['confirmed'] = True
                    st.rerun()
            
            with col_reset2:
                if st.button("🏠 Yeni Prompt Oluştur", use_container_width=True, type="secondary"):
                    st.session_state.clear()
                    st.rerun()
        
        else:
            st.error("😞 Görsel oluşturulamadı.")
            
            with st.expander("🔍 Olası Çözümler"):
                st.markdown("""
                1. ✅ API key'inizi kontrol edin
                2. ✅ Kredi durumunuzu kontrol edin ([Platform](https://platform.stability.ai/account/credits))
                3. ✅ İnternet bağlantınızı kontrol edin
                4. ✅ Rate limit aşmadığınızdan emin olun
                5. ✅ Seçtiğiniz modelin aktif olduğundan emin olun
                """)
            
            if st.button("↩ Geri Dön", use_container_width=True):
                st.session_state['confirmed'] = False
                st.rerun()
        
        st.session_state['confirmed'] = False
        st.stop()
    
    with tab2:
        st.markdown("## Görsel Kütüphanesi")
        st.caption("Geçmişte oluşturduğunuz tüm görseller")
        
        library_items = load_library()
        
        if not library_items:
            st.info("🎨 Henüz kütüphanede görsel yok. İlk görselinizi oluşturun!")
        else:
            st.success(f"📊 Toplam {len(library_items)} görsel bulundu")
            
            # Filtreleme
            col_filter1, col_filter2 = st.columns(2)
            
            with col_filter1:
                filter_model = st.multiselect(
                    "🤖 Model Filtrele",
                    options=list(set([item['metadata']['model'] for item in library_items])),
                    default=None
                )
            
            with col_filter2:
                filter_style = st.multiselect(
                    "🎭 Stil Filtrele",
                    options=list(set([item['metadata']['style'] for item in library_items])),
                    default=None
                )
            
            # Filtreleme uygula
            filtered_items = library_items
            if filter_model:
                filtered_items = [item for item in filtered_items if item['metadata']['model'] in filter_model]
            if filter_style:
                filtered_items = [item for item in filtered_items if item['metadata']['style'] in filter_style]
            
            st.markdown("---")
            
            # Görselleri göster (3 sütun)
            cols_per_row = 3
            for idx in range(0, len(filtered_items), cols_per_row):
                cols = st.columns(cols_per_row)
                
                for col_idx, col in enumerate(cols):
                    item_idx = idx + col_idx
                    if item_idx < len(filtered_items):
                        item = filtered_items[item_idx]
                        metadata = item['metadata']
                        
                        with col:
                            # Görsel göster
                            image = Image.open(item['image_path'])
                            st.image(image, use_container_width=True)
                            
                            # Metadata göster
                            with st.expander("📋 Detaylar"):
                                # Tarih formatını düzenle
                                date_str = metadata['timestamp'][:8]
                                time_str = metadata['timestamp'][9:]
                                formatted_date = f"{date_str[:4]}.{date_str[4:6]}.{date_str[6:8]}"
                                formatted_time = f"{time_str[:2]}.{time_str[2:4]}.{time_str[4:6]}"
                                
                                st.markdown(f"""
                                📅 Tarih: {formatted_date} - {formatted_time}
                                
                                ✍️ Prompt:
                                """)
                                
                                st.text_area(
                                    "",
                                    value=metadata['prompt'],
                                    height=150,
                                    disabled=True,
                                    label_visibility="collapsed"
                                    
                                )

                                
                                st.markdown(f"""
                                🤖 Model: {metadata['model']}  
                                🎭 Stil: {metadata['style']}  
                                📐 En-Boy: {metadata['aspect_ratio']}
                                """)
                                
                                # İndir butonu
                                with open(item['image_path'], 'rb') as f:
                                    st.download_button(
                                        label="💾 İndir",
                                        data=f.read(),
                                        file_name=metadata['image_file'],
                                        mime="image/png",
                                        use_container_width=True,
                                        key=f"download_{metadata['timestamp']}"
                                    )
    



if __name__ == "__main__":
    main()