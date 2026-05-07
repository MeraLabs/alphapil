"""
CanvasInterpreter - Core recursive parser for AlphaPIL.

This module provides the fundamental parsing logic for handling nested functions
using a while loop and re.search pattern matching.
"""

import re
import asyncio
import inspect
from typing import Any, Dict, List, Optional, Callable


class CanvasInterpreter:
    """
    Core interpreter class that handles recursive parsing of nested functions.
    
    The parser resolves functions from inside-out using a while loop with re.search
    to find and replace nested function calls until no more patterns remain.
    """
    
    def __init__(self):
        """Initialize the interpreter with an empty function registry."""
        self.functions: Dict[str, Callable] = {}
        self.variables: Dict[str, Any] = {}
    
    def register_function(self, name: str, func: Callable) -> None:
        """
        Register a function that can be called in templates.
        
        Args:
            name: Function name (without $ prefix)
            func: Callable that will be executed when the function is encountered
        """
        self.functions[name] = func
    
    def set_variable(self, name: str, value: Any) -> None:
        """
        Set a variable that can be used in templates.
        
        Args:
            name: Variable name (without {} wrapper)
            value: Value to assign to the variable
        """
        self.variables[name] = value
    
    def _find_innermost_function(self, text: str) -> Optional[re.Match]:
        """
        Find the innermost function call in the text.
        
        This regex pattern matches function calls like $functionName[...;...] 
        and ensures we find the innermost nested calls first.
        
        Args:
            text: Text to search for function calls
            
        Returns:
            Match object if function found, None otherwise
        """
        # Pattern matches: $functionName[arguments]
        # Uses negative lookahead to avoid matching nested brackets incorrectly
        pattern = r'\$(\w+)\[([^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*)\]'
        return re.search(pattern, text)
    
    def _parse_arguments(self, args_str: str) -> List[str]:
        """
        Parse function arguments, handling quoted strings and semicolon separators.
        
        Args:
            args_str: String containing function arguments
            
        Returns:
            List of parsed arguments
        """
        if not args_str.strip():
            return []
        
        args = []
        current_arg = ""
        in_quotes = False
        quote_char = None
        nesting_depth = 0
        
        i = 0
        while i < len(args_str):
            char = args_str[i]
            
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
                current_arg += char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
                current_arg += char
            elif not in_quotes:
                if char in ('[', '('):
                    nesting_depth += 1
                    current_arg += char
                elif char in (']', ')'):
                    nesting_depth -= 1
                    current_arg += char
                elif char == ';' and nesting_depth == 0:
                    args.append(current_arg.strip())
                    current_arg = ""
                else:
                    current_arg += char
            else:
                current_arg += char
            
            i += 1
        
        # Always append the last argument, even if empty, to ensure correct argument count
        args.append(current_arg.strip())
        
        return args
    
    def _resolve_variables(self, text: str) -> str:
        """
        Resolve variable placeholders like {variable_name} in the text.
        
        Args:
            text: Text containing variable placeholders
            
        Returns:
            Text with variables replaced by their values
        """
        def replace_var(match):
            var_name = match.group(1)
            # Support default values: {var|default}
            default_val = ""
            if '|' in var_name:
                var_name, default_val = var_name.split('|', 1)
            
            # Use get() with default_val (or empty string if not provided)
            # Note: variables dict values should be strings ideally
            val = self.variables.get(var_name, default_val)
            return str(val) if val is not None else default_val
        
        # Match variables with optional |default part: {name} or {name|default}
        # Allow any characters except closing brace inside
        return re.sub(r'\{([^\}]+)\}', replace_var, text)
    
    async def _preprocess_argument(self, arg: str) -> str:
        """
        Recursively resolve all nested functions and variables in an argument.
        
        Execution order:
        1. Variable replacement: {var} → value
        2. Nested function evaluation: $func[...] → result (recursively)
        
        This ensures that expressions like $drawRect[10;10;$math[100 * 2];50;red]
        work correctly by evaluating $math[100 * 2] → "200" before passing to _drawRect.
        
        Args:
            arg: Argument string that may contain nested functions and variables
            
        Returns:
            Fully resolved argument value
        """
        # First pass: resolve variables
        arg = self._resolve_variables(arg)
        
        # Second pass: resolve nested functions recursively
        max_iterations = 100  # Prevent infinite loops in nested functions
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            match = self._find_innermost_function(arg)
            
            if not match:
                break  # No more functions to resolve
            
            func_name = match.group(1)
            args_str = match.group(2)
            
            # Recursively preprocess nested arguments
            nested_args = self._parse_arguments(args_str)
            
            # Process nested arguments async
            processed_nested_args = []
            for a in nested_args:
                processed_nested_args.append(await self._preprocess_argument(a))
            
            # Execute the function
            if func_name not in self.functions:
                raise ValueError(f"Unknown function: ${func_name}")
            
            try:
                result = await self._execute_function(func_name, processed_nested_args)
                # Clean up numeric results
                if func_name in ['math', 'random', 'length', 'getHex']:
                    result = str(result).strip()
                else:
                    result = str(result)
            except Exception as e:
                raise RuntimeError(f"Error in nested function ${func_name}: {e}")
            
            # Replace in original string
            arg = arg[:match.start()] + result + arg[match.end():]
        
        if iteration >= max_iterations:
            raise RuntimeError(f"Argument preprocessing exceeded maximum iterations: {arg}")
        
        return arg
    
    async def _execute_function(self, func_name: str, args: List[str]) -> str:
        """
        Execute a registered function with parsed arguments (Async).
        Supports both sync and async functions, and flexible argument mapping.
        
        Args:
            func_name: Name of the function to execute
            args: List of argument strings
            
        Returns:
            String result of the function execution
        """
        if func_name not in self.functions:
            raise ValueError(f"Unknown function: ${func_name}")
        
        try:
            func = self.functions[func_name]
            
            # Split into named and unnamed arguments
            named_args = {}
            unnamed_args = []
            
            for arg in args:
                if '=' in arg and not arg.startswith(('http://', 'https://')):
                    parts = arg.split('=', 1)
                    key = parts[0].strip()
                    val = parts[1].strip()
                    
                    # Only treat as named arg if:
                    # 1. key is a valid identifier
                    # 2. value doesn't start with '=' (avoids '==')
                    # 3. key doesn't end with common comparison symbols (avoids '!=', '<=', '>=')
                    if key.isidentifier() and not val.startswith('=') and not key.endswith(('!', '<', '>')):
                        named_args[key] = val
                        continue
                unnamed_args.append(arg)
            
            # Use inspect to map arguments to the function signature
            sig = inspect.signature(func)
            params = list(sig.parameters.values())
            
            # Build the argument set
            final_kwargs = {}
            
            # 1. Apply named arguments
            final_kwargs.update(named_args)
            
            # 2. Map unnamed arguments to remaining parameters
            unnamed_idx = 0
            for param in params:
                if param.name not in final_kwargs and unnamed_idx < len(unnamed_args):
                    final_kwargs[param.name] = unnamed_args[unnamed_idx]
                    unnamed_idx += 1
            
            # Execute the function - only pass arguments that exist in the function signature
            safe_kwargs = {k: v for k, v in final_kwargs.items() if k in sig.parameters}
            result = func(**safe_kwargs)
            
            # Handle async functions
            if inspect.iscoroutine(result):
                result = await result
            
            # Strip whitespace from result for numeric functions
            if func_name in ['math', 'random', 'length', 'getHex']:
                result = str(result).strip()
            
            return str(result)
        except Exception as e:
            # Provide more detailed error info for debugging
            raise RuntimeError(f"Error executing function ${func_name} with args {args}: {e}")
    
    async def parse(self, template: str) -> str:
        """
        Parse a template string with correct execution order (Async).
        
        Execution order:
        1. Resolve variables: {var} → value
        2. Find innermost function
        3. Preprocess arguments (recursively resolve variables + nested functions)
        4. Execute function with fully resolved arguments
        5. Replace function call with result
        6. Repeat until no functions remain
        
        This ensures expressions like $drawRect[10;10;$math[100 * 2];50;red]
        work correctly by evaluating nested $math before passing to _drawRect.
        
        Args:
            template: Template string containing function calls and variables
            
        Returns:
            Fully resolved template string
        """
        result = template
        
        # Main parsing loop with iteration limit to prevent infinite loops
        max_iterations = 1000
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            # Step 1: Resolve variables first
            result = self._resolve_variables(result)
            
            # Step 2: Find the innermost function call
            match = self._find_innermost_function(result)
            
            if not match:
                break  # No more function calls to resolve
            
            func_name = match.group(1)
            args_str = match.group(2)
            
            # Step 3: Parse and preprocess arguments
            # This recursively resolves all variables and nested functions in each argument
            args = self._parse_arguments(args_str)
            
            # Process arguments async
            processed_args = []
            for arg in args:
                processed_args.append(await self._preprocess_argument(arg))
            
            # Step 4: Execute function with fully resolved arguments
            try:
                func_result = await self._execute_function(func_name, processed_args)
            except Exception as e:
                raise RuntimeError(f"Failed to execute ${func_name}: {e}")
            
            # Step 5: Replace the function call with its result
            result = result[:match.start()] + func_result + result[match.end():]
        
        if iteration >= max_iterations:
            raise RuntimeError("Parser exceeded maximum iterations - possible infinite loop in template")
        
        return result
