# drawPattern

Draws a geometric background pattern (dots, lines, grid) within a bounded rectangular region. This is ideal for adding premium texture overlays to cards, tech HUDs, or banners.

## Syntax

```bash
$drawPattern[x;y;width;height;pattern_type;color]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position of the bounding box. | Required |
| **y** | `int/str` | Y position of the bounding box. | Required |
| **width** | `int/str` | Width of the bounding box. | Required |
| **height** | `int/str` | Height of the bounding box. | Required |
| **pattern_type**| `string` | The pattern style to draw: `dots`, `lines`, `grid`. | `dots` |
| **color** | `string` | Color of the pattern elements. | `black` |

## Example

```bash
# Draw a subtle gray grid pattern in a background card
$drawRect[50;50;300;400;#1a1a2e;radius=15]
$drawPattern[50;50;300;400;grid;white/5]
```
