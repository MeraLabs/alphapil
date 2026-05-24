# drawTextIn

Draws text centered/aligned within a bounding box specified by position and dimensions (`x, y, w, h`) or coordinates (`x1, y1, x2, y2`). It wraps and aligns text beautifully.

## Syntax

```bash
$drawTextIn[x;y;w;h;text;color;size;font;stroke_width;stroke_fill;shadow_color;shadow_offset;glow_color;glow_radius;x1;x2;y1;y2;max_width;truncate_width]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position of the bounding box. | `None` |
| **y** | `int/str` | Y position of the bounding box. | `None` |
| **w** | `int/str` | Width of the bounding box. | `None` |
| **h** | `int/str` | Height of the bounding box. | `None` |
| **text** | `string` | The text string to render. | Required |
| **color** | `string` | Text fill color. | Current state color |
| **size** | `int` | Font size in pixels. | Current state size |
| **font** | `string` | Font family/name or font alias. | Current state font |
| **stroke_width**| `int` | Width of text stroke outline. | `None` |
| **stroke_fill**| `string` | Color of text stroke outline. | `None` |
| **shadow_color**| `string` | Drop shadow color. | `None` |
| **shadow_offset**| `string` | Shadow offset as `dx,dy`. | `0,0` |
| **glow_color** | `string` | Outer glow color. | `None` |
| **glow_radius**| `int` | Outer glow blur radius. | `0` |
| **x1 / x2** | `int/str` | Alternative boundary X coordinates. | `None` |
| **y1 / y2** | `int/str` | Alternative boundary Y coordinates. | `None` |
| **max_width** | `int/str` | Maximum text line wrap width. | `None` |
| **truncate_width**| `int/str`| Truncate text width with `...`. | `None` |

## Example

```bash
# Draw text perfectly centered in a 300x100 card at (50, 50)
$drawTextIn[50;50;300;100;Welcome to AlphaPIL;white;24;bold]
```
