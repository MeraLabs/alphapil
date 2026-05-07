# createCanvas

Creates a new blank image canvas to start drawing.

## Syntax

```bash
$createCanvas[width;height;color]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **width** | `int` | The width of the canvas in pixels. | Required |
| **height** | `int` | The height of the canvas in pixels. | Required |
| **color** | `string` | Background color (Hex, RGB, or Name). | `#000000` (Black) |

## Example

```bash
# Create a 1080p canvas with a dark blue background
$createCanvas[1920;1080;#000033]
```

!!! info
    Every AlphaPIL script must start with `$createCanvas` or `$loadImage` to initialize the engine.
