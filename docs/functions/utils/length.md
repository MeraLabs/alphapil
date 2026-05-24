# length

Returns the number of characters in a string.

## Syntax

```bash
$length[text]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The text to measure. | Required |

## Example

```bash
# Get the length of a username and dynamically adjust font size or container
$setVar[userLength;$length[{username}]]
```
