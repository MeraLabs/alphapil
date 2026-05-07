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
                   color: str = "black", outline: str = None, fill: str = None, 
                   outline_width: str = "1", anchor: str = "lt") -> str:
        self._ensure_canvas()
        try:
            w = self._parse_num(width)
            h = self._parse_num(height)
            
            # Apply anchor offset
            ax, ay = self._get_anchor_offset(anchor, w, h)
            x1 = self._parse_position(x, 'x') + ax
            y1 = self._parse_position(y, 'y') + ay
            
            lw = int(self._parse_num(outline_width))
            x2 = x1 + w
            y2 = y1 + h
            bbox = [(x1, y1), (x2, y2)]

            fill_color = self._get_color(fill) if fill else self._get_color(color)
            outline_color = self._get_color(outline) if outline else None

            if outline_color:
                self.draw.rectangle(bbox, fill=fill_color, outline=outline_color, width=lw)
            else:
                self.draw.rectangle(bbox, fill=fill_color)

            return f"Rectangle drawn at ({x1}, {y1}) size {w}x{h}"
        except ValueError as e:
            raise ValueError(f"Invalid rectangle parameters: {e}")

    def _draw_circle(self, cx: str, cy: str, radius: str, 
                     color: str = "black", outline: str = None, fill: str = None,
                     outline_width: str = "1", anchor: str = "mm") -> str:
        self._ensure_canvas()
        try:
            r = self._parse_num(radius)
            w = h = r * 2
            
            # Apply anchor offset (Default 'mm' for circles)
            ax, ay = self._get_anchor_offset(anchor, 0, 0) # Center is pivot for mm
            # If anchor is 'lt', we must shift by radius to treat cx/cy as top-left
            if anchor == 'lt':
                center_x = self._parse_position(cx, 'x') + r
                center_y = self._parse_position(cy, 'y') + r
            else:
                center_x = self._parse_position(cx, 'x')
                center_y = self._parse_position(cy, 'y')

            lw = int(self._parse_num(outline_width))

            left = center_x - r
            top = center_y - r
            right = center_x + r
            bottom = center_y + r
            bbox = [(left, top), (right, bottom)]

            fill_color = self._get_color(fill) if fill else self._get_color(color)
            outline_color = self._get_color(outline) if outline else None

            if outline_color:
                self.draw.ellipse(bbox, fill=fill_color, outline=outline_color, width=lw)
            else:
                self.draw.ellipse(bbox, fill=fill_color)

            return f"Circle drawn at ({center_x}, {center_y}) with radius {r}"
        except ValueError as e:
            raise ValueError(f"Invalid circle parameters: {e}")

    def _draw_rounded_rect(self, x: str, y: str, width: str, height: str, 
                           radius: str = "10", color: str = "black", 
                           outline: str = None, fill: str = None,
                           outline_width: str = "1", anchor: str = "lt") -> str:
        self._ensure_canvas()
        try:
            w = self._parse_num(width)
            h = self._parse_num(height)
            
            # Apply anchor offset
            ax, ay = self._get_anchor_offset(anchor, w, h)
            x1 = self._parse_position(x, 'x') + ax
            y1 = self._parse_position(y, 'y') + ay
            
            r = self._parse_num(radius)
            lw = int(self._parse_num(outline_width))
            x2 = x1 + w
            y2 = y1 + h

            fill_color = self._get_color(fill) if fill else self._get_color(color)
            outline_color = self._get_color(outline) if outline else None

            bbox = [(x1, y1), (x2, y2)]
            if hasattr(self.draw, 'rounded_rectangle'):
                if outline_color:
                    self.draw.rounded_rectangle(bbox, radius=r, fill=fill_color, outline=outline_color, width=lw)
                else:
                    self.draw.rounded_rectangle(bbox, radius=r, fill=fill_color)
            else:
                if outline_color:
                    self.draw.rectangle(bbox, fill=fill_color, outline=outline_color, width=lw)
                else:
                    self.draw.rectangle(bbox, fill=fill_color)

            return f"Rounded rectangle drawn at ({x1}, {y1}) size {w}x{h}"
        except ValueError as e:
            raise ValueError(f"Invalid rounded rectangle parameters: {e}")

    def _draw_line(self, x1: str, y1: str, x2: str, y2: str, 
                   color: str = "black", width: str = "1") -> str:
        self._ensure_canvas()
        try:
            start_x = self._parse_position(x1, 'x')
            start_y = self._parse_position(y1, 'y')
            end_x = self._parse_position(x2, 'x')
            end_y = self._parse_position(y2, 'y')
            line_width = self._parse_num(width)

            line_color = self._get_color(color)

            self.draw.line([(start_x, start_y), (end_x, end_y)],
                           fill=line_color, width=line_width)

            return f"Line drawn from ({start_x}, {start_y}) to ({end_x}, {end_y})"
        except ValueError as e:
            raise ValueError(f"Invalid line parameters: {e}")

    # -------------------------
    # NEW METHODS ADDED
    # -------------------------

    def _draw_polygon(self, points_list: str, color: str = "black",
                       outline: str = None, fill: str = None,
                       outline_width: str = "1") -> str:
        self._ensure_canvas()
        try:
            raw_points = [p.strip() for p in points_list.split(",")]
            if len(raw_points) < 6 or len(raw_points) % 2 != 0:
                raise ValueError("Polygon requires even number of coordinates (x1,y1,x2,y2...)")

            points = []
            for i in range(0, len(raw_points), 2):
                x = self._parse_position(raw_points[i], 'x')
                y = self._parse_position(raw_points[i + 1], 'y')
                points.append((x, y))

            fill_color = self._get_color(fill) if fill else self._get_color(color)
            outline_color = self._get_color(outline) if outline else None
            lw = int(self._parse_num(outline_width))

            if outline_color:
                self.draw.polygon(points, fill=fill_color, outline=outline_color, width=lw)
            else:
                self.draw.polygon(points, fill=fill_color)

            return f"Polygon drawn with {len(points)} points"
        except ValueError as e:
            raise ValueError(f"Invalid polygon parameters: {e}")

    def _draw_triangle(self, x1: str, y1: str,
                       x2: str, y2: str,
                       x3: str, y3: str,
                       color: str = "black", outline: str = None, fill: str = None,
                       outline_width: str = "1") -> str:
        self._ensure_canvas()
        try:
            p1 = (self._parse_position(x1, 'x'), self._parse_position(y1, 'y'))
            p2 = (self._parse_position(x2, 'x'), self._parse_position(y2, 'y'))
            p3 = (self._parse_position(x3, 'x'), self._parse_position(y3, 'y'))

            fill_color = self._get_color(fill) if fill else self._get_color(color)
            outline_color = self._get_color(outline) if outline else None
            lw = int(self._parse_num(outline_width))

            if outline_color:
                self.draw.polygon([p1, p2, p3], fill=fill_color, outline=outline_color, width=lw)
            else:
                self.draw.polygon([p1, p2, p3], fill=fill_color)

            return "Triangle drawn"
        except ValueError as e:
            raise ValueError(f"Invalid triangle parameters: {e}")

    def _draw_star(self, x: str, y: str, points: str,
                   outer_radius: str, inner_radius: str,
                   color: str = "black", outline: str = None, fill: str = None,
                   outline_width: str = "1") -> str:
        self._ensure_canvas()
        try:
            cx = self._parse_position(x, 'x')
            cy = self._parse_position(y, 'y')
            num_points = int(self._parse_num(points))
            r_outer = self._parse_num(outer_radius)
            r_inner = self._parse_num(inner_radius)
            lw = int(self._parse_num(outline_width))

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
            outline_color = self._get_color(outline) if outline else None

            if outline_color:
                self.draw.polygon(star_points, fill=fill_color, outline=outline_color, width=lw)
            else:
                self.draw.polygon(star_points, fill=fill_color)

            return f"Star drawn at ({cx}, {cy}) with {num_points} points"
        except ValueError as e:
            raise ValueError(f"Invalid star parameters: {e}")

    def _draw_arc(self, x: str, y: str, w: str, h: str,
                  start_angle: str, end_angle: str,
                  color: str = "black", width: str = "1") -> str:
        self._ensure_canvas()
        try:
            x1 = self._parse_position(x, 'x')
            y1 = self._parse_position(y, 'y')
            width_box = self._parse_num(w)
            height_box = self._parse_num(h)
            start = self._parse_num(start_angle)
            end = self._parse_num(end_angle)
            line_width = self._parse_num(width)

            bbox = [(x1, y1), (x1 + width_box, y1 + height_box)]
            line_color = self._get_color(color)

            self.draw.arc(bbox, start=start, end=end,
                          fill=line_color, width=line_width)

            return f"Arc drawn at ({x1}, {y1}) from {start}° to {end}°"
        except ValueError as e:
            raise ValueError(f"Invalid arc parameters: {e}")
