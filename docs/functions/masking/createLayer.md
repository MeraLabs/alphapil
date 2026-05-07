# createLayer

Creates a new transparent layer for complex compositions.

## Syntax

```bash
$createLayer[name]
```

## Parameters

| Parameter | Type | Description |
| :--- | :--- | :--- |
| **name** | `string` | Unique name for the layer. |

## Example

```bash
$createLayer[shadows]
$switchLayer[shadows]
# ... draw things on shadow layer ...
$switchLayer[main]
```
