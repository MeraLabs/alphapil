# substring

Extracts a portion of a string between a starting index and an optional ending index. Supports negative indices to slice from the end of the string.

## Syntax

```bash
$substring[text;start;end]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The original source text. | Required |
| **start** | `int` | The zero-based index to begin extraction. Supports negative values. | Required |
| **end** | `int` | The zero-based index before which to end extraction. Supports negative values. | `None` (Slices to end) |

## Example

```bash
# Get the first 3 characters of a string
$setVar[prefix;$substring[AlphaPIL;0;3]] # Stores "Alp"

# Get the last 3 characters of a string using a negative start index
$setVar[suffix;$substring[AlphaPIL;-3]] # Stores "PIL"
```
