import json
import os

DEFAULT_CONFIG = {
    "size_presets": {
        "US (2x2 in)": [50.8, 50.8],
        "EU (35x45 mm)": [35.0, 45.0],
        "India (35x35 mm)": [35.0, 35.0],
        "Custom": [35.0, 45.0]
    },
    "background_colors": {
        "White": "#FFFFFF",
        "Light Blue": "#ADD8E6",
        "Grey": "#808080",
        "Dark Blue": "#00008B",
        "Red": "#FF0000",
        "Tan": "#D2B48C"
    },
    "image_adjustments": {
        "brightness": {"min": 0.5, "max": 1.5, "default": 1.0},
        "contrast": {"min": 0.5, "max": 1.5, "default": 1.0},
        "saturation": {"min": 0.0, "max": 2.0, "default": 1.0},
        "sharpness": {"min": 0.0, "max": 3.0, "default": 1.0},
        "skin_glow": {"min": 0.0, "max": 1.0, "default": 0.0},
        "smooth_skin": {"min": 0.0, "max": 1.0, "default": 0.0}
    },
    "face_detection": {
        "scale_factor": 1.1,
        "min_neighbors": 5,
        "min_size": [100, 100],
        "face_crop_height_ratio": 0.55,
        "face_crop_offset_ratio": 0.05
    },
    "skin_detection": {
        "ycrcb_lower": [0, 133, 77],
        "ycrcb_upper": [255, 173, 127],
        "blur_kernel": [7, 7],
        "lightening_boost_factor": 0.25
    },
    "ui_styles": {
        "active_color": "#1f538d",
        "inactive_color": "gray30",
        "canvas_bg": "#2b2b2b",
        "crop_handle_size": 10,
        "crop_box_color": "#00a8ff",
        "mask_overlay_rgba": [255, 0, 0, 80],
        "primary_button": "#3498db",
        "secondary_button": "#9b59b6",
        "warning_button": "#e67e22",
        "success_button": "#2ecc71",
        "section_label": "#3498db"
    },
    "brush_settings": {
        "min_size": 5,
        "max_size": 100,
        "default_size": 20
    },
    "export_settings": {
        "print_sheet_size": [1800, 1200],
        "margin_gap_large": [15, 15],
        "margin_gap_small": [0, 0],
        "photo_quality": 95,
        "sheet_quality": 98,
        "sheet_outline": "#dddddd"
    },
    "app_defaults": {
        "geometry": "1100x700",
        "dpi": 300,
        "default_model": "Balanced (u2net)",
        "sidebar_width": 280,
        "initial_crop": [0.25, 0.25, 0.75, 0.75]
    }
}

class ConfigManager:
    CONFIG_PATH = "config.json"

    @classmethod
    def load_config(cls):
        if not os.path.exists(cls.CONFIG_PATH):
            cls.save_config(DEFAULT_CONFIG)
            return DEFAULT_CONFIG
        
        try:
            with open(cls.CONFIG_PATH, "r") as f:
                config = json.load(f)
                updated = False
                
                for key, value in DEFAULT_CONFIG.items():
                    if key not in config:
                        config[key] = value
                        updated = True
                    elif isinstance(value, dict) and isinstance(config[key], dict):
                        # Simple one-level deep merge for sub-dictionaries
                        for sub_key, sub_value in value.items():
                            if sub_key not in config[key]:
                                config[key][sub_key] = sub_value
                                updated = True
                
                if updated:
                    cls.save_config(config)
                return config
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            return DEFAULT_CONFIG

    @classmethod
    def save_config(cls, config):
        try:
            with open(cls.CONFIG_PATH, "w") as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

# Load settings once at startup
SETTINGS = ConfigManager.load_config()
