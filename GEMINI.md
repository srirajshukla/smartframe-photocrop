# SmartFrame - Development Plan

## Project Overview
A unified Python desktop application for AI-powered portrait editing, background removal, and professional photo formatting. Optimized for low-to-mid tier laptops without dedicated GPUs.

## Tech Stack
- **UI Framework:** `customtkinter` (Modern Tkinter wrapper)
- **Face Detection & Alignment:** `MediaPipe` / `OpenCV` Haar Cascades
- **Background Removal:** `rembg` (Supporting `u2net`, `isnet`, and `birefnet-portrait` models)
- **Image Processing:** `Pillow` (PIL) and `OpenCV`
- **Packaging:** `PyInstaller` (for standalone executable)

## Core Features
1. **Interactive Cropping & Formatting**
   - Standard presets (US 2x2", EU 35x45mm, India 35x35mm, etc.).
   - Custom dimensions (mm/px) and shapes (Rectangle, Rounded, Oval).
   - Draggable crop box with aspect ratio locking.
   - Auto-centering and rotation based on face detection.

2. **AI-Powered Background Removal**
   - Toggle between "Fast", "Balanced", and "Ultra Quality" (BiRefNet) models.
   - Replace background with standard colors (White, Blue, Grey) or custom hex codes.
   - Advanced alpha matting for smooth hair and edge transitions.

3. **Manual Mask Refinement**
   - Brush and Eraser tools to manually fix AI segmentation errors.
   - Real-time preview updates on the mask.

4. **Targeted Face Editing**
   - Face-specific brightness, contrast, and gamma adjustments using the segmentation mask.
   - "Skin Glow" and "Smooth Skin" retouching filters.

5. **Export & Printing**
   - Export single high-resolution image.
   - "Print Sheet" generator (e.g., 4x6 inch layout with multiple photos).
   - Metadata stripping and JPEG file size optimization.

## Architectural Strategy
- **Unified App:** Single Python process handling UI and processing.
- **Proxy Editing:** Perform all UI interactions on a downscaled preview image for responsiveness; apply operations to the full-resolution source only during export.
- **Modular Pipeline:** Separate the AI inference, mask generation, and visual adjustment layers to allow non-destructive editing.
- **Threaded Processing:** All heavy AI/Image tasks run in background threads to keep the UI responsive.
