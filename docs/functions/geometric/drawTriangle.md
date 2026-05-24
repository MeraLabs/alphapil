# drawTriangle

Draws a triangle defined by three sets of coordinates on the canvas.

## Syntax

```bash
$drawTriangle[x1;y1;x2;y2;x3;y3;color;outline;fill;outline_width]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x1** | `int/str` | X coordinate of the first vertex. | Required |
| **y1** | `int/str` | Y coordinate of the first vertex. | Required |
| **x2** | `int/str` | X coordinate of the second vertex. | Required |
| **y2** | `int/str` | Y coordinate of the second vertex. | Required |
| **x3** | `int/str` | X coordinate of the third vertex. | Required |
| **y3** | `int/str` | Y coordinate of the third vertex. | Required |
| **color** | `string` | Primary fill color (if `fill` is not specified). | Current state color |
| **outline**| `string` | Outline stroke color. | `none` |
| **fill** | `string` | Fill color style (e.g. `none` or a color name/hex). | `solid` |
| **outline_width**| `int` | Stroke width/thickness of the outline. | Current state stroke width |

## Example

```bash
# Draw a simple white triangle with vertexes at (100,50), (50,150), (150,150)
$drawTriangle[100;50;50;150;150;150;white]

# Draw a triangle with a white outline, red fill, and outline width of 4
$drawTriangle[200;10;150;100;250;100;fill=red;outline=white;outline_width=4]
```
