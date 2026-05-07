# drawLine

Draws a straight line between two points.

## Syntax

```bash
$drawLine[x1;y1;x2;y2;color;width]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x1** | `int/str` | Start X coordinate. | Required |
| **y1** | `int/str` | Start Y coordinate. | Required |
| **x2** | `int/str` | End X coordinate. | Required |
| **y2** | `int/str` | End Y coordinate. | Required |
| **color** | `string` | Line color. | `black` |
| **width** | `int` | Line thickness. | `1` |

## Example

```bash
$drawLine[0;0;center;center;red;2]
```
