# $drawRadialGradient

Draws a circular radial gradient.

## Syntax
`$drawRadialGradient[cx;cy;radius;colors]`

## Parameters
| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **cx** | `int/str` | X position of the gradient center. | Required |
| **cy** | `int/str` | Y position of the gradient center. | Required |
| **radius** | `int` | Radius of the gradient circular bounds. | Required |
| **colors** | `string` | Semicolon-separated color stops (e.g., `white,0;transparent,1`). | Required |

## Example
```bash
$drawRadialGradient[center;middle;100;white,0;blue,1]
```
