# drawTextGradient

Draws text with a vertical linear gradient.

## Syntax

```bash
$drawTextGradient[text;x;y;size;color1;color2;font]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The text to draw. | Required |
| **x** | `int/str` | X position. | Required |
| **y** | `int/str` | Y position. | Required |
| **size** | `int` | Font size. | Required |
| **color1** | `string` | Top color of the gradient. | Required |
| **color2** | `string` | Bottom color of the gradient. | Required |
| **font** | `string` | Font path or alias. | `None` |

## Example

```bash
$drawTextGradient[SUNSET;center;center;80;orange;purple]
```
