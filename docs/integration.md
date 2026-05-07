# Python Integration

AlphaPIL is designed to be easily integrated into any Python application, such as web servers (FastAPI/Flask) or Discord bots.

## Basic Usage

The `CanvasEngine` provides an asynchronous `render_template` method that returns the final image as `bytes`.

```python
from alphapil import CanvasEngine
import asyncio

async def main():
    engine = CanvasEngine()
    
    template = """
    $createCanvas[400;200;white]
    $drawText[center;center;Hello {user};black;32]
    """
    
    # Render and get bytes
    image_bytes = await engine.render_template(template, {"user": "Alpha"})
    
    # Save to file
    with open("output.png", "wb") as f:
        f.write(image_bytes)

asyncio.run(main())
```

## Integration with FastAPI

You can serve generated images directly in a web response.

```python
from fastapi import FastAPI, Response
from alphapil import CanvasEngine

app = FastAPI()
engine = CanvasEngine()

@app.get("/generate/{name}")
async def generate_image(name: str):
    template = """
    $createCanvas[500;200;#1a1a1a]
    $drawText[center;center;Welcome {name};white;40]
    """
    
    image_bytes = await engine.render_template(template, {"name": name})
    
    return Response(content=image_bytes, media_type="image/png")
```

## Integration with Discord.py

To use AlphaPIL in a Discord bot, convert the `bytes` into a `discord.File` using `io.BytesIO`.

```python
import discord
from discord.ext import commands
from io import BytesIO
from alphapil import CanvasEngine

class ImageBot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.engine = CanvasEngine()

    @commands.command()
    async def welcome(self, ctx):
        template = "$createCanvas[400;100;blue]$drawText[center;center;Welcome!;white;24]"
        
        # 1. Get bytes from engine
        image_bytes = await self.engine.render_template(template)
        
        # 2. Wrap in BytesIO and create discord.File
        file = discord.File(BytesIO(image_bytes), filename="welcome.png")
        
        # 3. Send to Discord
        await ctx.send(file=file)
```

!!! tip
    The `render_template_file` method is also available if you prefer keeping your AlphaPIL code in separate `.txt` files.
