from PIL import Image, ImageDraw
from utils.constants import (
    DPI, PRINT_SHEET_SIZE, MARGIN_GAP_LARGE, MARGIN_GAP_SMALL,
    SHEET_OUTLINE
)

class Exporter:
    @staticmethod
    def get_standardized_photo(image, target_w_mm, target_h_mm):
        if not image: return None
        
        target_ratio = target_w_mm / target_h_mm
        img_w, img_h = image.size
        img_ratio = img_w / img_h
        
        if img_ratio > target_ratio:
            new_w = img_h * target_ratio
            left = (img_w - new_w) / 2
            temp = image.crop((left, 0, left + new_w, img_h))
        else:
            new_h = img_w / target_ratio
            top = (img_h - new_h) / 2
            temp = image.crop((0, top, img_w, top + new_h))
            
        w_px = int((target_w_mm / 25.4) * DPI)
        h_px = int((target_h_mm / 25.4) * DPI)
        
        return temp.resize((w_px, h_px), Image.Resampling.LANCZOS)

    @staticmethod
    def generate_print_sheet(image, target_w_mm, target_h_mm):
        if not image: return None
        
        sheet_w, sheet_h = PRINT_SHEET_SIZE
        photo_w = int((target_w_mm / 25.4) * DPI)
        photo_h = int((target_h_mm / 25.4) * DPI)
        
        def calc_fit(sw, sh, pw, ph, m, g):
            return int(max(0, (sw - 2*m + g) // (pw + g))), int(max(0, (sh - 2*m + g) // (ph + g)))

        # Use large margins/gaps for small photos, and zero for large ones (e.g. 5x7 on 4x6)
        m, g = MARGIN_GAP_LARGE if (photo_w < 600 and photo_h < 600) else MARGIN_GAP_SMALL
        
        c1, r1 = calc_fit(sheet_w, sheet_h, photo_w, photo_h, m[0], g[0])
        c2, r2 = calc_fit(sheet_w, sheet_h, photo_h, photo_w, m[0], g[0])
        
        use_rotated = (c2 * r2) > (c1 * r1)
        num_cols, num_rows = (c2, r2) if use_rotated else (c1, r1)
        
        photo = Exporter.get_standardized_photo(image, target_w_mm, target_h_mm)
        if use_rotated:
            photo = photo.rotate(90, expand=True)
            pw, ph = photo_h, photo_w
        else:
            pw, ph = photo_w, photo_h
            
        sheet = Image.new("RGB", (sheet_w, sheet_h), "WHITE")
        draw = ImageDraw.Draw(sheet)
        
        grid_w = num_cols * pw + (num_cols - 1) * g[0]
        grid_h = num_rows * ph + (num_rows - 1) * g[1]
        ox, oy = (sheet_w - grid_w) // 2, (sheet_h - grid_h) // 2
        
        for r in range(num_rows):
            for c in range(num_cols):
                x, y = ox + c * (pw + g[0]), oy + r * (ph + g[1])
                sheet.paste(photo, (x, y))
                draw.rectangle([x, y, x + pw, y + ph], outline=SHEET_OUTLINE)
                
        return sheet
