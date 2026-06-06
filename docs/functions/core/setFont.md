# setFont

Sets the default font, size, and optional variable font variation for all subsequent text drawing commands.

## Syntax

```bash
$setFont[font_name;size;variation]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **font_name** | `string` | Path to a `.ttf` or `.otf` file, a system font name, or a font alias. | Required |
| **size** | `int` | Default font size in pixels. | `12` |
| **variation** | `string` | Variable font axes (e.g. `wght=700` or `wght=400,wdth=100`) or predefined variation name (e.g. `Bold`). | `None` |

## Example

```bash
$loadFont[fonts/Inter-Variable.ttf;myFont]
# Set default font to Inter at size 32 with a custom bold weight axis
$setFont[myFont;32;wght=700]
$drawText[10;10;Default Style Text]
```
