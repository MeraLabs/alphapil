# $drawBarChart

Draws a professional bar chart with theme support.

## Syntax
`$drawBarChart[x;y;w;h;vals;labels;theme;color;gap;show_lab;font;size;radius;max_val]`

## Parameters
| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position of the chart. | Required |
| **y** | `int/str` | Y position of the chart. | Required |
| **w** | `int/str` | Width of the chart. | Required |
| **h** | `int/str` | Height of the chart. | Required |
| **vals** | `list/str` | Comma or semicolon-separated values (e.g. `10,50,30,80`). | Required |
| **labels** | `list/str` | Comma or semicolon-separated label strings for each bar. | Required |
| **theme** | `string` | Color theme name (e.g. `modern`, `minimal`, `ocean`). | `modern` |
| **color** | `string` | Override theme with a single fill color. | `None` |
| **gap** | `int` | Gap between bars in pixels. | `10` |
| **show_lab** | `bool` | Whether to display X-axis labels. | `true` |
| **font** | `string` | Custom font name for labels. | Default font |
| **size** | `int` | Font size for labels. | `20` |
| **radius** | `int` | Corner radius for the bars. | `0` |
| **max_val** | `float` | Custom maximum value limit for scaling the bars. | `None` |

## Example
```bash
$drawBarChart[50;50;400;200;vals=10,50,30,80;labels=Mon,Tue,Wed,Thu;theme=ocean]
```
