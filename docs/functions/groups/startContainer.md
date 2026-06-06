# $startContainer

Starts a new container box. Keywords like `center`, `right`, and `bottom` inside this box will resolve relative to its boundaries instead of the whole canvas.

## Syntax
`$startContainer[x;y;w;h;padding;anchor]`

## Parameters
| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position of the container top-left corner (or relative to parent anchor). | Required |
| **y** | `int/str` | Y position of the container top-left corner (or relative to parent anchor). | Required |
| **w** | `int/str` | Width of the container. | Required |
| **h** | `int/str` | Height of the container. | Required |
| **padding** | `int` | Optional internal padding applied to elements inside. | `0` |
| **anchor** | `string` | Anchor placement point for the container itself (e.g. `lt`, `mm`, `rb`). | `lt` |

## Example
```bash
$createCanvas[800;600;white]
$startContainer[100;100;600;400]
  # This rectangle will fill the container
  $drawRect[0;0;100%;100%;#f0f0f0]
  # This text will be centered within the 600x400 container
  $drawText[center;middle;Centered in Box;black;24]
$endContainer[]
```

> [!NOTE]
> Containers can be nested. Keywords will always refer to the innermost active container.
