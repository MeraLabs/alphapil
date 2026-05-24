# adjustColor

Adjusts the brightness, contrast, and color saturation of the current active layer or canvas using professional enhancement filters.

## Syntax

```bash
$adjustColor[brightness;contrast;saturation]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **brightness**| `float` | Brightness multiplier. `1.0` is original, `< 1.0` darkens, `> 1.0` brightens. | `1.0` |
| **contrast** | `float` | Contrast multiplier. `1.0` is original, `< 1.0` softens contrast, `> 1.0` sharpens contrast. | `1.0` |
| **saturation**| `float` | Saturation/color multiplier. `1.0` is original, `0.0` is black & white, `> 1.0` intensifies colors. | `1.0` |

## Example

```bash
# Saturated, high-contrast, slightly brightened effect (perfect for vibrant banners)
$adjustColor[brightness=1.1;contrast=1.2;saturation=1.5]

# Convert an image layer to black and white
$createLayer[photo]
$switchLayer[photo]
$drawImage[0;0;assets/user.jpg]
$adjustColor[saturation=0.0]
$switchLayer[main]
$mergeLayer[photo]
```
