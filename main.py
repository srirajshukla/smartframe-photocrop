import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

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
        self.open_button.grid(row=2, column=0, padx=20, pady=10)

        # --- STEP 2: FORMAT ---
        self.format_label = ctk.CTkLabel(self.sidebar_frame, text="2. Format & Size", font=ctk.CTkFont(weight="bold"))
        self.format_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.size_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, 
                                                values=["US (2x2 in)", "EU (35x45 mm)", "India (35x35 mm)", "Custom"])
        self.size_optionemenu.grid(row=4, column=0, padx=20, pady=10)

        # --- STEP 3: AI ACTIONS ---
        self.ai_label = ctk.CTkLabel(self.sidebar_frame, text="3. AI Processing", font=ctk.CTkFont(weight="bold"))
        self.ai_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.auto_crop_button = ctk.CTkButton(self.sidebar_frame, text="Auto-Crop Face")
        self.auto_crop_button.grid(row=6, column=0, padx=20, pady=5)
        
        self.remove_bg_button = ctk.CTkButton(self.sidebar_frame, text="Remove Background", fg_color="transparent", border_width=2)
        self.remove_bg_button.grid(row=7, column=0, padx=20, pady=5)

        # --- STEP 4: REFINEMENT ---
        self.refine_label = ctk.CTkLabel(self.sidebar_frame, text="4. Refinement", font=ctk.CTkFont(weight="bold"))
        self.refine_label.grid(row=8, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.brightness_slider = ctk.CTkSlider(self.sidebar_frame, from_=0, to=2, number_of_steps=100)
        self.brightness_slider.grid(row=9, column=0, padx=20, pady=10)
        self.brightness_slider.set(1.0)

        # --- MAIN PREVIEW AREA ---
        self.preview_frame = ctk.CTkFrame(self)
        self.preview_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.preview_frame.grid_rowconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(0, weight=1)

        self.image_label = ctk.CTkLabel(self.preview_frame, text="No Image Loaded")
        self.image_label.grid(row=0, column=0, sticky="nsew")

        # Variables
        self.original_image = None
        self.preview_image = None

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")])
        if file_path:
            self.original_image = Image.open(file_path)
            self.update_preview()

    def update_preview(self):
        if self.original_image:
            # Calculate preview size maintaining aspect ratio
            width, height = self.original_image.size
            ratio = min(800 / width, 600 / height)
            preview_size = (int(width * ratio), int(height * ratio))
            
            # Use CTkImage for high-DPI support and modern scaling
            self.preview_image = ctk.CTkImage(light_image=self.original_image,
                                             dark_image=self.original_image,
                                             size=preview_size)
            
            self.image_label.configure(image=self.preview_image, text="")

if __name__ == "__main__":
    app = PassportPhotoApp()
    app.mainloop()
