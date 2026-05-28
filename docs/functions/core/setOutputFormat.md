# setOutputFormat

Sets the target output compression format for the canvas rendering pipeline (e.g., `PNG`, `JPEG`, `WEBP`). This decides how the final image is serialized into bytes or files, allowing you to choose between slow, high-quality lossless formats with transparency (`PNG`) and ultra-fast compressed formats (`JPEG`).

## Syntax

```bash
$setOutputFormat[format]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **format** | `string` | The target image format (e.g., `PNG`, `JPEG`, `WEBP`). | `PNG` |

## Example

```bash
$createCanvas[1080;1620;#000000;1]
$setOutputFormat[JPEG] # Render as JPEG for maximum performance
$drawImage[0;0;resources/theme-irman.png;1080;1620]
```

!!! tip
    JPEG compression is significantly faster than PNG compression. If your template does not require any transparency or alpha channels, setting the format to `JPEG` or `JPG` will drastically improve response and rendering times (saving up to 500ms on server builds).
