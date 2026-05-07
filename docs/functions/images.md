# Images & Filters

Functions for loading, manipulating, and filtering images.

| Function | Syntax |
| :--- | :--- |
| **drawImage** | `$drawImage[x;y;path_or_url;w;h;opacity;radius;circle]` |
| **useImageAsCanvas** | `$useImageAsCanvas[path_or_url;height_var;width_var;fixed_width;fixed_height]` |
| **imageFilter** | `$imageFilter[filter_name]` |
| **clearImageCache** | `$clearImageCache[]` |

## Examples

### Loading Avatars
You can load images directly from URLs:
```bash
$drawImage[20;20;{avatar_url};60;60;circle=true]
```

### Background Images
```bash
$useImageAsCanvas[assets/bg.png;h;w;800;600]
```

### Applying Filters
```bash
$imageFilter[blur]
$imageFilter[grayscale]
```
