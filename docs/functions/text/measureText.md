# measureText

Measures the width and height of a text string based on a specific font size and family. Returns the size as a comma-separated string: `width,height`.

## Syntax

```bash
$measureText[text;size;font]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The text string to measure. | Required |
| **size** | `int` | Font size in pixels. | `12` |
| **font** | `string` | Font family/name or alias to measure with. | Current default font |

## Example

```bash
# Measure text and split into width and height
$setVar[dimensions;$measureText[AlphaPIL;24;bold]]
$setVar[w;$substring[{dimensions};0;comma]] # Note: Helper methods can extract values
```

!!! info
    This function is useful for dynamic layout calculations, such as setting container widths or placing background graphics behind text.
