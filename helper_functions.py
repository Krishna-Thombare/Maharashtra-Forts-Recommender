import pandas as pd
import re
import numpy as np
import os

FORT_IMAGE_FOLDER = "fort_images"

# Extract Single Construction Year:- "1560-1570" -> 1560
def extract_year(text):
    if "bce" in text:
        return None
    match = re.search(r"(\d{3, 4})", text)
    return int(match.group(1)) if match else None

# Handle Ordinals and Ranges
def get_ordinal_suffix(n):
    if n % 100 in [11,12,13]:
        return "th"
    elif n % 10 == 1:
        return "st"
    elif n % 10 == 2:
        return "nd"
    elif n % 10 == 3:
        return "rd"
    else:
        return "th"

# Extract Single Construction Century
def extract_centuries(text, year, bce_year):
    text_lower = str(text).lower().strip()
    
    ce_century = None
    bce_century = None
    
    # First handle BCE explicitly
    if "bce" in text_lower or "bc" in text_lower:
        # Look for century in BCE text
        match = re.search(r"(\d{1,2})(st|nd|rd|th)\s*century", text_lower)
        if match:
            century_num = int(match.group(1))
            suffix = get_ordinal_suffix(century_num)
            bce_century = f"{century_num}{suffix} Century BCE"
        # If BCE numeric year exists but no explicit century
        elif bce_year is not None and not pd.isna(bce_year):
            century_num = (int(bce_year)-1)//100 + 1
            bce_century = f"{century_num}{get_ordinal_suffix(century_num)} Century BCE"
        return ce_century, bce_century  # exit early for BCE
    
    # Then handle CE explicitly
    match = re.search(r"(\d{1,2})(st|nd|rd|th)\s*century", text_lower)
    if match:
        century_num = int(match.group(1))
        suffix = get_ordinal_suffix(century_num)
        ce_century = f"{century_num}{suffix} Century"
    
    # If CE numeric year exists but no explicit century
    if ce_century is None and year is not None and not pd.isna(year):
        century_num = (int(year)-1)//100 + 1
        ce_century = f"{century_num}{get_ordinal_suffix(century_num)} Century"
    
    return ce_century, bce_century

# Handle BCE:- "30 bce" -> 30
def extract_bce(text):
    match = re.search(r"(\d+)\s*bce", text)
    return int(match.group(1)) if match else None

# Extract Descriptive Text:- 1st Century BCE, ancient, Unknown
def extract_text(text, year, bce_year):
    leftovers = text
    # Remove numeric years
    leftovers = re.sub(r"\d{3,4}", "", leftovers)
    # Remove BCE mentions
    leftovers = re.sub(r"\b\d+\s*bce\b", "", leftovers, flags=re.IGNORECASE)
    # Remove ordinal centuries
    leftovers = re.sub(r"\b\d+(st|nd|rd|th)\s*century\b", "", leftovers, flags=re.IGNORECASE)
    # Remove common separators
    leftovers = leftovers.replace(";", "").replace(",", "").strip()
    return leftovers if leftovers else None

# Filter Text
def filter_text(text, min_len=5):
    if pd.isna(text):
        return "unknown"
    
    # Split text into words
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Keep only words with length >= min_len
    filtered = [w for w in words if len(w) >= min_len]
    
    if filtered:
        return " ".join(filtered)
    else:
        return "unknown"

# Image helpers
def normalize_fort_name(fort_name):
    fort_name = str(fort_name).lower().strip()
    fort_name = re.sub(r'[^a-z0-9\s]', '', fort_name)
    fort_name = fort_name.replace(" ", "_")
    return fort_name

def get_fort_image(fort_name):
    normalized_name = normalize_fort_name(fort_name)
    for ext in [".jpg", ".jpeg", ".png", ".webp"]:
        image_path = os.path.join(FORT_IMAGE_FOLDER, normalized_name + ext)
        if os.path.exists(image_path):
            return os.path.abspath(image_path)
    default_image = os.path.join(FORT_IMAGE_FOLDER, "default.jpg")
    if os.path.exists(default_image):
        return os.path.abspath(default_image)
    return None













