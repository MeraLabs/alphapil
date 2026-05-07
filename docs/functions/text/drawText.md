# drawText

Draws text onto the canvas with specified styling.

## Syntax

```bash
$drawText[x;y;text;color;size;font_alias]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X coordinate (or `center`). | Required |
| **y** | `int/str` | Y coordinate (or `center`). | Required |
| **text** | `string` | The text to display. | Required |
| **color** | `string` | Text color. | `white` |
| **size** | `int` | Font size in pixels. | `24` |
| **font_alias**| `string` | Alias of a font loaded via `$loadFont`. | `default` |

## Example

```bash
$loadFont[fonts/Roboto-Bold.ttf;bold]
$drawText[center;center;Hello World!;white;48;bold]
```
