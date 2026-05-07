# Text & Typography

Functions for rendering and manipulating text.

| Function | Syntax |
| :--- | :--- |
| **drawText** | `$drawText[x;y;text;color;size;font;anchor;...;max_width;truncate_width]` |
| **drawTextMid** | `$drawTextMid[text;x1;x2;y1;y2;max_width;...]` |
| **drawTextIn** | `$drawTextIn[text;x;y;w;h;max_width;...]` |
| **toUpper / toLower** | `$toUpper[text]` / `$toLower[text]` |
| **toTitle** | `$toTitle[text]` |
| **measureText** | `$measureText[text;size;font]` |
| **autoSizeText** | `$autoSizeText[text;max_width;start_size;min_size;font]` |
| **truncateText / wrapText** | `$truncateText[text;width]` / `$wrapText[text;width]` |
| **drawTextStroke** | `$drawTextStroke[text;x;y;size;color;stroke_w;stroke_c;font]` |
| **drawTextGradient** | `$drawTextGradient[text;x;y;size;color1;color2;font]` |

## Examples

### Basic Text
```bash
$drawText[10;10;Hello World;white;24]
```

### Auto-Sizing
Great for fitting usernames into a fixed area:
```bash
$autoSizeText[{username};190;33;18;bold_font]
```

### Gradients & Effects
```bash
$drawTextGradient[Glow;10;10;40;red;yellow]
```
