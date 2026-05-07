# random

Generates a random integer within a specified range.

## Syntax

```bash
$random[min;max]
# OR
$random[max] (uses 0 as minimum)
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **min** | `int` | Minimum value. | 0 (if max omitted) |
| **max** | `int` | Maximum value. | Required |

## Example

```bash
$setVar[posX;$random[0;800]]
$drawCircle[{posX};center;20;red]
```

### Nesting
This is very useful for adding "chaos" or variety to your templates:
```bash
$drawRect[0;0;100;100;rgb($random[255],$random[255],$random[255])]
```
