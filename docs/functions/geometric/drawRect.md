# drawRect

Draws a rectangle (or rounded rectangle) on the canvas, optionally with a drop shadow or outer glow.

## Syntax

```bash
$drawRect[x;y;width;height;color;outline;fill;outline_width;radius;anchor;shadow_color;shadow_offset;glow_color;glow_radius]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X coordinate of the starting point (supports `center`). | Required |
| **y** | `int/str` | Y coordinate of the starting point (supports `center`). | Required |
| **width** | `int` | Width of the rectangle. | Required |
| **height** | `int` | Height of the rectangle. | Required |
| **color** | `string` | Primary fill color (if `fill` is not specified). | Required |
| **outline** | `string` | Outline stroke color. | `none` |
| **fill** | `string` | Fill style (`none` or a specific color). | `solid` |
| **outline_width**| `int` | Thickness of the outline stroke. | `1` |
| **radius** | `int` | Corner radius (creates rounded corners). | `0` (Standard corner) |
| **anchor** | `string` | Positioning pivot point (e.g. `lt`, `center`). | `lt` |
| **shadow_color**| `string` | Color of the shape's drop shadow. | `None` |
| **shadow_offset**| `string` | Shadow offset as `dx,dy` (e.g. `5,5`). | `0,0` |
| **glow_color** | `string` | Color of the shape's outer glow. | `None` |
| **glow_radius**| `int` | Blur radius of the shape's outer glow. | `0` (No glow) |

## Examples

```bash
# Draw a simple blue rectangle with a drop shadow
$drawRect[50;50;200;100;blue;shadow_color=black/50;shadow_offset=6,6]

# Draw a beautiful glassmorphic card with a subtle cyan glow
$drawRect[
    x=100;y=100;
    width=300;height=200;
    radius=15;
    color=white/10;
    outline=white/20;outline_width=1;
    glow_color=cyan/30;glow_radius=15
]
```
