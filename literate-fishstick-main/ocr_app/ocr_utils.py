import torch
import torchvision.transforms as T
from PIL import Image
import json
from pathlib import Path
from ultralytics import YOLO  # Using YOLOv8 as an example
import io
import base64
import numpy as np
import os
from langdetect import detect, LangDetectException # <-- ADDED

# --- 1. DEFINE PATHS ---
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
CRNN_MODEL_PATH = MODEL_DIR / "crnn_ocr_model.pt"
VOCAB_PATH = MODEL_DIR / "vocabulary.json"
YOLO_MODEL_PATH = MODEL_DIR / "yolo_text_detector.pt"

# --- 2. LOAD MODELS & VOCAB (ONCE, ON APP START) ---
print("Loading models... This may take a moment.")
DEVICE = "cpu"

# --- Globals to hold models ---
YOLO_MODEL = None
CRNN_MODEL = None
IDX_TO_CHAR = {}

def load_models():
    global YOLO_MODEL, CRNN_MODEL, IDX_TO_CHAR
    
    # Load YOLO Detector
    if os.path.exists(YOLO_MODEL_PATH):
        try:
            YOLO_MODEL = YOLO(YOLO_MODEL_PATH)
            YOLO_MODEL.to(DEVICE)
            print("✅ YOLO model loaded successfully on CPU.")
        except Exception as e:
            print(f"❌ FAILED to load YOLO model: {e}")
    else:
        print(f"⚠️ WARNING: YOLO model not found at {YOLO_MODEL_PATH}")

    # Load CRNN Recognizer (from your notebook's CELL 7 & 8)
    if os.path.exists(CRNN_MODEL_PATH):
        try:
            CRNN_MODEL = torch.jit.load(str(CRNN_MODEL_PATH), map_location=DEVICE)
            CRNN_MODEL.eval()
            print("✅ CRNN TorchScript model loaded successfully on CPU.")
        except Exception as e:
            print(f"❌ FAILED to load CRNN model: {e}")
    else:
        print(f"⚠️ WARNING: CRNN model not found at {CRNN_MODEL_PATH}")

    # Load Vocabulary (from your notebook's CELL 8)
    if os.path.exists(VOCAB_PATH):
        try:
            with open(VOCAB_PATH, 'r', encoding='utf-8') as f:
                vocab_info = json.load(f)
            IDX_TO_CHAR = {str(k): v for k, v in vocab_info['idx_to_char'].items()}
            print("✅ Vocabulary loaded successfully.")
        except Exception as e:
            print(f"❌ FAILED to load vocabulary: {e}")
    else:
        print(f"⚠️ WARNING: Vocabulary not found at {VOCAB_PATH}")

# --- 3. DEFINE TRANSFORMS & DECODERS (FROM NOTEBOOK) ---

# CRNN Transform (from notebook CELL 8)
CRNN_TRANSFORM = T.Compose([
    T.Resize((32, 128)),
    T.Grayscale(num_output_channels=1),
    T.ToTensor(),
    T.Normalize([0.5], [0.5])
])

def ctc_greedy_decode(output, idx_to_char_map):
    """
    Decodes the raw model output (from notebook CELL 8).
    """
    pred = torch.argmax(output, dim=2)
    pred = pred.squeeze(1)
    
    decoded_chars = []
    last_char_idx = -1
    for idx in pred:
        idx = idx.item()
        if idx > 0 and idx != last_char_idx:
            decoded_chars.append(idx_to_char_map.get(str(idx), '?'))
        last_char_idx = idx
        
    return ''.join(decoded_chars)

def image_to_base64(img):
    """Converts a PIL Image to a base64 string to display in HTML."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# --- 4. MAIN PREDICTION FUNCTION ---

def run_prediction(image_file):
    """
    Runs the full Detection (YOLO) + Recognition (CRNN) pipeline.
    """
    if not YOLO_MODEL:
        return [{"error": "YOLO model is not loaded. Check server logs."}]
    if not CRNN_MODEL:
        return [{"error": "CRNN model is not loaded. Check server logs."}]
    if not IDX_TO_CHAR:
        return [{"error": "Vocabulary is not loaded. Check server logs."}]


    results_list = []
    
    try:
        # 1. Open image
        img_rgb = Image.open(image_file).convert("RGB")
        
        # 2. Run YOLO Detection
        yolo_results = YOLO_MODEL(img_rgb)
        
        # 3. Process each detection
        for res in yolo_results:
            for box in res.boxes:
                # Get bounding box coordinates
                x1, y1, x2, y2 = [int(coord) for coord in box.xyxy[0]]
                
                # 3a. Crop the text region from the original image
                cropped_img = img_rgb.crop((x1, y1, x2, y2))
                
                # 3b. Apply CRNN Transform (handles grayscale conversion)
                img_tensor = CRNN_TRANSFORM(cropped_img).unsqueeze(0).to(DEVICE)
                
                # 3c. Run CRNN Recognition
                with torch.no_grad():
                    output = CRNN_MODEL(img_tensor)
                
                # 3d. Decode the text
                predicted_text = ctc_greedy_decode(output, IDX_TO_CHAR)
                
                # --- START: NEW LANGUAGE DETECTION BLOCK ---
                language = "Unknown" # Default
                if predicted_text and len(predicted_text) > 5: # langdetect needs a few chars
                    try:
                        language = detect(predicted_text)
                    except LangDetectException:
                        language = "N/A" # Failed to detect
                elif predicted_text:
                    language = "Too short" # Too short to tell
                # --- END: NEW LANGUAGE DETECTION BLOCK ---
                
                # 3e. Save cropped image for display
                cropped_base64 = image_to_base64(cropped_img)
                
                results_list.append({
                    "text": predicted_text,
                    "language": language.upper(),  # <-- ADDED
                    "image_data": cropped_base64
                })
        
        if not results_list:
            return [{"text": "No text detected.", "language": "N/A", "image_data": None}]
            
        return results_list
        
    except Exception as e:
        print(f"❌ Error during prediction: {e}")
        return [{"error": str(e)}]

# --- 5. INITIAL MODEL LOAD ---
load_models()
