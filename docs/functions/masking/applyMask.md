# applyMask

Applies a grayscale image as an alpha mask to the current canvas or active layer. In a standard alpha mask, darker pixels in the mask image result in more transparent pixels on the target canvas, while white pixels remain opaque.

## Syntax

```bash
$applyMask[mask_path;x;y;invert]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **mask_path**| `string` | Local path to the grayscale mask image. | Required |
| **x** | `int/str` | X position to paste the mask. | `0` |
| **y** | `int/str` | Y position to paste the mask. | `0` |
| **invert** | `bool` | Set to `true` to invert the mask (white becomes transparent, black becomes opaque). | `false` |

## Example

```bash
# Apply a circular vignette/mask over the current canvas
$applyMask[assets/circle_mask.png;0;0;false]
```
