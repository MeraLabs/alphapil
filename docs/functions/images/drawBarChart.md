# $drawBarChart

Draws a professional bar chart with theme support.

## Syntax
`$drawBarChart[x;y;w;h;values;labels;theme;color;gap;show_labels;font;font_size]`

## Parameters
| Parameter | Description |
| :--- | :--- |
| `x`, `y` | Position of the chart |
| `w`, `h` | Dimensions of the chart |
| `values` | Semicolon-separated numbers (e.g., `10;20;30`) |
| `labels` | Semicolon-separated strings for X-axis |
| `theme` | Built-in theme name (e.g., `modern`, `ocean`, `vibrant`) |
| `color` | Override theme with a single color |
| `gap` | Gap between bars (default: 10) |

## Example
```bash
$drawBarChart[50;50;400;200;10;50;30;80;Mon;Tue;Wed;Thu;ocean]
```
