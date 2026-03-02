import customtkinter as ctk
from utils.constants import (
    SIZE_PRESETS, BG_COLORS, SEGMENTATION_MODELS, DEFAULT_MODEL_DISPLAY,
    PRIMARY_BTN_COLOR, SECONDARY_BTN_COLOR, WARNING_BTN_COLOR, SUCCESS_BTN_COLOR,
    SECTION_LABEL_COLOR, INACTIVE_COLOR, BRUSH_MIN, BRUSH_MAX, BRUSH_DEFAULT,
    ADJ_CONFIG, DPI
)

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, width=280, corner_radius=0, **kwargs)
        self.app = app
        
        # Logo/Title
        self.logo_label = ctk.CTkLabel(self, text="SmartFrame", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo_label.pack(pady=(20, 15), padx=20)

        # Tabview for Workflow
        self.tabs = ctk.CTkTabview(self, width=250)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        self.tab_setup = self.tabs.add("1. Setup")
        self.tab_bg = self.tabs.add("2. BG")
        self.tab_enhance = self.tabs.add("3. Edit")
        self.tab_export = self.tabs.add("4. Save")

        self.setup_setup_tab()
        self.setup_bg_tab()
        self.setup_enhance_tab()
        self.setup_export_tab()

        # Help Button at the bottom
        self.help_btn = ctk.CTkButton(self, text="Help & Workflow", fg_color="transparent", border_width=1, command=self.app.show_help)
        self.help_btn.pack(side="bottom", fill="x", padx=20, pady=20)

    def setup_setup_tab(self):
        # Frame for grouping
        f = self.tab_setup
        self.add_section_label(f, "File Management")
        self.app.open_btn = self.add_btn(f, "Open Image", self.app.open_image, fg_color=PRIMARY_BTN_COLOR)
        self.add_btn(f, "Rotate 90°", self.app.rotate_image, fg_color=INACTIVE_COLOR)
        
        self.add_section_label(f, "Format & Size")
        self.app.size_optionemenu = ctk.CTkOptionMenu(f, values=list(SIZE_PRESETS.keys()), command=self.app.on_format_change)
        self.app.size_optionemenu.pack(fill="x", padx=10, pady=10)

    def setup_bg_tab(self):
        f = self.tab_bg

        self.add_section_label(f, "AI Auto-Align")
        self.add_btn(f, "Magic Auto-Crop", self.app.auto_crop_face, fg_color=SECONDARY_BTN_COLOR)
        self.add_btn(f, "Confirm Crop", self.app.confirm_crop, fg_color=SUCCESS_BTN_COLOR)

        self.add_section_label(f, "AI Background")
        
        ctk.CTkLabel(f, text="Model Quality:").pack(anchor="w", padx=10, pady=(5,0))
        self.app.model_optionemenu = ctk.CTkOptionMenu(f, values=list(SEGMENTATION_MODELS.keys()))
        self.app.model_optionemenu.set(DEFAULT_MODEL_DISPLAY)
        self.app.model_optionemenu.pack(fill="x", padx=10, pady=5)

        self.app.remove_bg_btn = self.add_btn(f, "Remove Background", self.app.remove_background, fg_color=WARNING_BTN_COLOR)
        
        self.add_section_label(f, "Refine Mask")
        tool_frame = ctk.CTkFrame(f, fg_color="transparent")
        tool_frame.pack(fill="x", padx=5, pady=5)
        
        self.app.brush_btn = ctk.CTkButton(tool_frame, text="Brush", width=55, command=lambda: self.app.toggle_mode("brush"))
        self.app.brush_btn.grid(row=0, column=0, padx=2)
        self.app.eraser_btn = ctk.CTkButton(tool_frame, text="Eraser", width=55, command=lambda: self.app.toggle_mode("eraser"))
        self.app.eraser_btn.grid(row=0, column=1, padx=2)
        ctk.CTkButton(tool_frame, text="Undo", width=50, command=self.app.undo_mask).grid(row=0, column=2, padx=2)
        ctk.CTkButton(tool_frame, text="Redo", width=50, command=self.app.redo_mask).grid(row=0, column=3, padx=2)

        ctk.CTkLabel(f, text="Brush Size:").pack(anchor="w", padx=10, pady=(5,0))
        self.app.brush_size_slider = ctk.CTkSlider(f, from_=BRUSH_MIN, to=BRUSH_MAX)
        self.app.brush_size_slider.set(BRUSH_DEFAULT)
        self.app.brush_size_slider.pack(fill="x", padx=10, pady=5)
        
        self.add_section_label(f, "New Background")
        self.app.bg_color_optionemenu = ctk.CTkOptionMenu(f, values=list(BG_COLORS.keys()), command=self.app.on_bg_color_change)
        self.app.bg_color_optionemenu.pack(fill="x", padx=10, pady=5)

    def setup_enhance_tab(self):
        # We use a scrollable frame for filters as they are many
        f = ctk.CTkScrollableFrame(self.tab_enhance, fg_color="transparent")
        f.pack(fill="both", expand=True)
        
        self.add_section_label(f, "Exposure")
        self.add_slider_grp(f, "Brightness", "brightness", "brightness_slider")
        self.add_slider_grp(f, "Contrast", "contrast", "contrast_slider")
        
        self.add_section_label(f, "Detail & Color")
        self.add_slider_grp(f, "Saturation", "saturation", "saturation_slider")
        self.add_slider_grp(f, "Sharpness", "sharpness", "sharpness_slider")
        
        self.add_section_label(f, "Portrait Retouching")
        self.add_slider_grp(f, "Subject Lightening", "skin_glow", "lightening_slider")
        self.add_slider_grp(f, "Blur", "smooth_skin", "smoothing_slider")

        # Bottom space
        ctk.CTkLabel(f, text="").pack(pady=10)
        self.add_btn(f, "Reset All Edits", self.app.reset_adjustments, fg_color="transparent", border_width=1)

    def setup_export_tab(self):
        f = self.tab_export
        self.add_section_label(f, "Final Delivery")
        self.add_btn(f, f"Save Single Photo ({DPI} DPI)", self.app.export_single, fg_color=SUCCESS_BTN_COLOR)
        self.add_btn(f, "Generate 4x6 Print Sheet", self.app.export_print_sheet, fg_color="transparent", border_width=2)

    # --- UI HELPERS ---
    def add_section_label(self, master, text):
        lbl = ctk.CTkLabel(master, text=text, font=ctk.CTkFont(size=13, weight="bold"), text_color=SECTION_LABEL_COLOR)
        lbl.pack(anchor="w", padx=10, pady=(15, 5))

    def add_btn(self, master, text, command, **kwargs):
        btn = ctk.CTkButton(master, text=text, command=command, **kwargs)
        btn.pack(fill="x", padx=10, pady=5)
        return btn

    def add_slider_grp(self, master, label, config_key, attr_name):
        cfg = ADJ_CONFIG.get(config_key, {"min": 0, "max": 1, "default": 0})
        ctk.CTkLabel(master, text=label).pack(anchor="w", padx=10, pady=(5,0))
        s = ctk.CTkSlider(master, from_=cfg["min"], to=cfg["max"], command=self.app.on_adjustment_change)
        s.set(cfg["default"])
        s.pack(fill="x", padx=10, pady=5)
        setattr(self.app, attr_name, s)
        return s
