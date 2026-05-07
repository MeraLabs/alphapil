# drawTextMid

A powerful centering function that can center text within a box or between two points.

## Syntax

```bash
$drawTextMid[x1;y1;x2;y2;text;color;size;font;...]
```

## Parameters (Partial List - Supports all Text Effects)

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x1, x2** | `int/str` | Centers horizontally between these two points. | Optional |
| **y1, y2** | `int/str` | Centers vertically between these two points. | Optional |
| **x, y, w, h** | `int` | Centers within a box starting at (x,y) with width w and height h. | Optional |
| **text** | `string` | The text to draw. | Required |

## Example

```bash
# Center text in a 200x50 button box
$drawRect[10;10;200;50;blue]
$drawTextMid[x=10;y=10;w=200;h=50;text=Click Me;color=white;size=16]
```
