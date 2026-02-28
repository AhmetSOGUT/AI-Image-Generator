import os
import json
import io
from datetime import datetime
from deep_translator import GoogleTranslator
from PIL import Image
from config import LIBRARY_FOLDER



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