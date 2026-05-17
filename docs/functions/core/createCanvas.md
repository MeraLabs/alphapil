# createCanvas

Creates a new blank image canvas to start drawing. Supports optional Anti-Aliasing (Supersampling).

## Syntax

```bash
$createCanvas[width;height;color;aa]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **width** | `int` | The width of the canvas in pixels. | Required |
| **height** | `int` | The height of the canvas in pixels. | Required |
| **color** | `string` | Background color (Hex, RGB, or Name). | `#000000` (Black) |
| **aa** | `int` | Anti-aliasing factor (e.g., 2, 4). Higher is better quality but slower. | `1` (No AA) |

## Example

```bash
# Create a 1080p canvas with 4x Supersampling for ultra-smooth edges
$createCanvas[1920;1080;#000033;4]
```

!!! info
    Every AlphaPIL script must start with `$createCanvas` or `$loadImage` to initialize the engine. Using `aa` will internally render at a higher resolution and downscale with Lanczos for professional results.
