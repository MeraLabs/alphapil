# loadFont

Registers a font file from a local path or a remote URL with an alias.

## Syntax

```bash
$loadFont[path_or_url;alias]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **path_or_url** | `string` | Local path to `.ttf`/`.otf` OR a direct URL to a font file. | Required |
| **alias** | `string` | A shorthand name to use instead of the full path/URL. | Required |

## Example

### Local Font
```bash
$loadFont[./assets/fonts/Bold.ttf;bold]
$drawText[50;50;Local Bold;white;24;bold]
```

### Remote Font (No download needed!)
```bash
$loadFont[https://github.com/google/fonts/raw/main/ofl/roboto/Roboto-Bold.ttf;roboto]
$drawText[50;150;Online Roboto;white;24;roboto]
```

## Where to find Font URLs?

To use remote fonts, you need a **direct link** to a `.ttf` or `.otf` file. 

1.  **Google Fonts (GitHub):** The most reliable source. Visit the [Google Fonts GitHub](https://github.com/google/fonts/tree/main/ofl), navigate to a font, and copy the link to the "Raw" file.
2.  **Discord:** You can upload a font to a Discord channel, right-click the file, and select **Copy Link**.
3.  **Open Source Projects:** Many fonts like *Inter* or *JetBrains Mono* host their files on GitHub.

!!! warning
    The URL must end in `.ttf` or `.otf`. Linking to a website like `fonts.google.com` will not work as those are preview pages, not the font files themselves.
