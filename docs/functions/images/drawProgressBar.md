# $drawProgressBar

Draws a modern rounded progress bar.

## Syntax
`$drawProgressBar[x;y;w;h;value;max_value;theme;color;bg_color;radius]`

## Parameters
| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position of the progress bar. | Required |
| **y** | `int/str` | Y position of the progress bar. | Required |
| **w** | `int/str` | Width of the progress bar. | Required |
| **h** | `int/str` | Height of the progress bar. | Required |
| **value** | `float` | Current value of the progress bar. | Required |
| **max_value** | `float` | Maximum possible value for normalization. | Required |
| **theme** | `string` | Color theme name (e.g. `modern`, `minimal`). | `modern` |
| **color** | `string` | Custom color for the active progress fill. | `None` |
| **bg_color** | `string` | Custom background/track color. | `None` |
| **radius** | `int` | Corner radius for the progress bar. | `0` |

## Example
```bash
$drawProgressBar[50;50;300;20;75;100;modern;#5865F2;gray;10]
```
