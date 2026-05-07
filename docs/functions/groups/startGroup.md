# startGroup

Starts a new coordinate group. All drawing commands inside the group use coordinates relative to the group's starting point.

## Syntax

```bash
$startGroup[x;y]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position for the group origin. | Required |
| **y** | `int/str` | Y position for the group origin. | Required |

## Example

```bash
$startGroup[100;100]
  # This circle will be drawn at 150, 150 on the main canvas
  $drawCircle[50;50;20;red]
$endGroup
```

!!! info
    Groups can be nested. Offsets from parent groups are added together.
