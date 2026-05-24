# autoSizeText

Calculates and returns the largest font size (as an integer) that allows the text to fit within a specified maximum width. It starts at a maximum size and decreases the font size step-by-step until the text fits or the minimum size limit is reached.

## Syntax

```bash
$autoSizeText[text;max_width;start_size;min_size;font]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The text string to fit. | Required |
| **max_width** | `int` | The maximum width available in pixels. | Required |
| **start_size**| `int` | The starting (maximum) font size to check. | `30` |
| **min_size** | `int` | The minimum font size to allow. | `10` |
| **font** | `string` | The font family name or alias. | Current default font |

## Example

```bash
# Calculate the optimal font size to fit inside 250px and render the text
$setVar[fitSize;$autoSizeText[Supercalifragilistic;250;40;12;bold]]
$drawText[20;100;Supercalifragilistic;white;{fitSize};bold]
```
