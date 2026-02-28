import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2"

# API KEY GOMULU
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

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