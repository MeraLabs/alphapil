# createCanvas

Creates a new blank image canvas to start drawing. Supports optional Anti-Aliasing (Supersampling).

## Syntax

```bash
$createCanvas[width;height;color;aa;strict;scale]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **width** | `int` | The width of the canvas in pixels. | Required |
| **height** | `int` | The height of the canvas in pixels. | Required |
| **color** | `string` | Background color (Hex, RGB, or Name). | `#000000` (Black) |
| **aa** | `int` | Anti-aliasing factor (e.g., 2, 4). Smooths edges. | `1` (No AA) |
| **strict** | `bool` | If false, errors won't crash the renderer. | `true` |
| **scale** | `int` | Output resolution multiplier (e.g., 2 for HiDPI). | `1` |

## Example

```bash
# Create a 420x520 design that outputs as a crisp 1260x1560 (3x scale) image
$createCanvas[420;520;#000033;2;false;3]
```

!!! info
    Every AlphaPIL script must start with `$createCanvas` or `$loadImage` to initialize the engine. Use `scale` to increase output resolution, and `aa` to smooth edges. The engine automatically applies `UnsharpMask` sharpening when using `scale` or `aa` for professional results.
