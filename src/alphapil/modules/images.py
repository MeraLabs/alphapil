"""
Images module - Image manipulation and rendering for AlphaPIL.

This module provides functions for drawing images on the canvas,
applying filters, and asynchronous image loading with aiohttp.
"""

import io
from typing import Union, Optional
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
import aiohttp


class ImagesMixin:
    """
    Mixin class providing image manipulation and rendering functionality.
    
    This mixin adds methods for drawing images, applying filters,
    and loading images from URLs asynchronously.
    """
    
    def _ensure_canvas_for_images(self):
        """Ensure canvas exists for image operations."""
        if not hasattr(self, 'canvas') or not self.canvas:
            raise RuntimeError("No canvas created. Call $createCanvas first.")
        
        if not hasattr(self, 'draw') or not self.draw:
            raise RuntimeError("No drawing context available. Call $createCanvas first.")
    
    def _get_image_cache(self):
        """Get or create image cache."""
        if not hasattr(self, '_image_cache'):
            self._image_cache = {}
        return self._image_cache
    
    async def _draw_image(self, x: str, y: str, image_path: str, 
                         width: str = None, height: str = None, 
                         opacity: str = "100", 
                         radius: str = None, circle: str = "false",
                         anchor: str = None) -> str:
        """
        Draw an image on the canvas (Async).
        """
        self._ensure_canvas_for_images()
        
        try:
            is_circle = str(circle).lower() in ['true', '1', 'yes', 'on']
            
            # Automatic Circle Centering: If circle=true, default anchor to mm
            if anchor is None:
                final_anchor = "mm" if is_circle else "lt"
            else:
                final_anchor = anchor

            # 2. Load image (Async)
            img = await self._load_image_async(image_path)
            
            # 3. Resize logic
            target_w = int(self._parse_num(width)) if width else None
            target_h = int(self._parse_num(height)) if height else None
            
            if target_w and target_h:
                img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            elif target_w:
                aspect = img.height / img.width
                target_h = int(target_w * aspect)
                img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            elif target_h:
                aspect = img.width / img.height
                target_w = int(target_h * aspect)
                img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            
            w, h = img.size
            radius_val = int(self._parse_num(radius)) if radius else 0
            
            # 4. Apply Anchor Offset
            ax, ay = self._get_anchor_offset(final_anchor, w, h)
            x_pos = int(self._parse_position(x, 'x') + ax)
            y_pos = int(self._parse_position(y, 'y') + ay)
            
            opacity_val = float(self._parse_num(opacity)) / 100.0
            
            # 5. Styling (Circle or Rounded)
            if is_circle:
                mask = Image.new("L", (w, h), 0)
                ImageDraw.Draw(mask).ellipse((0, 0, w, h), fill=255)
                output = Image.new("RGBA", (w, h), (0,0,0,0))
                output.paste(img, (0, 0), mask)
                img = output
            elif radius_val > 0:
                mask = Image.new("L", (w, h), 0)
                ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (w, h)], radius=radius_val, fill=255)
                output = Image.new("RGBA", (w, h), (0,0,0,0))
                output.paste(img, (0, 0), mask)
                img = output
            
            # 6. Apply opacity
            if opacity_val < 1.0:
                if img.mode != 'RGBA': img = img.convert('RGBA')
                r, g, b, a = img.split()
                a = a.point(lambda p: int(p * opacity_val))
                img = Image.merge('RGBA', (r, g, b, a))
            
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
                
            self.canvas.paste(img, (x_pos, y_pos), img)
            return f"Image drawn at ({x_pos}, {y_pos}) with anchor {final_anchor}"
            
        except Exception as e:
            raise ValueError(f"Failed to draw image: {e}. Proper Syntax: $drawImage[x;y;path_or_url;width;height;opacity;radius;circle;anchor]")

    async def _load_image_async(self, path: str) -> Image.Image:
        """Helper to load image from path or URL asynchronously."""
        cache = self._get_image_cache()
        if path in cache:
            return cache[path]
            
        if path.startswith(('http://', 'https://')):
            # Async download
            async with aiohttp.ClientSession() as session:
                async with session.get(path) as response:
                    if response.status != 200:
                        raise ValueError(f"Failed to download image: HTTP {response.status}")
                    data = await response.read()
                    img = Image.open(io.BytesIO(data))
        else:
            # Local file (sync IO, but fast enough usually)
            # In a strict async loop, utilize loop.run_in_executor for file IO if needed
            # For now, direct open is acceptable for small local files
            img = Image.open(path)
            
        # Convert to RGBA for consistency
        img = img.convert('RGBA')
        cache[path] = img
        return img
    
    # Internal helper methods for backward compatibility or direct usage
    # Note: These are no longer exposed as template commands
    
    async def _draw_image_async(self, x: str, y: str, image_url: str,
                               width: str = None, height: str = None,
                               opacity: str = "100") -> str:
        """Deprecated: Use _draw_image with URL"""
        return await self._draw_image(x, y, image_url, width, height, opacity)
        
    async def _draw_image_circle(self, url: str, x: str, y: str, size: str) -> str:
        """Deprecated: Use _draw_image with circle=True"""
        return await self._draw_image(x, y, url, size, size, circle="true")
        
    async def _draw_image_rounded(self, url: str, x: str, y: str,
                                  w: str, h: str, radius: str) -> str:
        """Deprecated: Use _draw_image with radius parameter"""
        return await self._draw_image(x, y, url, w, h, radius=radius)

    def _image_brightness(self, amount: str) -> str:
        """
        Adjust canvas brightness (0.0 to 2.0)
        """

        self._ensure_canvas_for_images()

        try:
            factor = self._parse_num(amount)
            enhancer = ImageEnhance.Brightness(self.canvas)
            self.canvas = enhancer.enhance(factor)
            self.draw = ImageDraw.Draw(self.canvas)
            return f"Brightness adjusted to {factor}"
        except Exception as e:
            raise ValueError(f"Brightness adjustment failed: {e}")

    # -------------------------------------------------

    def _image_contrast(self, amount: str) -> str:
        """
        Adjust canvas contrast.
        """

        self._ensure_canvas_for_images()

        try:
            factor = self._parse_num(amount)
            enhancer = ImageEnhance.Contrast(self.canvas)
            self.canvas = enhancer.enhance(factor)
            self.draw = ImageDraw.Draw(self.canvas)
            return f"Contrast adjusted to {factor}"
        except Exception as e:
            raise ValueError(f"Contrast adjustment failed: {e}")

    # -------------------------------------------------

    def _image_colorize(self, color: str) -> str:
        """
        Apply color tint over entire canvas or last drawn image.
        """

        self._ensure_canvas_for_images()

        try:
            tint_color = self._get_color(color)

            # Create overlay
            overlay = Image.new("RGBA", self.canvas.size, tint_color + (120,))
            tinted = Image.alpha_composite(
                self.canvas.convert("RGBA"), overlay
            )

            self.canvas = tinted
            self.draw = ImageDraw.Draw(self.canvas)

            return f"Canvas colorized with {color}"

        except Exception as e:
            raise ValueError(f"Colorize failed: {e}")

    def _image_filter(self, filter_name: str) -> str:
        """Apply a filter to the current canvas."""
        self._ensure_canvas_for_images()
        
        filters = {
            "blur": ImageFilter.BLUR,
            "contour": ImageFilter.CONTOUR,
            "detail": ImageFilter.DETAIL,
            "edge_enhance": ImageFilter.EDGE_ENHANCE,
            "edge_enhance_more": ImageFilter.EDGE_ENHANCE_MORE,
            "emboss": ImageFilter.EMBOSS,
            "find_edges": ImageFilter.FIND_EDGES,
            "sharpen": ImageFilter.SHARPEN,
            "smooth": ImageFilter.SMOOTH,
            "smooth_more": ImageFilter.SMOOTH_MORE
        }
        
        filter_name = filter_name.lower().strip()
        if filter_name in filters:
            self.canvas = self.canvas.filter(filters[filter_name])
            self.draw = ImageDraw.Draw(self.canvas)
            return f"Applied filter: {filter_name}"
        else:
            raise ValueError(f"Unsupported filter: {filter_name}")

    def clear_image_cache(self) -> str:
        """Clear the image cache."""
        if hasattr(self, '_image_cache'):
            self._image_cache.clear()
        return "Image cache cleared"

    async def _use_image_as_canvas(self, path: str, h_var: str = None, w_var: str = None,
                                   fixed_width: str = None, fixed_height: str = None) -> str:
        """
        Load an image and use it as the main canvas.
        The canvas size will match the image size exactly unless fixed dimensions are provided.
        
        Args:
            path: Path to image file or URL
            h_var: Variable name to store height
            w_var: Variable name to store width
            fixed_width: Force a specific width for the canvas
            fixed_height: Force a specific height for the canvas
            
        Returns:
            Confirmation message
        """
        try:
            # Load image (Async)
            img = await self._load_image_async(path)
            
            # Resize if fixed dimensions provided
            target_w = int(self._parse_num(fixed_width)) if fixed_width else None
            target_h = int(self._parse_num(fixed_height)) if fixed_height else None
            
            if target_w and target_h:
                img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
            elif target_w:
                aspect = img.height / img.width
                img = img.resize((target_w, int(target_w * aspect)), Image.Resampling.LANCZOS)
            elif target_h:
                aspect = img.width / img.height
                img = img.resize((int(target_h * aspect), target_h), Image.Resampling.LANCZOS)

            # Ensure RGBA for transparency support
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Set as canvas and recreate draw object
            self.canvas = img
            self.draw = ImageDraw.Draw(self.canvas)
            self.canvas_size = self.canvas.size
            
            # Store dimensions in variables if requested
            if h_var:
                self.set_variable(h_var, str(self.canvas.height))
            if w_var:
                self.set_variable(w_var, str(self.canvas.width))

            # Initialize layer state if masking mixin is present
            if hasattr(self, '_init_masking'):
                self._init_masking()
            
            return f"Canvas initialized from image: {path} ({self.canvas_size[0]}x{self.canvas_size[1]})"
            
        except Exception as e:
            raise ValueError(f"Failed to use image as canvas: {e}")