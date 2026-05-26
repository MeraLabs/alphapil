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

- **💻 Reverse Template Parser (Import Engine)**: Paste any pre-existing AlphaPIL code into the import panel to instantly parse it line-by-line and load it as editable visual designer layers.
- **🔤 Local Font Discoverer**: Searches and detects all system fonts installed on the computer at server launch and loads them into a searchable dropdown menu inside the Web UI.
- **📊 Simulated Charts & Graphs**: Real-time canvas overlay rendering engines simulating:
  - `$drawBarChart` (spacing, gaps, color themes, rounding radius, bottom labels).
  - `$drawLineChart` (segment connecting, node points, vertex indicators).
  - `$drawProgressBar` (progress track, rounded fill states).
- **🌈 Gradients Builder**: Multi-stop linear or radial gradients customizer. Customize color stops and slide gradient angles dynamically.
- **🤖 Mock Variables Inspector**: Supports testing `{variable_name}` placeholder interpolation live on the canvas. Simply define mock variables in the sidebar dashboard to test dynamic text, colors, and coordinates.
- **📏 Canvas Resize controls**: Drag handles or specify exact canvas widths and heights to visually scale the template canvas.
- **🎯 WYSIWYG Interactive Designer**: Click and drag directly on your canvas to visually draw bounding boxes, circles, rounded rectangles, lines, and text.
- **🔤 Real-Time Client-Side Simulation**:
  - `drawTextMid` Centering & Truncation: Centered text box alignment that dynamically clips overflowing text and appends `...` natively inside the browser context.
  - `drawTextIn` Decremental Scaling: Automatically estimates and reduces the active font size step-by-step to fit text entirely within your visually drawn bounds.
- **📚 Multi-Element Composition**: Customize fill colors, outlines, stroke widths, corner radii, and custom paths. Move layers up/down or delete them dynamically.
- **💾 Complete Template Export**: Instantly copy individual command snippets or export the **entire composed multi-line AlphaPIL template code block** to paste directly into your generator.
- **🎯 Real-Time Crosshair Reticles**: Live pixel-precise crosshair reticles overlaying the canvas.
- **🔍 Perfect Scale Tracking**: Mouse interactions are automatically translated to coordinate spaces relative to the *original, natural dimensions* of the background image, regardless of browser scaling.
- **📁 Dynamic Background Drag-and-Drop**: Easily drag and drop any image or browse to swap canvas backgrounds without restarting the local HTTP server.


