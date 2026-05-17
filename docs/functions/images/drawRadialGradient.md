# $drawRadialGradient

Draws a circular radial gradient.

## Syntax
`$drawRadialGradient[cx;cy;radius;colors]`

## Parameters
| Parameter | Description |
| :--- | :--- |
| `cx`, `cy` | Center coordinates |
| `radius` | Radius of the gradient |
| `colors` | Semicolon-separated color stops (e.g., `white,0;transparent,1`) |

## Example
```bash
$drawRadialGradient[center;middle;100;white,0;blue,1]
```
