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
                       vals: str, labels: str = "", theme: str = "modern",
                       color: str = None, gap: str = "10", 
                       show_lab: str = "true", font: str = None, size: str = "20",
                       radius: str = "0", max_val: str = None) -> str:
        self._ensure_canvas()
        try:
            x_pos = self._parse_position(x, 'x')
            y_pos = self._parse_position(y, 'y')
            width = self._parse_length(w, 'x')
            height = self._parse_length(h, 'y')
            
            # Parse values (supports both ; and , separators)
            # AI Preference: Use , to avoid conflict with top-level ; delimiter
            v_str = str(vals).replace(',', ';')
            val_list = [float(v.strip()) for v in v_str.split(';') if v.strip()]
            
            l_str = str(labels).replace(',', ';')
            lab_list = [l.strip() for l in l_str.split(';')]
            
            if not val_list:
                raise ValueError("No values provided for bar chart")
            
            bar_gap = self._parse_length(gap, 'x')
            r = self._parse_length(radius, 'x')
            
            # Normalization logic
            actual_max = max(val_list) if val_list else 1
            norm_max = float(self._parse_num(max_val)) if max_val else actual_max
            norm_max = max(norm_max, actual_max) # Prevent overflow
            
            num_bars = len(val_list)
            
            # Calculate bar width based on available space and gaps
            bar_width = (width - (num_bars - 1) * bar_gap) / num_bars
            
            theme_colors = self._get_theme_colors(theme)
            chart_color = self._get_color(color) if color else None
            
            font_obj = self._get_font(size, font)
            
            for i, val in enumerate(val_list):
                bar_height = (val / norm_max) * height
                bx = x_pos + i * (bar_width + bar_gap)
                by = y_pos + (height - bar_height)
                
                fill_color = chart_color or theme_colors[i % len(theme_colors)]
                
                bbox = [bx, by, bx + bar_width, y_pos + height]
                
                if r > 0:
                    self.draw.rounded_rectangle(bbox, radius=r, fill=fill_color)
                else:
                    self.draw.rectangle(bbox, fill=fill_color)
                
                if show_lab.lower() == "true" and i < len(lab_list):
                    label = lab_list[i]
                    l_bbox = self.draw.textbbox((0, 0), label, font=font_obj)
                    tw = l_bbox[2] - l_bbox[0]
                    self.draw.text((bx + (bar_width - tw)/2, y_pos + height + self._s(5)), 
                                   label, font=font_obj, fill=self._get_color(self._get_state('color', 'gray')))
            
            return f"Bar chart drawn at ({x_pos}, {y_pos})"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $drawBarChart[x;y;w;h;vals;labels;theme;color;gap;show_lab;font;size;radius;max_val]")

    def _draw_line_chart(self, x: str, y: str, w: str, h: str,
                        vals: str, labels: str = "", theme: str = "modern",
                        color: str = None, lw: str = "2",
                        points: str = "true", font: str = None, size: str = "20",
                        max_val: str = None) -> str:
        self._ensure_canvas()
        try:
            x_pos = self._parse_position(x, 'x')
            y_pos = self._parse_position(y, 'y')
            width = self._parse_length(w, 'x')
            height = self._parse_length(h, 'y')
            
            # Parse values (supports both ; and , separators)
            # AI Preference: Use , to avoid conflict with top-level ; delimiter
            v_str = str(vals).replace(',', ';')
            val_list = [float(v.strip()) for v in v_str.split(';') if v.strip()]
            
            l_str = str(labels).replace(',', ';')
            lab_list = [l.strip() for l in l_str.split(';')]
            
            if not val_list:
                raise ValueError("No values provided for line chart")
                
            # Normalization logic
            actual_max = max(val_list) if val_list else 1
            norm_max = float(self._parse_num(max_val)) if max_val else actual_max
            norm_max = max(norm_max, actual_max) # Prevent overflow
            
            num_points = len(val_list)
            
            theme_colors = self._get_theme_colors(theme)
            chart_color = self._get_color(color) or theme_colors[0]
            line_width = int(self._parse_length(lw, 'x'))
            
            points_list = []
            x_step = width / (num_points - 1) if num_points > 1 else width
            
            for i, val in enumerate(val_list):
                px = x_pos + i * x_step
                py = y_pos + height - (val / norm_max) * height
                points_list.append((px, py))
            
            if len(points_list) > 1:
                self.draw.line(points_list, fill=chart_color, width=line_width)
            
            if points.lower() == "true":
                r = line_width * 1.5
                for px, py in points_list:
                    self.draw.ellipse([px-r, py-r, px+r, py+r], fill=chart_color)
            
            return f"Line chart drawn at ({x_pos}, {y_pos})"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $drawLineChart[x;y;w;h;vals;labels;theme;color;lw;points;font;size;max_val]")

    def _draw_progress_bar(self, x: str, y: str, w: str, h: str,
                          value: str, max_value: str = "100",
                          theme: str = "modern", color: str = None,
                          bg_color: str = "gray", radius: str = "5") -> str:
        self._ensure_canvas()
        try:
            x_pos = self._parse_position(x, 'x')
            y_pos = self._parse_position(y, 'y')
            width = self._parse_length(w, 'x')
            height = self._parse_length(h, 'y')
            
            val = float(self._parse_num(value))
            m_val = float(self._parse_num(max_value))
            r = self._parse_length(radius, 'x')
            
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
