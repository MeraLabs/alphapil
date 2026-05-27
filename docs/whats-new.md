# What's New in AlphaPIL 🚀

Stay up to date with the latest features, improvements, and fixes in AlphaPIL.

---

## May 28, 2026 (v0.3.4)
!!! abstract "Feature Release: Sub-Millisecond Rendering Caches & Tracking-Aware Bounding Boxes"
    This major performance and feature release introduces global process-level caches (for system fonts, aliases, and processed images) and integrates tracking/letter-spacing support across `$drawTextMid` and `$drawTextIn`, featuring dynamic downscaled glow rendering for ultra-fast generation times.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **🚀 Performance** | **Global Process Caches** | Introduced process-level global caching for loaded image buffers, system font paths, and Pillow ImageFont objects. Subsequent renders take under 1ms. | [Manifest](ALPHAPIL_MANIFEST.txt) |
    | **🔆 Typography** | **Tracking-Aware Scaling** | Exposed `letter_spacing` (tracking) inside `$drawTextMid` and `$drawTextIn`. Bounding boxes and binary-search fitting loops are now fully tracking-aware. | [Docs](functions/text/drawTextIn.md) |
    | **🎨 Glow & Shadow** | **Sub-ms Glow Outline** | Completely redesigned glow and shadow layers to draw character-by-character with tracking. Added ceiling-division downscaling for large stroke/glow layers to make them instantaneous. | [Docs](functions/text/drawTextIn.md) |
    | **🤖 AI** | **Manifest v0.3.4** | Synchronized technical manifest version with the new letter-spacing and rendering speed upgrades. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

## May 28, 2026 (v0.3.3)
!!! abstract "Patch Release: Robust Coordinate Parser & Anchor-Aligned Glow Effects"
    This release introduces support for single-number coordinates in standard properties (such as shadow offset) and solves the spatial misalignment bug of regional text glows under custom anchors (like middle-middle `"mm"` alignment).

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **🎯 Parser** | **Single Coord Fallback** | `_parse_coords` now gracefully accepts single integers (e.g., `4`), converting them to duplicated coordinate pairs `(4, 4)` for properties like `shadow_offset`. | [Manifest](ALPHAPIL_MANIFEST.txt) |
    | **🔆 Typography** | **Anchor-Aligned Glow** | Completely rewrote glow logic to measure text bounding boxes dynamically and offset/draw/paste the glow relative to custom anchors. | [Docs](functions/text/drawTextIn.md) |
    | **🤖 AI** | **Manifest v0.3.3** | Synchronized technical manifest version with the new parsing and glow alignment enhancements. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

## May 26, 2026 (v0.3.2)
!!! abstract "Patch Release: Visual IDE Scroll Layout & Renaming Integration"
    This release fixes a critical flexbox scroll container layout centering bug where the top part of the image got cut off in the visual template designer. It also renames the generated HTML visualizer tool to `alphapil_ide_visualizer.html` to match its power as a full IDE & Visualizer, and integrates advanced text alignment tools ($drawTextMid, $drawTextIn).

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **📏 UI Fix** | **Safe Centering Scroll** | Implemented scroll-safe centering for the editor canvas to prevent top/left image cropping. | [Docs](functions/utils/open_coordinate_picker.md) |
    | **📛 Renaming** | **alphapil_ide_visualizer** | Renamed the visual template editor HTML output to reflect its full Visual IDE capabilities. | [Docs](functions/utils/open_coordinate_picker.md#features) |
    | **🔤 IDE Toolbar** | **Text Alignment Controls** | Exposed `$drawTextMid` (auto-truncation) and `$drawTextIn` (auto-scaling) directly in the Designer sidebar. | [Docs](functions/utils/open_coordinate_picker.md#features) |
    | **🤖 AI** | **Manifest v0.3.2** | Synchronized technical manifest version with the new f-string fixes, layout enhancements, and toolbar additions. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

## May 26, 2026 (v0.3.0)
!!! abstract "Feature Release: Interactive WYSIWYG Visual Template IDE"
    This major release upgrades the Visual Designer into a fully featured template IDE! You can now import existing AlphaPIL code via reverse-parsing, inspect and render actual local system fonts, test dynamic layouts with mock variable interpolation (`{user}` placeholders), sketch multi-stop linear/radial gradients, resize canvas dimensions, and visually compose advanced charts & graphs ($drawBarChart, $drawLineChart, $drawProgressBar) with live rendering simulations.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **💻 IDE** | **Reverse Parser** | Paste and import any hand-written AlphaPIL code directly into editable visual layers. | [Docs](functions/utils/open_coordinate_picker.md) |
    | **🔤 Typography** | **Local Fonts Discovery** | Discovers actual system fonts on launch and feeds a searchable dropdown inside the Web UI. | [Docs](functions/utils/open_coordinate_picker.md#features) |
    | **📊 Visualization** | **Simulated Charts** | Real-time HTML Canvas simulations for Bar Charts, Line Charts, and Progress Bars. | [Docs](functions/utils/open_coordinate_picker.md#features) |
    | **🌈 Gradients** | **Gradient Builder** | Sketched linear/radial gradient builder inside shapes with angle rotations and multi-stops. | [Docs](functions/utils/open_coordinate_picker.md#features) |
    | **🤖 Interpolation** | **Mock Variables Inspector**| Supports testing `{var}` placeholders live under customizable test variables. | [Docs](functions/utils/open_coordinate_picker.md#features) |
    | **📏 Dimensions** | **Canvas Resize** | Visually modify, scale, and adjust background canvas dimensions dynamically. | [Docs](functions/utils/open_coordinate_picker.md#features) |
    | **🤖 AI** | **Manifest v0.3.0** | Synchronized technical manifest version with the new WYSIWYG Visual Template IDE. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

## May 26, 2026 (v0.2.9)
!!! abstract "Feature Release: Interactive WYSIWYG Visual Template Designer"
    This release upgrades the coordinate picker into a fully fledged visual designer! You can now visually draw text bounding boxes, rectangles, circles, rounded rectangles, and lines directly over your image, manage layering/composition, see live client-side rendering simulations, and instantly copy single snippets or complete multi-line AlphaPIL template code block compositions.

    | Feature | Change | Description | Link |
    | :--- | :--- | :--- | :--- |
    | **🎨 Designer** | **Visual Builder** | Added drawing overlay canvas for real-time visual design and layout modeling. | [Docs](functions/utils/open_coordinate_picker.md) |
    | **🔤 Simulation** | **Text Simulations** | Replicated `drawTextMid` truncation and `drawTextIn` auto-scaling inside the browser. | [Docs](functions/utils/open_coordinate_picker.md#features) |
    | **📚 Composition** | **Layer Management** | Drag to draw, reorder indices, delete layers, and visual composition stack. | [Docs](functions/utils/open_coordinate_picker.md#features) |
    | **💾 Code Export** | **Template Generator** | Instantly export active single-command snippets or entire composed layout templates. | [Docs](functions/functions/utils/open_coordinate_picker.md) |
    | **🤖 AI** | **Manifest v0.2.9** | Synchronized technical manifest version with the new WYSIWYG Visual Designer. | [Manifest](ALPHAPIL_MANIFEST.txt) |

---

*To see previous updates, check our [GitHub Release History](https://github.com/MeraLabs/AlphaPIL/releases).*
