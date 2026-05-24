# drawCircle

Draws a circle on the canvas, optionally with a drop shadow or outer glow.

## Syntax

```bash
$drawCircle[cx;cy;radius;color;outline;fill;outline_width;anchor;shadow_color;shadow_offset;glow_color;glow_radius]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **cx** | `int/str` | X coordinate of the pivot/center (supports `center`). | Required |
| **cy** | `int/str` | Y coordinate of the pivot/center (supports `center`). | Required |
| **radius** | `int` | Radius of the circle. | Required |
| **color** | `string` | Primary fill color (if `fill` is not specified). | `black` |
| **outline** | `string` | Outline stroke color. | `none` |
| **fill** | `string` | Fill color/style. | `solid` |
| **outline_width**| `int` | Thickness of the outline stroke. | `1` |
| **anchor** | `string` | Positioning pivot point (e.g., `mm` for center, `lt`). | `mm` |
| **shadow_color**| `string` | Color of the circle's drop shadow. | `None` |
| **shadow_offset**| `string` | Shadow offset as `dx,dy` (e.g. `5,5`). | `0,0` |
| **glow_color** | `string` | Color of the circle's outer glow. | `None` |
| **glow_radius**| `int` | Blur radius of the circle's outer glow. | `0` (No glow) |

## Example

```bash
# Golden coin/circle in the center with a soft black drop shadow
$drawCircle[center;center;60;gold;shadow_color=black/60;shadow_offset=4,4]

# Circle with an intense neon green outer glow
$drawCircle[
    cx=200;cy=200;
    radius=40;
    color=white;
    glow_color=green_discord/60;glow_radius=20
]
```
