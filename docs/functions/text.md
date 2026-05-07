# Text & Typography

Functions for rendering and manipulating text.

| Function | Syntax |
| :--- | :--- |
| **drawText** | `$drawText[x;y;text;color;size;font;anchor;...;max_width;truncate_width]` |
| **text** | Alias for `$drawText` |
| **drawTextMid** | `$drawTextMid[text;x1;x2;y1;y2;max_width;...]` |
| **drawTextIn** | `$drawTextIn[text;x;y;w;h;max_width;...]` |
| **toUpper / toLower** | `$toUpper[text]` / `$toLower[text]` |
| **toTitle** | `$toTitle[text]` |
| **measureText** | `$measureText[text;size;font]` |
| **autoSizeText** | `$autoSizeText[text;max_width;start_size;min_size;font]` |
| **truncateText / wrapText** | `$truncateText[text;width]` / `$wrapText[text;width]` |

## Advanced drawText Parameters

The `$drawText` function (aliased as `$text`) is highly versatile. It supports named parameters for advanced styling:

- `stroke_width`: Width of the text outline.
- `stroke_fill`: Color of the text outline.
- `gradient_colors`: Comma-separated colors for a vertical gradient (e.g., `red,blue`).
- `max_width`: Automatically wraps text to fit this width.
- `truncate_width`: Automatically truncates text with `...` to fit this width.
- `shadow_color` & `shadow_offset`: Adds a drop shadow.
- `glow_color` & `glow_radius`: Adds an outer glow effect.

### Example: Styled Text
```bash
$drawText[
    text=AlphaPIL;
    x=center;y=center;
    size=40;
    gradient_colors=gold,orange;
    stroke_width=2;stroke_fill=black;
    shadow_color=gray;shadow_offset=2,2
]
```
