# setVar

Sets a template-local variable that can be used later in the script with `{variable_name}` syntax.

## Syntax

```bash
$setVar[name;value]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **name** | `string` | The name of the variable (without `{}`). | Required |
| **value** | `string` | The value to assign to the variable. | Required |

## Example

```bash
$setVar[bgColor;#121212]
$createCanvas[500;500;{bgColor}]
```
