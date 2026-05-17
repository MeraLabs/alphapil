"""
Charts module - Data visualization for AlphaPIL.

This module provides functions for drawing charts and graphs like bar charts,
line charts, and progress bars with theme support.
"""

from typing import List, Tuple, Union, Optional
from PIL import ImageDraw, ImageFont
from .base import AlphaMixin

class ChartsMixin(AlphaMixin):
    """
    Mixin class providing charting and graph functionality.
    """
    
    THEMES = {
        'modern': ['#5865F2', '#57F287', '#FEE75C', '#EB459E', '#ED4245'],
        'vibrant': ['#FF595E', '#FFCA3A', '#8AC926', '#1982C4', '#6A4C93'],
        'pastel': ['#FFB7B2', '#FFDAC1', '#E2F0CB', '#B5EAD7', '#C7CEEA'],
        'ocean': ['#0077B6', '#00B4D8', '#90E0EF', '#03045E', '#023E8A'],
        'forest': ['#2D6A4F', '#40916C', '#52B788', '#74C69D', '#95D5B2'],
        'sunset': ['#F94144', '#F3722C', '#F8961E', '#F9844A', '#F9C74F'],
        'cyberpunk': ['#FF00FF', '#00FFFF', '#FFFF00', '#00FF00', '#FF0000'],
        'dark_gold': ['#B8860B', '#DAA520', '#FFD700', '#8B4513', '#5D4037'],
        'slate': ['#264653', '#2A9D8F', '#E9C46A', '#F4A261', '#E76F51'],
        'neon': ['#39FF14', '#FF3131', '#00FFFF', '#FF00FF', '#FFFF00']
    }

    def _get_theme_colors(self, theme_name: str) -> List[Tuple[int, int, int, int]]:
        colors = self.THEMES.get(theme_name.lower(), self.THEMES['modern'])
        return [self._get_color(c) for c in colors]

    def _draw_bar_chart(self, x: str, y: str, w: str, h: str, 
                       values: str, labels: str = "", theme: str = "modern",
                       color: str = None, gap: str = "10", 
                       show_labels: str = "true", font: str = None, font_size: str = "12") -> str:
        self._ensure_canvas()
        try:
            x_pos = self._parse_position(x, 'x')
            y_pos = self._parse_position(y, 'y')
            width = self._s(self._parse_num(w))
            height = self._s(self._parse_num(h))
            
            val_list = [float(v.strip()) for v in values.split(';') if v.strip()]
            lab_list = [l.strip() for l in labels.split(';') if l.strip()]
            
            if not val_list:
                raise ValueError("No values provided for bar chart")
            
            bar_gap = self._s(self._parse_num(gap))
            max_val = max(val_list) if val_list else 1
            num_bars = len(val_list)
            
            bar_width = (width - (num_bars - 1) * bar_gap) / num_bars
            
            theme_colors = self._get_theme_colors(theme)
            chart_color = self._get_color(color) if color else None
            
            f_size = int(self._s(self._parse_num(font_size)))
            font_obj = self._get_font(font_size, font)
            
            for i, val in enumerate(val_list):
                bar_height = (val / max_val) * height
                bx = x_pos + i * (bar_width + bar_gap)
                by = y_pos + (height - bar_height)
                
                fill_color = chart_color or theme_colors[i % len(theme_colors)]
                
                self.draw.rectangle([bx, by, bx + bar_width, y_pos + height], fill=fill_color)
                
                if show_labels.lower() == "true" and i < len(lab_list):
                    label = lab_list[i]
                    bbox = self.draw.textbbox((0, 0), label, font=font_obj)
                    tw = bbox[2] - bbox[0]
                    self.draw.text((bx + (bar_width - tw)/2, y_pos + height + self._s(5)), 
                                   label, font=font_obj, fill=self._get_color('black'))
            
            return f"Bar chart drawn at ({x_pos}, {y_pos})"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $drawBarChart[x;y;w;h;values;labels;theme;color;gap;show_labels;font;font_size]")

    def _draw_line_chart(self, x: str, y: str, w: str, h: str,
                        values: str, labels: str = "", theme: str = "modern",
                        color: str = None, line_width: str = "2",
                        show_points: str = "true", font: str = None, font_size: str = "12") -> str:
        self._ensure_canvas()
        try:
            x_pos = self._parse_position(x, 'x')
            y_pos = self._parse_position(y, 'y')
            width = self._s(self._parse_num(w))
            height = self._s(self._parse_num(h))
            
            val_list = [float(v.strip()) for v in values.split(';') if v.strip()]
            lab_list = [l.strip() for l in labels.split(';') if l.strip()]
            
            if not val_list:
                raise ValueError("No values provided for line chart")
                
            max_val = max(val_list) if val_list else 1
            num_points = len(val_list)
            
            theme_colors = self._get_theme_colors(theme)
            chart_color = self._get_color(color) or theme_colors[0]
            lw = int(self._s(self._parse_num(line_width)))
            
            points = []
            x_step = width / (num_points - 1) if num_points > 1 else width
            
            for i, val in enumerate(val_list):
                px = x_pos + i * x_step
                py = y_pos + height - (val / max_val) * height
                points.append((px, py))
            
            if len(points) > 1:
                self.draw.line(points, fill=chart_color, width=lw)
            
            if show_points.lower() == "true":
                r = lw * 1.5
                for px, py in points:
                    self.draw.ellipse([px-r, py-r, px+r, py+r], fill=chart_color)
            
            return f"Line chart drawn at ({x_pos}, {y_pos})"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $drawLineChart[x;y;w;h;values;labels;theme;color;line_width;show_points;font;font_size]")

    def _draw_progress_bar(self, x: str, y: str, w: str, h: str,
                          value: str, max_value: str = "100",
                          theme: str = "modern", color: str = None,
                          bg_color: str = "gray", radius: str = "5") -> str:
        self._ensure_canvas()
        try:
            x_pos = self._parse_position(x, 'x')
            y_pos = self._parse_position(y, 'y')
            width = self._s(self._parse_num(w))
            height = self._s(self._parse_num(h))
            
            val = float(self._parse_num(value))
            m_val = float(self._parse_num(max_value))
            r = self._s(self._parse_num(radius))
            
            progress = min(max(val / m_val, 0), 1)
            
            theme_colors = self._get_theme_colors(theme)
            bar_color = self._get_color(color) or theme_colors[0]
            background = self._get_color(bg_color)
            
            # Draw background
            self.draw.rounded_rectangle([x_pos, y_pos, x_pos + width, y_pos + height], 
                                        radius=r, fill=background)
            
            # Draw progress
            if progress > 0:
                pw = width * progress
                self.draw.rounded_rectangle([x_pos, y_pos, x_pos + pw, y_pos + height], 
                                            radius=r, fill=bar_color)
            
            return "Progress bar drawn"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $drawProgressBar[x;y;w;h;value;max_value;theme;color;bg_color;radius]")
