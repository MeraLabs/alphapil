# save

Saves the current state of the canvas to an image file.

## Syntax

```bash
$save[filename]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **filename** | `string` | The path and name of the file to save (e.g., `output.png`). | Required |

## Example

```bash
$createCanvas[400;400;white]
$drawCircle[200;200;100;red]
$save[final_image.png]
```
