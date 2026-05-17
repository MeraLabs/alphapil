# $startContainer

Starts a new container box. Keywords like `center`, `right`, and `bottom` inside this box will resolve relative to its boundaries instead of the whole canvas.

## Syntax
`$startContainer[x;y;width;height]`

## Parameters
| Parameter | Description |
| :--- | :--- |
| `x` | X position of the container top-left corner |
| `y` | Y position of the container top-left corner |
| `width` | Width of the container |
| `height` | Height of the container |

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
