# truncateText

Truncates a string of text with a custom suffix (typically `...`) if it exceeds a specified maximum width in pixels.

## Syntax

```bash
$truncateText[text;width;size;font;suffix]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The text string to truncate. | Required |
| **width** | `int` | The maximum width allowed in pixels. | Required |
| **size** | `int` | The font size to use for measurement. | `12` |
| **font** | `string` | The font family name or alias. | Current default font |
| **suffix** | `string` | The truncation marker to append at the end. | `...` |

## Example

```bash
# Truncate user bio if it exceeds 200px wide
$setVar[shortBio;$truncateText[{userBio};200;12;regular;...]]
$drawText[20;120;{shortBio};white;12;regular]
```
