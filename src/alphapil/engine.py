"""
CanvasEngine - High-level canvas operations for AlphaPIL.

This module provides the CanvasEngine class that inherits from CanvasInterpreter
and all module mixins to provide comprehensive image generation capabilities.
"""

import io
from typing import Tuple, Union, Optional
from PIL import Image, ImageDraw, ImageFont
from .interpreter import CanvasInterpreter
from .modules import AlphaMixin, ShapesMixin, TextMixin, ImagesMixin, UtilsMixin, MaskingMixin, EffectsMixin, ChartsMixin


class CanvasEngine(CanvasInterpreter, ShapesMixin, TextMixin, ImagesMixin, UtilsMixin, MaskingMixin, EffectsMixin, ChartsMixin, AlphaMixin):
    """
    High-level canvas engine that extends CanvasInterpreter with Pillow-based
    image generation capabilities and all module mixins.
    """
    
    def __init__(self):
        """Initialize the canvas engine and register built-in functions."""
        # Initialize all parent classes properly
        CanvasInterpreter.__init__(self)
        AlphaMixin.__init__(self)
        ShapesMixin.__init__(self)
        TextMixin.__init__(self)
        ImagesMixin.__init__(self)
        UtilsMixin.__init__(self)
        MaskingMixin.__init__(self)
        EffectsMixin.__init__(self)
        ChartsMixin.__init__(self)
        
        # Initialize mixin states
        self._init_state()
        self._init_text()
        
        # Initialize canvas-specific attributes
        self.canvas: Optional[Image.Image] = None
        self.draw: Optional[ImageDraw.Draw] = None
        self.canvas_size: Tuple[int, int] = (0, 0)
        
        # Register all built-in functions from modules
        self._register_builtin_functions()
    
    async def render_template(self, template_text: str, data: dict = None) -> bytes:
        """
        Render a template with optional data injection (Async).
        
        Args:
            template_text: Template content as string
            data: Optional dictionary of variables to set
            
        Returns:
            Canvas image as bytes
            
        Raises:
            RuntimeError: If template rendering fails
        """
        try:
            # Reset engine state
            self.reset()
            
            # Inject data if provided
            if data:
                for key, value in data.items():
                    self.set_variable(key, str(value))
            
            # Clean up template: remove comments and handle line joins if any
            # Note: The interpreter's parse method will handle multiple commands 
            # sequentially if we just pass the whole string, as long as it finds 
            # them one by one.
            
            # Pre-process: remove comments
            lines = template_text.split('\n')
            clean_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    clean_lines.append(line)
            
            clean_template = ' '.join(clean_lines)
            
            # Parse and execute the entire template
            await self.parse(clean_template)
            
            # Return canvas as bytes
            return self.get_canvas_bytes()
            
        except Exception as e:
            raise RuntimeError(f"Template rendering failed: {e}")

    def get_bytes(self, format: str = "PNG") -> bytes:
        """Alias for get_canvas_bytes"""
        return self.get_canvas_bytes(format)

    async def render(self, template_text: str, data: dict = None) -> bytes:
        """Alias for render_template"""
        return await self.render_template(template_text, data)
    
    async def render_template_file(self, template_path: str, data: dict = None) -> bytes:
        """
        Render a template from file with optional data injection (Async).
        
        Args:
            template_path: Path to template file
            data: Optional dictionary of variables to set
            
        Returns:
            Canvas image as bytes
            
        Raises:
            FileNotFoundError: If template file doesn't exist
            RuntimeError: If template rendering fails
        """
        try:
            # Use async file reading if possible, but standard open is fine for text files
            # or could use aiofiles if dependency added. For now sync read is okay.
            with open(template_path, 'r', encoding='utf-8') as f:
                template_text = f.read()
            return await self.render_template(template_text, data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {template_path}")
        except Exception as e:
            raise RuntimeError(f"Template rendering failed: {e}")
    
    def _register_builtin_functions(self) -> None:
        """Register all built-in canvas manipulation functions from all modules."""
        # Core canvas functions
        self.register_function("createCanvas", self._create_canvas)
        self.register_function("save", self._save_canvas)
        self.register_function("setVar", self._set_var)
        self.register_function("getVar", self._get_var)
        self.register_function("getBytes", self.get_bytes)
        self.register_function("function", self._define_function)
        self.register_function("getErrors", self._get_errors)
        
        # Shape functions from ShapesMixin
        self.register_function("drawRect", self._draw_rect)
        self.register_function("drawCircle", self._draw_circle)
        self.register_function("drawRoundedRect", self._draw_rounded_rect)
        self.register_function("drawLine", self._draw_line)
        self.register_function("drawPolygon", self._draw_polygon)
        self.register_function("drawStar", self._draw_star)
        self.register_function("drawTriangle", self._draw_triangle)
        self.register_function("drawArc", self._draw_arc)
        
        # Text functions from TextMixin
        self.register_function("drawText", self._draw_text)
        self.register_function("text", self._draw_text) # Alias
        self.register_function("drawTextMid", self._draw_text_mid)
        self.register_function("drawTextIn", self._draw_text_in)
        self.register_function("toUpper", self._to_upper)
        self.register_function("toLower", self._to_lower)
        self.register_function("toTitle", self._to_title)
        self.register_function("measureText", self._measure_text)
        self.register_function("wrapText", self._wrap_text)
        self.register_function("autoSizeText", self._auto_size_text)
        self.register_function("truncateText", self._truncate_text)
        
        # Image functions from ImagesMixin
        self.register_function("drawImage", self._draw_image)
        self.register_function("useImageAsCanvas", self._use_image_as_canvas)
        self.register_function("imageFilter", self._image_filter)
        self.register_function("clearImageCache", self.clear_image_cache)
        self.register_function("drawPattern", self._draw_pattern)
        self.register_function("rotate", self._rotate_canvas)
        self.register_function("rotateCanvas", self._rotate_canvas)
        self.register_function("rotateLayer", self._rotate_canvas)
        self.register_function("adjustColor", self._adjust_color)
        
        # Utility functions from UtilsMixin
        self.register_function("math", self._math)
        self.register_function("if", self._if)
        self.register_function("random", self._random)
        self.register_function("getHex", self._get_hex)
        self.register_function("replace", self._replace)
        self.register_function("length", self._length)
        self.register_function("substring", self._substring)
        self.register_function("join", self._join)
        self.register_function("split", self._split)

        # Gradient & Effects functions
        self.register_function("drawLinearGradient", self._draw_linear_gradient)
        self.register_function("drawRadialGradient", self._draw_radial_gradient)
        self.register_function("blur", self._blur_region)

        # Chart functions from ChartsMixin
        self.register_function("drawBarChart", self._draw_bar_chart)
        self.register_function("drawLineChart", self._draw_line_chart)
        self.register_function("drawProgressBar", self._draw_progress_bar)

        # Masking functions from MaskingMixin
        self.register_function("createLayer", self._create_layer)
        self.register_function("switchLayer", self._switch_layer)
        self.register_function("mergeLayer", self._merge_layer)
        self.register_function("applyMask", self._apply_mask)

        # State management commands
        self.register_function("setFont", self._cmd_set_font)
        self.register_function("loadFont", self._load_font)
        self.register_function("getSystemFonts", self._get_system_fonts)
        self.register_function("setColor", self._cmd_set_color)
        self.register_function("setStroke", self._cmd_set_stroke)

        # Grouping commands
        self.register_function("startGroup", self._start_group)
        self.register_function("endGroup", self._end_group)
        self.register_function("startClip", self._start_clip)
        self.register_function("endClip", self._end_clip)
        self.register_function("startContainer", self._start_container)
        self.register_function("endContainer", self._end_container)
    
    def _create_canvas(self, width: str, height: str, color: str = "white", aa: str = "1", strict: str = "true", scale: str = "1") -> str:
        """
        Create a new canvas with optional Anti-Aliasing (aa), scale factor, and strict mode.
        
        Args:
            scale: Output resolution multiplier. scale=2 produces a 2x image for Retina/HiDPI.
                   This is independent of AA — use aa for edge smoothing, scale for output size.
        """
        try:
            # Parse base dimensions
            base_w = int(self._parse_num(width))
            base_h = int(self._parse_num(height))
            aa_factor = int(self._parse_num(aa))
            scale_factor = max(1, int(self._parse_num(scale)))
            is_strict = str(strict).lower() in ['true', '1', 'yes', 'on']
            
            # Set state
            self._set_state('aa', aa_factor)
            self._set_state('scale', scale_factor)
            self._set_state('strict', is_strict)
            self.strict_mode = is_strict
            
            # Output size = base * scale (what the user actually gets)
            # Internal size = base * scale * aa (for smooth rendering)
            output_w = base_w * scale_factor
            output_h = base_h * scale_factor
            w = output_w * aa_factor
            h = output_h * aa_factor
            
            self.canvas_size = (output_w, output_h)  # Final output size
            
            # Parse color
            bg_color = self._get_color(color) or (255, 255, 255, 255)
            
            self.canvas = Image.new("RGBA", (w, h), bg_color)
            self.draw = ImageDraw.Draw(self.canvas)
            
            parts = [f"Canvas created: {base_w}x{base_h}"]
            if scale_factor > 1:
                parts.append(f"scale={scale_factor} (output: {output_w}x{output_h})")
            if aa_factor > 1:
                parts.append(f"AA={aa_factor}")
            return " | ".join(parts)
        except ValueError as e:
            raise ValueError(f"{e}\nProper Syntax: $createCanvas[width;height;color;aa;strict;scale]")
    
    def _set_var(self, name: str, value: str) -> str:
        """
        Set a variable value.
        """
        try:
            self.set_variable(name, value)
            return f"Variable {name} set to {value}"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $setVar[name;value]")
    
    def _get_var(self, name: str, default: str = "") -> str:
        """
        Get a variable value.
        """
        return str(self.variables.get(name, default))
    
    def _save_canvas(self, filename: str = "output.png") -> str:
        """
        Save the current canvas with Lanczos downscaling if AA is enabled,
        post-downscale sharpening for crispness, and DPI metadata.
        """
        if not self.canvas:
            raise RuntimeError("No canvas to save. Call $createCanvas first.")
        
        try:
            img = self.canvas
            aa_factor = self._get_aa()
            scale_factor = int(self._get_state('scale', 1))
            
            # Downscale if AA was used
            if aa_factor > 1:
                img = img.resize(self.canvas_size, Image.Resampling.LANCZOS)
            
            # Post-downscale sharpening to restore crispness lost during resize
            if aa_factor > 1 or scale_factor > 1:
                from PIL import ImageFilter
                img = img.filter(ImageFilter.UnsharpMask(
                    radius=1.0, percent=60, threshold=2
                ))
                
            # Set high quality parameters for various formats
            # Embed DPI metadata scaled for output resolution
            dpi = 72 * scale_factor
            save_params = {"optimize": True, "dpi": (dpi, dpi)}
            if filename.lower().endswith(('.jpg', '.jpeg')):
                save_params.update({"quality": 100, "subsampling": 0})
            
            img.save(filename, **save_params)
            return f"Canvas saved as {filename}"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $save[filename]")
    
    def get_canvas_bytes(self, format: str = "PNG") -> bytes:
        """
        Get the canvas bytes with Lanczos downscaling if AA is enabled,
        post-downscale sharpening for crispness, and DPI metadata.
        """
        if not self.canvas:
            raise RuntimeError("No canvas available. Call $createCanvas first.")
        
        try:
            img = self.canvas
            aa_factor = self._get_aa()
            scale_factor = int(self._get_state('scale', 1))
            
            # Downscale if AA was used
            if aa_factor > 1:
                img = img.resize(self.canvas_size, Image.Resampling.LANCZOS)
            
            # Post-downscale sharpening to restore crispness lost during resize
            if aa_factor > 1 or scale_factor > 1:
                from PIL import ImageFilter
                img = img.filter(ImageFilter.UnsharpMask(
                    radius=1.0, percent=60, threshold=2
                ))
                
            img_bytes = io.BytesIO()
            
            # Set high quality parameters with DPI metadata
            dpi = 72 * scale_factor
            save_params = {"format": format, "optimize": True, "dpi": (dpi, dpi)}
            if format.upper() in ["JPEG", "JPG"]:
                save_params.update({"quality": 100, "subsampling": 0})
                
            img.save(img_bytes, **save_params)
            img_bytes.seek(0)
            return img_bytes.getvalue()
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $getBytes[format]")
    
    def reset(self) -> None:
        """Reset the canvas, drawing context, and state."""
        self.canvas = None
        self.draw = None
        self.canvas_size = (0, 0)
        self._init_state()
        self._init_text()
        if hasattr(self, '_image_cache'):
            self._image_cache.clear()
            
    # State management is now handled via AlphaMixin _cmd_* methods
