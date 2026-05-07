# setStroke

Sets the default stroke (outline) properties.

## Syntax

```bash
$setStroke[width;color]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **width** | `int` | Stroke thickness in pixels. | Required |
| **color** | `string` | Stroke color. | `black` |

## Example

```bash
$setStroke[5;red]
$drawRect[10;10;100;100;white;fill=none] # White box with 5px red border
```
