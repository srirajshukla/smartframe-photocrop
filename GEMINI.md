# SmartFrame - Development Plan

## Project Overview
A unified Python desktop application for AI-powered portrait editing, background removal, and professional photo formatting. Optimized for low-to-mid tier laptops without dedicated GPUs.

## Tech Stack
- **Dependency & Build Management:** `uv` (Fastest Python package manager)
- **UI Framework:** `customtkinter` (Modern Tkinter wrapper)
- **Face Detection & Alignment:** `OpenCV` Haar Cascades (Lightweight & Fast)
- **Background Removal:** `rembg` (Supporting `u2net`, `isnet`, and `birefnet-portrait` models)
- **Image Processing:** `Pillow` (PIL) and `OpenCV`

## Core Features
1. **Interactive Cropping & Formatting**
   - Standard presets (US 2x2", EU 35x45mm, India 35x35mm, etc.).
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

## Quick Start (Windows)
1. **Setup:** Run `./setup.ps1` (Ensures `uv` is used to sync dependencies).
2. **Run:** Run `./run.ps1` (Launches the app via `uv run`).

## Workflow (CLI)
- **Setup Environment:** `uv sync`
- **Run Application:** `uv run main.py`
- **Add Dependency:** `uv add <package>`

## Architectural Strategy
- **Unified App:** Single Python process handling UI and processing.
- **Proxy Editing:** Perform all UI interactions on a downscaled preview image for responsiveness.
- **Modular Pipeline:** Separate the AI inference, mask generation, and visual adjustment layers.
- **Threaded Processing:** All heavy AI/Image tasks run in background threads to keep the UI responsive.
