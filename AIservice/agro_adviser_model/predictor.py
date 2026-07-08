import numpy as np
import json
from agro_adviser_model.model_loader import model


# Load class names
with open("precautions/class_indices.json", "r") as f:
    CLASS_NAMES = json.load(f)

# Load cure data
with open("precautions/cures.json", "r", encoding="utf-8") as f:
    CURES_DATA = json.load(f)


def get_cure(disease_name, lang="en"):

    for item in CURES_DATA:
        if item["class_name"] == disease_name:
            return item["cures"][lang].split("\n")

    return []

def get_disease_name(class_name, lang="en"):
    """   
    Args:
        class_name (str): The raw class name from the model (e.g., "Apple___Apple_scab")
        lang (str): "en" for English or "te" for Telugu.
        
    Returns:
        str: The readable name or the raw class_name if not found.
    """
    for item in CURES_DATA:
        if item["class_name"] == class_name:
            # Returns the localized name from the disease_name dictionary
            return item.get("disease_name", {}).get(lang, class_name)
            
    return class_name

def predict_disease(img,lang):

    predictions = model.predict(img, verbose=0)

    class_idx = int(np.argmax(predictions[0]))
    confidence = float(np.max(predictions[0])) * 100

    disease_name = CLASS_NAMES[class_idx]

    cure = get_cure(disease_name, lang)
    disease=get_disease_name(disease_name,lang)

    return {
        "disease": disease_name,
        "index": class_idx,
        "disease_name":disease, 
        "cure": cure,
    }