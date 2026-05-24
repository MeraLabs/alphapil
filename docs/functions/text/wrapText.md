# wrapText

Wraps a text string so that no line exceeds a maximum width in pixels. It returns the wrapped text with newline characters (`\n`).

## Syntax

```bash
$wrapText[text;width;size;font]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The input text to wrap. | Required |
| **width** | `int` | The maximum allowable line width in pixels. | Required |
| **size** | `int` | The font size to use for calculation. | `12` |
| **font** | `string` | The font name/alias to use for calculation. | Current default font |

## Example

```bash
# Wrap a long paragraph to 300px width and render it
$setVar[wrapped;$wrapText[AlphaPIL is an asynchronous, template-based image generation engine;300;14;regular]]
$drawText[20;50;{wrapped};white;14;regular]
```
