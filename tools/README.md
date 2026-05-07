# AlphaPIL Developer Tools

This directory contains developer tools for working with AlphaPIL.

## Tools

### 📚 Documentation Generator (`gen_docs.py`)

Automatically generates comprehensive documentation by scanning all modules and extracting function definitions.

**Usage:**
```bash
python tools/gen_docs.py
```

**Features:**
- Scans all files in `src/alphapil/modules/`
- Extracts private methods (starting with `_`)
- Converts method names to command names (e.g., `_drawRect` → `$drawRect`)
- Parses docstrings and arguments
- Generates `COMMANDS.md` in project root

**Output:**
- `COMMANDS.md` - Complete command reference with usage examples

### 🖼️ Live Previewer (`previewer.py`)

Monitors the `templates/` folder and automatically renders templates when saved, providing instant visual feedback.

**Usage:**
```bash
python tools/previewer.py
```

**Features:**
- Real-time template monitoring using `watchdog`
- Automatic rendering on file save
- Dummy data injection for consistent testing
- Visual preview with PIL Image.show()
- Error reporting and debugging information

**Dummy Data:**
The previewer includes comprehensive mock data:
- User info: name, avatar_url, xp, level, rank
- Colors: primary_color, secondary_color, accent_color
- Content: title, subtitle, description
- Dimensions: canvas_width, canvas_height
- Status: online, premium status, verification
- And more...

**Installation:**
```bash
pip install -r tools/requirements.txt
```

## Development Workflow

1. **Start Previewer:**
   ```bash
   python tools/previewer.py
   ```

2. **Edit Templates:**
   - Modify files in `templates/`
   - Changes are automatically rendered and displayed

3. **Update Documentation:**
   ```bash
   python tools/gen_docs.py
   ```
   - Updates `COMMANDS.md` with new functions

4. **Test New Functions:**
   - Add functions to modules
   - Use previewer to test immediately
   - Update docs when ready

## File Structure

```
tools/
├── gen_docs.py      # Documentation generator
├── previewer.py     # Live template previewer
├── requirements.txt  # Tool dependencies
└── README.md        # This file
```

## Tips

- **Previewer**: Press Ctrl+C to stop monitoring
- **Documentation**: Run after adding new functions to modules
- **Dummy Data**: Modify `get_dummy_data()` in `previewer.py` for different test scenarios
- **Error Handling**: Both tools provide detailed error messages for debugging

## Troubleshooting

**Previewer Issues:**
- Ensure `templates/` directory exists
- Install watchdog: `pip install watchdog`
- Check template syntax for errors

**Documentation Issues:**
- Ensure modules have proper docstrings
- Check that functions start with underscore
- Verify module files are in `src/alphapil/modules/`

**Common Issues:**
- Missing imports in modules
- Incorrect function signatures
- Missing docstrings
- Invalid template syntax
