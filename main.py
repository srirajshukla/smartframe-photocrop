from ui.main_window import PassportPhotoApp
from PIL import Image

# Disable PIL limit for high-res mobile photos
Image.MAX_IMAGE_PIXELS = None

if __name__ == "__main__":
    app = PassportPhotoApp()
    app.mainloop()
