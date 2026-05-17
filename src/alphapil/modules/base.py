"""
Base module providing shared functionality for all AlphaPIL modules.

This module contains the AlphaMixin class with common helper methods
used across different functional modules.
"""

import re
from typing import Union, Tuple, Optional, List
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
            'stroke_color': 'black',
            'aa': 1,
            'strict': True
        }
        self._group_stack = [] # Stack of (x, y) offsets
        self._container_stack = [] # Stack of (x, y, w, h)
        self._clip_stack = [] # Stack of (canvas, draw, x, y, w, h, radius)

    def _get_aa(self) -> int:
        """Get the current anti-aliasing factor."""
        return int(self._get_state('aa', 1))

    def _s(self, value: Union[int, float]) -> Union[int, float]:
        """Scale a value by the combined anti-aliasing and scale factors."""
        scale = int(self._get_state('scale', 1))
        return value * self._get_aa() * scale

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
    # Grouping & Container Logic
    # -------------------------

    def _get_group_offset(self) -> Tuple[float, float]:
        """Calculate total offset from all active groups."""
        if hasattr(self, '_group_stack') and self._group_stack:
            return self._group_stack[-1]
        return 0.0, 0.0

    def _get_container(self) -> Optional[Tuple[float, float, float, float]]:
        """Get the current active container (x, y, w, h)."""
        if hasattr(self, '_container_stack') and self._container_stack:
            return self._container_stack[-1]
        return None

    def _start_group(self, x: str = "0", y: str = "0") -> str:
        """
        Start a new coordinate group. Numbers are scaled by AA.
        """
        if not hasattr(self, '_group_stack'):
            self._group_stack = []
        
        try:
            ox = self._parse_position(x, 'x', ignore_stack=True)
            oy = self._parse_position(y, 'y', ignore_stack=True)
            
            self._group_stack.append((ox, oy))
            return f"Group started at ({ox}, {oy})"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $startGroup[x;y]")

    def _start_container(self, x: str = "0", y: str = "0", w: str = "0", h: str = "0", padding: str = "0", anchor: str = "lt") -> str:
        """
        Start a new container box. Keywords like 'center' inside this box 
        will resolve relative to its boundaries.
        """
        if not hasattr(self, '_container_stack'):
            self._container_stack = []
            
        try:
            # Width and height are scaled lengths
            cw = self._parse_length(w, 'x')
            ch = self._parse_length(h, 'y')
            pad = self._parse_length(padding, 'x')
            
            # Apply anchor offset
            ax, ay = self._get_anchor_offset(anchor, cw, ch)

            # Parse x, y as absolute positions and apply anchor
            cx = self._parse_position(x, 'x') + ax
            cy = self._parse_position(y, 'y') + ay
            
            self._container_stack.append((cx, cy, cw, ch, pad))
            return f"Container started at ({cx}, {cy}) size {cw}x{ch}" + (f" with padding {padding}" if pad > 0 else "")
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $startContainer[x;y;w;h;padding;anchor]")

    def _end_group(self) -> str:
        """End the current coordinate group."""
        if hasattr(self, '_group_stack') and self._group_stack:
            self._group_stack.pop()
            return "Group ended"
        return "No active group to end"

    def _start_clip(self, x: str, y: str, w: str, h: str, radius: str = "0") -> str:
        """
        Start a clipping region. Everything drawn after this will be clipped to the 
        specified rectangular or rounded rectangular area.
        """
        self._ensure_canvas()
        try:
            cx = self._parse_position(x, 'x')
            cy = self._parse_position(y, 'y')
            cw = self._parse_length(w, 'x')
            ch = self._parse_length(h, 'y')
            r = self._parse_length(radius, 'x')

            # Store current state
            self._clip_stack.append({
                'canvas': self.canvas,
                'draw': self.draw,
                'x': cx, 'y': cy, 'w': cw, 'h': ch, 'radius': r
            })

            # Create a new transparent layer for drawing
            # It must be the same size as the base canvas to keep coordinates consistent
            from PIL import Image, ImageDraw
            layer = Image.new("RGBA", self.canvas.size, (0, 0, 0, 0))
            self.canvas = layer
            self.draw = ImageDraw.Draw(self.canvas)

            return f"Clip started at ({cx}, {cy}) size {cw}x{ch}"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $startClip[x;y;w;h;radius]")

    def _end_clip(self) -> str:
        """End the current clipping region and composite the results."""
        if not hasattr(self, '_clip_stack') or not self._clip_stack:
            return "No active clip to end"

        clip_data = self._clip_stack.pop()
        layer_to_composite = self.canvas
        
        # Restore previous canvas/draw
        self.canvas = clip_data['canvas']
        self.draw = clip_data['draw']

        # Create mask for the clip region
        from PIL import Image, ImageDraw
        mask = Image.new("L", layer_to_composite.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        
        x, y, w, h, r = clip_data['x'], clip_data['y'], clip_data['w'], clip_data['h'], clip_data['radius']
        bbox = [(x, y), (x + w, y + h)]
        
        if r > 0:
            mask_draw.rounded_rectangle(bbox, radius=r, fill=255)
        else:
            mask_draw.rectangle(bbox, fill=255)

        # Composite the layer onto the main canvas using the mask
        from PIL import ImageChops
        r_chan, g_chan, b_chan, a_chan = layer_to_composite.split()
        new_a = ImageChops.multiply(a_chan, mask)
        layer_to_composite.putalpha(new_a)
        
        self.canvas.alpha_composite(layer_to_composite)
        
        return "Clip ended"

    def _end_container(self) -> str:
        """End the current container."""
        if hasattr(self, '_container_stack') and self._container_stack:
            self._container_stack.pop()
            return "Container ended"
        return "No active container to end"

    # -------------------------
    # State Management Commands
    # -------------------------

    def _cmd_set_font(self, font_name: str, size: str = None) -> str:
        """Set current font and size."""
        try:
            self._set_state('font', font_name)
            if size:
                self._set_state('font_size', self._parse_num(size))
            return f"Font set to {font_name}" + (f" size {size}" if size else "")
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $setFont[font_path;size]")

    def _cmd_set_color(self, color: str) -> str:
        """Set current default color."""
        try:
            self._get_color(color)  # Validate color
            self._set_state('color', color)
            return f"Color set to {color}"
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $setColor[color]")

    def _cmd_set_stroke(self, width: str, color: str = None) -> str:
        """Set current stroke properties."""
        try:
            self._set_state('stroke_width', self._parse_num(width))
            if color:
                self._get_color(color)  # Validate
                self._set_state('stroke_color', color)
            return f"Stroke set to width {width}" + (f" color {color}" if color else "")
        except Exception as e:
            raise ValueError(f"{e}\nProper Syntax: $setStroke[width;color]")
    
    # -------------------------
    # Helper Methods
    # -------------------------

    def _get_color(self, color_str: str) -> Union[Tuple[int, int, int], Tuple[int, int, int, int]]:
        """
        Convert color string to RGBA tuple.
        Supports:
        - Named: 'white', 'red'
        - Hex: '#ffffff', '#ff0000'
        - RGB/RGBA: '255,255,255', '255,0,0,128'
        - Shorthand: 'white/20', '#ff0000/50', 'white,10'
        """
        if not color_str or str(color_str).lower() == "none":
            return None
        
        # Remove parentheses if present
        color_str = str(color_str).strip().lstrip('(').rstrip(')')
        
        # Handle alpha shorthand: 'color/alpha' or 'color,alpha' (if not 4-part RGBA)
        alpha_override = None
        
        # Detect separators for alpha override
        sep = None
        if '/' in color_str and not color_str.startswith(('http://', 'https://')):
            sep = '/'
        elif ',' in color_str and color_str.count(',') == 1:
            # Only treat single comma as alpha override (e.g. "white,50")
            # If 2 or 3 commas, it's RGB or RGBA.
            sep = ','

        if sep:
            parts = color_str.rsplit(sep, 1)
            if len(parts) == 2:
                try:
                    # Attempt to parse second part as alpha (0-100 or 0-255)
                    a_str = parts[1].strip()
                    a_val = float(a_str)
                    if a_val <= 1.0:
                        alpha_override = int(a_val * 255)
                    elif a_val <= 100.0:
                        alpha_override = int((a_val / 100.0) * 255)
                    else:
                        alpha_override = int(min(a_val, 255))
                    
                    # If valid alpha found, update color_str to the base color
                    color_str = parts[0].strip()
                except ValueError:
                    pass

        # Handle explicit comma-separated RGB/RGBA values (e.g. "255,0,0")
        if ',' in color_str and color_str.count(',') >= 2:
            try:
                parts = [int(p.strip()) for p in color_str.split(',')]
                if len(parts) == 3:
                    color = tuple(parts) + (255,)
                elif len(parts) == 4:
                    color = tuple(parts)
                else:
                    raise ValueError
                
                if alpha_override is not None:
                    color = color[:3] + (alpha_override,)
                return color
            except ValueError:
                pass
        
        try:
            # Standard Pillow color parsing
            color = ImageColor.getrgb(color_str)
            if len(color) == 3:
                color = color + (255,)
            
            if alpha_override is not None:
                color = color[:3] + (alpha_override,)
            return color
        except ValueError:
            # Fallback for common web colors if Pillow fails
            if color_str.startswith('#'):
                try:
                    color = ImageColor.getcolor(color_str, "RGBA")
                    if alpha_override is not None:
                        color = color[:3] + (alpha_override,)
                    return color
                except: pass
            raise ValueError(f"Unknown color: {color_str}")
    
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
            raise ValueError(f"Invalid number: {num_str}")
    
    def _parse_coords(self, coord_str: str) -> Tuple[Union[int, float], Union[int, float]]:
        """
        Parse coordinate string into (x, y) tuple.
        """
        coord_str = str(coord_str).strip().lstrip('(').rstrip(')')
        parts = coord_str.split(',')
        
        if len(parts) != 2:
            raise ValueError(f"Invalid coordinates: {coord_str}")
        
        return (self._parse_num(parts[0].strip()), self._parse_num(parts[1].strip()))

    def _get_context_info(self, axis: str) -> Tuple[float, float]:
        """
        Get the current coordinate context's origin and size.
        """
        self._ensure_canvas()
        
        # Priority: Clip > Container > Canvas
        current_clip = None
        if hasattr(self, '_clip_stack') and self._clip_stack:
            current_clip = self._clip_stack[-1]

        if current_clip:
            origin = current_clip['x'] if axis == 'x' else current_clip['y']
            size = current_clip['w'] if axis == 'x' else current_clip['h']
            return origin, size
            
        container = self._get_container()
        if container:
            if len(container) == 5:
                cx, cy, cw, ch, pad = container
            else:
                cx, cy, cw, ch = container
                pad = 0
            origin = (cx if axis == 'x' else cy) + pad
            size = (cw if axis == 'x' else ch) - (pad * 2)
            return origin, size
            
        return 0.0, (self.canvas.width if axis == 'x' else self.canvas.height)

    def _resolve_magnitude(self, val_str: str, axis: str, context_size: float) -> float:
        """
        Resolve a value string into a magnitude (pixels) relative to a 0-origin.
        Does NOT apply context origin or group offsets.
        """
        val_str = str(val_str).strip().lower()

        # 1. Percentage
        if val_str.endswith('%'):
            try:
                return context_size * (float(val_str[:-1]) / 100.0)
            except ValueError:
                pass

        # 2. Keywords (Relative to context start)
        if val_str in ('left', 'top'): return 0.0
        if val_str in ('right', 'bottom'): return context_size
        if val_str in ('center', 'middle'): return context_size / 2

        # 3. Expressions (Recursive)
        match = re.match(r'^(.+)\s*([+\-])\s*(.+)$', val_str)
        if match:
            left_str, op, right_str = match.groups()
            try:
                v1 = self._resolve_magnitude(left_str, axis, context_size)
                v2 = self._resolve_magnitude(right_str, axis, context_size)
                return v1 + v2 if op == '+' else v1 - v2
            except:
                pass

        # 4. Raw Number (Scale it!)
        try:
            return self._s(float(val_str))
        except ValueError:
            # Maybe it's mid()
            match_mid = re.match(r'^(?:mid|between)\(([^,;]+)[,;]([^,;]+)\)$', val_str)
            if match_mid:
                p1_str, p2_str = match_mid.groups()
                p1 = self._resolve_magnitude(p1_str, axis, context_size)
                p2 = self._resolve_magnitude(p2_str, axis, context_size)
                return (p1 + p2) / 2
            
            raise ValueError(f"Invalid coordinate value: {val_str}")

    def _parse_position(self, pos_str: str, axis: str, ignore_stack: bool = False) -> float:
        """
        Parse a position string into an absolute pixel coordinate on the canvas.
        """
        origin, size = self._get_context_info(axis)
        magnitude = self._resolve_magnitude(pos_str, axis, size)
        
        # Apply group offset if not ignored
        group_x, group_y = (0.0, 0.0) if ignore_stack else self._get_group_offset()
        offset = group_x if axis == 'x' else group_y
        
        return origin + magnitude + offset

    def _parse_length(self, len_str: str, axis: str) -> float:
        """
        Parse a length/dimension string into a magnitude (pixels).
        Useful for width, height, radius, stroke width, etc.
        """
        _, size = self._get_context_info(axis)
        return self._resolve_magnitude(len_str, axis, size)

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
    
    def _handle_error(self, message: str):
        """Handle error based on strict mode."""
        if self._get_state('strict', True):
            raise RuntimeError(message)
        else:
            self.errors.append(message)

    def _define_function(self, name: str, args: str, body: str) -> str:
        """Define a custom macro function."""
        try:
            arg_list = [a.strip() for a in args.split(',') if a.strip()]
            self.macros[name] = {'args': arg_list, 'body': body}
            return f"Function ${name} defined"
        except Exception as e:
            self._handle_error(f"Failed to define function: {e}")
            return ""

    def _get_errors(self) -> str:
        """Get all internal errors as a semicolon separated string."""
        return "; ".join(self.errors)

    def _ensure_canvas(self) -> None:
        """
        Ensure that a canvas exists before performing operations.
        """
        if not hasattr(self, 'canvas') or not self.canvas:
            raise RuntimeError("No canvas created. Call $createCanvas first.")
        
        if not hasattr(self, 'draw') or not self.draw:
            raise RuntimeError("No drawing context available. Call $createCanvas first.")
