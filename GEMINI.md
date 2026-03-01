# Passport Photo App - Development Plan

## Project Overview
A unified Python desktop application for creating passport-sized photos from mobile images. Optimized for low-to-mid tier laptops without dedicated GPUs.

## Tech Stack
- **UI Framework:** `customtkinter` (Modern Tkinter wrapper)
- **Face Detection & Alignment:** `MediaPipe` (BlazeFace/Selfie Segmentation)
- **Background Removal:** `rembg` (Supporting `u2netp`, `u2net`, and `isnet-general-use` models)
- **Image Processing:** `Pillow` (PIL) and `OpenCV`
- **Packaging:** `PyInstaller` (for standalone executable)

## Core Features
1. **Interactive Cropping & Formatting**
   - Standard presets (US 2x2", EU 35x45mm, India 35x35mm, etc.).
   - Custom dimensions (mm/px) and shapes (Rectangle, Rounded, Oval).
   - Draggable crop box with aspect ratio locking.
   - Auto-centering and rotation based on face detection.

2. **AI-Powered Background Removal**
   - Toggle between "Fast" (u2netp) and "High Quality" (u2net/isnet) models.
   - Replace background with standard colors (White, Blue, Grey) or custom hex codes.
   - Edge feathering to smooth hair and beard transitions.

3. **Manual Mask Refinement**
   - Brush and Eraser tools to manually fix AI segmentation errors.
   - Real-time preview updates on the mask.

4. **Targeted Face Editing**
   - Face-specific brightness, contrast, and gamma adjustments using the segmentation mask.
   - Optional skin smoothing filter.

5. **Export & Printing**
   - Export single high-resolution image.
   - "Print Sheet" generator (e.g., 4x6 inch layout with multiple photos).
   - Metadata stripping and JPEG file size optimization.

## Architectural Strategy
- **Unified App:** Single Python process handling UI and processing.
- **Proxy Editing:** Perform all UI interactions on a downscaled preview image for responsiveness; apply operations to the full-resolution source only during export.
- **Modular Pipeline:** Separate the AI inference, mask generation, and visual adjustment layers to allow non-destructive editing.

## Implementation Phases
### Phase 1: Environment & UI Scaffolding
- Set up Python virtual environment and install dependencies.
- Create the main `CustomTkinter` window with Sidebar (controls) and Main Canvas (preview).

### Phase 2: Image Handling & Basic Cropping
- Implement image loading and the interactive crop box.
- Add preset dimension logic and aspect ratio management.

### Phase 3: AI Integration
- Integrate `MediaPipe` for auto-cropping and head alignment.
- Integrate `rembg` for background removal with model selection.

### Phase 4: Refinement Tools
- Implement the manual mask brush/eraser.
- Implement face-specific lighting sliders using the mask.

### Phase 5: Export & Optimization
- Build the "Print Sheet" layout engine.
- Finalize export settings (size, metadata, format).
