import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
Image.MAX_IMAGE_PIXELS = None
import os
import cv2
import numpy as np

class PassportPhotoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Passport Photo Creator")
        self.geometry("1100x700")

        # Configure grid layout (1x2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(10, weight=1)

        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Passport Photo", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # --- STEP 1: FILE ---
        self.file_label = ctk.CTkLabel(self.sidebar_frame, text="1. File Management", font=ctk.CTkFont(weight="bold"))
        self.file_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.open_button = ctk.CTkButton(self.sidebar_frame, text="Open Image", command=self.open_image)
        self.open_button.grid(row=2, column=0, padx=20, pady=(10, 5))
        
        self.rotate_button = ctk.CTkButton(self.sidebar_frame, text="Rotate 90°", command=self.rotate_image)
        self.rotate_button.grid(row=3, column=0, padx=20, pady=(5, 10))

        # --- STEP 2: FORMAT ---
        self.format_label = ctk.CTkLabel(self.sidebar_frame, text="2. Format & Size", font=ctk.CTkFont(weight="bold"))
        self.format_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.size_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, 
            values=["US (2x2 in)", "EU (35x45 mm)", "India (35x35 mm)", "Custom"],
            command=self.on_format_change
        )
        self.size_optionemenu.grid(row=5, column=0, padx=20, pady=10)

        # --- STEP 3: AI ACTIONS ---
        self.ai_label = ctk.CTkLabel(self.sidebar_frame, text="3. AI Processing", font=ctk.CTkFont(weight="bold"))
        self.ai_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.auto_crop_button = ctk.CTkButton(self.sidebar_frame, text="Auto-Crop Face", command=self.auto_crop_face)
        self.auto_crop_button.grid(row=7, column=0, padx=20, pady=5)
        
        self.remove_bg_button = ctk.CTkButton(self.sidebar_frame, text="Remove Background", fg_color="transparent", border_width=2)
        self.remove_bg_button.grid(row=8, column=0, padx=20, pady=5)

        # --- STEP 4: REFINEMENT ---
        self.refine_label = ctk.CTkLabel(self.sidebar_frame, text="4. Refinement", font=ctk.CTkFont(weight="bold"))
        self.refine_label.grid(row=9, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.brightness_slider = ctk.CTkSlider(self.sidebar_frame, from_=0, to=2, number_of_steps=100)
        self.brightness_slider.grid(row=10, column=0, padx=20, pady=10)
        self.brightness_slider.set(1.0)

        # --- MAIN PREVIEW AREA ---
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)

        # Use Tkinter Canvas for drawing
        self.canvas = tk.Canvas(self.preview_frame, bg="#2b2b2b", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Bind mouse events
        self.canvas.bind("<ButtonPress-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
        self.preview_frame.bind("<Configure>", self.on_resize)

        # Variables
        self.original_image = None
        self.tk_image = None
        self.preview_scale = 1.0
        
        # Image placement on canvas
        self.img_x = 0
        self.img_y = 0
        self.img_w = 0
        self.img_h = 0
        
        # Crop State (Normalized coordinates 0.0 to 1.0)
        self.crop_norm = [0.25, 0.25, 0.75, 0.75] # nx1, ny1, nx2, ny2
        self.action = None
        self.start_x = 0
        self.start_y = 0
        self.drag_start_norm = [0, 0, 0, 0]
        self.handle_size = 10
        self._resize_timer = None

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.init_crop_box()
            self.update_preview()

    def rotate_image(self):
        if self.original_image:
            self.original_image = self.original_image.rotate(-90, expand=True)
            self.init_crop_box()
            self.update_preview()

    def auto_crop_face(self):
        if not self.original_image:
            return

        # Convert PIL image to numpy array for OpenCV
        img_rgb = self.original_image.convert("RGB")
        image_arr = np.array(img_rgb)
        
        # Convert RGB to BGR (OpenCV format) and then to Grayscale
        img_bgr = cv2.cvtColor(image_arr, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        # Load the pre-trained Haar cascade for frontal face
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5, 
            minSize=(100, 100)
        )
        
        if len(faces) == 0:
            print("No face detected.")
            return
            
        # Get the largest face by area
        x, y, w_face, h_face = max(faces, key=lambda rect: rect[2] * rect[3])
        
        img_h, img_w = image_arr.shape[:2]
        
        # Normalized bounding box
        fx = x / img_w
        fy = y / img_h
        fw = w_face / img_w
        fh = h_face / img_h
        
        # Passport photo logic: face usually occupies 50-60% of the image height.
        target_face_height_ratio = 0.55
        
        crop_h = fh / target_face_height_ratio
        
        ratio = self.get_aspect_ratio()
        if ratio:
            crop_w = crop_h * ratio
        else:
            crop_w = crop_h * 0.8  # fallback ratio
            
        # Calculate top left corner to center the face
        face_cx = fx + fw / 2.0
        face_cy = fy + fh / 2.0
        
        # In a passport photo, the face center is usually slightly above the vertical center
        # e.g., face center is at 45% of the total height from the top
        crop_cx = face_cx
        crop_cy = face_cy + (crop_h * 0.05) 
        
        nx1 = crop_cx - crop_w / 2.0
        nx2 = crop_cx + crop_w / 2.0
        ny1 = crop_cy - crop_h / 2.0
        ny2 = crop_cy + crop_h / 2.0
        
        # Clamp to image boundaries
        if nx1 < 0:
            nx2 -= nx1
            nx1 = 0
        if ny1 < 0:
            ny2 -= ny1
            ny1 = 0
        if nx2 > 1.0:
            nx1 -= (nx2 - 1.0)
            nx2 = 1.0
        if ny2 > 1.0:
            ny1 -= (ny2 - 1.0)
            ny2 = 1.0
            
        # Final clamp just in case
        nx1 = max(0.0, nx1)
        ny1 = max(0.0, ny1)
        nx2 = min(1.0, nx2)
        ny2 = min(1.0, ny2)
        
        # If after clamping the aspect ratio is destroyed, we re-enforce it
        if ratio:
            curr_w_px = (nx2 - nx1) * img_w
            curr_h_px = (ny2 - ny1) * img_h
            if curr_h_px > 0:
                curr_ratio = curr_w_px / curr_h_px
                if abs(curr_ratio - ratio) > 0.01:
                    new_w_px = curr_h_px * ratio
                    nx2 = nx1 + new_w_px / img_w
                    if nx2 > 1.0: 
                        nx2 = 1.0
                        new_w_px = (nx2 - nx1) * img_w
                        new_h_px = new_w_px / ratio
                        ny2 = ny1 + new_h_px / img_h
        
        self.crop_norm = [nx1, ny1, nx2, ny2]
        self.update_preview()

    def on_format_change(self, choice):
        if self.original_image:
            self.init_crop_box()
            self.update_preview()

    def get_aspect_ratio(self):
        val = self.size_optionemenu.get()
        if "2x2" in val: return 1.0
        if "35x45" in val: return 35.0 / 45.0
        if "35x35" in val: return 1.0
        return None

    def init_crop_box(self):
        if not self.original_image: return
        ratio = self.get_aspect_ratio()
        
        w, h = self.original_image.size
        # Center crop, 80% size
        if ratio:
            box_w = w * 0.8
            box_h = box_w / ratio
            if box_h > h * 0.8:
                box_h = h * 0.8
                box_w = box_h * ratio
        else:
            box_w = w * 0.8
            box_h = h * 0.8
            
        nx1 = (w - box_w) / 2 / w
        nx2 = nx1 + box_w / w
        ny1 = (h - box_h) / 2 / h
        ny2 = ny1 + box_h / h
        
        self.crop_norm = [nx1, ny1, nx2, ny2]

    def on_resize(self, event):
        if self._resize_timer:
            self.after_cancel(self._resize_timer)
        self._resize_timer = self.after(100, self.update_preview)

    def update_preview(self):
        if not self.original_image: return
        
        self.canvas.update_idletasks()
        c_width = self.canvas.winfo_width()
        c_height = self.canvas.winfo_height()
        
        if c_width <= 1 or c_height <= 1:
            return # Too small to draw
            
        w, h = self.original_image.size
        self.preview_scale = min(c_width / w, c_height / h)
        
        self.img_w = int(w * self.preview_scale)
        self.img_h = int(h * self.preview_scale)
        self.img_x = (c_width - self.img_w) // 2
        self.img_y = (c_height - self.img_h) // 2
        
        resized = self.original_image.resize((self.img_w, self.img_h), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        
        self.canvas.delete("all")
        self.canvas.create_image(self.img_x, self.img_y, image=self.tk_image, anchor="nw")
        
        self.draw_crop_box()

    def draw_crop_box(self):
        if not self.original_image: return
        
        nx1, ny1, nx2, ny2 = self.crop_norm
        x1 = self.img_x + nx1 * self.img_w
        y1 = self.img_y + ny1 * self.img_h
        x2 = self.img_x + nx2 * self.img_w
        y2 = self.img_y + ny2 * self.img_h
        
        self.canvas.delete("crop")
        
        # Dimming regions
        self.canvas.create_rectangle(self.img_x, self.img_y, self.img_x + self.img_w, y1, fill="black", stipple="gray50", outline="", tags="crop")
        self.canvas.create_rectangle(self.img_x, y2, self.img_x + self.img_w, self.img_y + self.img_h, fill="black", stipple="gray50", outline="", tags="crop")
        self.canvas.create_rectangle(self.img_x, y1, x1, y2, fill="black", stipple="gray50", outline="", tags="crop")
        self.canvas.create_rectangle(x2, y1, self.img_x + self.img_w, y2, fill="black", stipple="gray50", outline="", tags="crop")
        
        # Crop outline
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="#00a8ff", width=2, tags="crop")
        
        # Handles
        hs = self.handle_size
        handles = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
        for hx, hy in handles:
            self.canvas.create_rectangle(hx - hs/2, hy - hs/2, hx + hs/2, hy + hs/2, fill="#00a8ff", outline="white", tags="crop")

        # Draw dimensions for custom crop
        if self.size_optionemenu.get() == "Custom":
            w, h = self.original_image.size
            crop_w_px = int((nx2 - nx1) * w)
            crop_h_px = int((ny2 - ny1) * h)
            if crop_h_px > 0:
                ratio_val = crop_w_px / crop_h_px
                text_str = f"{crop_w_px} x {crop_h_px} (Ratio: {ratio_val:.2f})"
                
                # Draw text with black background to ensure it is readable
                text_id = self.canvas.create_text(x1 + 8, y1 + 8, text=text_str, fill="white", anchor="nw", font=("Arial", 12, "bold"), tags="crop")
                bbox = self.canvas.bbox(text_id)
                if bbox:
                    bg_id = self.canvas.create_rectangle(bbox[0]-4, bbox[1]-4, bbox[2]+4, bbox[3]+4, fill="black", outline="", tags="crop")
                    self.canvas.tag_lower(bg_id, text_id)

    def get_norm_coords(self, cx, cy):
        nx = (cx - self.img_x) / self.img_w
        ny = (cy - self.img_y) / self.img_h
        return nx, ny

    def get_action(self, event):
        nx, ny = self.get_norm_coords(event.x, event.y)
        nx1, ny1, nx2, ny2 = self.crop_norm
        
        tx = (self.handle_size + 5) / self.img_w
        ty = (self.handle_size + 5) / self.img_h
        
        if abs(nx - nx1) < tx and abs(ny - ny1) < ty: return "nw"
        if abs(nx - nx2) < tx and abs(ny - ny1) < ty: return "ne"
        if abs(nx - nx1) < tx and abs(ny - ny2) < ty: return "sw"
        if abs(nx - nx2) < tx and abs(ny - ny2) < ty: return "se"
        
        if nx1 < nx < nx2 and ny1 < ny < ny2: return "move"
        
        return None

    def on_mouse_press(self, event):
        if not self.original_image: return
        self.action = self.get_action(event)
        self.start_x = event.x
        self.start_y = event.y
        self.drag_start_norm = list(self.crop_norm)

    def on_mouse_drag(self, event):
        if not self.action or not self.original_image: return
        
        dx = (event.x - self.start_x) / self.img_w
        dy = (event.y - self.start_y) / self.img_h
        
        nx1, ny1, nx2, ny2 = self.drag_start_norm
        ratio = self.get_aspect_ratio()
        
        if self.action == "move":
            nx1 += dx
            nx2 += dx
            ny1 += dy
            ny2 += dy
            
            # Bounds check
            w_norm = nx2 - nx1
            h_norm = ny2 - ny1
            if nx1 < 0: nx1, nx2 = 0, w_norm
            if nx2 > 1: nx1, nx2 = 1 - w_norm, 1
            if ny1 < 0: ny1, ny2 = 0, h_norm
            if ny2 > 1: ny1, ny2 = 1 - h_norm, 1
        else:
            if "n" in self.action: ny1 += dy
            if "s" in self.action: ny2 += dy
            if "w" in self.action: nx1 += dx
            if "e" in self.action: nx2 += dx
            
            # Constrain to valid rect
            if nx1 > nx2 - 0.05:
                if "w" in self.action: nx1 = nx2 - 0.05
                else: nx2 = nx1 + 0.05
            if ny1 > ny2 - 0.05:
                if "n" in self.action: ny1 = ny2 - 0.05
                else: ny2 = ny1 + 0.05
                
            if ratio:
                # Enforce ratio based on the primary direction of movement
                new_w_px = (nx2 - nx1) * self.img_w
                new_h_px = (ny2 - ny1) * self.img_h
                
                if abs(event.x - self.start_x) > abs(event.y - self.start_y):
                    # Width drives height
                    new_h_px = new_w_px / ratio
                    if "n" in self.action: ny1 = ny2 - new_h_px / self.img_h
                    else: ny2 = ny1 + new_h_px / self.img_h
                else:
                    # Height drives width
                    new_w_px = new_h_px * ratio
                    if "w" in self.action: nx1 = nx2 - new_w_px / self.img_w
                    else: nx2 = nx1 + new_w_px / self.img_w

            # Global bounds check after ratio enforcing
            if nx1 < 0: nx1 = 0
            if ny1 < 0: ny1 = 0
            if nx2 > 1: nx2 = 1
            if ny2 > 1: ny2 = 1
            
            # Re-enforce ratio if bounds were hit
            if ratio:
                curr_w_px = (nx2 - nx1) * self.img_w
                curr_h_px = (ny2 - ny1) * self.img_h
                # Add tiny epsilon to avoid floating point issues
                if curr_w_px / curr_h_px > ratio + 0.001:
                    new_w_px = curr_h_px * ratio
                    if "w" in self.action: nx1 = nx2 - new_w_px / self.img_w
                    else: nx2 = nx1 + new_w_px / self.img_w
                elif curr_w_px / curr_h_px < ratio - 0.001:
                    new_h_px = curr_w_px / ratio
                    if "n" in self.action: ny1 = ny2 - new_h_px / self.img_h
                    else: ny2 = ny1 + new_h_px / self.img_h

        self.crop_norm = [nx1, ny1, nx2, ny2]
        self.draw_crop_box()

    def on_mouse_release(self, event):
        self.action = None

if __name__ == "__main__":
    app = PassportPhotoApp()
    app.mainloop()