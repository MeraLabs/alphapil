# What's New in AlphaPIL 🚀

Welcome to the latest version of AlphaPIL! We've introduced several powerful features to help you create professional, high-quality images with ease.

---

## Recent Enhancements

| Feature | Description | Documentation |
| :--- | :--- | :--- |
| **💎 High-Res AA** | 4x-8x Supersampling for ultra-smooth edges on shapes and text. | [createCanvas](functions/core/createCanvas.md) |
| **🎯 Container System** | New box-model containers for relative alignment and easier layout design. | [startContainer](functions/groups/startContainer.md) |
| **✨ Linear Gradients** | Multi-stop linear gradients with support for custom rotation angles. | [drawLinearGradient](functions/images/drawLinearGradient.md) |
| **🔆 Radial Gradients** | Create circular glow and lighting effects with radial color transitions. | [drawRadialGradient](functions/images/drawRadialGradient.md) |
| **🌫️ Regional Blur** | Gaussian blur for specific regions, perfect for Glassmorphism effects. | [blur](functions/images/blur.md) |
| **📊 Bar Charts** | Professional, themed bar charts with automatic data scaling. | [drawBarChart](functions/images/drawBarChart.md) |
| **📉 Line Charts** | Clean line graphs for visualizing data trends with multiple themes. | [drawLineChart](functions/images/drawLineChart.md) |
| **⏳ Progress Bars** | Modern rounded progress bars with custom colors and radius. | [drawProgressBar](functions/images/drawProgressBar.md) |

---

## Detailed Changes

### 1. Advanced Anti-Aliasing
You can now enable high-resolution rendering by adding an `aa` factor to `$createCanvas`. This internally renders the image at a higher scale and downsamples it for crisp edges.
*   **Link:** [Anti-Aliasing Guide](functions/core/createCanvas.md)

### 2. Smart Box Model (Containers)
Unlike groups, containers have width and height. Keywords like `center` and `right` now work relative to the active container, allowing for truly responsive-feeling templates.
*   **Link:** [Container System](functions/groups/startContainer.md)

### 3. Data Visualization
Introducing a full charting suite. Pass simple strings of data and labels, and AlphaPIL will handle the layout, scaling, and coloring automatically.
*   **Link:** [Charts Overview](functions/images/drawBarChart.md)

### 4. Optimized Performance
We've removed unnecessary dependencies like `discord.py` from the core package, making AlphaPIL lighter and faster for all environments.
