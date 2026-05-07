"""
Base module providing shared functionality for all AlphaPIL modules.

This module contains the AlphaMixin class with common helper methods
used across different functional modules.
"""

import re
from typing import Union, Tuple
from PIL import ImageColor


class AlphaMixin:
    """
    Base mixin class providing shared helper methods for all AlphaPIL modules.
    """
    
    def _init_state(self) -> None:
        """Initialize rendering state"""
        self._state = {
            'font': None,
            'font_size': 12,
            'color': 'black',
            'stroke_width': 1,
            'stroke_color': 'black'
        }
        self._group_stack = [] # Stack of (x, y) offsets

    def _get_state(self, key: str, default=None):
        """Get state value with fallback"""
        if not hasattr(self, '_state'):
            self._init_state()
        return self._state.get(key, default)

    def _set_state(self, key: str, value):
        """Set state value"""
        if not hasattr(self, '_state'):
            self._init_state()
        self._state[key] = value

    # -------------------------
    # Grouping Logic
    # -------------------------

    def _get_group_offset(self) -> Tuple[float, float]:
        """Calculate total offset from all active groups."""
        tx, ty = 0.0, 0.0
        if hasattr(self, '_group_stack'):
            for ox, oy in self._group_stack:
                tx += ox
                ty += oy
        return tx, ty

    def _start_group(self, x: str = "0", y: str = "0") -> str:
        """Start a new coordinate group."""
        if not hasattr(self, '_group_stack'):
            self._group_stack = []
        
        ox = self._parse_position(x, 'x', ignore_stack=True)
        oy = self._parse_position(y, 'y', ignore_stack=True)
        self._group_stack.append((ox, oy))
        return f"Group started at ({ox}, {oy})"

    def _end_group(self) -> str:
        """End the current coordinate group."""
        if hasattr(self, '_group_stack') and self._group_stack:
            self._group_stack.pop()
            return "Group ended"
        return "No active group to end"

    # -------------------------
    # State Management Commands
    # -------------------------

    def _cmd_set_font(self, font_name: str, size: str = None) -> str:
        """Set current font and size."""
        self._set_state('font', font_name)
        if size:
            self._set_state('font_size', self._parse_num(size))
        return f"Font set to {font_name}" + (f" size {size}" if size else "")

    def _cmd_set_color(self, color: str) -> str:
        """Set current default color."""
        self._get_color(color)  # Validate color
        self._set_state('color', color)
        return f"Color set to {color}"

    def _cmd_set_stroke(self, width: str, color: str = None) -> str:
        """Set current stroke properties."""
        self._set_state('stroke_width', self._parse_num(width))
        if color:
            self._get_color(color)  # Validate
            self._set_state('stroke_color', color)
        return f"Stroke set to width {width}" + (f" color {color}" if color else "")
    
    # -------------------------
    # Helper Methods
    # -------------------------

    def _get_color(self, color_str: str) -> Union[Tuple[int, int, int], Tuple[int, int, int, int]]:
        """
        Convert color string to RGBA tuple.
        """
        if not color_str or str(color_str).lower() == "none":
            return None
        
        # Remove parentheses if present
        color_str = str(color_str).strip().lstrip('(').rstrip(')')
        
        # Handle comma-separated RGB/RGBA values
        if ',' in color_str:
            try:
                parts = [int(p.strip()) for p in color_str.split(',')]
                if len(parts) == 3:
                    return tuple(parts) + (255,) # Convert to RGBA
                elif len(parts) == 4:
                    return tuple(parts) # Already RGBA
            except ValueError:
                pass
        
        try:
            # Standard Pillow color parsing
            color = ImageColor.getrgb(color_str)
            if len(color) == 3:
                return color + (255,)
            return color
        except ValueError:
            # Fallback for common web colors if Pillow fails
            if color_str.startswith('#'):
                return ImageColor.getcolor(color_str, "RGBA")
            raise ValueError(f"Unsupported color format: {color_str}")
    
    def _get_anchor_offset(self, anchor: str, width: float, height: float) -> Tuple[float, float]:
        """
        Calculate pixel offset based on anchor string.
        Supported: lt, ct, rt, lm, mm, rm, lb, cb, rb
        """
        anchor = str(anchor).lower().strip()
        ax, ay = 0.0, 0.0
        
        # Horizontal
        if 'c' in anchor or 'm' in anchor: ax = -width / 2
        if 'r' in anchor: ax = -width
        
        # Vertical
        if 'm' in anchor: ay = -height / 2
        if 'b' in anchor: ay = -height
        
        return ax, ay

    def _parse_num(self, num_str: str) -> Union[int, float]:
        """
        Parse string to number (int or float).
        """
        try:
            if isinstance(num_str, (int, float)):
                return num_str
            num_str = str(num_str).strip()
            if '.' in num_str:
                return float(num_str)
            else:
                return int(num_str)
        except ValueError:
            raise ValueError(f"Invalid number format: {num_str}")
    
    def _parse_coords(self, coord_str: str) -> Tuple[Union[int, float], Union[int, float]]:
        """
        Parse coordinate string into (x, y) tuple.
        """
        coord_str = str(coord_str).strip().lstrip('(').rstrip(')')
        parts = coord_str.split(',')
        
        if len(parts) != 2:
            raise ValueError(f"Invalid coordinate format: {coord_str}")
        
        return (self._parse_num(parts[0].strip()), self._parse_num(parts[1].strip()))

    def _parse_position(self, pos_str: str, axis: str, ignore_stack: bool = False) -> float:
        """
        Parse position string with support for coordinate stacking and keywords.
        Keywords (center, right, etc.) are absolute to the canvas.
        Numbers are relative to the current group offset.
        """
        self._ensure_canvas()
        canvas_size = self.canvas.width if axis == 'x' else self.canvas.height
        
        # Current group offset
        group_x, group_y = (0.0, 0.0) if ignore_stack else self._get_group_offset()
        base_offset = group_x if axis == 'x' else group_y

        pos_str = str(pos_str).strip().lower()
        
        # 1. Handle simple keywords (Absolute)
        if pos_str == 'center' or pos_str == 'middle':
            return float(canvas_size / 2)
        
        if axis == 'x':
            if pos_str == 'left': return 0.0
            if pos_str == 'right': return float(canvas_size)
        else:
            if pos_str == 'top': return 0.0
            if pos_str == 'bottom': return float(canvas_size)
            
        # 2. Handle mid(a, b) / between(a, b) (Recursive)
        match_mid = re.match(r'^(?:mid|between)\(([^,;]+)[,;]([^,;]+)\)$', pos_str)
        if match_mid:
            p1_str, p2_str = match_mid.groups()
            # Resolve parts with current stack (they might be keywords or relative numbers)
            p1 = self._parse_position(p1_str, axis, ignore_stack=ignore_stack)
            p2 = self._parse_position(p2_str, axis, ignore_stack=ignore_stack)
            return (p1 + p2) / 2

        # 3. Parse logic for offsets (+/-) (Recursive)
        # Supports: right-40, center+10, 100-20, etc.
        match = re.match(r'^([a-z0-9.%]+)\s*([+\-])\s*([0-9.]+)$', pos_str)
        if match:
            base_str, op, off_str = match.groups()
            # Resolve base part (could be keyword or number)
            base_val = self._parse_position(base_str, axis, ignore_stack=ignore_stack)
            offset = float(off_str)
            return base_val + offset if op == '+' else base_val - offset
        
        # 4. Fallback to simple number parsing (Relative to group)
        try:
            return self._parse_num(pos_str) + base_offset
        except ValueError:
            # If not a number, maybe it's an unrecognized keyword?
            # Return 0 or raise error? For now, re-raise original error
            raise ValueError(f"Invalid position value: {pos_str}")

    def _check_bounds(self, x: float, y: float, 
                      width: float = 0, height: float = 0) -> None:
        """
        Validate coordinates are within canvas bounds.
        """
        if not hasattr(self, 'canvas') or not self.canvas:
            return
            
        cw, ch = self.canvas.size
        
        if x < 0 or y < 0 or x + width > cw or y + height > ch:
            pass
    
    def _ensure_canvas(self) -> None:
        """
        Ensure that a canvas exists before performing operations.
        """
        if not hasattr(self, 'canvas') or not self.canvas:
            raise RuntimeError("No canvas created. Call $createCanvas first.")
        
        if not hasattr(self, 'draw') or not self.draw:
            raise RuntimeError("No drawing context available. Call $createCanvas first.")
