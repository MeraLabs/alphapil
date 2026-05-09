# Getting Started

Learn how to install and start using AlphaPIL in your projects.

## Installation

### From PyPI (Recommended)

```bash
pip install alphapil
```

### From Source (Development)

```bash
git clone https://github.com/MeraLabs/AlphaPIL.git
cd AlphaPIL
pip install -e .
```

## Basic Usage

AlphaPIL uses a "Template Engine" to process image generation commands.

```python
import asyncio
from alphapil import CanvasEngine

async def main():
    # Initialize the engine
    engine = CanvasEngine()

    # Define your template
    template = """
    $createCanvas[500;500;white]
    $drawCircle[250;250;100;red;black;none;5]
    $drawText[250;250;AlphaPIL;black;20;center]
    $save[circle.png]
    """

    # Render the template
    await engine.render(template)

asyncio.run(main())
```

## Using Variables

You can inject variables into your templates using the `{var_name}` syntax.

```python
import asyncio
from alphapil import CanvasEngine

async def main():
    engine = CanvasEngine()
    
    data = {
        "name": "Alpha",
        "color": "#ff0000"
    }

    template = """
    $createCanvas[400;200;{color}]
    $drawText[200;100;Hello {name}!;white;30;center]
    $save[hello.png]
    """

    await engine.render(template, data)

asyncio.run(main())
```
