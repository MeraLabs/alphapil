# join

Concatenates multiple items together into a single string using a specified separator string.

## Syntax

```bash
$join[separator;item1;item2;...]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **separator**| `string` | The string to insert between items. | Required |
| **item1 / 2...**| `string` | Any number of strings to join together. | Required |

## Example

```bash
# Join values with spaces to make a full name
$setVar[fullName;$join[ ;Yogeswar;Prasad]] # Stores "Yogeswar Prasad"
```
