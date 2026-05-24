# getBytes

Returns the current canvas image as raw bytes in the specified format. This is extremely useful when integrating AlphaPIL into web APIs or webhooks where you want to stream the generated image directly to the client without saving it to disk first.

## Syntax

```bash
$getBytes[format]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **format** | `string` | The image format to export (e.g., `PNG`, `JPEG`, `WEBP`). | `PNG` |

## Example

```bash
$createCanvas[400;400;blue]
$drawCircle[center;center;100;white]
# Return the image directly as JPEG bytes
$getBytes[JPEG]
```

!!! note
    `$getBytes` is often the final command in an API-driven template script to return the image stream back to the calling Python application.
