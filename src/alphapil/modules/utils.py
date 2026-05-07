"""
Utils module - Utility functions for AlphaPIL.

This module provides various utility functions like math operations,
conditional logic, random numbers, color conversion, and text manipulation.
"""

import random
import re
from typing import Union


class UtilsMixin:
    """
    Mixin class providing utility functions for various operations.
    
    This mixin adds math operations, conditional logic, random numbers,
    color conversion, and text manipulation utilities.
    """
    
    def _math(self, expression: str) -> str:
        """
        Safely evaluate mathematical expressions.
        
        Supports basic arithmetic operations: +, -, *, /, **, %, //
        Also supports parentheses and basic math functions.
        
        Args:
            expression: Mathematical expression as string
            
        Returns:
            Result of the evaluation as clean numeric string
            (returns integer string if whole number, float otherwise)
            
        Raises:
            ValueError: If expression contains unsafe characters or invalid syntax
        """
        # Sanitize expression - only allow numbers, operators, parentheses, and spaces
        allowed_chars = r'0-9+\-*/().\s%'
        
        # Check for allowed characters (simpler regex, no function support for now)
        if not re.match(rf'^[{allowed_chars}]+$', expression):
            raise ValueError(f"Unsafe mathematical expression: {expression}")
        
        try:
            # Use eval with restricted globals for safety
            result = eval(expression, {"__builtins__": {}}, {})
            
            # Return as clean string - int if whole number, float otherwise
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            return str(result).strip()
        except Exception as e:
            raise ValueError(f"Invalid mathematical expression: {expression}. Error: {e}")
    
    def _if(self, condition: str, true_val: str = "", false_val: str = "") -> str:
        """
        Flexible conditional logic with optional branches.
        
        Both true_val and false_val are optional, allowing patterns like:
        - $if[condition;action;] → Execute action if true, do nothing if false
        - $if[condition;;fallback] → Do nothing if true, execute fallback if false  
        - $if[condition;action;fallback] → Standard ternary behavior
        - $if[condition;;] → Do nothing regardless
        
        Args:
            condition: Condition to evaluate (supports comparisons and truthiness)
            true_val: Value to return if condition is true (optional, default: "")
            false_val: Value to return if condition is false (optional, default: "")
            
        Returns:
            true_val or false_val based on condition evaluation
            
        Examples:
            $if[{has_avatar};$drawImage[...];] → Draw if has_avatar, else nothing
            $if[{level} > 10;⭐;] → Show star only if level > 10
        """
        # Condition is already preprocessed (variables resolved)
        condition = condition.strip()
        
        # Check for empty/falsy values
        if not condition or condition.lower() in ['false', '0', 'none', 'null', '']:
            return false_val
        
        # Check for comparison operators (in order of precedence)
        # Use regex to be more robust
        if '==' in condition:
            left, right = condition.split('==', 1)
            return true_val if left.strip() == right.strip() else false_val
        elif '!=' in condition:
            left, right = condition.split('!=', 1)
            return true_val if left.strip() != right.strip() else false_val
        elif '>=' in condition:
            try:
                left, right = condition.split('>=', 1)
                return true_val if float(left.strip()) >= float(right.strip()) else false_val
            except ValueError:
                # If can't convert to float, do string comparison
                left, right = condition.split('>=', 1)
                return true_val if left.strip() >= right.strip() else false_val
        elif '<=' in condition:
            try:
                left, right = condition.split('<=', 1)
                return true_val if float(left.strip()) <= float(right.strip()) else false_val
            except ValueError:
                left, right = condition.split('<=', 1)
                return true_val if left.strip() <= right.strip() else false_val
        elif '>' in condition:
            try:
                left, right = condition.split('>', 1)
                return true_val if float(left.strip()) > float(right.strip()) else false_val
            except ValueError:
                left, right = condition.split('>', 1)
                return true_val if left.strip() > right.strip() else false_val
        elif '<' in condition:
            try:
                left, right = condition.split('<', 1)
                return true_val if float(left.strip()) < float(right.strip()) else false_val
            except ValueError:
                left, right = condition.split('<', 1)
                return true_val if left.strip() < right.strip() else false_val
        else:
            # Truthy check - any non-empty value is true
            return true_val
    
    def _random(self, min_val: str, max_val: str = None) -> str:
        """
        Generate a random integer.
        
        Args:
            min_val: Minimum value (or only value if max_val is not provided)
            max_val: Maximum value (optional)
            
        Returns:
            Random integer as string
        """
        try:
            min_num = int(min_val)
            
            if max_val is not None:
                max_num = int(max_val)
                result = random.randint(min_num, max_num)
            else:
                # If only one value provided, use 0 as minimum
                result = random.randint(0, min_num)
            
            return str(result)
        except ValueError as e:
            raise ValueError(f"Invalid random number parameters: {e}")
    
    def _get_hex(self, color_name: str) -> str:
        """
        Convert color names to hex values.
        
        Supports common color names and Discord-specific colors like 'blurple'.
        
        Args:
            color_name: Color name to convert
            
        Returns:
            Hex color value as string
        """
        # Define color mappings
        color_map = {
            # Standard colors
            'red': '#FF0000',
            'green': '#00FF00',
            'blue': '#0000FF',
            'yellow': '#FFFF00',
            'cyan': '#00FFFF',
            'magenta': '#FF00FF',
            'white': '#FFFFFF',
            'black': '#000000',
            'gray': '#808080',
            'grey': '#808080',
            'orange': '#FFA500',
            'purple': '#800080',
            'pink': '#FFC0CB',
            'brown': '#A52A2A',
            'lime': '#00FF00',
            'navy': '#000080',
            'teal': '#008080',
            'silver': '#C0C0C0',
            'gold': '#FFD700',
            
            # Discord colors
            'blurple': '#5865F2',
            'discord': '#5865F2',
            'green_discord': '#57F287',
            'yellow_discord': '#FEE75C',
            'fuchsia': '#EB459E',
            'red_discord': '#ED4245',
            
            # Light variants
            'lightblue': '#ADD8E6',
            'lightgreen': '#90EE90',
            'lightgray': '#D3D3D3',
            'lightgrey': '#D3D3D3',
            'lightred': '#FFB6C1',
            'lightyellow': '#FFFFE0',
            
            # Dark variants
            'darkblue': '#00008B',
            'darkgreen': '#006400',
            'darkgray': '#A9A9A9',
            'darkgrey': '#A9A9A9',
            'darkred': '#8B0000',
            'darkyellow': '#BDB76B',
        }
        
        color_name_lower = color_name.lower().strip()
        
        if color_name_lower in color_map:
            return color_map[color_name_lower]
        
        # If already a hex color, return as-is
        if re.match(r'^#[0-9A-Fa-f]{6}$', color_name):
            return color_name
        
        # Try to parse as RGB values
        if re.match(r'^\d+,\s*\d+,\s*\d+$', color_name):
            try:
                r, g, b = map(int, color_name.split(','))
                return f'#{r:02X}{g:02X}{b:02X}'
            except ValueError:
                pass
        
        raise ValueError(f"Unknown color name: {color_name}")
    
    def _replace(self, text: str, old: str, new: str) -> str:
        """
        Replace all occurrences of a substring in text.
        
        Args:
            text: Original text
            old: Substring to replace
            new: Replacement substring
            
        Returns:
            Text with replacements made
        """
        return text.replace(old, new)
    
    def _length(self, text: str) -> str:
        """
        Get the length of a string.
        
        Args:
            text: Text to measure
            
        Returns:
            Length as string
        """
        return str(len(text))
    
    def _substring(self, text: str, start: str, end: str = None) -> str:
        """
        Extract a substring from text.
        
        Args:
            text: Original text
            start: Start index (supports negative indices)
            end: End index (optional, supports negative indices)
            
        Returns:
            Substring
        """
        try:
            start_idx = int(start)
            
            if end is not None:
                end_idx = int(end)
                return text[start_idx:end_idx]
            else:
                return text[start_idx:]
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid substring parameters: {e}")
    
    def _join(self, separator: str, *items) -> str:
        """
        Join multiple items with a separator.
        
        Args:
            separator: String to use as separator
            *items: Items to join
            
        Returns:
            Joined string
        """
        return separator.join(items)
    
    def _split(self, text: str, separator: str = " ") -> str:
        """
        Split text by separator and return as comma-separated list.
        
        Args:
            text: Text to split
            separator: Separator to split by (default: space)
            
        Returns:
            Comma-separated list of parts
        """
        parts = text.split(separator)
        return ",".join(parts)
