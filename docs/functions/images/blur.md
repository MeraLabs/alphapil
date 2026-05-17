# $blur

Applies a Gaussian blur to a specific region or the entire canvas. Perfect for Glassmorphism effects.

## Syntax
`$blur[radius;x;y;w;h]`

## Parameters
| Parameter | Description |
| :--- | :--- |
| `radius` | Blur intensity |
| `x`, `y` | (Optional) Top-left corner of the region to blur |
| `w`, `h` | (Optional) Dimensions of the region to blur |

## Example
```bash
# Blur a specific region for a glass effect
$blur[10;50;50;200;100]
```
