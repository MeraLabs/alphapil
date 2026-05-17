# $startContainer

Starts a new container box. Keywords like `center`, `right`, and `bottom` inside this box will resolve relative to its boundaries instead of the whole canvas.

## Syntax
`$startContainer[x;y;width;height;padding;anchor]`

## Parameters
| Parameter | Description |
| :--- | :--- |
| `x` | X position of the container top-left corner (or adjusted by anchor) |
| `y` | Y position of the container top-left corner (or adjusted by anchor) |
| `width` | Width of the container |
| `height` | Height of the container |
| `padding` | Optional internal padding applied to elements inside |
| `anchor` | Anchor position for container placement (e.g. `lt`, `mm`, `rb`) |

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
