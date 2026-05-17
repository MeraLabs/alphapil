# $drawBarChart

Draws a professional bar chart with theme support.

## Syntax
`$drawBarChart[x;y;w;h;vals;labels;theme;color;gap;show_lab;font;size;radius;max_val]`

## Parameters
| Parameter | Description |
| :--- | :--- |
| `x`, `y` | Position of the chart |
| `w`, `h` | Dimensions of the chart |
| `vals` | Comma or semicolon-separated numbers (e.g., `10,20,30`) |
| `labels` | Comma or semicolon-separated strings for X-axis |
| `theme` | Built-in theme name (e.g., `modern`, `minimal`) |
| `color` | Override theme with a single color |
| `gap` | Gap between bars in pixels (default: 10) |
| `show_lab` | Show X-axis labels (`true`/`false`) |
| `font` | Custom font name for labels |
| `size` | Font size for labels (default: 20) |
| `radius` | Corner radius for the bars (default: 0) |
| `max_val` | Manual maximum value for normalization (optional) |

## Example
```bash
$drawBarChart[50;50;400;200;vals=10,50,30,80;labels=Mon,Tue,Wed,Thu;theme=ocean]
```
