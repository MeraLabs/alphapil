# replace

Replaces all occurrences of a target substring in a given text with a new substring.

## Syntax

```bash
$replace[text;old;new]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **text** | `string` | The original source text. | Required |
| **old** | `string` | The substring to find and replace. | Required |
| **new** | `string` | The new substring to insert in place of the old substring. | Required |

## Example

```bash
# Replace space with dashes
$setVar[slug;$replace[Hello World; ;-] # Stores "Hello-World"
```
