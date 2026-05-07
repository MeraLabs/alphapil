# Core & System Commands

These functions manage the canvas, files, and core engine settings.

| Function | Description | Syntax |
| :--- | :--- | :--- |
| **createCanvas** | Creates a new blank image. | `$createCanvas[width;height;color]` |
| **save** | Saves the current canvas to a file. | `$save[filename]` |
| **getBytes** | Returns the current canvas as bytes. | `$getBytes[format]` |
| **setVar** | Sets a template-local variable. | `$setVar[name;value]` |
| **setFont** | Sets the default font and size. | `$setFont[font_path;size]` |
| **loadFont** | Loads a local or remote font (URL) with an alias. | `$loadFont[path_or_url;alias]` |
| **setColor** | Sets the default fill color. | `$setColor[color]` |
| **setStroke** | Sets the default stroke width and color. | `$setStroke[width;color]` |

## Examples

### Creating and Saving
```bash
$createCanvas[800;600;#1a1a2e]
# ... drawing commands ...
$save[output.png]
```

### Managing Fonts
```bash
$loadFont[fonts/bold.ttf;mybold]
$drawText[10;10;Hello;white;24;mybold]
```
