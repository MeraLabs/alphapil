# switchLayer

Switches subsequent drawing operations to a specific layer. Once switched, any drawing commands (like rectangles, circles, text, or gradients) are rendered directly on that layer rather than the main canvas.

## Syntax

```bash
$switchLayer[name]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **name** | `string` | The target layer name. Use `main`, `canvas`, or leave blank to switch back to the main canvas. | Required |

## Example

```bash
# Create a layer
$createLayer[profileCard]

# Switch drawing context to the layer
$switchLayer[profileCard]
$drawCircle[center;center;50;blue] # This draws on the profileCard layer

# Switch back to the main canvas
$switchLayer[main]
```

!!! note
    To composite a layer back onto the main canvas after drawing on it, use `$mergeLayer`.
