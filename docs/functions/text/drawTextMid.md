# drawTextMid

Centers text perfectly between two X coordinates (`x1`, `x2`) and two Y coordinates (`y1`, `y2`). If the text width exceeds the available horizontal space (`x2 - x1`), it automatically truncates the text with `...` to keep it within bounds.

## Syntax

```bash
$drawTextMid[x1;y1;x2;y2;text;color;size;font;stroke_width;stroke_fill;shadow_color;shadow_offset;glow_color;glow_radius;variation]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x1** | `int/str` | Start X coordinate. | Required |
| **y1** | `int/str` | Start Y coordinate. | Required |
| **x2** | `int/str` | End X coordinate (used to calculate horizontal center and maximum width). | Required |
| **y2** | `int/str` | End Y coordinate (used to calculate vertical center). | Required |
| **text** | `string` | The text to draw. | Required |
| **color** | `string` | Text fill color. | `white` |
| **size** | `int` | Font size in pixels. | `24` |
| **font** | `string` | Font alias loaded via `$loadFont`. | `default` |
| **variation** | `string` | Variable font variation axes (e.g. `wght=700`). | `None` |

## Example

```bash
# Center text inside a horizontal region from X=100 to X=400, auto-truncating if it is too long
$drawTextMid[100;50;400;100;This text is extremely long and will be auto-truncated;white;18]
```
