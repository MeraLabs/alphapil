# drawArc

Draws an arc (part of an ellipse).

## Syntax

```bash
$drawArc[x;y;w;h;start_angle;end_angle;color;width]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | Top-left X of the bounding box. | Required |
| **y** | `int/str` | Top-left Y of the bounding box. | Required |
| **w** | `int` | Width of the bounding box. | Required |
| **h** | `int` | Height of the bounding box. | Required |
| **start_angle** | `int` | Starting angle in degrees. | Required |
| **end_angle** | `int` | Ending angle in degrees. | Required |
| **color** | `string` | Arc color. | `black` |
| **width** | `int` | Arc thickness. | `1` |

## Example

```bash
# Draw a semi-circle
$drawArc[100;100;200;200;0;180;red;5]
```
