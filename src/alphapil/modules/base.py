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
    
    This class contains common functionality like color parsing, number conversion,
    and relative position parsing that are used across multiple modules to avoid code duplication.
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
    
    def _get_color(self, color_str: str) -> Union[Tuple[int, int, int], Tuple[int, int, int, int]]:
        """
        Convert color string to RGB/RGBA tuple.
        
        Supports:
        - Named colors: "red", "blue", "lightgray"
        - Hex colors: "#FF0000", "#FF0000FF"
        - RGB tuples: "255,0,0" or "(255,0,0)"
        - RGBA tuples: "255,0,0,128" or "(255,0,0,128)"
        
        Args:
            color_str: Color string in various formats
            
        Returns:
            RGB or RGBA tuple
            
        Raises:
            ValueError: If color format is invalid
        """
        if not color_str or color_str.lower() == "none":
            return None
        
        # Remove parentheses if present
        color_str = color_str.strip().lstrip('(').rstrip(')')
        
        # Handle comma-separated RGB/RGBA values
        if ',' in color_str:
            try:
                parts = [int(p.strip()) for p in color_str.split(',')]
                if len(parts) == 3:
                    return tuple(parts)  # RGB
                elif len(parts) == 4:
                    return tuple(parts)  # RGBA
                else:
                    raise ValueError(f"Invalid color format: {color_str}")
            except ValueError:
                pass  # Fall through to other parsing methods
        
        # Use PIL's ImageColor for named colors and hex
        try:
            color = ImageColor.getrgb(color_str)
            # Ensure it's always RGBA for consistent drawing behavior on layers
            if len(color) == 3:
                return color + (255,)
            return color
        except ValueError:
            try:
                # Try getting RGBA directly
                return ImageColor.getcolor(color_str, "RGBA")
            except ValueError:
                raise ValueError(f"Unsupported color format: {color_str}")
    
    def _parse_num(self, num_str: str) -> Union[int, float]:
        """
        Parse string to number (int or float).
        
        Args:
            num_str: String containing numeric value
            
        Returns:
            Integer or float value
            
        Raises:
            ValueError: If string cannot be parsed as number
        """
        try:
            if '.' in num_str:
                return float(num_str)
            else:
                return int(num_str)
        except ValueError:
            raise ValueError(f"Invalid number format: {num_str}")
    
    def _parse_coords(self, coord_str: str) -> Tuple[Union[int, float], Union[int, float]]:
        """
        Parse coordinate string into (x, y) tuple.
        
        Supports formats:
        - "100,200"
        - "(100,200)"
        - "100.5,200.3"
        
        Args:
            coord_str: Coordinate string
            
        Returns:
            Tuple of (x, y) coordinates
        """
        coord_str = coord_str.strip().lstrip('(').rstrip(')')
        parts = coord_str.split(',')
        
        if len(parts) != 2:
            raise ValueError(f"Invalid coordinate format: {coord_str}")
        
        return (self._parse_num(parts[0].strip()), self._parse_num(parts[1].strip()))

    def _parse_position(self, pos_str: str, axis: str) -> float:
        """
        Parse position string supporting:
        - Absolute: "100"
        - Keywords: "center", "left", "right", "top", "bottom", "middle"
        - Offset: "center+50", "right-100"
        - Percentage: "50%", "25%"
        
        Args:
            pos_str: Position string
            axis: 'x' or 'y' to determine canvas dimension
            
        Returns:
            Absolute pixel position
        """
        self._ensure_canvas()
        canvas_size = self.canvas.width if axis == 'x' else self.canvas.height
        
        pos_str = str(pos_str).strip().lower()
        
        # Handle simple keywords
        if pos_str == 'center' or pos_str == 'middle':
            return canvas_size / 2
        
        if axis == 'x':
            if pos_str == 'left': return 0
            if pos_str == 'right': return canvas_size
        else:
            if pos_str == 'top': return 0
            if pos_str == 'bottom': return canvas_size
            
        # Handle mid(a, b) / between(a, b)
        match_mid = re.match(r'^(?:mid|between)\(([^,;]+)[,;]([^,;]+)\)$', pos_str)
        if match_mid:
            p1_str, p2_str = match_mid.groups()
            p1 = self._parse_position(p1_str, axis)
            p2 = self._parse_position(p2_str, axis)
            return (p1 + p2) / 2

        # Handle parsing of complex expressions like "center+50" or "right-100"
        base_val = 0
        offset = 0
        
        # Check for percentages
        if pos_str.endswith('%'):
            try:
                percent = float(pos_str[:-1])
                return (percent / 100) * canvas_size
            except ValueError:
                pass
                
        # Parse logic for offsets
        # Match pattern: keyword/number +/- number
        # e.g. center+50, 100-20, right-50, 50%+10
        match = re.match(r'^([a-z0-9.%]+)\s*([+\-])\s*([0-9.]+)$', pos_str)
        
        if match:
            base_str, op, off_str = match.groups()
            
            # Recurse for the base part (handles keywords and percentages)
            # Use current function recursively but safeguard against infinite recursion if needed
            # For simple keywords/percents, we can just call logic here or recursive
            
            # Simple base resolution
            if base_str in ['center', 'middle']:
                base_val = canvas_size / 2
            elif base_str == 'left' and axis == 'x': base_val = 0
            elif base_str == 'right' and axis == 'x': base_val = canvas_size
            elif base_str == 'top' and axis == 'y': base_val = 0
            elif base_str == 'bottom' and axis == 'y': base_val = canvas_size
            elif base_str.endswith('%'):
                try: 
                    base_val = (float(base_str[:-1]) / 100) * canvas_size
                except: base_val = 0
            else:
                try: base_val = float(base_str)
                except: base_val = 0
                
            offset = float(off_str)
            
            if op == '+':
                return base_val + offset
            else:
                return base_val - offset
        
        # Fallback to simple number parsing
        return self._parse_num(pos_str)

    def _check_bounds(self, x: float, y: float, 
                      width: float = 0, height: float = 0) -> None:
        """
        Validate coordinates are within canvas bounds.
        Currently just logs warning if outside (could raise error if strict mode enabled).
        """
        if not hasattr(self, 'canvas') or not self.canvas:
            return
            
        cw, ch = self.canvas.size
        
        if x < 0 or y < 0 or x + width > cw or y + height > ch:
            # For now just silent, or we could print/log a warning
            pass
    
    def _ensure_canvas(self) -> None:
        """
        Ensure that a canvas exists before performing operations.
        
        Raises:
            RuntimeError: If no canvas has been created
        """
        if not hasattr(self, 'canvas') or not self.canvas:
            raise RuntimeError("No canvas created. Call $createCanvas first.")
        
        if not hasattr(self, 'draw') or not self.draw:
            raise RuntimeError("No drawing context available. Call $createCanvas first.")
