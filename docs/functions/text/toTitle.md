# toTitle

Converts a string to title case (first letter of each word capitalized).

## Syntax

```bash
$toTitle[text]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The text string to convert. | Required |

## Example

```bash
# Convert a raw name or title to title case
$setVar[formattedName;$toTitle[yogeswar prasad]] # Stores "Yogeswar Prasad"
```
