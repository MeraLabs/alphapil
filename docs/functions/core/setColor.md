# setColor

Sets the default primary color for drawing operations.

## Syntax

```bash
$setColor[color]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **color** | `string` | Hex, RGB(A), or Name (e.g., `#FF0000`, `red`). | Required |

## Example

```bash
$setColor[blue]
$drawRect[0;0;100;100] # Draws a blue rectangle
```
