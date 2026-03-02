from utils.config_manager import SETTINGS

# Bridge SETTINGS from config.json to existing constant names used in the app
SIZE_PRESETS = SETTINGS.get("size_presets")
BG_COLORS = SETTINGS.get("background_colors")
ADJ_CONFIG = SETTINGS.get("image_adjustments")

# UI Defaults
app_defaults = SETTINGS.get("app_defaults", {})
DEFAULT_GEOMETRY = app_defaults.get("geometry", "1100x700")
SIDEBAR_WIDTH = app_defaults.get("sidebar_width", 280)
DPI = app_defaults.get("dpi", 300)
DEFAULT_MODEL_DISPLAY = app_defaults.get("default_model", "Balanced (u2net)")
INITIAL_CROP = app_defaults.get("initial_crop", [0.25, 0.25, 0.75, 0.75])

# Segmentation Models
SEGMENTATION_MODELS = {
    "Fast (u2netp)": "u2netp",
    "Balanced (u2net)": "u2net",
    "High Quality (isnet)": "isnet-general-use"
}

# Face Detection
FACE_DET_CONFIG = SETTINGS.get("face_detection", {})
FACE_SCALE = FACE_DET_CONFIG.get("scale_factor", 1.1)
FACE_MIN_NEIGHBORS = FACE_DET_CONFIG.get("min_neighbors", 5)
FACE_MIN_SIZE = tuple(FACE_DET_CONFIG.get("min_size", [100, 100]))
FACE_CROP_HEIGHT_RATIO = FACE_DET_CONFIG.get("face_crop_height_ratio", 0.55)
FACE_CROP_OFFSET_RATIO = FACE_DET_CONFIG.get("face_crop_offset_ratio", 0.05)

# Skin Detection
SKIN_DET_CONFIG = SETTINGS.get("skin_detection", {})
SKIN_LOWER = SKIN_DET_CONFIG.get("ycrcb_lower", [0, 133, 77])
SKIN_UPPER = SKIN_DET_CONFIG.get("ycrcb_upper", [255, 173, 127])
SKIN_BLUR_KERNEL = tuple(SKIN_DET_CONFIG.get("blur_kernel", [7, 7]))
SKIN_BOOST = SKIN_DET_CONFIG.get("lightening_boost_factor", 0.25)

# UI Styles
UI_STYLES = SETTINGS.get("ui_styles", {})
ACTIVE_COLOR = UI_STYLES.get("active_color", "#1f538d")
INACTIVE_COLOR = UI_STYLES.get("inactive_color", "gray30")
CANVAS_BG = UI_STYLES.get("canvas_bg", "#2b2b2b")
HANDLE_SIZE = UI_STYLES.get("crop_handle_size", 10)
CROP_BOX_COLOR = UI_STYLES.get("crop_box_color", "#00a8ff")
MASK_OVERLAY_RGBA = tuple(UI_STYLES.get("mask_overlay_rgba", [255, 0, 0, 80]))

PRIMARY_BTN_COLOR = UI_STYLES.get("primary_button", "#3498db")
SECONDARY_BTN_COLOR = UI_STYLES.get("secondary_button", "#9b59b6")
WARNING_BTN_COLOR = UI_STYLES.get("warning_button", "#e67e22")
SUCCESS_BTN_COLOR = UI_STYLES.get("success_button", "#2ecc71")
SECTION_LABEL_COLOR = UI_STYLES.get("section_label", "#3498db")

# Brush Settings
BRUSH_CONFIG = SETTINGS.get("brush_settings", {})
BRUSH_MIN = BRUSH_CONFIG.get("min_size", 5)
BRUSH_MAX = BRUSH_CONFIG.get("max_size", 100)
BRUSH_DEFAULT = BRUSH_CONFIG.get("default_size", 20)

# Export Settings
EXPORT_CONFIG = SETTINGS.get("export_settings", {})
PRINT_SHEET_SIZE = tuple(EXPORT_CONFIG.get("print_sheet_size", [1800, 1200]))
MARGIN_GAP_LARGE = tuple(EXPORT_CONFIG.get("margin_gap_large", [15, 15]))
MARGIN_GAP_SMALL = tuple(EXPORT_CONFIG.get("margin_gap_small", [0, 0]))
PHOTO_QUALITY = EXPORT_CONFIG.get("photo_quality", 95)
SHEET_QUALITY = EXPORT_CONFIG.get("sheet_quality", 98)
SHEET_OUTLINE = EXPORT_CONFIG.get("sheet_outline", "#dddddd")
