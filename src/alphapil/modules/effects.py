"""
Effects module - Special effects and filters for AlphaPIL.

This is an example of how to easily extend AlphaPIL by adding new modules.
Simply create a new Python file in the modules/ directory and create a mixin class.
"""

import random
import math
from typing import Union
import numpy as np
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
            
            # NumPy vectorized noise: operates on entire image array at once
            arr = np.array(self.canvas, dtype=np.int16)
            h, w = arr.shape[:2]
            
            # Create a random mask for which pixels get noise
            mask = np.random.random((h, w)) < (noise_level / 100.0)
            
            # Generate noise values for all pixels, apply only where mask is True
            noise = np.random.randint(-int(noise_level), int(noise_level) + 1, size=(h, w, 1), dtype=np.int16)
            noise_broadcast = np.broadcast_to(noise, (h, w, arr.shape[2]))
            
            # Apply noise only to masked pixels, clamp to [0, 255]
            arr[mask] = np.clip(arr[mask] + noise_broadcast[mask], 0, 255)
            
            self.canvas = Image.fromarray(arr.astype(np.uint8), self.canvas.mode)
            self.draw = ImageDraw.Draw(self.canvas)
            
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
            
            theta = math.radians(rot_angle)
            cos_t = math.cos(theta)
            sin_t = math.sin(theta)
            
            # Calculate active gradient projection length L
            L = width * abs(cos_t) + height * abs(sin_t)
            if L == 0:
                L = 1.0
                
            diag = int(math.ceil(math.sqrt(iw**2 + ih**2)))
            if diag % 2 != 0:
                diag += 1  # Keep it even for clean centering
            
            pad_left = (diag - L) / 2.0
            
            # ── NumPy vectorized 1D gradient generation ──
            # Build t-values for all pixels at once
            px_arr = np.arange(diag, dtype=np.float64)
            t_arr = np.clip((px_arr - pad_left) / L, 0.0, 1.0)
            
            # Build color array using piecewise linear interpolation across all stops
            stop_positions = np.array([s[0] for s in stops], dtype=np.float64)
            stop_colors = np.array([s[1] for s in stops], dtype=np.float64)  # (N, 4)
            
            # For each t, find which segment it falls in and interpolate
            # np.searchsorted gives the insertion index; clamp to valid segment range
            indices = np.searchsorted(stop_positions, t_arr, side='right') - 1
            indices = np.clip(indices, 0, len(stops) - 2)
            
            # Get the bounding stop colors and positions for each pixel
            t0 = stop_positions[indices]          # (diag,)
            t1 = stop_positions[indices + 1]      # (diag,)
            c0 = stop_colors[indices]             # (diag, 4)
            c1 = stop_colors[indices + 1]         # (diag, 4)
            
            # Compute local interpolation factor within each segment
            seg_len = t1 - t0
            seg_len[seg_len == 0] = 1.0  # avoid division by zero
            local_t = ((t_arr - t0) / seg_len)[:, np.newaxis]  # (diag, 1)
            
            # Interpolate colors: (diag, 4)
            grad_row = np.clip(c0 + (c1 - c0) * local_t, 0, 255).astype(np.uint8)
            
            # Create 1D gradient image from array (1 row, diag columns, 4 channels)
            grad_1d = Image.fromarray(grad_row.reshape(1, diag, 4), "RGBA")
                
            # Stretch the 1D gradient to a square of size (diag, diag)
            grad_sq = grad_1d.resize((diag, diag), Image.Resampling.BILINEAR)
            
            # Rotate square image (-rot_angle to match standard coordinate system rotation)
            grad_rotated = grad_sq.rotate(-rot_angle, resample=Image.Resampling.BILINEAR)
            
            # Crop out the central (iw, ih) rectangle
            left = (diag - iw) // 2
            top = (diag - ih) // 2
            right = left + iw
            bottom = top + ih
            grad_img = grad_rotated.crop((left, top, right, bottom))

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
            
            # ── NumPy vectorized radial gradient ──
            # Create coordinate grids
            y_coords, x_coords = np.mgrid[0:size, 0:size]
            
            # Compute distance from center for every pixel
            dist = np.sqrt((x_coords - r)**2 + (y_coords - r)**2)
            t_arr = dist / r  # (size, size) normalized distance
            
            # Build stop arrays
            stop_positions = np.array([s[0] for s in stops], dtype=np.float64)
            stop_colors = np.array([s[1] for s in stops], dtype=np.float64)  # (N, 4)
            
            # Flatten t for vectorized interpolation, clamp to [0, 1]
            t_flat = np.clip(t_arr.ravel(), 0.0, 1.0)  # (size*size,)
            
            # Find segment indices
            indices = np.searchsorted(stop_positions, t_flat, side='right') - 1
            indices = np.clip(indices, 0, len(stops) - 2)
            
            # Interpolate colors
            t0 = stop_positions[indices]
            t1 = stop_positions[indices + 1]
            c0 = stop_colors[indices]        # (size*size, 4)
            c1 = stop_colors[indices + 1]    # (size*size, 4)
            
            seg_len = t1 - t0
            seg_len[seg_len == 0] = 1.0
            local_t = ((t_flat - t0) / seg_len)[:, np.newaxis]  # (size*size, 1)
            
            colors_flat = np.clip(c0 + (c1 - c0) * local_t, 0, 255).astype(np.uint8)  # (size*size, 4)
            
            # Reshape to image and apply circular mask (pixels outside radius = transparent)
            colors_2d = colors_flat.reshape(size, size, 4)
            outside_mask = t_arr > 1.0
            colors_2d[outside_mask] = (0, 0, 0, 0)
            
            grad_img = Image.fromarray(colors_2d, "RGBA")

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
