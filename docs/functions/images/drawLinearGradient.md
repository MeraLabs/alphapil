# $drawLinearGradient

Draws a rectangle filled with a linear gradient. Supports multiple color stops and rotation.

## Syntax
`$drawLinearGradient[x;y;w;h;colors;angle]`

## Parameters
| Parameter | Description |
| :--- | :--- |
| `x`, `y` | Position of the top-left corner |
| `w`, `h` | Dimensions of the gradient box |
| `colors` | Semicolon-separated color stops (e.g., `red,0;blue,0.5;green,1`) |
| `angle` | Rotation angle in degrees (default: 90 for vertical) |

## Example
```bash
$drawLinearGradient[10;10;200;100;red,0;blue,1;45]
```
