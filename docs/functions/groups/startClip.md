# startClip

Starts a clipping region. Any elements (images, shapes, text) drawn after calling this function will be confined inside the specified rectangular or rounded rectangular boundaries. Anything extending outside is cropped.

## Syntax

```bash
$startClip[x;y;w;h;radius]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **x** | `int/str` | X position of the clipping boundary (supports `center`). | Required |
| **y** | `int/str` | Y position of the clipping boundary (supports `center`). | Required |
| **w** | `int` | Width of the clipping boundary. | Required |
| **h** | `int` | Height of the clipping boundary. | Required |
| **radius** | `int` | Corner radius to make a rounded rectangular clipping boundary. | `0` (Standard rectangle) |

## Example

```bash
# Clip a user avatar into a rounded profile picture container
$startClip[100;100;80;80;40]
$drawImage[100;100;{avatarUrl};80;80]
$endClip[]
```

!!! note
    Always call `$endClip` to restore normal canvas drawing when you are done with the clipped region.
