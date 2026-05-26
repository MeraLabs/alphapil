# What's New in AlphaPIL 🚀

Stay up to date with the latest features, improvements, and fixes in AlphaPIL.

---

## May 26, 2026 (v0.2.7)
!!! abstract "Feature Release: Perfect Box Alignment & Auto-Sizing Text"
    This release completely updates `$drawTextMid` and `$drawTextIn` to follow professional box layout standards: `$drawTextMid` automatically truncates text to fit between bounds, and `$drawTextIn` automatically scales down font size step-by-step to fit completely inside a box without truncation.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **🔤 Layout** | **Auto-Truncation** | Updated `$drawTextMid` to automatically truncate text with `...` if it exceeds the horizontal boundaries (`x2 - x1`). | [Docs](functions/text/drawTextMid.md) |
    | **🎯 Layout** | **Auto-Sizing** | Updated `$drawTextIn` to dynamically scale down the font size until the text fits perfectly within the bounding box (`x1, y1` to `x2, y2`). | [Docs](functions/text/drawTextIn.md) |
    | **🤖 AI** | **Manifest v0.2.7** | Synchronized technical manifest with the package version 0.2.7. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

## May 26, 2026 (v0.2.6)
!!! abstract "Feature Release: Variable Fonts Support"
    This release introduces native support for OpenType variable fonts, giving you dynamic control over font weights, widths, slants, and custom variations directly in your templates.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **🔤 Layout** | **Variable Fonts** | Added dynamic variable font axis selection (`wght=700`, `Bold`, etc.) to `$setFont` and `$drawText`. | [Docs](functions/text/drawText.md) |
    | **🤖 AI** | **Manifest v0.2.6** | Synchronized technical manifest with the package version 0.2.6. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

## May 26, 2026 (v0.2.5)
!!! abstract "Patch Update: Fixed \$useImageAsCanvas Dimension Resolution"
    This patch resolves a critical bug where `$useImageAsCanvas` would crash due to the lack of an existing canvas when resolving its fixed dimensions.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **🐛 Fix** | **\$useImageAsCanvas** | Allowed parsing `fixed_width` and `fixed_height` when no canvas has been created yet by temporarily using the loaded image as context. | [Docs](functions/images/useImageAsCanvas.md) |
    | **🤖 AI** | **Manifest v0.2.5** | Synchronized technical manifest with the package version 0.2.5. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

## May 24, 2026 (v0.2.4)
!!! abstract "Feature Release: Rotation, Color Enhancements & Shape Shadows/Glows"
    This update adds powerful creative control to AlphaPIL: rotate the canvas or active layers, adjust image qualities (brightness, contrast, saturation) dynamically, generate background patterns, and apply drop shadows and outer glow effects natively to shapes. Additionally, redundant text helper functions were cleaned up.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **🔄 Rotation** | **Canvas & Layer Rotation** | Added `$rotate` to rotate the active layer or canvas by any angle. | [Docs](functions/images/rotate.md) |
    | **🎨 Enhancements** | **Color Adjustment** | Added `$adjustColor` for brightness, contrast, and saturation. | [Docs](functions/images/adjustColor.md) |
    | **🏁 Patterns** | **Pattern Drawing** | Added `$drawPattern` for background dots, lines, and grids. | [Docs](functions/images/drawPattern.md) |
    | **🔆 Shadows & Glows** | **Shape Effects** | Integrated shadows & glows directly into `$drawRect`, `$drawCircle`, and `$drawRoundedRect`. | [Docs](functions/geometric/drawRect.md) |
    | **🧹 Clean-up** | **Redundant Helpers** | Deprecated and removed unused text stroke/gradient helper functions. | [Docs](functions/text/drawText.md) |
    | **🤖 AI** | **Manifest v0.2.4** | Synchronized technical manifest with all new shapes parameters and commands. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

## May 17, 2026 (v0.2.3)
!!! abstract "Major Feature Update: High-DPI Rendering & Chart Quality"
    This update introduces a robust post-processing pipeline for crystal-clear image exports at retina/High-DPI resolutions, alongside significant readability improvements for charts.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **💎 Rendering** | **Output Scaling** | Added `scale` to `$createCanvas` for high-DPI/Retina output independent of AA. | [Docs](functions/core/createCanvas.md) |
    | **✨ Quality** | **Sharpening Pipeline** | Engine now automatically applies `UnsharpMask` after Lanczos downsampling for superior crispness. | [GitHub](https://github.com/MeraLabs/AlphaPIL) |
    | **📊 Charts** | **Label Legibility** | Increased default chart label `size` to 20 and added adaptive state-based coloring. | [Docs](functions/images/drawBarChart.md) |
    | **🤖 AI** | **Manifest v0.2.3** | Updated manifest with proper scale logic, chart clipping tips, and updated syntax. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

## May 17, 2026 (v0.2.2)
!!! abstract "Patch Update: Container Anchor Support"
    This patch adds anchor support for the `startContainer` function to easily center containers on the canvas.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **🎯 Layout** | **Container Anchor** | Added `anchor` parameter to `$startContainer` allowing precise centering (`anchor=mm`). | [Docs](functions/groups/startContainer.md) |
    | **🤖 AI** | **Manifest v0.2.2** | Updated technical manifest to document `$startContainer` anchor parameter. | [Manifest](ALPHAPIL_MANIFEST.txt) |

## May 17, 2026
!!! abstract "Major Feature Update: High-Res Rendering & Modern UI"
    This update introduces the foundation for professional-grade image generation and modern UI components.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **💎 Rendering** | **Anti-Aliasing (AA)** | 4x-8x Supersampling for ultra-smooth edges on shapes and text. | [Docs](functions/core/createCanvas.md) |
    | **🎯 Layout** | **Container System** | Box-model containers with relative alignment (`center`, `right`, etc.). | [Docs](functions/groups/startContainer.md) |
    | **✨ Effects** | **Linear Gradients** | Multi-stop gradients with custom rotation and AA support. | [Docs](functions/images/drawLinearGradient.md) |
    | **🔆 Effects** | **Radial Gradients** | Circular glow and lighting effects for modern designs. | [Docs](functions/images/drawRadialGradient.md) |
    | **🌫️ Effects** | **Regional Blur** | Gaussian blur for specific regions (Glassmorphism). | [Docs](functions/images/blur.md) |
    | **📊 Charts** | **Bar Charts** | Themed, automatic scaling bar charts for data visualization. | [Docs](functions/images/drawBarChart.md) |
    | **📉 Charts** | **Line Charts** | Professional line graphs with multiple color themes. | [Docs](functions/images/drawLineChart.md) |
    | **⏳ Charts** | **Progress Bars** | Modern rounded progress bars with custom radius and styling. | [Docs](functions/images/drawProgressBar.md) |
    | **🛠️ Dev** | **Custom Macros** | Define your own functions with `$function` for reusable UI components. | [Docs](functions/utils/function.md) |
    | **🛡️ Safety** | **Strict Mode** | Toggle `strict=false` to prevent errors from crashing the renderer. | [Docs](functions/core/createCanvas.md) |
    | **🔤 Fonts** | **Auto-Discovery** | Use any system font (Arial, Impact, etc.) by name via `$getSystemFonts`. | [Docs](functions/core/getSystemFonts.md) |
    | **📦 Core** | **Dependency Cleanup** | Removed `discord.py` from core for a lighter, faster package. | [GitHub](https://github.com/MeraLabs/AlphaPIL) |

---

## May 17, 2026 (v0.2.3)
!!! abstract "Patch Update: Bug Fixes & Variable Support"
    This patch fixes critical import issues and improves variable handling for AI agents.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **🐛 Fix** | **Import Error** | Fixed `NameError` related to `Optional` and `Tuple` in core modules. | [GitHub](https://github.com/MeraLabs/AlphaPIL) |
    | **📥 Variable** | **$getVar** | Added explicit `$getVar` function to complement `{var}` syntax. | [Docs](functions/core/getVar.md) |
    | **🤖 AI** | **Manifest v0.2.1** | Updated technical manifest with $getVar and better positioning logic. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

*To see previous updates, check our [GitHub Release History](https://github.com/MeraLabs/AlphaPIL/releases).*
