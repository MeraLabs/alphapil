"""
Text module - Text rendering and manipulation for AlphaPIL.

This module provides functions for drawing text on the canvas and
performing text transformations like case conversion.
"""

import io
import aiohttp
from typing import Union, Dict, Optional
from PIL import ImageDraw, ImageFont, ImageFilter, Image


class TextMixin:
    """
    Mixin class providing text rendering and manipulation functionality.
    
    This mixin adds methods for drawing text, measuring text dimensions,
    and performing text transformations.
    """
    
    def _init_text(self):
        """Initialize text state."""
        self._font_aliases: Dict[str, str] = {}
        self._font_cache: Dict[str, bytes] = {}
        
    async def _load_font(self, path: str, alias: str) -> str:
        """
        Register a font file path or URL to an alias.
        
        Args:
            path: Path to .ttf/.otf file or a direct URL
            alias: Shorthand name to use later
            
        Returns:
            Confirmation message
        """
        if not hasattr(self, '_font_aliases'):
            self._init_text()
            
        if path.startswith(('http://', 'https://')):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(path) as response:
                        if response.status != 200:
                            raise ValueError(f"Failed to download font: HTTP {response.status}")
                        font_data = await response.read()
                        self._font_cache[alias] = font_data
                        self._font_aliases[alias] = path # Store path as reference
                return f"Remote font '{path}' loaded and cached as alias '{alias}'"
            except Exception as e:
                raise RuntimeError(f"Error loading remote font: {e}")
        else:
            self._font_aliases[alias] = path
            return f"Local font alias '{alias}' registered for {path}"

    def _get_font(self, size: Union[str, int], font_path: str = None) -> ImageFont.ImageFont:
        """
        Get a font object for text rendering.
        
        Args:
            size: Font size as string or integer
            font_path: Path to font file or alias
            
        Returns:
            PIL ImageFont object
        """
        font_size = int(size) if isinstance(size, str) else size
        
        # Check if font_path is a cached alias (Remote Font)
        if font_path and hasattr(self, '_font_cache') and font_path in self._font_cache:
            return ImageFont.truetype(io.BytesIO(self._font_cache[font_path]), font_size)

        # Check if font_path is a registered alias (Local Path)
        if font_path and hasattr(self, '_font_aliases') and font_path in self._font_aliases:
            font_path = self._font_aliases[font_path]

        if font_path:
            try:
                # Check if path itself is a URL but wasn't pre-loaded (not recommended but handled)
                if font_path.startswith(('http://', 'https://')):
                    # We can't easily sync download here without blocking, 
                    # so we fallback to default if not pre-loaded via $loadFont
                    pass
                else:
                    return ImageFont.truetype(font_path, font_size)
            except:
                pass  # Fall back to default font
        
        # Try common system fonts
        common_fonts = ["arial.ttf", "arialbd.ttf", "times.ttf", "cour.ttf", "DejaVuSans.ttf"]
        
        for font_name in common_fonts:
            try:
                return ImageFont.truetype(font_name, font_size)
            except:
                continue
        
        # Fall back to default font
        return ImageFont.load_default()
    
    def _draw_text(self, x: str, y: str, text: str, color: str = None, 
                   size: str = None, font: str = None, anchor: str = None,
                   stroke_width: str = None, stroke_fill: str = None,
                   shadow_color: str = None, shadow_offset: str = "0,0",
                   glow_color: str = None, glow_radius: str = "0",
                   max_width: str = None, truncate_width: str = None,
                   gradient_colors: str = None) -> str:
        """
        Draw text on the canvas with optional stroke, shadow, glow, wrapping, truncation, and gradient.
        Uses global state defaults (setFont, setColor, setStroke) if parameters are missing.
        
        Args:
            x, y: Position
            text: Content
            color: Text color
            size: Font size
            font: Font alias or path
            anchor: PIL anchor (e.g., 'mm', 'la')
            stroke_width, stroke_fill: Stroke properties
            shadow_color, shadow_offset: Shadow properties
            glow_color, glow_radius: Glow properties
            max_width: Wrap text if it exceeds this width
            truncate_width: Truncate text if it exceeds this width
            gradient_colors: Comma-separated colors for vertical gradient (e.g., "red,blue")
        """
        self._ensure_canvas()
        
        try:
            # Apply defaults from state
            color = color or self._get_state('color', 'black')
            size = size or str(self._get_state('font_size', 12))
            font = font or self._get_state('font', None)
            
            # Stroke defaults
            if stroke_width is None:
                sw = int(self._get_state('stroke_width', 0))
            else:
                sw = int(self._parse_num(stroke_width))
                
            if stroke_fill:
                stroke_color = self._get_color(stroke_fill)
            else:
                stroke_color = self._get_color(self._get_state('stroke_color', 'black')) if sw > 0 else None

            # 0. Apply Truncation and Wrapping first
            if truncate_width:
                text = self._truncate_text(text, truncate_width, size, font)
            if max_width:
                text = self._wrap_text(text, max_width, size, font)

            x_pos = self._parse_position(x, 'x')
            y_pos = self._parse_position(y, 'y')
            font_size = self._parse_num(size)
            gr = int(self._parse_num(glow_radius))
            
            text_color = self._get_color(color)
            font_obj = self._get_font(font_size, font)
            
            # 1. Apply Glow Effect
            if glow_color and gr > 0:
                gc = self._get_color(glow_color)
                bbox = self.draw.textbbox((0, 0), text, font=font_obj, stroke_width=sw)
                tw, th = int(bbox[2]-bbox[0] + gr*4), int(bbox[3]-bbox[1] + gr*4)
                glow_img = Image.new("RGBA", (tw, th), (0,0,0,0))
                ImageDraw.Draw(glow_img).text((gr*2, gr*2), text, font=font_obj, fill=gc, stroke_width=sw+gr, stroke_fill=gc)
                glow_img = glow_img.filter(ImageFilter.GaussianBlur(gr))
                self.canvas.paste(glow_img, (int(x_pos - gr*2), int(y_pos - gr*2)), glow_img)

            # 2. Apply Shadow Effect
            if shadow_color:
                sc = self._get_color(shadow_color)
                sx, sy = self._parse_coords(shadow_offset)
                self.draw.text((x_pos + sx, y_pos + sy), text, font=font_obj, fill=sc, stroke_width=sw, stroke_fill=sc, anchor=anchor)

            # 3. Handle Gradient
            if gradient_colors:
                colors = [c.strip() for c in gradient_colors.split(',')]
                if len(colors) >= 2:
                    bbox = self.draw.textbbox((0, 0), text, font=font_obj)
                    tw, th = int(bbox[2]-bbox[0]), int(bbox[3]-bbox[1])
                    if tw > 0 and th > 0:
                        gradient = Image.new("RGBA", (tw, th))
                        c1 = self._get_color(colors[0])
                        c2 = self._get_color(colors[1])
                        for i in range(th):
                            ratio = i / th
                            r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
                            g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
                            b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
                            ImageDraw.Draw(gradient).line([(0, i), (tw, i)], fill=(r, g, b, 255))
                        
                        mask = Image.new("L", (tw, th), 0)
                        ImageDraw.Draw(mask).text((0, 0), text, font=font_obj, fill=255)
                        self.canvas.paste(gradient, (int(x_pos), int(y_pos)), mask)
                        return f"Gradient text '{text}' drawn at ({x_pos}, {y_pos})"

            # 4. Draw Main Text
            text_kwargs = {
                'xy': (x_pos, y_pos),
                'text': text,
                'fill': text_color,
                'font': font_obj,
                'stroke_width': sw,
                'stroke_fill': stroke_color
            }
            if anchor: text_kwargs['anchor'] = anchor
            
            self.draw.text(**text_kwargs)
            return f"Text '{text}' drawn at ({x_pos}, {y_pos})"
        except ValueError as e:
            raise ValueError(f"Invalid text parameters: {e}. Proper Syntax: $drawText[x;y;text;color;size;font;anchor;...]")
    
    def _to_upper(self, text: str) -> str:
        """
        Convert text to uppercase.
        
        Args:
            text: Text to convert
            
        Returns:
            Uppercase text
        """
        return text.upper()
    
    def _to_lower(self, text: str) -> str:
        """
        Convert text to lowercase.
        
        Args:
            text: Text to convert
            
        Returns:
            Lowercase text
        """
        return text.lower()
    
    def _to_title(self, text: str) -> str:
        """
        Convert text to title case.
        
        Args:
            text: Text to convert
            
        Returns:
            Title case text
        """
        return text.title()
    
    def _measure_text(self, text: str, size: str = "12", font: str = None) -> str:
        """
        Measure text dimensions.
        
        Args:
            text: Text to measure
            size: Font size as string (default: "12")
            font: Font file path (optional)
            
        Returns:
            String with width and height in format "width,height"
        """
        try:
            font_size = self._parse_num(size)
            font_obj = self._get_font(font_size, font)
            
            # Get text bounding box
            bbox = self.draw.textbbox((0, 0), text, font=font_obj)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            
            return f"{width},{height}"
        except ValueError as e:
            raise ValueError(f"Invalid text measurement parameters: {e}")
    
    def _wrap_text(self, text: str, max_width: str, size: str = "12", font: str = None) -> str:
        """
        Wrap text to fit within a maximum width.
        Supports wrapping long words that exceed max_width.
        """
        try:
            max_w = self._parse_num(max_width)
            font_size = self._parse_num(size)
            font_obj = self._get_font(font_size, font)
            
            lines = []
            paragraphs = text.split('\n')
            
            for paragraph in paragraphs:
                words = paragraph.split(' ')
                current_line = []
                
                for word in words:
                    if not word and not current_line: continue
                    
                    test_line = ' '.join(current_line + [word]) if current_line else word
                    bbox = self.draw.textbbox((0, 0), test_line, font=font_obj)
                    
                    if (bbox[2] - bbox[0]) <= max_w:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(' '.join(current_line))
                            current_line = [word]
                            # Check if the single word is still too long
                            bbox = self.draw.textbbox((0, 0), word, font=font_obj)
                            if (bbox[2] - bbox[0]) > max_w:
                                # Break long word
                                word_part = ""
                                for char in word:
                                    if self.draw.textbbox((0, 0), word_part + char, font=font_obj)[2]-bbox[0] <= max_w:
                                        word_part += char
                                    else:
                                        if word_part: lines.append(word_part)
                                        word_part = char
                                current_line = [word_part]
                        else:
                            # Single word is too long for an empty line
                            word_part = ""
                            for char in word:
                                if self.draw.textbbox((0, 0), word_part + char, font=font_obj)[2] <= max_w:
                                    word_part += char
                                else:
                                    if word_part: lines.append(word_part)
                                    word_part = char
                            current_line = [word_part]
                
                if current_line:
                    lines.append(' '.join(current_line))
            
            return '\n'.join(lines)
        except ValueError as e:
            raise ValueError(f"Invalid text wrapping parameters: {e}")

    def _auto_size_text(self, text: str, max_width: str, start_size: str = "30", 
                        min_size: str = "10", font: str = None) -> str:
        """
        Calculates the best font size (decreasing from start_size) to fit text 
        within max_width. Returns the resulting size.
        """
        try:
            max_w = self._parse_num(max_width)
            current_size = int(self._parse_num(start_size))
            m_size = int(self._parse_num(min_size))
            
            while current_size >= m_size:
                font_obj = self._get_font(current_size, font)
                bbox = self.draw.textbbox((0, 0), text, font=font_obj)
                if (bbox[2] - bbox[0]) <= max_w:
                    return str(current_size)
                current_size -= 1
                
            return str(m_size)
        except Exception as e:
            raise ValueError(f"Invalid auto-size parameters: {e}")

    def _truncate_text(self, text: str, max_width: str, size: str = "12", font: str = None, suffix: str = "...") -> str:
        """
        Truncate text to fit within a maximum width.
        """
        try:
            max_w = self._parse_num(max_width)
            font_size = self._parse_num(size)
            font_obj = self._get_font(font_size, font)
            
            bbox = self.draw.textbbox((0, 0), text, font=font_obj)
            if (bbox[2] - bbox[0]) <= max_w:
                return text
                
            current = text
            while len(current) > 0:
                current = current[:-1]
                test_str = current + suffix
                bbox = self.draw.textbbox((0, 0), test_str, font=font_obj)
                if (bbox[2] - bbox[0]) <= max_w:
                    return test_str
            return suffix
        except Exception as e:
            raise ValueError(f"Invalid truncation parameters: {e}")

    def _draw_text_stroke(self, text: str, x: str, y: str,
                          size: str, color: str,
                          stroke_width: str,
                          stroke_color: str,
                          font: str = None) -> str:
        """
        Draw text with stroke (outline).
        """

        self._ensure_canvas()

        try:
            x_pos = self._parse_position(x, 'x')
            y_pos = self._parse_position(y, 'y')
            font_size = self._parse_num(size)
            sw = self._parse_num(stroke_width)

            font_obj = self._get_font(font_size, font)
            fill_color = self._get_color(color)
            outline_color = self._get_color(stroke_color)

            self.draw.text(
                (x_pos, y_pos),
                text,
                font=font_obj,
                fill=fill_color,
                stroke_width=sw,
                stroke_fill=outline_color
            )

            return f"Text with stroke drawn at ({x_pos}, {y_pos})"
        except ValueError as e:
            raise ValueError(f"Invalid stroke text parameters: {e}")

    def _draw_text_gradient(self, text: str, x: str, y: str,
                            size: str,
                            color1: str, color2: str,
                            font: str = None) -> str:
        """
        Draw text filled with vertical linear gradient.
        """

        self._ensure_canvas()

        try:
            x_pos = self._parse_position(x, 'x')
            y_pos = self._parse_position(y, 'y')
            font_size = self._parse_num(size)

            font_obj = self._get_font(font_size, font)

            # Measure text
            bbox = self.draw.textbbox((0, 0), text, font=font_obj)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]

            # Create gradient image
            gradient = Image.new("RGBA", (width, height))
            top_color = self._get_color(color1)
            bottom_color = self._get_color(color2)

            for i in range(height):
                ratio = i / height
                r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
                g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
                b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
                ImageDraw.Draw(gradient).line([(0, i), (width, i)], fill=(r, g, b))

            # Create mask
            mask = Image.new("L", (width, height), 0)
            ImageDraw.Draw(mask).text((0, 0), text, font=font_obj, fill=255)

            # Paste gradient using mask
            self.canvas.paste(gradient, (x_pos, y_pos), mask)

            return f"Gradient text drawn at ({x_pos}, {y_pos})"
        except ValueError as e:
            raise ValueError(f"Invalid gradient text parameters: {e}")

    def _draw_text_center(self, text: str, y: str,
                          size: str, color: str,
                          font: str = None, anchor: str = "la",
                          stroke_width: str = "0", stroke_fill: str = None) -> str:
        """
        Draw text centered horizontally on canvas.
        """

        self._ensure_canvas()

        try:
            y_pos = self._parse_position(y, 'y')
            font_size = self._parse_num(size)
            sw = int(self._parse_num(stroke_width))

            font_obj = self._get_font(font_size, font)
            fill_color = self._get_color(color)
            stroke_color = self._get_color(stroke_fill) if stroke_fill else None

            bbox = self.draw.textbbox((0, 0), text, font=font_obj)
            text_width = bbox[2] - bbox[0]

            canvas_width = self.canvas.width
            x_pos = (canvas_width - text_width) // 2

            self.draw.text(
                (x_pos, y_pos),
                text,
                font=font_obj,
                fill=fill_color,
                anchor=anchor,
                stroke_width=sw,
                stroke_fill=stroke_color
            )

            return f"Centered text drawn at y={y_pos}"
        except ValueError as e:
            raise ValueError(f"Invalid centered text parameters: {e}")

    def _draw_text_wrapped(self, text: str, x: str, y: str,
                           max_width: str, size: str, color: str,
                           font: str = None, anchor: str = "la",
                           stroke_width: str = "0", stroke_fill: str = None) -> str:
        """
        Draw wrapped text with stroke support.
        """
        self._ensure_canvas()
        
        try:
            wrapped_text = self._wrap_text(text, max_width, size, font)
            return self._draw_text(x, y, wrapped_text, color, size, font, anchor, stroke_width, stroke_fill)
        except Exception as e:
            raise ValueError(f"Failed to draw wrapped text: {e}")

    def _draw_text_mid(self, x1: str = None, y1: str = None, 
                        x2: str = None, y2: str = None, 
                        text: str = "", 
                        color: str = None, 
                        size: str = None, font: str = None, 
                        stroke_width: str = None, stroke_fill: str = None,
                        shadow_color: str = None, shadow_offset: str = "0,0",
                        glow_color: str = None, glow_radius: str = "0",
                        x: str = None, y: str = None,
                        w: str = None, h: str = None,
                        max_width: str = None, truncate_width: str = None) -> str:
        """
        Multifunctional centering function with wrap/truncate support.
        - Centers horizontally if (x1, x2) are provided.
        - Centers vertically if (y1, y2) are provided.
        - If w or h are provided, calculates x2=x+w or y2=y+h automatically.
        - Supports all standard text effects and transformations.
        """
        self._ensure_canvas()
        try:
            # Horizontal logic
            if x1 is not None and x2 is not None:
                xm = f"mid({x1},{x2})"
            elif x is not None and w is not None:
                xm = f"mid({x},{x}+{w})"
            elif x is not None:
                xm = x
            elif x1 is not None:
                xm = x1
            else:
                xm = "center"

            # Vertical logic
            if y1 is not None and y2 is not None:
                ym = f"mid({y1},{y2})"
            elif y is not None and h is not None:
                ym = f"mid({y},{y}+{h})"
            elif y is not None:
                ym = y
            elif y1 is not None:
                ym = y1
            else:
                ym = "middle"

            return self._draw_text(xm, ym, text, color, size, font, "mm", 
                                  stroke_width, stroke_fill, 
                                  shadow_color, shadow_offset, 
                                  glow_color, glow_radius,
                                  max_width, truncate_width)
        except Exception as e:
            raise ValueError(f"Failed to draw multifunctional text: {e}. Proper Syntax: $drawTextMid[x1;y1;x2;y2;text;color;size;font;...]")

    def _draw_text_in(self, x: str = None, y: str = None, w: str = None, h: str = None, 
                      text: str = "", color: str = None, 
                      size: str = None, font: str = None, 
                      stroke_width: str = None, stroke_fill: str = None,
                      shadow_color: str = None, shadow_offset: str = "0,0",
                      glow_color: str = None, glow_radius: str = "0",
                      x1: str = None, x2: str = None, y1: str = None, y2: str = None,
                      max_width: str = None, truncate_width: str = None) -> str:
        """
        Alias for _draw_text_mid but optimized for box dimensions (x, y, w, h).
        """
        return self._draw_text_mid(x1=x1, y1=y1, x2=x2, y2=y2, text=text, 
                                 color=color, size=size, font=font, 
                                 stroke_width=stroke_width, stroke_fill=stroke_fill,
                                 shadow_color=shadow_color, shadow_offset=shadow_offset,
                                 glow_color=glow_color, glow_radius=glow_radius,
                                 x=x, y=y, w=w, h=h,
                                 max_width=max_width, truncate_width=truncate_width)
        except Exception as e:
            raise ValueError(f"Failed to draw text in box: {e}. Proper Syntax: $drawTextIn[x;y;w;h;text;color;size;font;...]")

    # Note: _draw_text_center and _draw_text_wrapped are now logically covered 
    # by _draw_text and _draw_text_mid with parameters.