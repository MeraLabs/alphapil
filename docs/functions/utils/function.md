# $function

Defines a custom macro function (User-Defined Function) that can be reused throughout your template.

## Syntax
`$function[name;arguments;body]`

## Parameters
| Parameter | Description |
| :--- | :--- |
| `name` | The name of your custom function (call it using `$name[...]`) |
| `arguments` | Comma-separated list of parameter names (e.g., `x,y,text`) |
| `body` | The AlphaPIL commands to execute. Use `{arg_name}` to reference parameters. |

## Example
```bash
# Define a custom "StatBox" function
$function[StatBox;x,y,label,value;
    $drawRoundedRect[{x};{y};150;80;10;#2C2F33]
    $drawText[{x}+75;{y}+25;{label};gray;12;middle]
    $drawText[{x}+75;{y}+55;{value};white;18;middle]
]

# Use the custom function
$StatBox[50;50;Followers;1.2k]
$StatBox[220;50;Likes;50k]
```

> [!TIP]
> Custom functions are great for UI components like buttons, badges, or recurring stat cards.
