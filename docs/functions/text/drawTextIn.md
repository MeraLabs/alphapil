# drawTextIn

Draws text perfectly centered/fitted within a bounding box specified by `x1`, `y1`, `x2`, `y2`. If the text rendered width or height exceeds the box's boundaries, the function **automatically scales down the font size step-by-step** until the entire text fits perfectly inside the box without being truncated.

## Syntax

```bash
$drawTextIn[x1;y1;x2;y2;text;color;size;font;stroke_width;stroke_fill;shadow_color;shadow_offset;glow_color;glow_radius;variation]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x1** | `int/str` | Start X coordinate of the bounding box. | Required |
| **y1** | `int/str` | Start Y coordinate of the bounding box. | Required |
| **x2** | `int/str` | End X coordinate of the bounding box. | Required |
| **y2** | `int/str` | End Y coordinate of the bounding box. | Required |
| **text** | `string` | The text string to render. | Required |
| **color** | `string` | Text fill color. | Current state color |
| **size** | `int` | Maximum font size in pixels (scales down if needed). | Current state size |
| **font** | `string` | Font family/name or font alias. | Current state font |
| **stroke_width**| `int` | Width of text stroke outline. | `None` |
| **stroke_fill**| `string` | Color of text stroke outline. | `None` |
| **shadow_color**| `string` | Drop shadow color. | `None` |
| **shadow_offset**| `string` | Shadow offset as `dx,dy`. | `0,0` |
| **glow_color** | `string` | Outer glow color. | `None` |
| **glow_radius**| `int` | Outer glow blur radius. | `0` |
| **variation** | `string` | Variable font variation axes (e.g. `wght=700`). | `None` |

## Example

```bash
# Draw text perfectly fitted inside a box from X=73 to 217 and Y=935 to 1322
# The text will automatically scale down from size 14 to fit inside these bounds if it exceeds
$drawTextIn[73;1322;217;935;Captain America;white;14;Name]
```
