# drawRect

Draws a rectangle on the canvas.

## Syntax

```bash
$drawRect[x;y;width;height;color;outline;fill;outline_width]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X coordinate (or `center`). | Required |
| **y** | `int/str` | Y coordinate (or `center`). | Required |
| **width** | `int` | Width of the rectangle. | Required |
| **height** | `int` | Height of the rectangle. | Required |
| **color** | `string` | Primary color. | Required |
| **outline** | `string` | Outline color. | `none` |
| **fill** | `string` | Fill style (`none` or color). | `solid` |
| **outline_width**| `int` | Thickness of the outline. | `1` |
| **radius** | `int` | Corner radius for rounded rectangles. | `0` |
| **anchor** | `string` | Positioning pivot point. | `lt` |

## Example

```bash
# Draw a simple blue rectangle
$drawRect[50;50;200;100;blue]

# Draw a rectangle with a white outline and no fill
$drawRect[100;100;300;200;blue;white;none;5]

# Draw a rounded rectangle with radius 10
$drawRect[100;100;300;200;blue;white;none;5;10]
```
