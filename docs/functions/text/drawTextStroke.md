# drawTextStroke

Draws text with a dedicated outline (stroke).

## Syntax

```bash
$drawTextStroke[text;x;y;size;color;stroke_width;stroke_color;font]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The text to draw. | Required |
| **x** | `int/str` | X position. | Required |
| **y** | `int/str` | Y position. | Required |
| **size** | `int` | Font size. | Required |
| **color** | `string` | Inner text color. | Required |
| **stroke_width** | `int` | Thickness of the outline. | Required |
| **stroke_color** | `string` | Color of the outline. | Required |
| **font** | `string` | Font path or alias. | `None` |

## Example

```bash
$drawTextStroke[OUTLINE;center;center;64;white;3;black]
```
