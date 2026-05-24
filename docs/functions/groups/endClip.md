# endClip

Ends the active clipping region defined by a previous `$startClip` call, compositing the clipped artwork back onto the main canvas, and restores normal drawing operations to the parent canvas.

## Syntax

```bash
$endClip[]
```

## Parameters

This function does not take any parameters.

## Example

```bash
$startClip[50;50;200;200;10]
# Draw some shapes that will be clipped
$drawCircle[center;center;120;blue]
$endClip[]
```
