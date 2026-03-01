import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageDraw
import numpy as np

from utils.constants import SIZE_PRESETS, BG_COLORS, DEFAULT_GEOMETRY, SEGMENTATION_MODELS
from core.image_engine import ImageEngine
from core.exporter import Exporter
from ui.sidebar import Sidebar
from ui.preview_canvas import PreviewCanvas

class PassportPhotoApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Passport Photo Creator")
        self.geometry(DEFAULT_GEOMETRY)

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Core State
        self.original_image = None # This will store the CURRENT working image (cropped/rotated)
        self.image_before_bg_removal = None
        self.current_mask = None
        self.mask_undo_stack = []
        self.mask_redo_stack = []
        
        self.mode = "crop" # crop, brush, eraser
        self.crop_norm = [0.25, 0.25, 0.75, 0.75]
        
        # UI State for drag/drop
        self.action = None
        self.start_x = self.start_y = 0
        self.drag_start_norm = [0,0,0,0]
        self.last_paint_x = self.last_paint_y = None
        
        # Timers
        self._adj_timer = None
        self._resize_timer = None

        # Components
        self.sidebar = Sidebar(self, self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_rowconfigure(0, weight=1)
        
        self.canvas = PreviewCanvas(self.preview_frame, self)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.preview_frame.bind("<Configure>", self.on_resize)

    # --- IMAGE OPS ---
    def open_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.jpeg *.png *.webp")])
        if path:
            self.original_image = Image.open(path)
            self.image_before_bg_removal = None
            self.current_mask = None
            self.init_crop_box()
            self.update_preview()

    def rotate_image(self):
        if self.original_image:
            self.original_image = self.original_image.rotate(-90, expand=True)
            if self.image_before_bg_removal: self.image_before_bg_removal = self.image_before_bg_removal.rotate(-90, expand=True)
            if self.current_mask: self.current_mask = self.current_mask.rotate(-90, expand=True)
            self.init_crop_box()
            self.update_preview()

    def remove_background(self):
        if not self.original_image: return
        self.remove_bg_btn.configure(state="disabled", text="Processing...")
        self.update_idletasks()
        try:
            self.image_before_bg_removal = self.original_image.copy()
            
            # Get the internal model id from the selected display name
            model_display_name = self.model_optionemenu.get()
            model_id = SEGMENTATION_MODELS.get(model_display_name, "u2net")
            
            _, self.current_mask = ImageEngine.remove_bg(self.original_image, model_name=model_id)
            self.apply_mask()
            # Switch to BG tab for refinement
            self.sidebar.tabs.set("2. BG")
        finally:
            self.remove_bg_btn.configure(state="normal", text="Remove Background")

    def apply_mask(self):
        if self.image_before_bg_removal and self.current_mask:
            bg_hex = BG_COLORS.get(self.bg_color_optionemenu.get(), "#FFFFFF")
            self.original_image = ImageEngine.apply_filters(
                self.image_before_bg_removal, self.current_mask, bg_hex,
                brightness=self.brightness_slider.get(),
                contrast=self.contrast_slider.get(),
                saturation=self.saturation_slider.get(),
                sharpness=self.sharpness_slider.get(),
                smoothing=self.smoothing_slider.get(),
                lightening=self.lightening_slider.get(),
                is_editing_mask=(self.mode in ["brush", "eraser"])
            )
            self.update_preview()

    def auto_crop_face(self):
        if not self.original_image: return
        bbox = ImageEngine.detect_face(self.original_image)
        if not bbox: return
        
        fx, fy, fw, fh = bbox
        ratio = self.get_aspect_ratio() or 0.8
        
        crop_h = fh / 0.55
        crop_w = crop_h * ratio
        
        cx, cy = fx + fw/2, fy + fh/2 + (crop_h * 0.05)
        nx1, ny1 = max(0, cx - crop_w/2), max(0, cy - crop_h/2)
        nx2, ny2 = min(1, nx1 + crop_w), min(1, ny1 + crop_h)
        
        self.crop_norm = [nx1, ny1, nx2, ny2]
        self.update_preview()

    def confirm_crop(self):
        if not self.original_image: return
        w, h = self.original_image.size
        nx1, ny1, nx2, ny2 = self.crop_norm
        box = (int(nx1*w), int(ny1*h), int(nx2*w), int(ny2*h))
        
        self.original_image = self.original_image.crop(box)
        if self.image_before_bg_removal: self.image_before_bg_removal = self.image_before_bg_removal.crop(box)
        if self.current_mask: self.current_mask = self.current_mask.crop(box)
        
        self.crop_norm = [0, 0, 1, 1]
        self.mask_undo_stack.clear()
        self.mask_redo_stack.clear()
        self.update_preview()

    def reset_adjustments(self):
        # Reset slider values to defaults
        self.brightness_slider.set(1.0)
        self.contrast_slider.set(1.0)
        self.saturation_slider.set(1.0)
        self.sharpness_slider.set(1.0)
        self.lightening_slider.set(0.0)
        self.smoothing_slider.set(0.0)
        self.apply_mask()

    # --- UI EVENT HANDLERS ---
    def on_format_change(self, _):
        self.init_crop_box()
        self.update_preview()

    def on_bg_color_change(self, _):
        self.apply_mask()

    def on_adjustment_change(self, _):
        if self._adj_timer: self.after_cancel(self._adj_timer)
        self._adj_timer = self.after(50, self.apply_mask)

    def on_resize(self, _):
        if self._resize_timer: self.after_cancel(self._resize_timer)
        self._resize_timer = self.after(100, self.update_preview)

    def toggle_mode(self, mode):
        self.mode = "crop" if self.mode == mode else mode
        active_color = "#1f538d"
        self.brush_btn.configure(fg_color=active_color if self.mode == "brush" else "gray30")
        self.eraser_btn.configure(fg_color=active_color if self.mode == "eraser" else "gray30")
        self.canvas.config(cursor="crosshair" if self.mode in ["brush", "eraser"] else "arrow")
        self.apply_mask()

    def undo_mask(self):
        if self.mask_undo_stack:
            self.mask_redo_stack.append(self.current_mask.copy())
            self.current_mask = self.mask_undo_stack.pop()
            self.apply_mask()

    def redo_mask(self):
        if self.mask_redo_stack:
            self.mask_undo_stack.append(self.current_mask.copy())
            self.current_mask = self.mask_redo_stack.pop()
            self.apply_mask()

    # --- MOUSE LOGIC ---
    def on_mouse_press(self, e):
        if not self.original_image: return
        self.action = self.get_action(e)
        if self.action == "paint":
            self.mask_undo_stack.append(self.current_mask.copy())
            self.mask_redo_stack.clear()
            self.paint(e.x, e.y, True)
        else:
            self.start_x, self.start_y = e.x, e.y
            self.drag_start_norm = list(self.crop_norm)

    def on_mouse_drag(self, e):
        if not self.action or not self.original_image: return
        if self.action == "paint":
            self.paint(e.x, e.y)
        else:
            dx = (e.x - self.start_x) / self.canvas.img_data[2]
            dy = (e.y - self.start_y) / self.canvas.img_data[3]
            self.handle_crop_drag(dx, dy, e)
            self.canvas.update_image(self.original_image, self.crop_norm, self.mode)

    def on_mouse_release(self, _):
        self.action = None
        self.last_paint_x = self.last_paint_y = None

    def paint(self, x, y, start=False):
        if not self.current_mask: return
        nx, ny = self.canvas.get_norm(x, y)
        if not (0<=nx<=1 and 0<=ny<=1): return
        
        ix, iy = int(nx*self.current_mask.width), int(ny*self.current_mask.height)
        draw = ImageDraw.Draw(self.current_mask)
        r = int(self.brush_size_slider.get() / self.canvas.img_data[4])
        color = 255 if self.mode == "brush" else 0
        
        if not start and self.last_paint_x is not None:
            draw.line([(self.last_paint_x, self.last_paint_y), (ix, iy)], fill=color, width=r*2)
        draw.ellipse([ix-r, iy-r, ix+r, iy+r], fill=color)
        
        self.last_paint_x, self.last_paint_y = ix, iy
        self.apply_mask()

    # --- HELPERS ---
    def get_action(self, e):
        if self.mode in ["brush", "eraser"]: return "paint"
        nx, ny = self.canvas.get_norm(e.x, e.y)
        nx1, ny1, nx2, ny2 = self.crop_norm
        t = 15 / self.canvas.img_data[2]
        if abs(nx-nx1)<t and abs(ny-ny1)<t: return "nw"
        if abs(nx-nx2)<t and abs(ny-ny1)<t: return "ne"
        if abs(nx-nx1)<t and abs(ny-ny2)<t: return "sw"
        if abs(nx-nx2)<t and abs(ny-ny2)<t: return "se"
        if nx1<nx<nx2 and ny1<ny<ny2: return "move"
        return None

    def handle_crop_drag(self, dx, dy, e):
        n1, n2, n3, n4 = self.drag_start_norm
        ratio = self.get_aspect_ratio()
        if self.action == "move":
            self.crop_norm = [n1+dx, n2+dy, n3+dx, n4+dy]
        else:
            if "n" in self.action: n2 += dy
            if "s" in self.action: n4 += dy
            if "w" in self.action: n1 += dx
            if "e" in self.action: n3 += dx
            
            if ratio:
                w, h = (n3-n1)*self.canvas.img_data[2], (n4-n2)*self.canvas.img_data[3]
                if abs(e.x-self.start_x) > abs(e.y-self.start_y):
                    h = w/ratio
                    if "n" in self.action: n2 = n4 - h/self.canvas.img_data[3]
                    else: n4 = n2 + h/self.canvas.img_data[3]
                else:
                    w = h*ratio
                    if "w" in self.action: n1 = n3 - w/self.canvas.img_data[2]
                    else: n3 = n1 + w/self.canvas.img_data[2]
            self.crop_norm = [max(0,min(1,n1)), max(0,min(1,n2)), max(0,min(1,n3)), max(0,min(1,n4))]

    def init_crop_box(self):
        if not self.original_image: return
        w, h = self.original_image.size
        r = self.get_aspect_ratio() or 0.8
        bw = w*0.8
        bh = bw/r
        if bh > h*0.8: bh=h*0.8; bw=bh*r
        nx1 = (w-bw)/2/w; ny1 = (h-bh)/2/h
        self.crop_norm = [nx1, ny1, nx1+bw/w, ny1+bh/h]

    def get_aspect_ratio(self):
        w, h = SIZE_PRESETS.get(self.size_optionemenu.get(), (35, 45))
        return w/h

    def update_preview(self):
        self.canvas.update_image(self.original_image, self.crop_norm, self.mode)

    # --- EXPORT ---
    def export_single(self):
        path = filedialog.asksaveasfilename(defaultextension=".jpg", initialfile="photo.jpg")
        if path:
            w, h = SIZE_PRESETS.get(self.size_optionemenu.get())
            Exporter.get_standardized_photo(self.original_image, w, h).save(path, dpi=(300,300), quality=95)

    def export_print_sheet(self):
        path = filedialog.asksaveasfilename(defaultextension=".jpg", initialfile="sheet.jpg")
        if path:
            w, h = SIZE_PRESETS.get(self.size_optionemenu.get())
            Exporter.generate_print_sheet(self.original_image, w, h).save(path, dpi=(300,300), quality=98)

if __name__ == "__main__":
    app = PassportPhotoApp()
    app.mainloop()
