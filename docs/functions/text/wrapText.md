# wrapText

Wraps a text string so that no line exceeds a maximum width in pixels. It returns the wrapped text with newline characters (`\n`).

## Syntax

```bash
$wrapText[text;max_width;size;font;is_scaled]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The input text to wrap. | Required |
| **max_width** | `int` | The maximum allowable line width in pixels. | Required |
| **size** | `int` | The font size to use for calculation. | `12` |
| **font** | `string` | The font name/alias to use for calculation. | Current default font |
| **is_scaled** | `bool` | Whether the maximum width should be scaled based on the canvas scale factor. | `false` |

## Example

```bash
# Wrap a long paragraph to 300px width and render it
$setVar[wrapped;$wrapText[AlphaPIL is an asynchronous, template-based image generation engine;300;14;regular]]
$drawText[20;50;{wrapped};white;14;regular]
```
