# getHex

Converts a color name (like standard CSS colors or Discord-specific colors) to its corresponding 6-character hexadecimal color string.

## Syntax

```bash
$getHex[color_name]
```

## Parameters

| Parameter | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| **color_name** | `string` | The color name to convert (e.g., `red`, `blurple`, `gold`). | Required |

## Color Mappings Supported

- **Standard Colors:** `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`, `white`, `black`, `gray`, `orange`, `purple`, `pink`, `brown`, `lime`, `navy`, `teal`, `silver`, `gold`, etc.
- **Discord Palette:** `blurple`, `discord` (`#5865F2`), `green_discord` (`#57F287`), `yellow_discord` (`#FEE75C`), `fuchsia` (`#EB459E`), `red_discord` (`#ED4245`).
- **Variants:** `lightblue`, `lightgreen`, `darkblue`, `darkgreen`, etc.

## Example

```bash
# Get the hex code for Discord's blurple color
$setVar[bpColor;$getHex[blurple]] # Stores "#5865F2"
```
