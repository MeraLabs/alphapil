# setFont

Sets the default font and size for all subsequent text drawing commands.

## Syntax

```bash
$setFont[font_path;size]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **font_path** | `string` | Path to a `.ttf` or `.otf` file, or a font alias. | Required |
| **size** | `int` | Default font size in pixels. | `12` |

## Example

```bash
$loadFont[fonts/Inter.ttf;myFont]
$setFont[myFont;32]
$drawText[10;10;Default Style Text]
```
