import customtkinter as ctk
from utils.constants import SIZE_PRESETS, BG_COLORS

class Sidebar(ctk.CTkScrollableFrame):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, width=250, corner_radius=0, **kwargs)
        self.app = app
        self._current_row = 0
        
        # --- 1. FILE ---
        self.add_label("1. File Management")
        self.app.open_btn = self.add_button("Open Image", self.app.open_image)
        self.app.rotate_btn = self.add_button("Rotate 90°", self.app.rotate_image)

        # --- 2. FORMAT ---
        self.add_label("2. Format & Size")
        self.app.size_optionemenu = ctk.CTkOptionMenu(self, values=list(SIZE_PRESETS.keys()), command=self.app.on_format_change)
        self.app.size_optionemenu.grid(row=self.next_row(), column=0, padx=20, pady=10)

        # --- 3. AI ---
        self.add_label("3. AI Processing")
        self.add_button("Auto-Crop Face", self.app.auto_crop_face)
        self.app.remove_bg_btn = self.add_button("Remove Background", self.app.remove_background, fg_color="transparent", border_width=2)
        self.add_button("Confirm Crop", self.app.confirm_crop, fg_color="#2ecc71", hover_color="#27ae60")

        # --- 4. MASK ---
        self.add_label("4. Mask Refinement")
        tool_frame = ctk.CTkFrame(self, fg_color="transparent")
        tool_frame.grid(row=self.next_row(), column=0, padx=20, pady=5, sticky="ew")
        tool_frame.grid_columnconfigure((0,1,2,3), weight=1)
        
        self.app.brush_btn = ctk.CTkButton(tool_frame, text="Brush", width=50, command=lambda: self.app.toggle_mode("brush"))
        self.app.brush_btn.grid(row=0, column=0, padx=2)
        self.app.eraser_btn = ctk.CTkButton(tool_frame, text="Eraser", width=50, command=lambda: self.app.toggle_mode("eraser"))
        self.app.eraser_btn.grid(row=0, column=1, padx=2)
        ctk.CTkButton(tool_frame, text="Undo", width=50, command=self.app.undo_mask).grid(row=0, column=2, padx=2)
        ctk.CTkButton(tool_frame, text="Redo", width=50, command=self.app.redo_mask).grid(row=0, column=3, padx=2)

        self.add_label("Brush Size:")
        self.app.brush_size_slider = self.add_slider(5, 100, 20)
        
        self.add_label("Background Color:")
        self.app.bg_color_optionemenu = ctk.CTkOptionMenu(self, values=list(BG_COLORS.keys()), command=self.app.on_bg_color_change)
        self.app.bg_color_optionemenu.grid(row=self.next_row(), column=0, padx=20, pady=5)

        self.add_label("Foreground Brightness:")
        self.app.brightness_slider = self.add_slider(0.5, 1.5, 1.0, self.app.on_adjustment_change)

        # --- 5. ADJUSTMENTS ---
        self.add_label("5. Image Adjustments")
        self.add_label("Contrast:")
        self.app.contrast_slider = self.add_slider(0.5, 1.5, 1.0, self.app.on_adjustment_change)
        self.add_label("Saturation:")
        self.app.saturation_slider = self.add_slider(0.0, 2.0, 1.0, self.app.on_adjustment_change)
        self.add_label("Sharpness:")
        self.app.sharpness_slider = self.add_slider(0.0, 3.0, 1.0, self.app.on_adjustment_change)
        self.add_label("Skin Lightening:")
        self.app.lightening_slider = self.add_slider(0.0, 1.0, 0.0, self.app.on_adjustment_change)
        self.add_label("Skin Smoothing:")
        self.app.smoothing_slider = self.add_slider(0.0, 1.0, 0.0, self.app.on_adjustment_change)

        # --- 6. EXPORT ---
        self.add_label("6. Export & Print")
        self.add_button("Save Single Photo", self.app.export_single)
        self.add_button("Save 4x6 Print Sheet", self.app.export_print_sheet, fg_color="transparent", border_width=2)

        self.grid_rowconfigure(self.next_row(), weight=1)

    def add_label(self, text, weight="bold"):
        lbl = ctk.CTkLabel(self, text=text, font=ctk.CTkFont(weight=weight))
        lbl.grid(row=self.next_row(), column=0, padx=20, pady=(10, 0), sticky="w")
        return lbl

    def add_button(self, text, command, **kwargs):
        btn = ctk.CTkButton(self, text=text, command=command, **kwargs)
        btn.grid(row=self.next_row(), column=0, padx=20, pady=5)
        return btn

    def add_slider(self, from_, to, start, command=None):
        s = ctk.CTkSlider(self, from_=from_, to=to, command=command)
        s.set(start)
        s.grid(row=self.next_row(), column=0, padx=20, pady=5)
        return s

    def next_row(self):
        r = self._current_row
        self._current_row += 1
        return r
