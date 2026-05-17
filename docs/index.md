# AlphaPIL

![AlphaPIL](https://raw.githubusercontent.com/MeraLabs/AlphaPIL/main/assets/banner.png)

**AlphaPIL** is a powerful, template-based image generation library for Python. It simplifies complex image manipulations using a straightforward, scriptable syntax.

## Why AlphaPIL?

- 🎨 **Syntax Driven** - Create complex layouts with a simple, readable syntax.
- ⚡ **Performant** - Built on top of PIL (Pillow) for fast image processing.
- 🔧 **Extensible** - Easily add new functions and filters.
- 🏆 **Bot Ready** - Perfect for Discord bots, automated reports, and social media cards.

## What's New 🚀

AlphaPIL has been upgraded with modern rendering and layout features!

| Feature | Description | Documentation |
| :--- | :--- | :--- |
| **Anti-Aliasing (AA)** | 4x-8x Supersampling for ultra-smooth edges. | [createCanvas](functions/core/createCanvas.md) |
| **Container System** | Local alignment boxes for easier layouts. | [startContainer](functions/groups/startContainer.md) |
| **Linear Gradients** | Multi-stop gradients with custom rotation. | [drawLinearGradient](functions/images/drawLinearGradient.md) |
| **Radial Gradients** | Circular glow and lighting effects. | [drawRadialGradient](functions/images/drawRadialGradient.md) |
| **Regional Blur** | Glassmorphism and frosting effects. | [blur](functions/images/blur.md) |
| **Modern Charts** | Themed Bar, Line, and Progress charts. | [drawBarChart](functions/images/drawBarChart.md) |

## Quick Example

```bash
$createCanvas[400;200;#2C3E50]
$drawRect[10;10;380;180;#34495E;#1ABC9C]
$drawText[200;100;Hello AlphaPIL!;white;24;center]
$save[output.png]
```

## Community & Support

- [GitHub Repository](https://github.com/MeraLabs/AlphaPIL)
- [Discord Server](https://discord.gg/your-link)
- [Issue Tracker](https://github.com/MeraLabs/AlphaPIL/issues)
