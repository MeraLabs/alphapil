# mergeLayer

Composites a layer onto the main canvas or another layer.

## Syntax

```bash
$mergeLayer[name;x;y;opacity;target]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **name** | `string` | Source layer name. | Required |
| **x, y** | `int/str` | Position to paste the layer. | `0, 0` |
| **opacity** | `int` | Opacity percentage. | `100` |
| **target** | `string` | Target layer name (or `main`). | `main` |

## Example

```bash
$mergeLayer[overlay;0;0;50;main]
```
