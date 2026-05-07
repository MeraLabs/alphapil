# if

Basic conditional logic.

## Syntax

```bash
$if[condition;true_val;false_val]
```

## Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **condition** | `string` | Expression to check (e.g., `{val} == 1`). |
| **true_val** | `string` | Result if condition is true. |
| **false_val** | `string` | Result if condition is false. |

## Example

```bash
$setVar[points;10]
$drawText[10;10;$if[{points} > 5;Winner;Loser]]
```
