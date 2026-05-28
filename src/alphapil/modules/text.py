"""
Text module - Text rendering and manipulation for AlphaPIL.

This module provides functions for drawing text on the canvas and
performing text transformations like case conversion.
"""

import io
import aiohttp
import os
import platform
import time
from typing import Union, Dict, Optional, List, Tuple
from PIL import ImageDraw, ImageFont, ImageFilter, Image


# Global caches for shared memory across all CanvasEngine instances
_GLOBAL_FONT_CACHE = {}      # alias -> font_bytes
_GLOBAL_FONT_ALIASES = {}    # alias -> path
_GLOBAL_SYSTEM_FONTS = {}    # name_lower -> font_path
_GLOBAL_FONT_OBJ_CACHE = {}  # (font_path_or_alias, font_size, variation) -> ImageFont object


from .base import AlphaMixin


class TextMixin(AlphaMixin):
    """
    Mixin class providing text rendering and manipulation functionality.
    """
    
    def _init_text(self):
        """Initialize text state."""
        pass

    async def _load_font(self, path: str, alias: str) -> str:
        """
        Register a font file path or URL to an alias.
        """
        if path.startswith(('http://', 'https://')):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(path) as response:
                        if response.status != 200:
                            raise ValueError(f"Failed to download font: HTTP {response.status}")
                        font_data = await response.read()
                        _GLOBAL_FONT_CACHE[alias] = font_data
                        _GLOBAL_FONT_ALIASES[alias] = path # Store path as reference
                return f"Remote font '{path}' loaded and cached as alias '{alias}'"
            except Exception as e:
                raise RuntimeError(f"{e}\nProper Syntax: $loadFont[font_path;alias]")
        else:
            _GLOBAL_FONT_ALIASES[alias] = path
            return f"Local font alias '{alias}' registered for {path}"

    def _discover_system_fonts(self) -> None:
        """Scan system directories for fonts once and cache their paths."""
        if _GLOBAL_SYSTEM_FONTS:
            return

        system = platform.system()
        paths = []

        if system == "Windows":
            paths = [os.path.join(os.environ.get('WINDIR', 'C:\\Windows'), 'Fonts')]
        elif system == "Darwin": # macOS
            paths = ['/Library/Fonts', '/System/Library/Fonts', os.path.expanduser('~/Library/Fonts')]
        else: # Linux
            paths = ['/usr/share/fonts', '/usr/local/share/fonts', os.path.expanduser('~/.fonts'), os.path.expanduser('~/.local/share/fonts')]

        for p in paths:
            if not os.path.exists(p): continue
            for root, _, files in os.walk(p):
                for f in files:
                    if f.lower().endswith(('.ttf', '.otf')):
                        # Store both "Arial" and "Arial.ttf" as keys
                        name = os.path.splitext(f)[0].lower()
                        full_path = os.path.join(root, f)
                        _GLOBAL_SYSTEM_FONTS[name] = full_path
                        _GLOBAL_SYSTEM_FONTS[f.lower()] = full_path

    def _get_system_fonts(self) -> str:
        """Return a semicolon-separated list of all discovered system font names."""
        self._discover_system_fonts()
        # Filter out the .ttf entries to just show clean names
        names = sorted(list(set([k for k in _GLOBAL_SYSTEM_FONTS.keys() if not k.endswith(('.ttf', '.otf'))])))
        return "; ".join(names)

    def _apply_font_variation(self, font: ImageFont.FreeTypeFont, variation: str) -> None:
        if not variation or not hasattr(font, 'set_variation_by_name'):
            return
        import re
        try:
            # Check if it looks like axes key-value pairs (e.g. "wght=700,wdth=100")
            if '=' in variation or ':' in variation:
                axes = {}
                parts = re.split(r'[;,]', variation)
                for part in parts:
                    if '=' in part:
                        k, v = part.split('=', 1)
                    elif ':' in part:
                        k, v = part.split(':', 1)
                    else:
                        continue
                    axes[k.strip()] = float(self._parse_num(v.strip()))
                font.set_variation_by_axes(axes)
            else:
                # Predefined name (e.g., 'Regular', 'Bold')
                font.set_variation_by_name(variation)
        except Exception as e:
            self.errors.append(f"Failed to apply font variation '{variation}': {e}")

    def _get_font(self, size: Union[str, int], font_path: str = None, variation: str = None) -> ImageFont.ImageFont:
        """
        Get a font object. Supports aliases, system names, direct paths, and variable font variations.
        """
        font_size = int(self._s(self._parse_num(size)))
        variation = variation or self._get_state('font_variation', None)
        
        # Resolve registered Local aliases first to ensure cache-key consistency
        resolved_path = font_path
        if font_path and font_path in _GLOBAL_FONT_ALIASES:
            resolved_path = _GLOBAL_FONT_ALIASES[font_path]
            
        cache_key = (resolved_path, font_size, variation)
        if cache_key in _GLOBAL_FONT_OBJ_CACHE:
            return _GLOBAL_FONT_OBJ_CACHE[cache_key]
        
        font_obj = None
        
        # 1. Check cached Remote Font aliases
        if font_path and font_path in _GLOBAL_FONT_CACHE:
            font_obj = ImageFont.truetype(io.BytesIO(_GLOBAL_FONT_CACHE[font_path]), font_size)

        if not font_obj and resolved_path:
            # 2. Try as direct path
            try:
                if not resolved_path.startswith(('http://', 'https://')):
                    if os.path.exists(resolved_path):
                        font_obj = ImageFont.truetype(resolved_path, font_size)
            except: pass

            if not font_obj:
                # 3. Try as system font name (Auto-Discovery)
                self._discover_system_fonts()
                name_lower = resolved_path.lower()
                if name_lower in _GLOBAL_SYSTEM_FONTS:
                    try:
                        font_obj = ImageFont.truetype(_GLOBAL_SYSTEM_FONTS[name_lower], font_size)
                    except: pass

            if not font_obj:
                # 4. Try Pillow's internal search for standard names
                try:
                    font_obj = ImageFont.truetype(resolved_path, font_size)
                except: pass
        
        if not font_obj:
            # 5. Fallback to common fonts
            common_fonts = ["arial.ttf", "arialbd.ttf", "times.ttf", "cour.ttf", "DejaVuSans.ttf"]
            for font_name in common_fonts:
                try:
                    font_obj = ImageFont.truetype(font_name, font_size)
                    break
                except: continue
        
        if not font_obj:
            # 6. Ultimate Fallback
            font_obj = ImageFont.load_default()
            
        # Apply variable font variation if provided
        if font_obj and variation:
            self._apply_font_variation(font_obj, variation)
            
        _GLOBAL_FONT_OBJ_CACHE[cache_key] = font_obj
        return font_obj
    
    def _get_text_bbox(self, x_pos: float, y_pos: float, text: str, font_obj, anchor: str, sw: int, tracking: float) -> Tuple[float, float, float, float]:
        """
        Compute tracking-aware bounding box for text.
        """
        if tracking != 0:
            current_x = x_pos
            if anchor and 'r' in anchor:
                full_w = sum(self.draw.textlength(c, font=font_obj) for c in text) + tracking * (len(text) - 1)
                current_x -= full_w
            elif anchor and ('c' in anchor or 'm' in anchor):
                full_w = sum(self.draw.textlength(c, font=font_obj) for c in text) + tracking * (len(text) - 1)
                current_x -= full_w / 2

            min_l, min_t, max_r, max_b = None, None, None, None
            for char in text:
                # Optimize: calculate character bounding box without stroke_width (extremely fast)
                char_bbox = self.draw.textbbox((current_x, y_pos), char, font=font_obj, anchor=anchor)
                l, t, r, b = char_bbox
                if min_l is None:
                    min_l, min_t, max_r, max_b = l, t, r, b
                else:
                    min_l = min(min_l, l)
                    min_t = min(min_t, t)
                    max_r = max(max_r, r)
                    max_b = max(max_b, b)
                current_x += self.draw.textlength(char, font=font_obj) + tracking
            
            # Apply stroke expansion once at the end if active
            if sw > 0:
                return (min_l - sw, min_t - sw, max_r + sw, max_b + sw)
            return (min_l, min_t, max_r, max_b)
        else:
            return self.draw.textbbox((x_pos, y_pos), text, font=font_obj, anchor=anchor, stroke_width=sw)

    def _draw_text(self, x: str, y: str, text: str, color: str = None, 
                   size: str = None, font: str = None, anchor: str = None,
                   stroke_width: str = None, stroke_fill: str = None,
                   shadow_color: str = None, shadow_offset: str = "0,0",
                   glow_color: str = None, glow_radius: str = "0",
                   max_width: str = None, truncate_width: str = None,
                   gradient_colors: str = None,
                   line_height: str = None, letter_spacing: str = "0",
                   variation: str = None) -> str:
        """
        Draw text on the canvas with optional stroke, shadow, glow, wrapping, truncation, gradient, and variable font variation.
        Uses global state defaults (setFont, setColor, setStroke) if parameters are missing.
        """
        self._ensure_canvas()
        
        try:
            # Apply defaults from state
            color = color or self._get_state('color', 'black')
            size = size or str(self._get_state('font_size', 12))
            font = font or self._get_state('font', None)
            
            # Stroke defaults
            if stroke_width is None:
                sw = int(self._s(self._get_state('stroke_width', 0)))
            else:
                sw = int(self._s(self._parse_num(stroke_width)))
                
            if stroke_fill:
                stroke_color = self._get_color(stroke_fill)
            else:
                stroke_color = self._get_color(self._get_state('stroke_color', 'black')) if sw > 0 else None

            # 0. Apply Truncation and Wrapping first
            if truncate_width:
                tw_val = self._s(self._parse_num(truncate_width))
                text = self._truncate_text(text, str(tw_val), size, font, is_scaled=True)
            if max_width:
                mw_val = self._s(self._parse_num(max_width))
                text = self._wrap_text(text, str(mw_val), size, font, is_scaled=True)

            x_pos = self._parse_position(x, 'x')
            y_pos = self._parse_position(y, 'y')
            # Font size is already scaled inside _get_font
            gr = int(self._parse_length(glow_radius, 'x'))
            tracking = self._parse_length(letter_spacing, 'x')
            
            text_color = self._get_color(color)
            font_obj = self._get_font(size, font, variation)
            
            # Metrics for perfect alignment
            ascent, descent = font_obj.getmetrics()
            line_spacing = int(self._parse_num(line_height) * (ascent + descent)) if line_height else None

            # 1. Apply Glow Effect
            if glow_color and gr > 0:
                gc = self._get_color(glow_color)
                bbox = self._get_text_bbox(x_pos, y_pos, text, font_obj, anchor, sw, tracking)
                left, top, right, bottom = bbox
                tw, th = int(right - left), int(bottom - top)
                if tw > 0 and th > 0:
                    # Optimize glow drawing with a dynamic downscale factor (ceil(total_stroke / 8)) to keep stroke_width under 8px
                    total_stroke = sw + gr
                    ds = (total_stroke + 7) // 8
                    
                    if ds > 1:
                        # Load smaller font for downscaled drawing
                        logical_size = float(self._parse_num(size or "24"))
                        ds_font = self._get_font(str(logical_size / ds), font, variation)
                        
                        ds_gr = max(1, int(gr / ds))
                        ds_sw = max(0, int(sw / ds))
                        ds_tracking = tracking / ds
                        ds_tw = max(1, int(tw / ds))
                        ds_th = max(1, int(th / ds))
                        ds_left = left / ds
                        ds_top = top / ds
                        ds_x_pos = x_pos / ds
                        ds_y_pos = y_pos / ds
                        
                        glow_img_ds = Image.new("RGBA", (ds_tw + ds_gr*4, ds_th + ds_gr*4), (0,0,0,0))
                        glow_draw_ds = ImageDraw.Draw(glow_img_ds)
                        
                        if tracking != 0:
                            current_x = ds_x_pos - ds_left + ds_gr*2
                            if anchor and 'r' in anchor:
                                full_w = sum(self.draw.textlength(c, font=ds_font) for c in text) + ds_tracking * (len(text) - 1)
                                current_x -= full_w
                            elif anchor and ('c' in anchor or 'm' in anchor):
                                full_w = sum(self.draw.textlength(c, font=ds_font) for c in text) + ds_tracking * (len(text) - 1)
                                current_x -= full_w / 2

                            for char in text:
                                glow_draw_ds.text(
                                    (current_x, ds_y_pos - ds_top + ds_gr*2),
                                    char,
                                    font=ds_font,
                                    fill=gc,
                                    stroke_width=ds_sw + ds_gr,
                                    stroke_fill=gc,
                                    anchor=anchor
                                )
                                current_x += self.draw.textlength(char, font=ds_font) + ds_tracking
                        else:
                            glow_draw_ds.text(
                                (ds_x_pos - ds_left + ds_gr*2, ds_y_pos - ds_top + ds_gr*2),
                                text,
                                font=ds_font,
                                fill=gc,
                                stroke_width=ds_sw + ds_gr,
                                stroke_fill=gc,
                                anchor=anchor
                            )
                        
                        glow_img_ds = glow_img_ds.filter(ImageFilter.GaussianBlur(ds_gr))
                        glow_img = glow_img_ds.resize((tw + gr*4, th + gr*4), Image.Resampling.BILINEAR)
                    else:
                        glow_img = Image.new("RGBA", (tw + gr*4, th + gr*4), (0,0,0,0))
                        glow_draw = ImageDraw.Draw(glow_img)
                        if tracking != 0:
                            current_x = x_pos - left + gr*2
                            if anchor and 'r' in anchor:
                                full_w = sum(self.draw.textlength(c, font=font_obj) for c in text) + tracking * (len(text) - 1)
                                current_x -= full_w
                            elif anchor and ('c' in anchor or 'm' in anchor):
                                full_w = sum(self.draw.textlength(c, font=font_obj) for c in text) + tracking * (len(text) - 1)
                                current_x -= full_w / 2

                            for char in text:
                                glow_draw.text(
                                    (current_x, y_pos - top + gr*2),
                                    char,
                                    font=font_obj,
                                    fill=gc,
                                    stroke_width=sw+gr,
                                    stroke_fill=gc,
                                    anchor=anchor
                                )
                                current_x += self.draw.textlength(char, font=font_obj) + tracking
                        else:
                            glow_draw.text(
                                (x_pos - left + gr*2, y_pos - top + gr*2),
                                text,
                                font=font_obj,
                                fill=gc,
                                stroke_width=sw+gr,
                                stroke_fill=gc,
                                anchor=anchor
                            )
                        glow_img = glow_img.filter(ImageFilter.GaussianBlur(gr))
                    
                    self.canvas.paste(glow_img, (int(left - gr*2), int(top - gr*2)), glow_img)

            # 2. Apply Shadow Effect
            if shadow_color:
                sc = self._get_color(shadow_color)
                raw_sx, raw_sy = self._parse_coords(shadow_offset)
                sx, sy = self._s(raw_sx), self._s(raw_sy)
                if tracking != 0:
                    current_x = x_pos + sx
                    if anchor and 'r' in anchor:
                        full_w = sum(self.draw.textlength(c, font=font_obj) for c in text) + tracking * (len(text) - 1)
                        current_x -= full_w
                    elif anchor and ('c' in anchor or 'm' in anchor):
                        full_w = sum(self.draw.textlength(c, font=font_obj) for c in text) + tracking * (len(text) - 1)
                        current_x -= full_w / 2

                    for char in text:
                        self.draw.text((current_x, y_pos + sy), char, font=font_obj, fill=sc, stroke_width=sw, stroke_fill=sc, anchor=anchor)
                        current_x += self.draw.textlength(char, font=font_obj) + tracking
                else:
                    self.draw.text((x_pos + sx, y_pos + sy), text, font=font_obj, fill=sc, stroke_width=sw, stroke_fill=sc, anchor=anchor)

            # 3. Handle Gradient
            if gradient_colors:
                colors = [c.strip() for c in gradient_colors.split(',')]
                if len(colors) >= 2:
                    bbox = self._get_text_bbox(x_pos, y_pos, text, font_obj, anchor, 0, tracking)
                    left, top, right, bottom = bbox
                    tw, th = int(right - left), int(bottom - top)
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
                        mask_draw = ImageDraw.Draw(mask)
                        if tracking != 0:
                            current_x = -left + x_pos
                            if anchor and 'r' in anchor:
                                full_w = sum(self.draw.textlength(c, font=font_obj) for c in text) + tracking * (len(text) - 1)
                                current_x -= full_w
                            elif anchor and ('c' in anchor or 'm' in anchor):
                                full_w = sum(self.draw.textlength(c, font=font_obj) for c in text) + tracking * (len(text) - 1)
                                current_x -= full_w / 2

                            for char in text:
                                mask_draw.text((current_x, -top + y_pos), char, font=font_obj, fill=255, anchor=anchor)
                                current_x += mask_draw.textlength(char, font=font_obj) + tracking
                        else:
                            mask_draw.text((-left + x_pos, -top + y_pos), text, font=font_obj, fill=255, anchor=anchor)
                        self.canvas.paste(gradient, (int(left), int(top)), mask)
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
            if line_spacing: text_kwargs['spacing'] = line_spacing

            # Manual Letter Spacing (Tracking)
            if tracking != 0:
                current_x = x_pos
                # Handle anchor offset for tracking
                if anchor and 'r' in anchor:
                    # Calculate total width with tracking
                    full_w = sum(self.draw.textlength(c, font=font_obj) for c in text) + tracking * (len(text) - 1)
                    current_x -= full_w
                elif anchor and ('c' in anchor or 'm' in anchor):
                    full_w = sum(self.draw.textlength(c, font=font_obj) for c in text) + tracking * (len(text) - 1)
                    current_x -= full_w / 2

                for char in text:
                    self.draw.text((current_x, y_pos), char, **{k:v for k,v in text_kwargs.items() if k not in ['xy', 'text', 'spacing']})
                    current_x += self.draw.textlength(char, font=font_obj) + tracking
            else:
                self.draw.text(**text_kwargs)
            
            return f"Text '{text}' drawn at ({x_pos}, {y_pos})"
        except ValueError as e:
            raise ValueError(f"{e}\nProper Syntax: $drawText[x;y;text;color;size;font;anchor;stroke_width;stroke_fill;shadow_color;shadow_offset;glow_color;glow_radius;max_width;truncate_width;gradient_colors;line_height;letter_spacing;variation]")
    
    def _to_upper(self, text: str) -> str:
        """
        Convert text to uppercase.
        """
        try:
            return str(text).upper()
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $toUpper[text]")

    def _to_lower(self, text: str) -> str:
        """
        Convert text to lowercase.
        """
        try:
            return str(text).lower()
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $toLower[text]")

    def _to_title(self, text: str) -> str:
        """
        Convert text to title case.
        """
        try:
            return str(text).title()
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $toTitle[text]")
    
    def _measure_text(self, text: str, size: str = "12", font: str = None) -> str:
        """
        Measure text dimensions. Returns logical size (unscaled).
        """
        try:
            font_obj = self._get_font(size, font)
            bbox = self.draw.textbbox((0, 0), text, font=font_obj)
            
            # Width and height are scaled values from bbox
            width = (bbox[2] - bbox[0]) / self._get_aa()
            height = (bbox[3] - bbox[1]) / self._get_aa()
            
            return f"{width},{height}"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $measureText[text;size;font]")
    
    def _wrap_text(self, text: str, max_width: str, size: str = "12", font: str = None, is_scaled: bool = False) -> str:
        """
        Wrap text to fit within a maximum width.
        """
        try:
            max_w = float(max_width) if is_scaled else self._s(self._parse_num(max_width))
            font_obj = self._get_font(size, font)
            
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
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $wrapText[text;width;size;font]")

    def _auto_size_text(self, text: str, max_width: str, start_size: str = "30", 
                        min_size: str = "10", font: str = None) -> str:
        """
        Calculates the best font size to fit text within max_width.
        """
        try:
            max_w = self._s(self._parse_num(max_width))
            current_size = int(self._parse_num(start_size))
            m_size = int(self._parse_num(min_size))
            
            while current_size >= m_size:
                # _get_font will handle scaling for internal check
                font_obj = self._get_font(current_size, font)
                bbox = self.draw.textbbox((0, 0), text, font=font_obj)
                if (bbox[2] - bbox[0]) <= max_w:
                    return str(current_size)
                current_size -= 1
                
            return str(m_size)
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $autoSizeText[text;max_width;start_size;min_size;font]")

    def _truncate_text(self, text: str, max_width: str, size: str = "12", font: str = None, suffix: str = "...", is_scaled: bool = False) -> str:
        """
        Truncate text to fit within a maximum width.
        """
        try:
            max_w = float(max_width) if is_scaled else self._s(self._parse_num(max_width))
            font_obj = self._get_font(size, font)
            
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
            raise ValueError(f"{e}\nProper Syntax: $truncateText[text;width;size;font;suffix]")

    def _draw_text_mid(self, x1: str, y1: str, x2: str, y2: str, 
                        text: str, color: str = None, 
                        size: str = None, font: str = None, 
                        stroke_width: str = None, stroke_fill: str = None,
                        shadow_color: str = None, shadow_offset: str = "0,0",
                        glow_color: str = None, glow_radius: str = "0",
                        letter_spacing: str = "0", variation: str = None) -> str:
        """
        Draw text centered between two X coordinates (x1, x2) and two Y coordinates (y1, y2).
        If the text width exceeds the available width (x2 - x1), it automatically truncates the text.
        """
        self._ensure_canvas()
        try:
            x1_val = self._parse_position(x1, 'x')
            x2_val = self._parse_position(x2, 'x')
            y1_val = self._parse_position(y1, 'y')
            y2_val = self._parse_position(y2, 'y')
            
            bx1 = min(x1_val, x2_val)
            bx2 = max(x1_val, x2_val)
            by1 = min(y1_val, y2_val)
            by2 = max(y1_val, y2_val)
            
            # Midpoint
            xm_pos = (bx1 + bx2) / 2
            ym_pos = (by1 + by2) / 2
            
            # Convert to logical coordinates for _draw_text
            xm = str(xm_pos / self._s(1))
            ym = str(ym_pos / self._s(1))
            
            # Calculate maximum available width and truncate if it exceeds
            max_w = bx2 - bx1
            logical_max_w = max_w / self._s(1)
            
            return self._draw_text(x=xm, y=ym, text=text, color=color, 
                                   size=size, font=font, anchor="mm",
                                   stroke_width=stroke_width, stroke_fill=stroke_fill,
                                   shadow_color=shadow_color, shadow_offset=shadow_offset,
                                   glow_color=glow_color, glow_radius=glow_radius,
                                   truncate_width=str(logical_max_w), letter_spacing=letter_spacing,
                                   variation=variation)
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $drawTextMid[x1;y1;x2;y2;text;color;size;font;stroke_width;stroke_fill;shadow_color;shadow_offset;glow_color;glow_radius;letter_spacing;variation]")

    def _draw_text_in(self, x1: str, y1: str, x2: str, y2: str, 
                      text: str, color: str = None, 
                      size: str = None, font: str = None, 
                      stroke_width: str = None, stroke_fill: str = None,
                      shadow_color: str = None, shadow_offset: str = "0,0",
                      glow_color: str = None, glow_radius: str = "0",
                      letter_spacing: str = "0", variation: str = None) -> str:
        """
        Draw text fitted inside a bounding box (x1, y1, x2, y2).
        If the text exceeds the box dimensions, it automatically scales down the font size until it fits.
        """
        self._ensure_canvas()
        try:
            x1_val = self._parse_position(x1, 'x')
            x2_val = self._parse_position(x2, 'x')
            y1_val = self._parse_position(y1, 'y')
            y2_val = self._parse_position(y2, 'y')
            
            bx1 = min(x1_val, x2_val)
            bx2 = max(x1_val, x2_val)
            by1 = min(y1_val, y2_val)
            by2 = max(y1_val, y2_val)
            
            box_w = bx2 - bx1
            box_h = by2 - by1
            
            # Start with the requested font size
            requested_size = float(self._parse_num(size or "24"))
            
            tracking_val = self._parse_length(letter_spacing, 'x')
            sw_val = int(self._s(self._parse_num(stroke_width or "0")))
            
            # Binary search to find the perfect font size that fits the bounding box (O(log N))
            low = 2.0
            high = requested_size
            best_size = low
            
            while low <= high:
                mid = (low + high) / 2
                font_obj = self._get_font(str(mid), font, variation)
                bbox = self._get_text_bbox(0, 0, text, font_obj, None, sw_val, tracking_val)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                
                if text_w <= box_w and text_h <= box_h:
                    best_size = mid
                    low = mid + 0.5  # Try a slightly larger font size
                else:
                    high = mid - 0.5  # Need a smaller font size
                    
            current_size = best_size
                
            # Midpoint of the box
            xm_pos = (bx1 + bx2) / 2
            ym_pos = (by1 + by2) / 2
            
            xm = str(xm_pos / self._s(1))
            ym = str(ym_pos / self._s(1))
            
            return self._draw_text(x=xm, y=ym, text=text, color=color, 
                                   size=str(current_size), font=font, anchor="mm",
                                   stroke_width=stroke_width, stroke_fill=stroke_fill,
                                   shadow_color=shadow_color, shadow_offset=shadow_offset,
                                   glow_color=glow_color, glow_radius=glow_radius,
                                   letter_spacing=letter_spacing, variation=variation)
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $drawTextIn[x1;y1;x2;y2;text;color;size;font;stroke_width;stroke_fill;shadow_color;shadow_offset;glow_color;glow_radius;letter_spacing;variation]")

    # Note: _draw_text_center and _draw_text_wrapped are now logically covered 
    # by _draw_text and _draw_text_mid with parameters.