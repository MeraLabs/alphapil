# AlphaPIL

### About
**AlphaPIL** is an asynchronous, template-based image generation engine built on top of Pillow (PIL). It is designed to make it easy to build dynamic images using a simple, readable template language.

It is open-source and free to use, providing a powerful recursive parser for handling nested functions in image generation templates, with full support for asynchronous operations.

AlphaPIL is suitable for developers building Discord bots, automated social media graphics, or any application requiring high-performance, template-driven image creation. This package is proudly maintained by the **[MeraLabs](https://github.com/MeraLabs)** organization.

### Features
- **60+ Pre-built Functions**: AlphaPIL comes packed with over 60 pre-built functions for shapes, text manipulation, image filtering, and masking.
- **Asynchronous by Design**: Built from the ground up to support `asyncio`, making it perfect for modern web frameworks and Discord bots.
- **Powerful DSL**: Use a simple `$function[arg1;arg2]` syntax to define your images. Supports nested functions like `$drawText[$toUpper[hello];10;10]`.
- **Advanced Text Rendering**: Support for text gradients, strokes, automatic wrapping, and auto-sizing.
- **Layer & Masking System**: Create complex compositions with multi-layer support and alpha masking.
- **Image Caching**: Built-in caching for remote images to ensure fast rendering during repeated operations.

### Setup
Install AlphaPIL via pip:
```bash
pip install alphapil
```

Basic usage in your Python project:
```python
import asyncio
from alphapil import CanvasEngine

async def main():
    engine = CanvasEngine()
    
    template = """
    $createCanvas[800;400;#1a1a1a]
    $setColor[#ffffff]
    $setFont[Arial;40]
    $drawText[Hello from AlphaPIL!;50;50]
    $save[output.png]
    """
    
    await engine.render_template(template)
    print("Image generated successfully!")

asyncio.run(main())
```

### Rendering with Data
You can inject dynamic data into your templates easily:

```python
data = {
    "username": "Alex",
    "score": "950"
}

template = """
$createCanvas[500;200;white]
$setColor[black]
$setFont[Roboto;30]
$drawText[User: {username};20;20]
$drawText[Score: {score};20;60]
"""

image_bytes = await engine.render_template(template, data=data)
```

### Advanced Masking
AlphaPIL supports complex masking for creating avatars or stylized images:

```python
template = """
$createCanvas[400;400;transparent]
$createLayer[mask]
$drawCircle[200;200;180;white]
$switchLayer[main]
$drawImage[https://example.com/avatar.png;0;0;400;400]
$applyMask[mask]
"""
```

### Support
Need help? Join our official Discord community for support and updates!
**[Join MeraLabs Discord](https://discord.gg/AXbuM6aaeQ)**

### Contributing
Refer to the [Contribution Documentation](https://github.com/MeraLabs/AlphaPIL/blob/main/CONTRIBUTING.md) for more information.

### Keywords
`alphapil` `image-generation` `pillow` `python` `async` `discord-bot` `template-engine` `meralabs` `canvas` `dsl`
