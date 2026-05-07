# math

Evaluates a mathematical expression and returns the result.

## Syntax

```bash
$math[expression]
```

## Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **expression** | `string` | A valid math expression (e.g., `10 + 20 * 2`). |

## Example

```bash
$setVar[total;$math[50 * 2]]
$drawText[10;10;Result: {total}]
```

### Nesting
Because `$math` returns a number string, it can be used inside other functions:
```bash
$drawRect[10;10;$math[100 + 50];50;red]
```
