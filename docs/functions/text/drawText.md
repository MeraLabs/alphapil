# drawText

Draws text onto the canvas with specified styling, alignment, outline strokes, shadow/glow effects, gradients, and wrapping.

## Syntax

```bash
$drawText[x;y;text;color;size;font;anchor;stroke_width;stroke_fill;shadow_color;shadow_offset;glow_color;glow_radius;max_width;truncate_width;gradient_colors;line_height;letter_spacing]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X coordinate (supports `left`, `center`, `right`). | Required |
| **y** | `int/str` | Y coordinate (supports `top`, `middle`, `bottom`). | Required |
| **text** | `string` | The text string to display. | Required |
| **color** | `string` | Text fill color. | `white` |
| **size** | `int` | Font size in pixels. | `24` |
| **font** | `string` | Font alias loaded via `$loadFont`. | `default` |
| **anchor** | `string` | Text alignment pivot point (e.g. `la`, `mm`, `rs`). | `la` |
| **stroke_width**| `int` | Width of the outline/stroke. | `0` (No stroke) |
| **stroke_fill**| `string` | Color of the outline/stroke. | `black` |
| **shadow_color**| `string` | Color of the text drop shadow. | `None` |
| **shadow_offset**| `string` | Drop shadow offset as `dx,dy` (e.g., `4,4`). | `0,0` |
| **glow_color** | `string` | Color of the outer text glow. | `None` |
| **glow_radius**| `int` | Blur radius of the outer text glow. | `0` (No glow) |
| **max_width** | `int/str` | Wrap text automatically to fit this width. | `None` |
| **truncate_width**| `int/str`| Truncate text with `...` if it exceeds this width. | `None` |
| **gradient_colors**| `string`| Comma-separated gradient colors (e.g. `gold,orange`). | `None` |
| **line_height**| `float` | Line spacing multiplier for wrapped text (e.g. `1.2`). | `1.0` |
| **letter_spacing**| `int` | Tracking (letter-spacing) in pixels. | `0` |

## Examples

### Modern Outline & Glow Effect
```bash
$drawText[
    x=center;y=200;
    text=GLOWING TEXT;
    color=white;
    size=36;
    stroke_width=2;stroke_fill=black;
    glow_color=cyan/50;glow_radius=10
]
```

### Premium Gradient & Drop Shadow
```bash
$drawText[
    x=center;y=300;
    text=CHAMPION;
    size=64;
    gradient_colors=gold,orange;
    stroke_width=3;stroke_fill=black;
    shadow_color=black/60;shadow_offset=5,5
]
```
