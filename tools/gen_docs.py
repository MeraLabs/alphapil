#!/usr/bin/env python3
"""
AlphaPIL Documentation Generator

This script automatically generates documentation by scanning all modules
and extracting function definitions and their docstrings.
"""

import os
import re
import sys
import ast
from typing import Dict, List, Tuple


def extract_functions_from_file(filepath: str) -> List[Tuple[str, str, List[str]]]:
    """
    Extract function information from a Python file.
    
    Args:
        filepath: Path to the Python file
        
    Returns:
        List of tuples: (function_name, docstring, arguments)
    """
    functions = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to extract function definitions
        tree = ast.parse(content)
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                
                # Only include private methods (starting with underscore)
                if not func_name.startswith('_'):
                    continue
                
                # Extract docstring
                docstring = ast.get_docstring(node) or "No documentation available"
                
                # Extract arguments
                args = []
                for arg in node.args.args:
                    if arg.arg != 'self':
                        args.append(arg.arg)
                
                functions.append((func_name, docstring, args))
    
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    
    return functions


def format_function_docs(functions: List[Tuple[str, str, List[str]]], module_name: str) -> str:
    """
    Format function documentation for a module.
    
    Args:
        functions: List of function information
        module_name: Name of the module
        
    Returns:
        Formatted markdown string
    """
    if not functions:
        return ""
    
    docs = f"## {module_name.title()} Module\n\n"
    
    for func_name, docstring, args in functions:
        # Convert function name to command name
        command_name = func_name[1:]  # Remove underscore
        command = f"${command_name}"
        
        # Format arguments
        if args:
            args_str = "; ".join([f"{arg}" for arg in args])
            command_with_args = f"{command}[{args_str}]"
        else:
            command_with_args = f"{command}[]"
        
        # Clean up docstring
        docstring_clean = docstring.replace('\n', ' ').strip()
        if len(docstring_clean) > 200:
            docstring_clean = docstring_clean[:197] + "..."
        
        docs += f"### `{command_with_args}`\n\n"
        docs += f"{docstring_clean}\n\n"
        
        # Add argument details if available
        if args:
            docs += "**Arguments:**\n"
            for arg in args:
                docs += f"- `{arg}`: Argument description\n"
            docs += "\n"
        
        docs += "---\n\n"
    
    return docs


def scan_modules_directory(modules_dir: str) -> Dict[str, List[Tuple[str, str, List[str]]]]:
    """
    Scan the modules directory and extract all functions.
    
    Args:
        modules_dir: Path to the modules directory
        
    Returns:
        Dictionary mapping module names to their functions
    """
    modules = {}
    
    for filename in os.listdir(modules_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_path = os.path.join(modules_dir, filename)
            module_name = filename[:-3]  # Remove .py extension
            
            functions = extract_functions_from_file(module_path)
            if functions:
                modules[module_name] = functions
    
    return modules


def generate_commands_markdown(modules_dir: str, output_file: str):
    """
    Generate the complete COMMANDS.md file.
    
    Args:
        modules_dir: Path to modules directory
        output_file: Path to output markdown file
    """
    modules = scan_modules_directory(modules_dir)
    
    # Create header
    content = """# AlphaPIL Commands Documentation

This file contains automatically generated documentation for all AlphaPIL commands.

## Usage

Commands are called using the format: `$commandName[arg1;arg2;...]`

Nested functions are supported and resolved from inside-out:
```
$drawText[$toUpper[{name}];...]
```

---

"""
    
    # Add each module's documentation
    for module_name, functions in sorted(modules.items()):
        content += format_function_docs(functions, module_name)
    
    # Add footer
    content += """
## Notes

- All coordinates are relative to the top-left corner of the canvas
- Colors can be specified as names (red, blue, etc.), hex (#FF0000), or RGB (255,0,0)
- String arguments should be quoted if they contain special characters
- Nested functions are resolved recursively from the innermost to outermost

---

*This documentation was automatically generated by tools/gen_docs.py*
"""
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Documentation generated: {output_file}")
    
    # Print summary
    total_functions = sum(len(functions) for functions in modules.values())
    print(f"Found {len(modules)} modules with {total_functions} total functions")


def main():
    """Main function to run the documentation generator."""
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    modules_dir = os.path.join(project_root, 'src', 'alphapil', 'modules')
    output_file = os.path.join(project_root, 'COMMANDS.md')
    
    if not os.path.exists(modules_dir):
        print(f"Error: Modules directory not found: {modules_dir}")
        sys.exit(1)
    
    generate_commands_markdown(modules_dir, output_file)


if __name__ == "__main__":
    main()
