# Geometric Shapes

Functions for drawing basic and complex geometric shapes.

| Function | Syntax |
| :--- | :--- |
| **drawRect** | `$drawRect[x;y;width;height;color;outline;fill;outline_width]` |
| **drawCircle** | `$drawCircle[cx;cy;radius;color;outline;fill;outline_width]` |
| **drawRoundedRect** | `$drawRoundedRect[x;y;width;height;radius;color;outline;fill;outline_width]` |
| **drawLine** | `$drawLine[x1;y1;x2;y2;color;width]` |
| **drawPolygon** | `$drawPolygon[points_list;color;outline;fill;outline_width]` |
| **drawTriangle** | `$drawTriangle[x1;y1;x2;y2;x3;y3;color;outline;fill;outline_width]` |
| **drawStar** | `$drawStar[x;y;points;outer_radius;inner_radius;color;outline;fill;outline_width]` |
| **drawArc** | `$drawArc[x;y;w;h;start_angle;end_angle;color;width]` |

## Examples

### Rectangles & Circles
```bash
# A red rectangle with white outline
$drawRect[50;50;200;100;red;white;none;2]

# A centered blue circle
$drawCircle[x=center;y=center;100;blue]
```

### Complex Shapes
```bash
# A golden 5-point star
$drawStar[x=center;y=center;5;50;20;gold;white;none;2]
```
