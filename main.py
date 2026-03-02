from ui.main_window import PassportPhotoApp
from PIL import Image

# Disable PIL limit for high-res mobile photos
Image.MAX_IMAGE_PIXELS = None

def main():
    app = PassportPhotoApp()
    app.mainloop()
    

if __name__ == "__main__":
    main()
