"""
Effects module - Special effects and filters for AlphaPIL.

This is an example of how to easily extend AlphaPIL by adding new modules.
Simply create a new Python file in the modules/ directory and create a mixin class.
"""

import random
from typing import Union
from PIL import Image, ImageDraw, ImageFilter
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
    
    @staticmethod
    def _normalize_rgba(color):
        """Ensure a color tuple is always 4-channel RGBA."""
        if color is None:
            return (0, 0, 0, 0)
        if len(color) == 3:
            return color + (255,)
        return color

    def _draw_linear_gradient(self, x: str, y: str, w: str, h: str, 
                             colors: str, angle: str = "90") -> str:
        """
        Draw a linear gradient rectangle with multiple color stops and rotation.
        Syntax: $drawLinearGradient[x;y;w;h;color1,stop1;color2,stop2;...;angle]
        """
        self._ensure_canvas()
        try:
            x1 = self._parse_position(x, 'x')
            y1 = self._parse_position(y, 'y')
            width = self._parse_length(w, 'x')
            height = self._parse_length(h, 'y')
            rot_angle = float(self._parse_num(angle))

            # Parse color stops: "red,0;blue,1"
            stops = []
            for item in colors.split(';'):
                parts = item.split(',')
                if len(parts) == 2:
                    color = self._normalize_rgba(self._get_color(parts[0].strip()))
                    stop = float(parts[1].strip())
                    stops.append((stop, color))
            
            if not stops:
                raise ValueError("At least one color stop required")
            stops.sort()

            # Create gradient buffer
            iw, ih = int(width), int(height)
            grad_img = Image.new("RGBA", (iw, ih), (0, 0, 0, 0))
            
            import math
            theta = math.radians(rot_angle)
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)
            
            cx = width / 2.0
            cy = height / 2.0
            R = 0.5 * (width * abs(cos_t) + height * abs(sin_t))
            if R == 0:
                R = 1.0

            def lerp_color(c1, c2, t):
                return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))

            pixels = grad_img.load()
            for py in range(ih):
                for px in range(iw):
                    dx = px - cx
                    dy = py - cy
                    proj = dx * cos_t + dy * sin_t
                    t = (proj + R) / (2.0 * R)
                    t = max(0.0, min(1.0, t))
                    
                    c = stops[0][1]
                    for j in range(len(stops) - 1):
                        if stops[j][0] <= t <= stops[j+1][0]:
                            div = stops[j+1][0] - stops[j][0]
                            local_t = (t - stops[j][0]) / div if div != 0 else 0.0
                            c = lerp_color(stops[j][1], stops[j+1][1], local_t)
                            break
                        elif t > stops[j+1][0]:
                            c = stops[j+1][1]
                    
                    pixels[px, py] = c

            # Composite gradient onto the current canvas IN-PLACE
            # This preserves the canvas object reference (critical for clip stack integrity)
            self.canvas.alpha_composite(grad_img, (int(x1), int(y1)))
            self.draw = ImageDraw.Draw(self.canvas)
            return f"Linear gradient drawn at ({x1}, {y1})"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $drawLinearGradient[x;y;w;h;colors;angle]")

    def _draw_radial_gradient(self, cx: str, cy: str, radius: str, colors: str) -> str:
        """
        Draw a radial gradient.
        Syntax: $drawRadialGradient[cx;cy;radius;color1,stop1;color2,stop2;...]
        """
        self._ensure_canvas()
        try:
            x_pos = self._parse_position(cx, 'x')
            y_pos = self._parse_position(cy, 'y')
            r = self._parse_length(radius, 'x')
            
            stops = []
            for item in colors.split(';'):
                parts = item.split(',')
                if len(parts) == 2:
                    color = self._normalize_rgba(self._get_color(parts[0].strip()))
                    stop = float(parts[1].strip())
                    stops.append((stop, color))
            stops.sort()

            size = int(r * 2)
            grad_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
            
            def lerp_color(c1, c2, t):
                return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(4))

            pixels = grad_img.load()
            for y in range(size):
                for x in range(size):
                    dist = ((x - r)**2 + (y - r)**2)**0.5
                    t = dist / r
                    if t > 1.0:
                        continue
                    
                    c = stops[0][1]
                    for j in range(len(stops) - 1):
                        if stops[j][0] <= t <= stops[j+1][0]:
                            div = stops[j+1][0] - stops[j][0]
                            local_t = (t - stops[j][0]) / div if div != 0 else 0.0
                            c = lerp_color(stops[j][1], stops[j+1][1], local_t)
                            break
                        elif t > stops[j+1][0]:
                            c = stops[j+1][1]
                    
                    pixels[x, y] = c

            # Composite in-place to preserve clip stack canvas references
            paste_x = int(x_pos - r)
            paste_y = int(y_pos - r)
            self.canvas.alpha_composite(grad_img, (paste_x, paste_y))
            self.draw = ImageDraw.Draw(self.canvas)
            return "Radial gradient drawn"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $drawRadialGradient[cx;cy;radius;colors]")

    def _blur_region(self, radius: str, x: str = None, y: str = None, w: str = None, h: str = None) -> str:
        """
        Blur a specific region of the canvas (Glassmorphism).
        """
        self._ensure_canvas()
        try:
            r = self._parse_length(radius, 'x')
            
            if x is None:
                # Blur whole canvas
                self.canvas = self.canvas.filter(ImageFilter.GaussianBlur(r))
                self.draw = ImageDraw.Draw(self.canvas)
                return f"Canvas blurred with radius {r}"
            
            x1 = self._parse_position(x, 'x')
            y1 = self._parse_position(y, 'y')
            width = self._parse_length(w, 'x')
            height = self._parse_length(h, 'y')
            
            box = (int(x1), int(y1), int(x1 + width), int(y1 + height))
            region = self.canvas.crop(box)
            region = region.filter(ImageFilter.GaussianBlur(r))
            self.canvas.paste(region, (int(x1), int(y1)))
            
            return f"Region at ({x1}, {y1}) blurred"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $blur[radius;x;y;w;h]")
    
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

    def _rotate_canvas(self, angle: str, expand: str = "false") -> str:
        """
        Rotate the current canvas (or active layer) by a given angle in degrees counter-clockwise.
        
        Args:
            angle: Angle of rotation in degrees
            expand: "true" to expand canvas size to fit the rotated image, "false" to keep same size
            
        Returns:
            Confirmation message
        """
        self._ensure_canvas()
        try:
            from PIL import Image, ImageDraw
            
            rot_angle = float(self._parse_num(angle))
            should_expand = str(expand).lower() in ['true', '1', 'yes', 'on']
            
            # Determine target layer or canvas
            target_img = self.canvas
            is_layer = False
            if hasattr(self, '_current_layer_name') and self._current_layer_name and self._current_layer_name in self._layers:
                target_img = self._layers[self._current_layer_name]
                is_layer = True
                
            # Perform rotation with BICUBIC resampling for crisp details
            rotated = target_img.rotate(rot_angle, resample=Image.Resampling.BICUBIC, expand=should_expand)
            
            if not is_layer:
                self.canvas = rotated
                self.canvas_size = self.canvas.size
                self.draw = ImageDraw.Draw(self.canvas)
            else:
                self._layers[self._current_layer_name] = rotated
                self.draw = ImageDraw.Draw(rotated)
                
            return f"Rotated canvas by {rot_angle} degrees"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $rotate[angle;expand]")

    def _adjust_color(self, brightness: str = "1.0", contrast: str = "1.0", saturation: str = "1.0") -> str:
        """
        Adjust the brightness, contrast, or saturation/color of the current active layer or canvas.
        Values: 1.0 is original, <1.0 decreases, >1.0 increases.
        
        Args:
            brightness: Brightness multiplier (default: 1.0)
            contrast: Contrast multiplier (default: 1.0)
            saturation: Saturation multiplier (default: 1.0)
            
        Returns:
            Confirmation message
        """
        self._ensure_canvas()
        try:
            from PIL import ImageEnhance, ImageDraw
            
            b_val = float(self._parse_num(brightness)) if brightness else 1.0
            c_val = float(self._parse_num(contrast)) if contrast else 1.0
            s_val = float(self._parse_num(saturation)) if saturation else 1.0
            
            # Determine target layer or canvas
            target_img = self.canvas
            is_layer = False
            if hasattr(self, '_current_layer_name') and self._current_layer_name and self._current_layer_name in self._layers:
                target_img = self._layers[self._current_layer_name]
                is_layer = True
                
            img = target_img
            
            # 1. Saturation (Color)
            if s_val != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(s_val)
                
            # 2. Brightness
            if b_val != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(b_val)
                
            # 3. Contrast
            if c_val != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(c_val)
                
            if not is_layer:
                self.canvas = img
                self.draw = ImageDraw.Draw(self.canvas)
            else:
                self._layers[self._current_layer_name] = img
                self.draw = ImageDraw.Draw(img)
                
            return "Adjusted image colors"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $adjustColor[brightness;contrast;saturation]")
