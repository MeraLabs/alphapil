# toLower

Converts a string to lowercase.

## Syntax

```bash
$toLower[text]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The text string to convert. | Required |

## Example

```bash
# Convert user input variable to lowercase for comparison or rendering
$setVar[cleanText;$toLower[{userInput}]]
```
