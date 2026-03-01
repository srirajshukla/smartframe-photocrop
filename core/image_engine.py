import cv2
import numpy as np
from PIL import Image, ImageEnhance
from rembg import remove

class ImageEngine:
    @staticmethod
    def detect_face(pil_image):
        """Detects the largest face and returns normalized coordinates [fx, fy, fw, fh]."""
        img_rgb = pil_image.convert("RGB")
        image_arr = np.array(img_rgb)
        img_bgr = cv2.cvtColor(image_arr, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(cascade_path)
        
        faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
        
        if len(faces) == 0:
            return None
            
        x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])
        img_h, img_w = image_arr.shape[:2]
        
        return [x/img_w, y/img_h, w/img_w, h/img_h]

    @staticmethod
    def remove_bg(pil_image, model_name="u2net"):
        """Removes background using rembg and returns (RGBA image, Alpha mask)."""
        from rembg import new_session
        session = new_session(model_name)
        output_rgba = remove(pil_image, session=session)
        mask = output_rgba.split()[3]
        return output_rgba, mask

    @staticmethod
    def apply_filters(base_image, mask, bg_color_hex, 
                      brightness=1.0, contrast=1.0, saturation=1.0, 
                      sharpness=1.0, smoothing=0.0, lightening=0.0,
                      is_editing_mask=False):
        """Applies all adjustments and composites foreground onto background."""
        if not base_image or not mask:
            return base_image

        # 1. Smoothing (Bilateral)
        if smoothing > 0:
            img_np = np.array(base_image)
            d = int(smoothing * 10) + 1
            sigma = smoothing * 40
            img_np = cv2.bilateralFilter(img_np, d, sigma, sigma)
            fg = Image.fromarray(img_np)
        else:
            fg = base_image.copy()

        # 2. Skin Lightening
        if lightening > 0:
            img_np = np.array(fg)
            img_ycrcb = cv2.cvtColor(img_np, cv2.COLOR_RGB2YCrCb)
            lower = np.array([0, 133, 77], dtype=np.uint8)
            upper = np.array([255, 173, 127], dtype=np.uint8)
            skin_mask = cv2.inRange(img_ycrcb, lower, upper)
            skin_mask = cv2.GaussianBlur(skin_mask, (7, 7), 0) / 255.0
            
            boost = 1.0 + (lightening * 0.25)
            img_ycrcb = img_ycrcb.astype(float)
            img_ycrcb[:,:,0] = img_ycrcb[:,:,0] * (1.0 + (boost - 1.0) * skin_mask)
            img_ycrcb[:,:,0] = np.clip(img_ycrcb[:,:,0], 0, 255)
            fg = Image.fromarray(cv2.cvtColor(img_ycrcb.astype(np.uint8), cv2.COLOR_YCrCb2RGB))

        # 3. Enhancements
        if brightness != 1.0: fg = ImageEnhance.Brightness(fg).enhance(brightness)
        if contrast != 1.0: fg = ImageEnhance.Contrast(fg).enhance(contrast)
        if saturation != 1.0: fg = ImageEnhance.Color(fg).enhance(saturation)
        if sharpness != 1.0: fg = ImageEnhance.Sharpness(fg).enhance(sharpness)

        # 4. Composition
        if is_editing_mask:
            overlay_bg = base_image.copy().convert("RGBA")
            red_layer = Image.new("RGBA", overlay_bg.size, (255, 0, 0, 80))
            overlay_bg = Image.alpha_composite(overlay_bg, red_layer).convert("RGB")
            return Image.composite(fg, overlay_bg, mask)
        else:
            solid_bg = Image.new("RGB", base_image.size, bg_color_hex)
            return Image.composite(fg, solid_bg, mask)
