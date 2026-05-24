# useImageAsCanvas

Loads a local image or remote image (from a URL) and uses it as the base canvas for subsequent drawing operations instead of starting with a blank canvas.

## Syntax

```bash
$useImageAsCanvas[path;h_var;w_var;fixed_width;fixed_height]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **path** | `string` | Local file path or HTTP(S) URL of the base image. | Required |
| **h_var** | `string` | Variable name in which to save the resulting canvas height. | `None` |
| **w_var** | `string` | Variable name in which to save the resulting canvas width. | `None` |
| **fixed_width**| `int` | Force a specific width for the canvas (resizes image). | `None` (Keeps original) |
| **fixed_height**| `int` | Force a specific height for the canvas (resizes image). | `None` (Keeps original) |

## Example

```bash
# Initialize a canvas from a background template and store dimensions
$useImageAsCanvas[assets/bg.png;canvasHeight;canvasWidth]

# Force size and scale to fit 800px wide while maintaining aspect ratio
$useImageAsCanvas[https://example.com/card.jpg;;;800]
```

!!! info
    The engine automatically converts the loaded image to `RGBA` mode to support layered drawing and alpha channels. If one fixed dimension is specified, the aspect ratio of the image is preserved.
