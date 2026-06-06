# $getVar

Retrieves the value of a variable previously set with `$setVar`.

## Syntax
`$getVar[name;default]`

## Parameters
| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **name** | `string` | The name of the variable to retrieve. | Required |
| **default** | `string` | Optional fallback value to return if the variable is not defined. | `""` |

## Example
```bash
$setVar[primaryColor;blue]
$drawRect[10;10;100;100;$getVar[primaryColor]]
```

> [!TIP]
> You can also use the shorthand `{name}` or `{name|default}` to retrieve variables. `$getVar` is useful when using variables inside complex math expressions or when you prefer function-style syntax.
