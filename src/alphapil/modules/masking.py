"""
Masking module - Layer management and masking for AlphaPIL.

This module provides functions for creating layers, switching drawing contexts,
merging layers, and applying image masks.
"""

from typing import Dict, Optional, Tuple, Union
from PIL import Image, ImageDraw, ImageChops

class MaskingMixin:
    """
    Mixin class providing layering and masking functionality.
    
    This mixin adds methods for creating layers, drawing on specific layers,
    merging layers onto the main canvas, and applying masks.
    """
    
    def _init_masking(self):
        """Initialize masking state."""
        self._layers: Dict[str, Image.Image] = {}
        self._current_layer_name: Optional[str] = None
        
    def _create_layer(self, name: str) -> str:
        """
        Create a new transparent layer matching canvas size.
        
        Args:
            name: Name of the layer
            
        Returns:
            Confirmation message
        """
        self._ensure_canvas_exists()
        
        if not hasattr(self, '_layers'):
            self._init_masking()
            
        width, height = self.canvas.size
        # Create transparent RGBA layer
        layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        self._layers[name] = layer
        
        # Determine target for drawing context if we switch immediately? 
        # No, user must call switch explicitly usually.
        
        return f"Layer '{name}' created"

    def _switch_layer(self, name: str) -> str:
        """
        Switch drawing operations to specified layer or main canvas.
        Pass 'main', 'canvas', or empty string to switch back to main canvas.
        
        Args:
            name: Layer name or 'main'
            
        Returns:
            Confirmation message
        """
        self._ensure_canvas_exists()
        
        if not hasattr(self, '_layers'):
            self._init_masking()
            
        name_lower = str(name).lower().strip()
        
        if name_lower in ['main', 'canvas', '']:
            self._current_layer_name = None
            self.draw = ImageDraw.Draw(self.canvas)
            return "Switched drawing to main canvas"
            
        if name not in self._layers:
            raise ValueError(f"Layer '{name}' does not exist. Create it first with $createLayer")
            
        self._current_layer_name = name
        self.draw = ImageDraw.Draw(self._layers[name])
        return f"Switched drawing to layer '{name}'"
    
    def _merge_layer(self, name: str, x: str = "0", y: str = "0", opacity: str = "100", target: str = "main") -> str:
        """
        Composite layer onto a target (main canvas by default) at position with opacity.
        
        Args:
            name: Name of layer to merge (source)
            x: X position (default 0)
            y: Y position (default 0)
            opacity: Opacity percent (0-100)
            target: Target layer name or 'main' (default 'main')
            
        Returns:
            Confirmation message
        """
        self._ensure_canvas_exists()
        
        if not hasattr(self, '_layers') or name not in self._layers:
            raise ValueError(f"Layer '{name}' does not exist")
            
        layer = self._layers[name]
        
        # Parse arguments
        target_x = int(self._parse_position(x, 'x'))
        target_y = int(self._parse_position(y, 'y'))
        try:
            opacity_val = float(self._parse_num(opacity)) / 100.0
        except:
            opacity_val = 1.0
        
        # Create copy to merge so we don't modify original layer state
        to_merge = layer.copy()
        
        # Apply opacity if needed
        if opacity_val < 1.0:
            if to_merge.mode != 'RGBA':
                to_merge = to_merge.convert('RGBA')
            
            # Multiply alpha channel by opacity
            # split() returns tuple (r, g, b, a)
            r, g, b, a = to_merge.split()
            a = a.point(lambda p: int(p * opacity_val))
            to_merge = Image.merge('RGBA', (r, g, b, a))
            
        # Determine target image
        target_name = str(target).lower().strip()
        
        if target_name in ['main', 'canvas', '']:
            target_img = self.canvas
            # Ensure main canvas is RGBA for proper blending if we have a layer
            if target_img.mode != 'RGBA':
                target_img = target_img.convert('RGBA')
                self.canvas = target_img
            target_is_main = True
        else:
            if target not in self._layers:
                raise ValueError(f"Target layer '{target}' does not exist")
            target_img = self._layers[target]
            target_is_main = False
            
        # Paste with alpha composite logic
        # Using to_merge as mask enables proper alpha blending
        if to_merge.mode == 'RGBA':
            target_img.paste(to_merge, (target_x, target_y), to_merge)
        else:
            target_img.paste(to_merge, (target_x, target_y))
        
        # Update drawing context based on new image object if needed
        if self._current_layer_name:
            # If we were drawing on a layer, stay on it (unless it was converted/replaced)
            # Actually, to be safe, always re-init draw if the target was the current target
            if not target_is_main and self._current_layer_name == target:
                self.draw = ImageDraw.Draw(self._layers[self._current_layer_name])
        elif target_is_main:
            self.draw = ImageDraw.Draw(self.canvas)
            
        return f"Merged layer '{name}' onto {'main canvas' if target_is_main else 'layer ' + target}"
        
    def _apply_mask(self, mask_path: str, x: str = "0", y: str = "0", invert: str = "false") -> str:
        """
        Apply an image as an alpha mask to the current canvas/layer.
        Darker pixels in mask = more transparent (standard alpha mask).
        
        Args:
            mask_path: Path to mask image
            x: X position
            y: Y position
            invert: "true" to invert mask
            
        Returns:
            Confirmation message
        """
        self._ensure_canvas_exists()
        
        # Load mask image
        try:
            mask_img = Image.open(mask_path).convert('L')
        except Exception as e:
            # Try as variable replacement or existing layer? 
            # For now assume path
            raise ValueError(f"Failed to load mask image: {e}")
            
        should_invert = str(invert).lower() in ['true', '1', 'yes', 'on']
        if should_invert:
            mask_img = ImageChops.invert(mask_img)
            
        # Target
        target_img = self.canvas
        if self._current_layer_name and self._current_layer_name in self._layers:
            target_img = self._layers[self._current_layer_name]
            
        if target_img.mode != 'RGBA':
            target_img = target_img.convert('RGBA')
            if not self._current_layer_name:
                self.canvas = target_img
        
        # Positioning
        target_x = int(self._parse_position(x, 'x'))
        target_y = int(self._parse_position(y, 'y'))
        
        # Create full size mask canvas
        width, height = target_img.size
        full_mask = Image.new('L', (width, height), 255) # White = opaque
        full_mask.paste(mask_img, (target_x, target_y))
        
        # Combine alpha
        current_alpha = target_img.split()[3]
        new_alpha = ImageChops.multiply(current_alpha, full_mask)
        
        target_img.putalpha(new_alpha)
        
        return f"Applied mask from {mask_path}"

    def _ensure_canvas_exists(self):
        """Helper to ensure canvas exists"""
        if not hasattr(self, 'canvas') or not self.canvas:
            raise RuntimeError("No canvas created. Call $createCanvas first.")
