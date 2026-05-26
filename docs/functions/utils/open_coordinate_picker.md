# Open Coordinate Picker 🎯

AlphaPIL provides an interactive web-based coordinate picker to help you easily inspect and select exact pixel coordinates on any generated canvas. 

You can launch the coordinate picker from your terminal or directly inside your Python code.

---

## Command Line Interface (CLI)

When `alphapil` is installed, a command-line script called `alphapil-picker` is registered globally.

### Usage

```bash
alphapil-picker <path_to_image>
```

For example, to inspect `output.png`:
```bash
alphapil-picker output.png
```

### Auto-Detection
If you run `alphapil-picker` without specifying a path, it will automatically look for standard default canvas names in your current folder:
1. `output.png`
2. `output.jpg`
3. `canvas.png`

---

## Python Programmatic API

You can launch the coordinate picker directly from your Python scripts or Jupyter Notebooks using either the standalone function or the Canvas Engine instance method.

### Standalone Function

```python
from alphapil import open_coordinate_picker

# Launch the visual coordinate picker server
open_coordinate_picker("output.png")
```

### Canvas Engine Method

```python
from alphapil import CanvasEngine

engine = CanvasEngine()
# ... generate / save your canvas ...

# Launch coordinate picker on the output image
engine.open_coordinate_picker("output.png")
```

---

## Features

- **Real-Time Crosshair Reticles**: Moving the mouse over the image displays real-time crosshair guides matching the cursor position.
- **Perfect Scale Tracking**: Coordinates are calculated relative to the *original natural dimensions* of the image, even when the browser or HTML canvas scales the image visually.
- **Single-Click Copy**: Clicking anywhere on the image copies the coordinates directly to your clipboard in the format `X;Y` (semicolon separated), which is standard for AlphaPIL templates.
- **Dynamic File Drag-and-Drop**: You can drag and drop any local image or use the browse card to switch files instantly without restarting the server.
