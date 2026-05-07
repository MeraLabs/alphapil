# imageFilter

Applies a visual filter to the entire current canvas.

## Syntax

```bash
$imageFilter[filter_name]
```

## Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **filter_name** | `string` | Name of the filter. |

### Available Filters:
`blur`, `contour`, `detail`, `edge_enhance`, `emboss`, `find_edges`, `sharpen`, `smooth`.

## Example

```bash
$drawImage[0;0;photo.jpg]
$imageFilter[blur]
```
