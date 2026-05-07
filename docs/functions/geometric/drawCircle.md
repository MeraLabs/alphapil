# drawCircle

Draws a circle on the canvas.

## Syntax

```bash
$drawCircle[cx;cy;radius;color;outline;fill;outline_width]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **cx** | `int/str` | X coordinate of the center. | Required |
| **cy** | `int/str` | Y coordinate of the center. | Required |
| **radius** | `int` | Radius of the circle. | Required |
| **color** | `string` | Primary color. | `black` |
| **outline** | `string` | Outline color. | `none` |
| **fill** | `string` | Fill color/style. | `solid` |
| **outline_width**| `int` | Stroke width. | `1` |
| **anchor** | `string` | Positioning pivot point. | `mm` |

## Example

```bash
# Red circle in the center
$drawCircle[center;center;50;red]
```
