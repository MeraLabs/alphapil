# drawImage

Draws an image onto the canvas. Supports URLs, local files, and advanced styling.

## Syntax

```bash
$drawImage[x;y;image_path;width;height;opacity;radius;circle]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position. | Required |
| **y** | `int/str` | Y position. | Required |
| **image_path** | `string` | URL or local path to the image. | Required |
| **width** | `int` | Resize to width (maintains aspect if height omitted).| `None` |
| **height** | `int` | Resize to height. | `None` |
| **opacity** | `int` | Opacity percentage (0-100). | `100` |
| **radius** | `int` | Rounded corner radius. | `None` |
| **circle** | `bool` | Crop to a circle (`true`/`false`). | `false` |
| **anchor** | `string` | Positioning pivot point (e.g. `mm`, `lt`). | `lt` (`mm` if circle=true) |

## Example

```bash
# Draw a user's avatar as a circle centered at 200,200
$drawImage[200;200;https://example.com/avatar.png;100;100;circle=true]
```
