"""
Effects module - Special effects and filters for AlphaPIL.

This is an example of how to easily extend AlphaPIL by adding new modules.
Simply create a new Python file in the modules/ directory and create a mixin class.
"""

import random
from typing import Union
from PIL import ImageDraw, ImageFilter
from .base import AlphaMixin


class EffectsMixin(AlphaMixin):
    """
    Example mixin class demonstrating how to extend AlphaPIL with new functionality.
    
    This mixin adds special effects like noise, gradients, and patterns.
    """
    
    def _add_noise(self, intensity: str = "10") -> str:
        """
        Add random noise to the canvas.
        
        Args:
            intensity: Noise intensity as string (default: "10")
            
        Returns:
            Confirmation message
        """
        self._ensure_canvas()
        
        try:
            noise_level = self._parse_num(intensity)
            pixels = self.canvas.load()
            
            for i in range(self.canvas.width):
                for j in range(self.canvas.height):
                    if random.random() < noise_level / 100:
                        # Add random color variation
                        r, g, b = pixels[i, j]
                        noise = random.randint(-noise_level, noise_level)
                        pixels[i, j] = (
                            max(0, min(255, r + noise)),
                            max(0, min(255, g + noise)),
                            max(0, min(255, b + noise))
                        )
            
            return f"Added noise with intensity {noise_level}"
        except ValueError as e:
            raise ValueError(f"Invalid noise parameters: {e}")
    
    def _draw_gradient(self, x1: str, y1: str, x2: str, y2: str, 
                      color1: str, color2: str, direction: str = "horizontal") -> str:
        """
        Draw a gradient rectangle.
        
        Args:
            x1: Start X coordinate as string
            y1: Start Y coordinate as string
            x2: End X coordinate as string
            y2: End Y coordinate as string
            color1: Start color
            color2: End color
            direction: "horizontal" or "vertical" (default: "horizontal")
            
        Returns:
            Confirmation message
        """
        self._ensure_canvas()
        
        try:
            start_x = self._parse_num(x1)
            start_y = self._parse_num(y1)
            end_x = self._parse_num(x2)
            end_y = self._parse_num(y2)
            
            start_color = self._get_color(color1)
            end_color = self._get_color(color2)
            
            if direction.lower() == "horizontal":
                width = end_x - start_x
                height = end_y - start_y
                
                for i in range(width):
                    ratio = i / width
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                    
                    self.draw.line([(start_x + i, start_y), (start_x + i, end_y)], 
                                 fill=(r, g, b))
            else:  # vertical
                width = end_x - start_x
                height = end_y - start_y
                
                for i in range(height):
                    ratio = i / height
                    r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
                    g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
                    b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
                    
                    self.draw.line([(start_x, start_y + i), (end_x, start_y + i)], 
                                 fill=(r, g, b))
            
            return f"Gradient drawn from ({start_x}, {start_y}) to ({end_x}, {end_y})"
        except ValueError as e:
            raise ValueError(f"Invalid gradient parameters: {e}")
    
    def _draw_pattern(self, x: str, y: str, width: str, height: str, 
                     pattern_type: str = "dots", color: str = "black") -> str:
        """
        Draw a pattern fill.
        
        Args:
            x: X coordinate as string
            y: Y coordinate as string
            width: Pattern width as string
            height: Pattern height as string
            pattern_type: "dots", "lines", "grid" (default: "dots")
            color: Pattern color (default: "black")
            
        Returns:
            Confirmation message
        """
        self._ensure_canvas()
        
        try:
            start_x = self._parse_num(x)
            start_y = self._parse_num(y)
            pattern_width = self._parse_num(width)
            pattern_height = self._parse_num(height)
            
            pattern_color = self._get_color(color)
            
            if pattern_type.lower() == "dots":
                # Draw dot pattern
                for i in range(0, int(pattern_width), 10):
                    for j in range(0, int(pattern_height), 10):
                        self.draw.ellipse(
                            [(start_x + i - 2, start_y + j - 2), 
                             (start_x + i + 2, start_y + j + 2)],
                            fill=pattern_color
                        )
            elif pattern_type.lower() == "lines":
                # Draw diagonal lines
                for i in range(0, int(pattern_width + pattern_height), 10):
                    self.draw.line(
                        [(start_x + i, start_y), 
                         (start_x + i - pattern_height, start_y + pattern_height)],
                        fill=pattern_color
                    )
            elif pattern_type.lower() == "grid":
                # Draw grid pattern
                for i in range(0, int(pattern_width), 15):
                    self.draw.line(
                        [(start_x + i, start_y), 
                         (start_x + i, start_y + pattern_height)],
                        fill=pattern_color
                    )
                for j in range(0, int(pattern_height), 15):
                    self.draw.line(
                        [(start_x, start_y + j), 
                         (start_x + pattern_width, start_y + j)],
                        fill=pattern_color
                    )
            
            return f"{pattern_type} pattern drawn at ({start_x}, {start_y})"
        except ValueError as e:
            raise ValueError(f"Invalid pattern parameters: {e}")
