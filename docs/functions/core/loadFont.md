# loadFont

Registers a font file with an alias for easier reference in text functions.

## Syntax

```bash
$loadFont[path;alias]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **path** | `string` | Path to the font file (local path). | Required |
| **alias** | `string` | A shorthand name to use instead of the full path. | Required |

## Example

```bash
$loadFont[./assets/fonts/Bold.ttf;bold]
$drawText[50;50;Bold Text;white;24;bold]
```
