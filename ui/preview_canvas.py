import tkinter as tk
from PIL import Image, ImageTk, ImageDraw

class PreviewCanvas(tk.Canvas):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, bg="#2b2b2b", highlightthickness=0, **kwargs)
        self.app = app
        self.tk_image = None
        self.handle_size = 10
        
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

    def update_image(self, pil_image, crop_norm, mode):
        if not pil_image: return
        
        self.update_idletasks()
        cw, ch = self.winfo_width(), self.winfo_height()
        if cw <= 1: return
        
        w, h = pil_image.size
        scale = min(cw/w, ch/h)
        iw, ih = int(w*scale), int(h*scale)
        ix, iy = (cw-iw)//2, (ch-ih)//2
        
        resized = pil_image.resize((iw, ih), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        
        self.delete("all")
        self.create_image(ix, iy, image=self.tk_image, anchor="nw")
        
        # Draw crop box if in crop mode
        if mode == "crop":
            nx1, ny1, nx2, ny2 = crop_norm
            x1, y1 = ix + nx1*iw, iy + ny1*ih
            x2, y2 = ix + nx2*iw, iy + ny2*ih
            
            # Dimming
            self.create_rectangle(ix, iy, ix+iw, y1, fill="black", stipple="gray50", outline="", tags="crop")
            self.create_rectangle(ix, y2, ix+iw, iy+ih, fill="black", stipple="gray50", outline="", tags="crop")
            self.create_rectangle(ix, y1, x1, y2, fill="black", stipple="gray50", outline="", tags="crop")
            self.create_rectangle(x2, y1, ix+iw, y2, fill="black", stipple="gray50", outline="", tags="crop")
            self.create_rectangle(x1, y1, x2, y2, outline="#00a8ff", width=2, tags="crop")
            
            for hx, hy in [(x1,y1), (x2,y1), (x1,y2), (x2,y2)]:
                self.create_rectangle(hx-5, hy-5, hx+5, hy+5, fill="#00a8ff", outline="white", tags="crop")

            if self.app.size_optionemenu.get() == "Custom":
                cw_px, ch_px = int((nx2-nx1)*w), int((ny2-ny1)*h)
                txt = f"{cw_px}x{ch_px} ({cw_px/ch_px:.2f})"
                tid = self.create_text(x1+8, y1+8, text=txt, fill="white", anchor="nw", font=("Arial", 10, "bold"), tags="crop")
                bbox = self.bbox(tid)
                if bbox: self.tag_lower(self.create_rectangle(bbox[0]-2, bbox[1]-2, bbox[2]+2, bbox[3]+2, fill="black", outline="", tags="crop"), tid)

        # Store for coordinate mapping
        self.img_data = (ix, iy, iw, ih, scale)

    def get_norm(self, x, y):
        ix, iy, iw, ih, _ = self.img_data
        return (x-ix)/iw, (y-iy)/ih

    def on_press(self, e): self.app.on_mouse_press(e)
    def on_drag(self, e): self.app.on_mouse_drag(e)
    def on_release(self, e): self.app.on_mouse_release(e)
