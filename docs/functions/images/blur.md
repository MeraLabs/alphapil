# $blur

Applies a Gaussian blur to a specific region or the entire canvas. Perfect for Glassmorphism effects.

## Syntax
`$blur[radius;x;y;w;h]`

## Parameters
| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **radius** | `int` | Blur intensity / radius. | Required |
| **x** | `int/str` | X coordinate of the region to blur. | `None` (full width if omitted) |
| **y** | `int/str` | Y coordinate of the region to blur. | `None` (full height if omitted) |
| **w** | `int/str` | Width of the region to blur. | `None` |
| **h** | `int/str` | Height of the region to blur. | `None` |

## Example
```bash
# Blur a specific region for a glass effect
$blur[10;50;50;200;100]
```
