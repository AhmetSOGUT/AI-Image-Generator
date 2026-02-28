import requests
import json
import io
from PIL import Image
from config import OLLAMA_URL, OLLAMA_MODEL, STABILITY_API_KEY, SYSTEM_PROMPT



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
     # ai_engine.py içinde call_ollama fonksiyonunun hata kısmı:
    except Exception as e:
        # st.error(...) satırını SİL, yerine bunu yaz:
        return {"error": "Ollama servisine bağlanılamadı. Lütfen Ollama'nın arka planda çalıştığından emin olun."}   
    
    except json.JSONDecodeError as e:
        st.error(f"JSON Parse Hatası: {e}")
        return {
            "error": "JSON parsing failed",
            "raw_response": raw_response[:500]
        }
    #except Exception as e:
     #   st.error(f"Ollama Hatası: {e}")
      #  return {"error": str(e)}


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

