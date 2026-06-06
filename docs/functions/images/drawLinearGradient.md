# $drawLinearGradient

Draws a rectangle filled with a linear gradient. Supports multiple color stops and rotation.

## Syntax
`$drawLinearGradient[x;y;w;h;colors;angle]`

## Parameters
| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position of the top-left corner. | Required |
| **y** | `int/str` | Y position of the top-left corner. | Required |
| **w** | `int/str` | Width of the gradient bounding box. | Required |
| **h** | `int/str` | Height of the gradient bounding box. | Required |
| **colors** | `string` | Semicolon-separated color stops (e.g., `red,0;blue,0.5;green,1`). | Required |
| **angle** | `int` | Rotation angle of the gradient in degrees. | `90` (vertical) |

## Example
```bash
$drawLinearGradient[10;10;200;100;red,0;blue,1;45]
```
