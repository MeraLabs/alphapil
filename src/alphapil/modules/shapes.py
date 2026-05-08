"""
Shapes module - Drawing primitives for AlphaPIL.

This module provides functions for drawing basic shapes like rectangles,
circles, rounded rectangles, lines, polygons, stars, triangles, and arcs
on the canvas.
"""

from typing import Union, List, Tuple
from PIL import ImageDraw
import math


class ShapesMixin:
    """
    Mixin class providing shape drawing functionality.
    
    This mixin adds methods for drawing various geometric shapes
    on the canvas using Pillow's ImageDraw module.
    """

    # -------------------------
    # Existing Methods
    # -------------------------

    def _draw_rect(self, x: str, y: str, width: str, height: str, 
                   color: str = None, outline: str = None, fill: str = None, 
                   outline_width: str = None, radius: str = "0", anchor: str = "lt") -> str:
        try:
            self._ensure_canvas()
            w = self._parse_num(width)
            h = self._parse_num(height)
            r = self._parse_num(radius)
            
            # Apply defaults from state
            color = color or self._get_state('color', 'black')
            lw = int(self._parse_num(outline_width)) if outline_width else int(self._get_state('stroke_width', 0))
            
            # Apply anchor offset
            ax, ay = self._get_anchor_offset(anchor, w, h)
            x1 = self._parse_position(x, 'x') + ax
            y1 = self._parse_position(y, 'y') + ay
            
            x2 = x1 + w
            y2 = y1 + h
            bbox = [(x1, y1), (x2, y2)]

            fill_color = self._get_color(fill) if fill else self._get_color(color)
            
            # Outline logic
            outline_color = None
            if outline:
                outline_color = self._get_color(outline)
            elif lw > 0:
                outline_color = self._get_color(self._get_state('stroke_color', 'black'))

            if r > 0 and hasattr(self.draw, 'rounded_rectangle'):
                if outline_color:
                    self.draw.rounded_rectangle(bbox, radius=r, fill=fill_color, outline=outline_color, width=lw)
                else:
                    self.draw.rounded_rectangle(bbox, radius=r, fill=fill_color)
            else:
                if outline_color:
                    self.draw.rectangle(bbox, fill=fill_color, outline=outline_color, width=lw)
                else:
                    self.draw.rectangle(bbox, fill=fill_color)

            return f"Rectangle drawn at ({x1}, {y1}) size {w}x{h}" + (f" with radius {r}" if r > 0 else "")
        except ValueError as e:
            raise ValueError(f"{e}\nProper Syntax: $drawRect[x;y;width;height;color;outline;fill;outline_width;radius;anchor]")

    def _draw_rounded_rect(self, x: str, y: str, width: str, height: str, radius: str = "10",
                           color: str = None, outline: str = None, fill: str = None,
                           outline_width: str = None, anchor: str = "lt") -> str:
        """
        Draw a rounded rectangle with specific parameter order from docs.
        """
        try:
            return self._draw_rect(x=x, y=y, width=width, height=height, radius=radius,
                                  color=color, outline=outline, fill=fill,
                                  outline_width=outline_width, anchor=anchor)
        except ValueError as e:
            # Re-raise with specific syntax for rounded rect if it fails
            raise ValueError(f"{str(e).split('\n')[0]}\nProper Syntax: $drawRoundedRect[x;y;width;height;radius;color;outline;fill;outline_width;anchor]")

    def _draw_circle(self, cx: str, cy: str, radius: str, 
                     color: str = None, outline: str = None, fill: str = None,
                     outline_width: str = None, anchor: str = "mm") -> str:
        try:
            self._ensure_canvas()
            r = self._parse_num(radius)
            w = h = r * 2
            
            # Apply defaults from state
            color = color or self._get_state('color', 'black')
            lw = int(self._parse_num(outline_width)) if outline_width else int(self._get_state('stroke_width', 0))

            # Universal Anchor Logic: Anchor offset is calculated relative to center for 'mm'
            # or shifted for others.
            ax, ay = self._get_anchor_offset(anchor, w, h)
            
            # cx/cy are the raw center provided. If anchor=mm, ax/ay = -r, -r
            # so left = cx - r, top = cy - r. 
            # Note: _get_anchor_offset for 'mm' returns -w/2, -h/2
            x_pos = self._parse_position(cx, 'x') + ax
            y_pos = self._parse_position(cy, 'y') + ay

            left = x_pos
            top = y_pos
            right = x_pos + w
            bottom = y_pos + h
            bbox = [(left, top), (right, bottom)]

            fill_color = self._get_color(fill) if fill else self._get_color(color)
            
            # Outline logic
            outline_color = None
            if outline:
                outline_color = self._get_color(outline)
            elif lw > 0:
                outline_color = self._get_color(self._get_state('stroke_color', 'black'))

            if outline_color:
                self.draw.ellipse(bbox, fill=fill_color, outline=outline_color, width=lw)
            else:
                self.draw.ellipse(bbox, fill=fill_color)

            return f"Circle drawn at ({x_pos+r}, {y_pos+r}) with radius {r}"
        except ValueError as e:
            raise ValueError(f"{e}\nProper Syntax: $drawCircle[cx;cy;radius;color;outline;fill;outline_width;anchor]")

    def _draw_line(self, x1: str, y1: str, x2: str, y2: str, 
                   color: str = None, width: str = None) -> str:
        try:
            self._ensure_canvas()
            start_x = self._parse_position(x1, 'x')
            start_y = self._parse_position(y1, 'y')
            end_x = self._parse_position(x2, 'x')
            end_y = self._parse_position(y2, 'y')
            
            # Apply defaults from state
            color = color or self._get_state('color', 'black')
            line_width = int(self._parse_num(width)) if width else int(self._get_state('stroke_width', 1))

            line_color = self._get_color(color)

            self.draw.line([(start_x, start_y), (end_x, end_y)],
                           fill=line_color, width=line_width)

            return f"Line drawn from ({start_x}, {start_y}) to ({end_x}, {end_y})"
        except ValueError as e:
            raise ValueError(f"{e}\nProper Syntax: $drawLine[x1;y1;x2;y2;color;width]")

    # -------------------------
    # NEW METHODS ADDED
    # -------------------------

    def _draw_polygon(self, points_list: str, color: str = None,
                       outline: str = None, fill: str = None,
                       outline_width: str = None) -> str:
        try:
            self._ensure_canvas()
            # Apply defaults from state
            color = color or self._get_state('color', 'black')
            lw = int(self._parse_num(outline_width)) if outline_width else int(self._get_state('stroke_width', 0))

            raw_points = [p.strip() for p in points_list.split(",")]
            if len(raw_points) < 6 or len(raw_points) % 2 != 0:
                raise ValueError("Polygon requires even number of coordinates (x1,y1,x2,y2...)")

            points = []
            for i in range(0, len(raw_points), 2):
                x = self._parse_position(raw_points[i], 'x')
                y = self._parse_position(raw_points[i + 1], 'y')
                points.append((x, y))

            fill_color = self._get_color(fill) if fill else self._get_color(color)
            
            # Outline logic
            outline_color = None
            if outline:
                outline_color = self._get_color(outline)
            elif lw > 0:
                outline_color = self._get_color(self._get_state('stroke_color', 'black'))

            if outline_color:
                self.draw.polygon(points, fill=fill_color, outline=outline_color, width=lw)
            else:
                self.draw.polygon(points, fill=fill_color)

            return f"Polygon drawn with {len(points)} points"
        except ValueError as e:
            raise ValueError(f"{e}\nProper Syntax: $drawPolygon[points_list;color;outline;fill;outline_width]")

    def _draw_triangle(self, x1: str, y1: str,
                       x2: str, y2: str,
                       x3: str, y3: str,
                       color: str = None, outline: str = None, fill: str = None,
                       outline_width: str = None) -> str:
        try:
            self._ensure_canvas()
            # Apply defaults from state
            color = color or self._get_state('color', 'black')
            lw = int(self._parse_num(outline_width)) if outline_width else int(self._get_state('stroke_width', 0))

            p1 = (self._parse_position(x1, 'x'), self._parse_position(y1, 'y'))
            p2 = (self._parse_position(x2, 'x'), self._parse_position(y2, 'y'))
            p3 = (self._parse_position(x3, 'x'), self._parse_position(y3, 'y'))

            fill_color = self._get_color(fill) if fill else self._get_color(color)
            
            # Outline logic
            outline_color = None
            if outline:
                outline_color = self._get_color(outline)
            elif lw > 0:
                outline_color = self._get_color(self._get_state('stroke_color', 'black'))

            if outline_color:
                self.draw.polygon([p1, p2, p3], fill=fill_color, outline=outline_color, width=lw)
            else:
                self.draw.polygon([p1, p2, p3], fill=fill_color)

            return "Triangle drawn"
        except ValueError as e:
            raise ValueError(f"{e}\nProper Syntax: $drawTriangle[x1;y1;x2;y2;x3;y3;color;outline;fill;outline_width]")

    def _draw_star(self, x: str, y: str, points: str,
                   outer_radius: str, inner_radius: str,
                   color: str = None, outline: str = None, fill: str = None,
                   outline_width: str = None) -> str:
        try:
            self._ensure_canvas()
            # Apply defaults from state
            color = color or self._get_state('color', 'black')
            lw = int(self._parse_num(outline_width)) if outline_width else int(self._get_state('stroke_width', 0))

            cx = self._parse_position(x, 'x')
            cy = self._parse_position(y, 'y')
            num_points = int(self._parse_num(points))
            r_outer = self._parse_num(outer_radius)
            r_inner = self._parse_num(inner_radius)

            if num_points < 2:
                raise ValueError("Star must have at least 2 points")

            star_points = []
            angle_step = math.pi / num_points

            for i in range(num_points * 2):
                r = r_outer if i % 2 == 0 else r_inner
                angle = i * angle_step - math.pi / 2
                px = cx + r * math.cos(angle)
                py = cy + r * math.sin(angle)
                star_points.append((px, py))

            fill_color = self._get_color(fill) if fill else self._get_color(color)
            
            # Outline logic
            outline_color = None
            if outline:
                outline_color = self._get_color(outline)
            elif lw > 0:
                outline_color = self._get_color(self._get_state('stroke_color', 'black'))

            if outline_color:
                self.draw.polygon(star_points, fill=fill_color, outline=outline_color, width=lw)
            else:
                self.draw.polygon(star_points, fill=fill_color)

            return f"Star drawn at ({cx}, {cy}) with {num_points} points"
        except ValueError as e:
            raise ValueError(f"{e}\nProper Syntax: $drawStar[x;y;points;outer_radius;inner_radius;color;outline;fill;outline_width]")

    def _draw_arc(self, x: str, y: str, w: str, h: str,
                  start_angle: str, end_angle: str,
                  color: str = None, width: str = None) -> str:
        self._ensure_canvas()
        try:
            x1 = self._parse_position(x, 'x')
            y1 = self._parse_position(y, 'y')
            width_box = self._parse_num(w)
            height_box = self._parse_num(h)
            start = self._parse_num(start_angle)
            end = self._parse_num(end_angle)
            
            # Apply defaults from state
            color = color or self._get_state('color', 'black')
            line_width = int(self._parse_num(width)) if width else int(self._get_state('stroke_width', 1))

            bbox = [(x1, y1), (x1 + width_box, y1 + height_box)]
            line_color = self._get_color(color)

            self.draw.arc(bbox, start=start, end=end,
                          fill=line_color, width=line_width)

            return f"Arc drawn at ({x1}, {y1}) from {start}° to {end}°"
        except ValueError as e:
            raise ValueError(f"{e}\nProper Syntax: $drawArc[x;y;w;h;start_angle;end_angle;color;width]")

