# $drawLineChart

Draws a line chart connecting data points.

## Syntax
`$drawLineChart[x;y;w;h;vals;labels;theme;color;lw;points;font;size;max_val]`

## Parameters
| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position of the chart. | Required |
| **y** | `int/str` | Y position of the chart. | Required |
| **w** | `int/str` | Width of the chart. | Required |
| **h** | `int/str` | Height of the chart. | Required |
| **vals** | `list/str` | Comma or semicolon-separated numeric values. | Required |
| **labels** | `list/str` | Comma or semicolon-separated label strings. | Required |
| **theme** | `string` | Color theme name. | `modern` |
| **color** | `string` | Override theme with a single line color. | `None` |
| **lw** | `int` | Line width for the graph in pixels. | `2` |
| **points** | `bool` | Whether to draw circular data points on the line nodes. | `true` |
| **font** | `string` | Custom font name for labels. | Default font |
| **size** | `int` | Font size for labels. | `20` |
| **max_val** | `float` | Custom maximum value limit for scaling the line. | `None` |

## Example
```bash
$drawLineChart[50;50;400;200;vals=10,20,15,25;labels=Jan,Feb,Mar,Apr;theme=modern;color=blue;lw=2;points=true]
```
