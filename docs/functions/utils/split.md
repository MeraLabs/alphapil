# split

Splits a string by a given separator and returns the results as a comma-separated list. This is highly useful for parsing complex custom inputs or formatting lists for other functions (like chart values).

## Syntax

```bash
$split[text;separator]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The text string to split. | Required |
| **separator**| `string` | The delimiter/separator to split by. | ` ` (space) |

## Example

```bash
# Split a hyphenated list into a comma-separated list of items
$setVar[items;$split[apple-banana-orange;-]] # Stores "apple,banana,orange"
```
