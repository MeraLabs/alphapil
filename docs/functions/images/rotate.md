# rotate

Rotates the current main canvas or the active layer by a specific angle in degrees counter-clockwise. This uses high-quality bicubic resampling to maintain edge crispness.

## Syntax

```bash
$rotate[angle;expand]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **angle** | `float` | Angle of rotation in degrees counter-clockwise. | Required |
| **expand** | `bool` | If `true`, expands the canvas size to fully fit the rotated image. If `false`, crops to the original bounds. | `false` |

## Example

```bash
# Create a layer, draw a rectangle, rotate it 45 degrees, and composite it
$createLayer[rotatedBox]
$switchLayer[rotatedBox]
$drawRect[center;center;100;100;gold]
$rotate[45]
$switchLayer[main]
$mergeLayer[rotatedBox;x=150;y=150]
```

!!! info
    When rotating the main canvas or active layers, the drawing context is automatically updated so that subsequent coordinates match the new rotated pixel boundaries.
