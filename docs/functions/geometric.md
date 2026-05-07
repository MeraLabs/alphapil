# Geometric Shapes

Functions for drawing basic and complex geometric shapes.

| Function | Syntax |
| :--- | :--- |
| **drawRect** | `$drawRect[x;y;width;height;radius;color;outline;fill;...]` |
| **drawCircle** | `$drawCircle[cx;cy;radius;color;outline;fill;outline_width]` |
| **drawLine** | `$drawLine[x1;y1;x2;y2;color;width]` |
| **drawPolygon** | `$drawPolygon[points_list;color;outline;fill;outline_width]` |
| **drawTriangle** | `$drawTriangle[x1;y1;x2;y2;x3;y3;color;outline;fill;outline_width]` |
| **drawStar** | `$drawStar[x;y;points;outer_radius;inner_radius;color;outline;fill;outline_width]` |
| **drawArc** | `$drawArc[x;y;w;h;start_angle;end_angle;color;width]` |

## Examples

### Rectangles (including Rounded)
The `$drawRect` function now supports an optional `radius` parameter to create rounded rectangles.

```bash
# A red rectangle with white outline
$drawRect[50;50;200;100;color=red;outline=white;outline_width=2]

# A rounded rectangle with 20px radius
$drawRect[x=50;y=200;width=200;height=100;radius=20;color=blue]
```

### Complex Shapes
```bash
# A golden 5-point star
$drawStar[x=center;y=center;5;50;20;gold;white;none;2]
```
