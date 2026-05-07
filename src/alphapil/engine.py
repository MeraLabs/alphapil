"""
CanvasEngine - High-level canvas operations for AlphaPIL.

This module provides the CanvasEngine class that inherits from CanvasInterpreter
and all module mixins to provide comprehensive image generation capabilities.
"""

import io
from typing import Tuple, Union, Optional
from PIL import Image, ImageDraw, ImageFont
from .interpreter import CanvasInterpreter
from .modules import AlphaMixin, ShapesMixin, TextMixin, ImagesMixin, UtilsMixin, MaskingMixin


class CanvasEngine(CanvasInterpreter, AlphaMixin, ShapesMixin, TextMixin, ImagesMixin, UtilsMixin, MaskingMixin):
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
            
            # Parse template line by line
            lines = template_text.strip().split('\n')
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                # Parse and execute the line (awaiting async parse)
                result = await self.parse(line)
            
            # Return canvas as bytes
            return self.get_canvas_bytes()
            
        except Exception as e:
            raise RuntimeError(f"Template rendering failed: {e}")
    
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
        
        # State management commands
        self.register_function("setFont", self._cmd_set_font)
        self.register_function("loadFont", self._load_font) # This is now async in TextMixin
        self.register_function("setColor", self._cmd_set_color)
        self.register_function("setStroke", self._cmd_set_stroke)
    
    def _create_canvas(self, width: str, height: str, color: str = "white") -> str:
        """
        Create a new canvas with specified dimensions and background color.
        
        Args:
            width: Canvas width as string
            height: Canvas height as string  
            color: Background color (default: "white")
            
        Returns:
            Confirmation message
        """
        try:
            w = int(width)
            h = int(height)
            self.canvas_size = (w, h)
            
            # Parse color using the helper from AlphaMixin
            bg_color = self._get_color(color) or (255, 255, 255)
            
            self.canvas = Image.new("RGB", (w, h), bg_color)
            self.draw = ImageDraw.Draw(self.canvas)
            return f"Canvas created: {w}x{h}"
        except ValueError as e:
            raise ValueError(f"Invalid canvas dimensions: {e}")
    
    def _set_var(self, name: str, value: str) -> str:
        """
        Set a variable value.
        
        Args:
            name: Variable name (without {} wrapper)
            value: Variable value
            
        Returns:
            Confirmation message
        """
        self.set_variable(name, value)
        return f"Variable {name} set to {value}"
    
    def _save_canvas(self, filename: str = "output.png") -> str:
        """
        Save the current canvas to a file with maximum quality.
        """
        if not self.canvas:
            raise RuntimeError("No canvas to save. Call $createCanvas first.")
        
        try:
            # Set high quality parameters for various formats
            save_params = {"optimize": True}
            if filename.lower().endswith(('.jpg', '.jpeg')):
                save_params.update({"quality": 100, "subsampling": 0})
            
            self.canvas.save(filename, **save_params)
            return f"Canvas saved as {filename}"
        except Exception as e:
            raise RuntimeError(f"Failed to save canvas: {e}")
    
    def get_canvas_bytes(self, format: str = "PNG") -> bytes:
        """
        Get the canvas as bytes with maximum quality.
        """
        if not self.canvas:
            raise RuntimeError("No canvas available. Call $createCanvas first.")
        
        img_bytes = io.BytesIO()
        
        # Set high quality parameters
        save_params = {"format": format, "optimize": True}
        if format.upper() in ["JPEG", "JPG"]:
            save_params.update({"quality": 100, "subsampling": 0})
            
        self.canvas.save(img_bytes, **save_params)
        img_bytes.seek(0)
        return img_bytes.getvalue()
    
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
