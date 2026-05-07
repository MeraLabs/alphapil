# drawStar

Draws a star shape.

## Syntax

```bash
$drawStar[x;y;points;outer_radius;inner_radius;color;outline;fill;outline_width]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position of the star center. | Required |
| **y** | `int/str` | Y position of the star center. | Required |
| **points** | `int` | Number of points on the star. | Required |
| **outer_radius** | `int` | Distance from center to outer points. | Required |
| **inner_radius** | `int` | Distance from center to inner points. | Required |
| **color** | `string` | Main color. | `black` |
| **outline** | `string` | Outline color. | `none` |
| **fill** | `string` | Fill style. | `solid` |
| **outline_width**| `int` | Stroke width. | `1` |

## Example

```bash
# A classic 5-pointed star
$drawStar[center;center;5;100;40;gold]
```
