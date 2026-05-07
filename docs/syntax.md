# Syntax Guide

AlphaPIL uses a custom scripting syntax inspired by common bot commands and functional programming.

## Function Syntax

All functions start with a `$` followed by the function name and arguments enclosed in `[]`, separated by `;`.

```
$functionName[arg1;arg2;arg3]
```

### Key Principles

1. **Top-Down Execution**: Templates are processed line by line.
2. **Case Sensitivity**: Function names are case-sensitive (e.g., `$drawRect` vs `$drawrect`).
3. **Variables**: Use `{variable_name}` to inject values into arguments.
4. **Colors**: Supports hex codes (`#ffffff`), RGB/RGBA, and common color names (`white`, `red`, etc.).

## Function Nesting

One of the most powerful features of AlphaPIL is **nesting**. Since functions return string values, you can use one function as an argument for another.

### How it works
The interpreter resolves functions from the **inside-out**. 

**Example:**
```bash
$drawRect[10;10;$math[100 + 50];$random[20;80];red]
```
In this case:
1. `$math[100 + 50]` is resolved to `150`.
2. `$random[20;80]` is resolved to a random number (e.g., `42`).
3. Finally, `$drawRect[10;10;150;42;red]` is executed.

### Composable Functions
Functions that are commonly used inside others include:
*   **Math & Logic:** `$math`, `$if`, `$random`
*   **Text Utilities:** `$toUpper`, `$toLower`, `$substring`, `$length`
*   **Color Utilities:** `$getHex`

## Advanced Positioning

### Anchors (Pivot Points)

Most drawing functions support an `anchor` parameter. This defines which part of the object "sits" on the coordinates you provided.

| Anchor | Description |
| :--- | :--- |
| **lt** | Left-Top (Default for most) |
| **ct** | Center-Top |
| **rt** | Right-Top |
| **lm** | Left-Middle |
| **mm** | Middle-Middle (Center) |
| **rm** | Right-Middle |
| **lb** | Left-Bottom |
| **cb** | Center-Bottom |
| **rb** | Right-Bottom |

**Example:**
```bash
# Draws a 100x100 square centered exactly at 500,500
$drawRect[500;500;100;100;red;anchor=mm]
```

### Coordinate Grouping

Groups allow you to define a set of elements relative to a starting point. If you move the group, all elements inside move with it.

```bash
$startGroup[100;100]
  $drawRect[0;0;50;50;blue]  # Drawn at 100,100
  $drawCircle[25;25;10;white] # Drawn at 125,125
$endGroup
```

---

## Variable Management

### Setting Variables

You can set internal template variables using `$setVar`.

```
$setVar[myColor;#ff5500]
$createCanvas[100;100;{myColor}]
```

### Dynamic Injection

When using the Python API, you can pass a dictionary of variables:

```python
engine.render(template, variables={"username": "John"})
```

In the template:
```
$drawText[10;10;Hello {username}!;white;12]
```

## Mathematical Expressions

Use the `$math` function to perform calculations.

```
$setVar[centerX;$math[800 / 2]]
$setVar[centerY;$math[600 / 2]]
$drawCircle[{centerX};{centerY};50;blue]
```

## Logic & Control Flow

### If Statements

The `$if` function allows for conditional rendering.

```
$if[{xp} > 1000;$drawText[10;10;Pro User;gold;16];$drawText[10;10;Newbie;white;16]]
```

Syntax: `$if[condition;true_branch;false_branch]`
