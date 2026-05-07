# drawRoundedRect

Draws a rectangle with rounded corners.

## Syntax

```bash
$drawRoundedRect[x;y;width;height;radius;color;outline;fill;outline_width]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position. | Required |
| **y** | `int/str` | Y position. | Required |
| **width** | `int` | Width of the rectangle. | Required |
| **height** | `int` | Height of the rectangle. | Required |
| **radius** | `int` | Corner radius. | `10` |
| **color** | `string` | Main color. | `black` |
| **outline** | `string` | Outline color. | `none` |
| **fill** | `string` | Fill style. | `solid` |
| **outline_width**| `int` | Stroke width. | `1` |

## Example

```bash
$drawRoundedRect[50;50;200;100;20;blue]
```
