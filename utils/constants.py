# Size Presets (Name: (width_mm, height_mm))
SIZE_PRESETS = {
    "US (2x2 in)": (50.8, 50.8),
    "EU (35x45 mm)": (35.0, 45.0),
    "India (35x35 mm)": (35.0, 35.0),
    "Custom": (35.0, 45.0) # Default fallback
}

# Background Colors (Name: Hex)
BG_COLORS = {
    "White": "#FFFFFF",
    "Light Blue": "#ADD8E6",
    "Grey": "#808080",
    "Dark Blue": "#00008B",
    "Red": "#FF0000",
    "Tan": "#D2B48C"
}

# Segmentation Models (Name: internal_id)
SEGMENTATION_MODELS = {
    "Fast (u2netp)": "u2netp",
    "Balanced (u2net)": "u2net",
    "High Quality (isnet)": "isnet-general-use"
}

# UI Defaults
DEFAULT_GEOMETRY = "1100x700"
SIDEBAR_WIDTH = 250
DPI = 300
