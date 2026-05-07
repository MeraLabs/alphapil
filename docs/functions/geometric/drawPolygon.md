# drawPolygon

Draws a polygon with a custom list of points.

## Syntax

```bash
$drawPolygon[points_list;color;outline;fill;outline_width]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **points_list** | `string` | Comma-separated points `x1,y1,x2,y2,x3,y3...`. | Required |
| **color** | `string` | Main color. | `black` |
| **outline** | `string` | Outline color. | `none` |
| **fill** | `string` | Fill style. | `solid` |
| **outline_width**| `int` | Stroke width. | `1` |

## Example

```bash
$drawPolygon[100,10;190,190;10,190;gold] # Draws a triangle
```
