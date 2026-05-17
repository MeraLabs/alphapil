# $drawLineChart

Draws a line chart connecting data points.

## Syntax
`$drawLineChart[x;y;w;h;vals;labels;theme;color;lw;points;font;size;max_val]`

## Parameters
| Parameter | Description |
| :--- | :--- |
| `x`, `y` | Position of the chart |
| `w`, `h` | Dimensions of the chart |
| `vals` | Comma or semicolon-separated numbers (e.g., `10,20,30`) |
| `labels` | Comma or semicolon-separated strings for X-axis |
| `theme` | Built-in theme name |
| `color` | Override theme with a single color |
| `lw` | Line width for the graph (default: 2) |
| `points` | Show data points (`true`/`false`) |
| `font` | Custom font name for labels |
| `size` | Font size for labels (default: 20) |
| `max_val` | Manual maximum value for normalization (optional) |

## Example
```bash
$drawLineChart[50;50;400;200;vals=10,20,15,25;labels=Jan,Feb,Mar,Apr;theme=modern;color=blue;lw=2;points=true]
```
