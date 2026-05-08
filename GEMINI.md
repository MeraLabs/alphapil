# AlphaPIL Development Ground Truth

This file serves as the definitive reference for all function signatures and parameter orders in the AlphaPIL package. **All code changes and documentation updates MUST align with this file.**

## Core Mandates
- **Consistency:** Function signatures in `src/alphapil/modules/` MUST match the parameter order listed here.
- **Documentation:** Markdown files in `docs/functions/` MUST match the syntax defined here.
- **Error Messages:** All functions should include a `Proper Syntax:` debug line in their `ValueError` or `Exception` handling that matches the syntax here.
- **Build Cleanup:** Every time a new version bump and build is performed, all older version artifacts in the `dist/` directory MUST be removed to keep the workspace clean.

---

## 1. Core Functions
| Function | Syntax |
| :--- | :--- |
| **createCanvas** | `$createCanvas[width;height;color]` |
| **save** | `$save[filename]` |
| **setVar** | `$setVar[name;value]` |
| **getBytes** | `$getBytes[format]` |

## 2. Geometric Shapes
| Function | Syntax |
| :--- | :--- |
| **drawRect** | `$drawRect[x;y;width;height;color;outline;fill;outline_width;radius;anchor]` |
| **drawRoundedRect** | `$drawRoundedRect[x;y;width;height;radius;color;outline;fill;outline_width;anchor]` |
| **drawCircle** | `$drawCircle[cx;cy;radius;color;outline;fill;outline_width;anchor]` |
| **drawLine** | `$drawLine[x1;y1;x2;y2;color;width]` |
| **drawPolygon** | `$drawPolygon[points_list;color;outline;fill;outline_width]` |
| **drawTriangle** | `$drawTriangle[x1;y1;x2;y2;x3;y3;color;outline;fill;outline_width]` |
| **drawStar** | `$drawStar[x;y;points;outer_radius;inner_radius;color;outline;fill;outline_width]` |
| **drawArc** | `$drawArc[x;y;w;h;start_angle;end_angle;color;width]` |

## 3. Text Functions
| Function | Syntax |
| :--- | :--- |
| **drawText** | `$drawText[x;y;text;color;size;font;anchor;stroke_width;stroke_fill;shadow_color;shadow_offset;glow_color;glow_radius;max_width;truncate_width;gradient_colors]` |
| **text** | (Alias for `drawText`) |
| **drawTextMid** | `$drawTextMid[x1;y1;x2;y2;text;color;size;font;stroke_width;stroke_fill;shadow_color;shadow_offset;glow_color;glow_radius;x;y;w;h;max_width;truncate_width]` |
| **drawTextIn** | `$drawTextIn[x;y;w;h;text;color;size;font;stroke_width;stroke_fill;shadow_color;shadow_offset;glow_color;glow_radius;x1;x2;y1;y2;max_width;truncate_width]` |
| **toUpper** | `$toUpper[text]` |
| **toLower** | `$toLower[text]` |
| **toTitle** | `$toTitle[text]` |
| **measureText** | `$measureText[text;size;font]` |
| **wrapText** | `$wrapText[text;width;size;font]` |
| **autoSizeText** | `$autoSizeText[text;max_width;start_size;min_size;font]` |
| **truncateText** | `$truncateText[text;width;size;font;suffix]` |

## 4. Image Functions
| Function | Syntax |
| :--- | :--- |
| **drawImage** | `$drawImage[x;y;image_path;width;height;opacity;radius;circle;anchor]` |
| **useImageAsCanvas** | `$useImageAsCanvas[path;h_var;w_var;fixed_width;fixed_height]` |
| **imageFilter** | `$imageFilter[filter_name]` |
| **clearImageCache** | `$clearImageCache[]` |

## 5. Utility Functions
| Function | Syntax |
| :--- | :--- |
| **math** | `$math[expression]` |
| **if** | `$if[condition;true_val;false_val]` |
| **random** | `$random[min_val;max_val]` |
| **getHex** | `$getHex[color_name]` |
| **replace** | `$replace[text;old;new]` |
| **length** | `$length[text]` |
| **substring** | `$substring[text;start;end]` |
| **join** | `$join[separator;item1;item2;...]` |
| **split** | `$split[text;separator]` |

## 6. Masking & Layers
| Function | Syntax |
| :--- | :--- |
| **createLayer** | `$createLayer[name]` |
| **switchLayer** | `$name` (or `$switchLayer[name]`) |
| **mergeLayer** | `$mergeLayer[name;x;y;opacity;target]` |
| **applyMask** | `$applyMask[mask_path;x;y;invert]` |

## 7. State & Style Management
| Function | Syntax |
| :--- | :--- |
| **setFont** | `$setFont[font_path;size]` |
| **loadFont** | `$loadFont[font_path;alias]` |
| **setColor** | `$setColor[color]` |
| **setStroke** | `$setStroke[width;color]` |
| **startGroup** | `$startGroup[x;y]` |
| **endGroup** | `$endGroup[]` |
