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
        self._group_stack = [] # Stack of (x, y) offsets

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

    def _parse_position(self, pos_str: str, axis: str, ignore_stack: bool = False) -> float:
        """
        Parse position string with support for coordinate stacking.
        """
        self._ensure_canvas()
        canvas_size = self.canvas.width if axis == 'x' else self.canvas.height
        
        # Add group offset if not ignored
        group_x, group_y = (0.0, 0.0) if ignore_stack else self._get_group_offset()
        base_offset = group_x if axis == 'x' else group_y

        pos_str = str(pos_str).strip().lower()
        
        # Handle simple keywords
        if pos_str == 'center' or pos_str == 'middle':
            return (canvas_size / 2) + base_offset
        
        if axis == 'x':
            if pos_str == 'left': return 0 + base_offset
            if pos_str == 'right': return canvas_size + base_offset
        else:
            if pos_str == 'top': return 0 + base_offset
            if pos_str == 'bottom': return canvas_size + base_offset
            
        # ... (rest of parsing logic) ...
        match_mid = re.match(r'^(?:mid|between)\(([^,;]+)[,;]([^,;]+)\)$', pos_str)
        if match_mid:
            p1_str, p2_str = match_mid.groups()
            p1 = self._parse_position(p1_str, axis, ignore_stack=True)
            p2 = self._parse_position(p2_str, axis, ignore_stack=True)
            return ((p1 + p2) / 2) + base_offset

        # Parse logic for offsets (+/-)
        match = re.match(r'^([a-z0-9.%]+)\s*([+\-])\s*([0-9.]+)$', pos_str)
        if match:
            base_str, op, off_str = match.groups()
            # Resolve base relative to canvas (ignore stack for base parts)
            base_val = self._parse_position(base_str, axis, ignore_stack=True)
            offset = float(off_str)
            final_val = base_val + offset if op == '+' else base_val - offset
            return final_val + base_offset
        
        # Fallback to simple number parsing
        return self._parse_num(pos_str) + base_offset

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
