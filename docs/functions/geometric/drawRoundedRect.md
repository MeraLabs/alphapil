# drawRoundedRect

Draws a rectangle with rounded corners, optionally with a drop shadow or outer glow.

## Syntax

```bash
$drawRoundedRect[x;y;width;height;radius;color;outline;fill;outline_width;anchor;shadow_color;shadow_offset;glow_color;glow_radius]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X coordinate of the starting point (supports `center`). | Required |
| **y** | `int/str` | Y coordinate of the starting point (supports `center`). | Required |
| **width** | `int` | Width of the rectangle. | Required |
| **height** | `int` | Height of the rectangle. | Required |
| **radius** | `int` | Corner radius (creates rounded corners). | `10` |
| **color** | `string` | Primary fill color (if `fill` is not specified). | `black` |
| **outline** | `string` | Outline stroke color. | `none` |
| **fill** | `string` | Fill style (`none` or a specific color). | `solid` |
| **outline_width**| `int` | Thickness of the outline stroke. | `1` |
| **anchor** | `string` | Positioning pivot point (e.g. `lt`, `center`). | `lt` |
| **shadow_color**| `string` | Color of the shape's drop shadow. | `None` |
| **shadow_offset**| `string` | Shadow offset as `dx,dy` (e.g. `5,5`). | `0,0` |
| **glow_color** | `string` | Color of the shape's outer glow. | `None` |
| **glow_radius**| `int` | Blur radius of the shape's outer glow. | `0` (No glow) |

## Example

```bash
# A beautiful rounded panel with a soft purple outer glow
$drawRoundedRect[
    x=100;y=100;
    width=300;height=200;
    radius=20;
    color=white/10;
    outline=white/30;
    glow_color=purple/45;glow_radius=15
]
```

!!! note
    `$drawRoundedRect` is a convenience wrapper around `$drawRect` with the same capabilities and rendering optimizations.
