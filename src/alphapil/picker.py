#!/usr/bin/env python3
"""
AlphaPIL Interactive Coordinate Picker

This module provides the interactive web-based coordinate picker
that can be run as a CLI tool or launched directly from Python.
"""

import os
import sys
import http.server
import socketserver
import webbrowser
import threading
import socket

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def generate_html(image_path, server_root, output_dir):
    # Determine paths relative to server_root (where the server runs)
    try:
        rel_image_path = os.path.relpath(image_path, server_root)
    except ValueError:
        rel_image_path = os.path.abspath(image_path)

    # Use forward slashes for HTML URLs
    rel_image_path = rel_image_path.replace(os.sep, '/')

    # Discover system fonts on launch to feed searchable dropdown
    system_fonts = []
    try:
        from .modules.text import TextMixin
        class FontDiscoverer(TextMixin):
            def __init__(self):
                self._system_fonts = {}
                self.errors = []
            def get_fonts(self):
                self._discover_system_fonts()
                return sorted(list(set([k.title() for k in self._system_fonts.keys() if not k.endswith(('.ttf', '.otf'))])))
        fd = FontDiscoverer()
        system_fonts = fd.get_fonts()
    except Exception:
        system_fonts = ["Arial", "Courier New", "Georgia", "Impact", "Times New Roman", "Trebuchet MS", "Verdana"]

    import json
    system_fonts_json = json.dumps(system_fonts)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AlphaPIL Visual IDE & Designer 🎯</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
        }}

        body {{
            background: radial-gradient(circle at top right, #1b1b32, #08080f);
            color: #f1f1f7;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }}

        header {{
            background: rgba(10, 10, 20, 0.85);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding: 12px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .logo {{
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.5px;
            background: linear-gradient(135deg, #5865F2, #57F287);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .logo-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #57F287;
            box-shadow: 0 0 12px #57F287;
        }}

        .main-container {{
            display: flex;
            flex: 1;
            padding: 20px 40px;
            gap: 30px;
            max-width: 1920px;
            margin: 0 auto;
            width: 100%;
        }}

        .picker-area {{
            flex: 1;
            background: rgba(10, 10, 20, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 24px;
            display: flex;
            padding: 20px;
            position: relative;
            min-height: 650px;
            max-height: 85vh;
            overflow: auto;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }}

        .image-wrapper {{
            position: relative;
            cursor: crosshair;
            display: inline-block;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.12);
            transition: width 0.2s, height 0.2s;
            margin: auto;
        }}

        #target-img {{
            max-width: 100%;
            height: auto;
            display: block;
            user-select: none;
            -webkit-user-drag: none;
        }}

        #overlay-canvas {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 10;
        }}

        .reticle-x, .reticle-y {{
            position: absolute;
            background: rgba(88, 101, 242, 0.35);
            pointer-events: none;
            display: none;
            z-index: 5;
        }}
        .reticle-x {{ height: 100%; width: 1px; top: 0; }}
        .reticle-y {{ width: 100%; height: 1px; left: 0; }}

        .control-panel {{
            width: 480px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            overflow-y: auto;
            max-height: 85vh;
            padding-right: 4px;
        }}

        .panel-card {{
            background: rgba(20, 20, 35, 0.7);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }}

        .panel-title {{
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 12px;
            color: #a5a5cc;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding-bottom: 6px;
        }}

        .coordinate-display {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
        }}

        .coord-box {{
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 8px;
            text-align: center;
        }}

        .coord-label {{
            font-size: 9px;
            font-weight: 600;
            color: #7d7db5;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 2px;
        }}

        .coord-value {{
            font-size: 22px;
            font-weight: 800;
            color: #ffffff;
        }}

        /* Tool Grid */
        .tool-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 6px;
        }}

        .tool-btn {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 8px 4px;
            color: #b5b5d5;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            transition: all 0.2s ease;
        }}

        .tool-btn:hover {{
            background: rgba(255, 255, 255, 0.06);
            color: #ffffff;
            border-color: rgba(88, 101, 242, 0.4);
        }}

        .tool-btn.active {{
            background: rgba(88, 101, 242, 0.15);
            border-color: #5865F2;
            color: #ffffff;
            box-shadow: 0 0 10px rgba(88, 101, 242, 0.25);
        }}

        .tool-icon {{
            font-size: 16px;
        }}

        /* Styling Inputs */
        .input-group {{
            margin-bottom: 10px;
        }}

        .input-label {{
            display: block;
            font-size: 11px;
            color: #8c8caf;
            margin-bottom: 4px;
            font-weight: 600;
        }}

        .input-field {{
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 6px 10px;
            color: white;
            font-size: 12px;
            outline: none;
            transition: border-color 0.2s ease;
        }}

        .input-field:focus {{
            border-color: #5865F2;
        }}

        .inline-inputs {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}

        .color-picker-wrapper {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .color-input-preview {{
            width: 28px;
            height: 28px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            cursor: pointer;
            padding: 0;
            background: none;
        }}

        /* Variables list */
        .var-row {{
            display: grid;
            grid-template-columns: 1fr 1fr 28px;
            gap: 8px;
            margin-bottom: 6px;
            align-items: center;
        }}

        .add-var-btn {{
            background: rgba(87, 242, 135, 0.15);
            border: 1px dashed #57F287;
            color: #57F287;
            padding: 6px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 11px;
            font-weight: 600;
            text-align: center;
            width: 100%;
            margin-top: 6px;
        }}

        /* Layer List */
        .layer-list {{
            max-height: 180px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}

        .layer-item {{
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 6px 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 11px;
        }}

        .layer-info {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: #d1d1e0;
        }}

        .layer-actions {{
            display: flex;
            gap: 4px;
        }}

        .layer-action-btn {{
            background: none;
            border: none;
            color: #8c8caf;
            cursor: pointer;
            padding: 2px;
            border-radius: 4px;
            font-size: 11px;
        }}

        .layer-action-btn:hover {{
            color: #ff4d4d;
            background: rgba(255, 77, 77, 0.1);
        }}

        .layer-action-btn.move:hover {{
            color: #57F287;
            background: rgba(87, 242, 135, 0.1);
        }}

        /* Code export/import */
        .clipboard-box {{
            background: rgba(0, 0, 0, 0.3);
            border: 1px dashed rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: monospace;
            font-size: 11px;
            color: #e2e2f0;
            cursor: pointer;
            margin-top: 6px;
        }}

        .copy-tag {{
            font-size: 9px;
            color: #5865F2;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}

        .full-code-area {{
            width: 100%;
            height: 110px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 6px;
            padding: 8px;
            color: #57F287;
            font-family: monospace;
            font-size: 10.5px;
            resize: none;
            outline: none;
            margin-bottom: 6px;
        }}

        .primary-btn {{
            width: 100%;
            background: linear-gradient(135deg, #5865F2, #4752c4);
            border: none;
            border-radius: 6px;
            color: white;
            padding: 8px;
            font-weight: 600;
            font-size: 12px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }}

        .primary-btn:hover {{
            box-shadow: 0 4px 12px rgba(88, 101, 242, 0.3);
        }}

        .toast {{
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: #57F287;
            color: #0c0c14;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 14px;
            box-shadow: 0 10px 25px rgba(87, 242, 135, 0.4);
            transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .toast.show {{
            transform: translateX(-50%) translateY(0);
        }}

        .upload-area {{
            border: 2px dashed rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 12px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .upload-area:hover {{
            border-color: #5865F2;
            background: rgba(88, 101, 242, 0.05);
        }}
    </style>
</head>
<body>

    <header>
        <div class="logo">
            <div class="logo-dot"></div>
            AlphaPIL IDE & Visualizer 🎯
        </div>
        <div style="font-size: 13px; color: #a5a5cc;">Canvas: <span id="canvas-size-header" style="color: white; font-weight: 600;">Loading...</span></div>
    </header>

    <div class="main-container">
        <!-- Visual Designing Canvas -->
        <div class="picker-area">
            <div class="image-wrapper" id="img-wrapper">
                <img id="target-img" src="/{rel_image_path}" alt="Rendered Canvas">
                <canvas id="overlay-canvas"></canvas>
                <div class="reticle-x" id="reticle-x"></div>
                <div class="reticle-y" id="reticle-y"></div>
            </div>
        </div>

        <div class="control-panel">
            <!-- Canvas Resizing Settings -->
            <div class="panel-card">
                <div class="panel-title">
                    <span>📏 Canvas Size settings</span>
                </div>
                <div class="inline-inputs">
                    <div class="input-group">
                        <label class="input-label">Canvas Width (px)</label>
                        <input type="number" class="input-field" id="canvas-w" oninput="resizeCanvasVisuals()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Canvas Height (px)</label>
                        <input type="number" class="input-field" id="canvas-h" oninput="resizeCanvasVisuals()">
                    </div>
                </div>
                <div class="coordinate-display" style="margin-top: 8px;">
                    <div class="coord-box">
                        <div class="coord-label">Cursor X</div>
                        <div class="coord-value" id="val-x">0</div>
                    </div>
                    <div class="coord-box">
                        <div class="coord-label">Cursor Y</div>
                        <div class="coord-value" id="val-y">0</div>
                    </div>
                </div>
            </div>

            <!-- Visual Tools selector grid -->
            <div class="panel-card">
                <div class="panel-title">
                    <span>🛠️ Designer Tools</span>
                </div>
                <div class="tool-grid">
                    <button class="tool-btn active" onclick="setTool('inspector')">
                        <span class="tool-icon">🎯</span>
                        <span>Inspect</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawText')">
                        <span class="tool-icon">🔤</span>
                        <span>Text</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawTextMid')">
                        <span class="tool-icon">↔️</span>
                        <span>TextMid</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawTextIn')">
                        <span class="tool-icon">↕️</span>
                        <span>TextIn</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawRect')">
                        <span class="tool-icon">🟩</span>
                        <span>Rect</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawRoundedRect')">
                        <span class="tool-icon">🟢</span>
                        <span>R-Rect</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawCircle')">
                        <span class="tool-icon">🟡</span>
                        <span>Circle</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawLine')">
                        <span class="tool-icon">➖</span>
                        <span>Line</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawImage')">
                        <span class="tool-icon">🖼️</span>
                        <span>Image</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawBarChart')">
                        <span class="tool-icon">📊</span>
                        <span>BarChart</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawLineChart')">
                        <span class="tool-icon">📈</span>
                        <span>LineChart</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawProgressBar')">
                        <span class="tool-icon">⏳</span>
                        <span>Progress</span>
                    </button>
                </div>
            </div>

            <!-- Variables & Interpolation Dashboard -->
            <div class="panel-card">
                <div class="panel-title">
                    <span>🤖 Mock Variables Inspector</span>
                </div>
                <div id="vars-list-container">
                    <!-- Dynamic variable rows here -->
                </div>
                <button class="add-var-btn" onclick="addMockVariableRow()">➕ Add Variable Row</button>
            </div>

            <!-- Import existing templates -->
            <div class="panel-card">
                <div class="panel-title">
                    <span>📥 Import AlphaPIL Code</span>
                </div>
                <textarea class="full-code-area" id="import-code-area" placeholder="Paste your AlphaPIL template code here..."></textarea>
                <button class="primary-btn" onclick="importAlphaPILCode()">
                    <span>⚡</span> Import & Parse Template
                </button>
            </div>

            <!-- Contextual Styling Config Box -->
            <div class="panel-card" id="settings-card" style="display: none;">
                <div class="panel-title" id="settings-title">
                    <span>⚙️ Styling Controls</span>
                </div>
                
                <!-- Text Configurations -->
                <div id="settings-group-text" style="display: none;">
                    <div class="input-group">
                        <label class="input-label">Text Content (Supports {{user}} variable placeholders)</label>
                        <input type="text" class="input-field" id="ctrl-text-content" value="Welcome {{user}}" oninput="updateActiveElement()">
                    </div>
                    <div class="inline-inputs">
                        <div class="input-group">
                            <label class="input-label">Font Family</label>
                            <select class="input-field" id="ctrl-font-family" onchange="updateActiveElement()"></select>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Font Size (px)</label>
                            <input type="text" class="input-field" id="ctrl-font-size" value="32" oninput="updateActiveElement()">
                        </div>
                    </div>
                    <div class="inline-inputs">
                        <div class="input-group">
                            <label class="input-label">Text Color</label>
                            <div class="color-picker-wrapper">
                                <input type="color" class="color-input-preview" id="ctrl-text-color-picker" value="#ffffff" oninput="syncColorInput('ctrl-text-color-picker', 'ctrl-text-color-text')">
                                <input type="text" class="input-field" id="ctrl-text-color-text" value="#ffffff" oninput="syncColorText('ctrl-text-color-text', 'ctrl-text-color-picker')">
                            </div>
                        </div>
                        <div class="input-group" id="anchor-wrapper">
                            <label class="input-label">Anchor Alignment</label>
                            <select class="input-field" id="ctrl-text-anchor" onchange="updateActiveElement()">
                                <option value="left">Left</option>
                                <option value="center">Center</option>
                                <option value="right">Right</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- Shapes & Outlines Configurations -->
                <div id="settings-group-shape" style="display: none;">
                    <div class="inline-inputs">
                        <div class="input-group">
                            <label class="input-label">Outline Color</label>
                            <div class="color-picker-wrapper">
                                <input type="color" class="color-input-preview" id="ctrl-outline-color-picker" value="#ffffff" oninput="syncColorInput('ctrl-outline-color-picker', 'ctrl-outline-color-text')">
                                <input type="text" class="input-field" id="ctrl-outline-color-text" value="#ffffff" oninput="syncColorText('ctrl-outline-color-text', 'ctrl-outline-color-picker')">
                            </div>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Fill Customization</label>
                            <select class="input-field" id="ctrl-fill-mode" onchange="toggleFillMode(this.value)">
                                <option value="solid">Solid Color</option>
                                <option value="none">Transparent</option>
                                <option value="gradient">Gradient Fill</option>
                            </select>
                        </div>
                    </div>
                    
                    <!-- Solid Fill Color Box -->
                    <div class="input-group" id="solid-fill-wrapper">
                        <label class="input-label">Solid Fill Color</label>
                        <div class="color-picker-wrapper">
                            <input type="color" class="color-input-preview" id="ctrl-fill-color-picker" value="#5865F2" oninput="syncColorInput('ctrl-fill-color-picker', 'ctrl-fill-color-text')">
                            <input type="text" class="input-field" id="ctrl-fill-color-text" value="#5865F2" oninput="syncColorText('ctrl-fill-color-text', 'ctrl-fill-color-picker')">
                        </div>
                    </div>

                    <!-- Gradients Visual Customizer Box -->
                    <div id="gradient-fill-wrapper" style="display: none; background: rgba(0,0,0,0.15); padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid rgba(255,255,255,0.05);">
                        <div class="inline-inputs">
                            <div class="input-group">
                                <label class="input-label">Gradient Type</label>
                                <select class="input-field" id="ctrl-grad-type" onchange="updateActiveElement()">
                                    <option value="linear">Linear</option>
                                    <option value="radial">Radial</option>
                                </select>
                            </div>
                            <div class="input-group" id="grad-angle-group">
                                <label class="input-label">Linear Angle (deg)</label>
                                <input type="range" min="0" max="360" value="90" id="ctrl-grad-angle" style="width: 100%;" oninput="updateActiveElement()">
                            </div>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Color Stops (Semicolon Separated: color,offset)</label>
                            <input type="text" class="input-field" id="ctrl-grad-stops" value="#ff0000,0;#0000ff,1" oninput="updateActiveElement()">
                        </div>
                    </div>

                    <div class="inline-inputs">
                        <div class="input-group">
                            <label class="input-label">Line Width (`lw`)</label>
                            <input type="text" class="input-field" id="ctrl-shape-lw" value="2" oninput="updateActiveElement()">
                        </div>
                        <div class="input-group" id="radius-wrapper">
                            <label class="input-label">Corner Radius (`radius`)</label>
                            <input type="text" class="input-field" id="ctrl-shape-radius" value="12" oninput="updateActiveElement()">
                        </div>
                    </div>
                </div>

                <!-- Images Configurations -->
                <div id="settings-group-image" style="display: none;">
                    <div class="input-group">
                        <label class="input-label">Local Image Path</label>
                        <input type="text" class="input-field" id="ctrl-image-path" value="resources/theme-irman.png" oninput="updateActiveElement()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Opacity (0.0 to 1.0)</label>
                        <input type="text" class="input-field" id="ctrl-image-opacity" value="1.0" oninput="updateActiveElement()">
                    </div>
                </div>

                <!-- Data Visualization Charts Configurations -->
                <div id="settings-group-chart" style="display: none;">
                    <div class="inline-inputs">
                        <div class="input-group">
                            <label class="input-label">Data Values (Comma Separated)</label>
                            <input type="text" class="input-field" id="ctrl-chart-vals" value="30,80,50,90,40" oninput="updateActiveElement()">
                        </div>
                        <div class="input-group" id="chart-labels-group">
                            <label class="input-label">Labels (Comma Separated)</label>
                            <input type="text" class="input-field" id="ctrl-chart-labels" value="Jan,Feb,Mar,Apr,May" oninput="updateActiveElement()">
                        </div>
                    </div>
                    <div class="inline-inputs">
                        <div class="input-group">
                            <label class="input-label">Chart Color Theme</label>
                            <select class="input-field" id="ctrl-chart-theme" onchange="updateActiveElement()">
                                <option value="blue">Ocean Blue</option>
                                <option value="green">Emerald Green</option>
                                <option value="modern">Modern Purple</option>
                                <option value="dark">Charcoal Gold</option>
                                <option value="neon">Neon Electric</option>
                            </select>
                        </div>
                        <div class="input-group">
                            <label class="input-label">Gap / Rounding</label>
                            <div class="inline-inputs">
                                <input type="number" class="input-field" id="ctrl-chart-gap" value="15" oninput="updateActiveElement()">
                                <input type="number" class="input-field" id="ctrl-chart-radius" value="6" oninput="updateActiveElement()">
                            </div>
                        </div>
                    </div>
                    <div class="inline-inputs" id="chart-extra-group">
                        <div class="input-group">
                            <label class="input-label">Max Scaled Value</label>
                            <input type="text" class="input-field" id="ctrl-chart-maxval" value="" placeholder="Auto" oninput="updateActiveElement()">
                        </div>
                        <div class="input-group" style="display: flex; align-items: center; gap: 6px; padding-top: 18px;">
                            <label style="cursor: pointer; font-size: 12px; color: #a5a5cc;">
                                <input type="checkbox" id="ctrl-chart-showlabels" checked onchange="updateActiveElement()"> Show Labels
                            </label>
                        </div>
                    </div>
                </div>

                <!-- Generated Snippet -->
                <div style="margin-top: 12px;">
                    <label class="input-label">Active Element Code Snippet:</label>
                    <div class="clipboard-box" onclick="copyActiveCode()">
                        <span id="active-snippet-text">Click and drag canvas to generate code</span>
                        <span class="copy-tag">COPY</span>
                    </div>
                </div>
            </div>

            <!-- Visual Composed Layers Card -->
            <div class="panel-card" id="layers-card" style="display: none;">
                <div class="panel-title">
                    <span>📚 Composed Layers</span>
                </div>
                <div class="layer-list" id="layers-list-container">
                    <!-- Dynamic Layer items here -->
                </div>
            </div>

            <!-- Composed Full Template Export Card -->
            <div class="panel-card" id="code-export-card" style="display: none;">
                <div class="panel-title">
                    <span>💾 Generated AlphaPIL Template</span>
                </div>
                <textarea class="full-code-area" id="full-template-code" readonly></textarea>
                <button class="primary-btn" onclick="copyFullTemplate()">
                    <span>📋</span> Copy Full Template Code
                </button>
            </div>

            <!-- Load Different Image Card -->
            <div class="panel-card">
                <div class="panel-title">
                    <span>📁 Load Background</span>
                </div>
                <div class="upload-area" onclick="document.getElementById('file-input').click()">
                    <div class="upload-text">Click to Browse/Drop Image</div>
                    <input type="file" id="file-input" style="display: none;" accept="image/*" onchange="loadFile(event)">
                </div>
            </div>
        </div>
    </div>

    <div class="toast" id="toast">
        <span id="toast-message">✅ Operation successful!</span>
    </div>

    <script>
        const img = document.getElementById('target-img');
        const canvas = document.getElementById('overlay-canvas');
        const ctx = canvas.getContext('2d');
        const valX = document.getElementById('val-x');
        const valY = document.getElementById('val-y');
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toast-message');

        // Dynamic System Fonts
        const systemFonts = {system_fonts_json};
        
        // Populate system fonts searchable list
        const fontDropdown = document.getElementById('ctrl-font-family');
        systemFonts.forEach(font => {{
            const opt = document.createElement('option');
            opt.value = font;
            opt.innerText = font;
            fontDropdown.appendChild(opt);
        }});
        
        // Designer States
        let elements = [];
        let activeTool = 'inspector';
        let isDrawing = false;
        let startX = 0, startY = 0;
        let currentX = 0, currentY = 0;
        let activeElementId = null;
        
        // Mock variables
        let mockVariables = {{
            user: "AlphaUser",
            title: "Captain America",
            margin: "30"
        }};

        // Initialize variables inspector on launch
        updateMockVariablesDashboard();

        // Canvas sizing states
        img.onload = () => {{
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            document.getElementById('canvas-w').value = img.naturalWidth;
            document.getElementById('canvas-h').value = img.naturalHeight;
            document.getElementById('canvas-size-header').innerText = `${{img.naturalWidth}}x${{img.naturalHeight}}`;
            drawAll();
        }};
        
        if (img.complete) {{
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            document.getElementById('canvas-w').value = img.naturalWidth;
            document.getElementById('canvas-h').value = img.naturalHeight;
            document.getElementById('canvas-size-header').innerText = `${{img.naturalWidth}}x${{img.naturalHeight}}`;
            setTimeout(drawAll, 200);
        }}

        // Scale inputs & canvas visual dimensions
        function resizeCanvasVisuals() {{
            const w = parseInt(document.getElementById('canvas-w').value) || img.naturalWidth;
            const h = parseInt(document.getElementById('canvas-h').value) || img.naturalHeight;
            canvas.width = w;
            canvas.height = h;
            img.style.width = w + 'px';
            img.style.height = h + 'px';
            document.getElementById('canvas-size-header').innerText = `${{w}}x${{h}}`;
            drawAll();
        }}

        // Translate cursor Client positions to natural pixel dimensions
        function getCoords(e) {{
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            return {{
                x: Math.floor((e.clientX - rect.left) * scaleX),
                y: Math.floor((e.clientY - rect.top) * scaleY),
                cx: e.clientX - rect.left,
                cy: e.clientY - rect.top
            }};
        }}

        // Variable interpolation solver
        function resolveVars(str) {{
            if (typeof str !== 'string') return str;
            // Solve {{variable}} replacements
            return str.replace(/\\{{(\\w+)\\}}/g, (match, name) => {{
                return mockVariables[name] !== undefined ? mockVariables[name] : match;
            }});
        }}

        // Coordinate Solver with dynamic variables and basic mathematical operations
        function parseCoord(val) {{
            const resolved = resolveVars(String(val));
            try {{
                // Sanitize mathematical characters only
                const sanitized = resolved.replace(/[^0-9\\\\+\\\\-\\\\*\\\\/\\\\%\\\\(\\\\)\\\\.\\\\s]/g, '');
                return Function(`"use strict"; return (${{sanitized}})` )();
            }} catch(e) {{
                return parseInt(resolved) || 0;
            }}
        }}

        // Variables Inspector list rendering
        function updateMockVariablesDashboard() {{
            const container = document.getElementById('vars-list-container');
            container.innerHTML = '';
            
            Object.keys(mockVariables).forEach(key => {{
                const row = document.createElement('div');
                row.className = 'var-row';
                row.innerHTML = `
                    <input type="text" class="input-field" value="${{key}}" onchange="renameMockVariable('${{key}}', this.value)" placeholder="var_name">
                    <input type="text" class="input-field" value="${{mockVariables[key]}}" oninput="setMockVariableValue('${{key}}', this.value)" placeholder="value">
                    <button class="layer-action-btn" onclick="deleteMockVariable('${{key}}')">🗑️</button>
                `;
                container.appendChild(row);
            }});
        }}

        function setMockVariableValue(key, val) {{
            mockVariables[key] = val;
            drawAll();
            updateLayersPanel();
        }}

        function renameMockVariable(oldKey, newKey) {{
            if (!newKey || oldKey === newKey) return;
            mockVariables[newKey] = mockVariables[oldKey];
            delete mockVariables[oldKey];
            updateMockVariablesDashboard();
            drawAll();
            updateLayersPanel();
        }}

        function deleteMockVariable(key) {{
            delete mockVariables[key];
            updateMockVariablesDashboard();
            drawAll();
            updateLayersPanel();
        }}

        function addMockVariableRow() {{
            const newKey = 'var_' + Object.keys(mockVariables).length;
            mockVariables[newKey] = 'value';
            updateMockVariablesDashboard();
            drawAll();
        }}

        // Handle Active Tool Selections
        function setTool(toolName) {{
            activeTool = toolName;
            
            document.querySelectorAll('.tool-btn').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.querySelector('.tool-icon').parentElement.onclick.toString().includes(toolName)) {{
                    btn.classList.add('active');
                }}
            }});

            const settingsCard = document.getElementById('settings-card');
            const gText = document.getElementById('settings-group-text');
            const gShape = document.getElementById('settings-group-shape');
            const gImg = document.getElementById('settings-group-image');
            const gChart = document.getElementById('settings-group-chart');
            
            if (toolName === 'inspector') {{
                settingsCard.style.display = 'none';
            }} else {{
                settingsCard.style.display = 'block';
                gText.style.display = (toolName.startsWith('drawText')) ? 'block' : 'none';
                gShape.style.display = (toolName.startsWith('drawRect') || toolName === 'drawRoundedRect' || toolName === 'drawCircle' || toolName === 'drawLine') ? 'block' : 'none';
                gImg.style.display = (toolName === 'drawImage') ? 'block' : 'none';
                gChart.style.display = (toolName.startsWith('drawBarChart') || toolName === 'drawLineChart' || toolName === 'drawProgressBar') ? 'block' : 'none';

                // Contextual sub-elements display
                document.getElementById('anchor-wrapper').style.display = (toolName === 'drawText') ? 'block' : 'none';
                document.getElementById('radius-wrapper').style.display = (toolName === 'drawRoundedRect') ? 'block' : 'none';
                document.getElementById('chart-labels-group').style.display = (toolName !== 'drawProgressBar') ? 'block' : 'none';
                document.getElementById('chart-extra-group').style.display = (toolName !== 'drawProgressBar') ? 'grid' : 'none';
                
                document.getElementById('settings-title').querySelector('span').innerText = `⚙️ ${{toolName}} Controls`;
                document.getElementById('active-snippet-text').innerText = "Click and drag canvas to generate code";
            }}
            drawAll();
        }}

        // Color & fill controls toggles
        function toggleFillMode(mode) {{
            const solidWrapper = document.getElementById('solid-fill-wrapper');
            const gradWrapper = document.getElementById('gradient-fill-wrapper');
            
            if (mode === 'solid') {{
                solidWrapper.style.display = 'block';
                gradWrapper.style.display = 'none';
            }} else if (mode === 'gradient') {{
                solidWrapper.style.display = 'none';
                gradWrapper.style.display = 'block';
            }} else {{
                solidWrapper.style.display = 'none';
                gradWrapper.style.display = 'none';
            }}
            updateActiveElement();
        }}

        function syncColorInput(pickerId, textId) {{
            document.getElementById(textId).value = document.getElementById(pickerId).value;
            updateActiveElement();
        }}

        function syncColorText(textId, pickerId) {{
            const val = document.getElementById(textId).value;
            if (/^#[0-9A-F]((6))$/i.test(val) || /^#[0-9A-F]((3))$/i.test(val)) {{
                document.getElementById(pickerId).value = val;
            }}
            updateActiveElement();
        }}

        // Canvas Interactions (Click & Drags)
        canvas.addEventListener('mousedown', (e) => {{
            const coord = getCoords(e);
            
            if (activeTool === 'inspector') {{
                const coordinates = `${{coord.x}};${{coord.y}}`;
                copyText(coordinates, "Coordinates copied!");
                return;
            }}

            isDrawing = true;
            startX = coord.x;
            startY = coord.y;
            currentX = startX;
            currentY = startY;

            if (activeTool === 'drawText') {{
                isDrawing = false;
                const newElem = createNewElement(startX, startY, 0, 0);
                elements.push(newElem);
                activeElementId = newElem.id;
                drawAll();
                updateLayersPanel();
            }}
        }});

        canvas.addEventListener('mousemove', (e) => {{
            const coord = getCoords(e);
            
            const rect = canvas.getBoundingClientRect();
            if (coord.x >= 0 && coord.x <= canvas.width && coord.y >= 0 && coord.y <= canvas.height) {{
                valX.innerText = coord.x;
                valY.innerText = coord.y;
                
                const rx = document.getElementById('reticle-x');
                const ry = document.getElementById('reticle-y');
                rx.style.left = coord.cx + 'px';
                rx.style.display = 'block';
                
                ry.style.top = coord.cy + 'px';
                ry.style.display = 'block';
            }} else {{
                hideReticle();
            }}

            if (!isDrawing) return;
            currentX = coord.x;
            currentY = coord.y;
            
            drawAll();
            drawPreviewShape();
        }});

        window.addEventListener('mouseup', (e) => {{
            if (!isDrawing) return;
            isDrawing = false;
            
            const w = currentX - startX;
            const h = currentY - startY;
            
            if (Math.abs(w) < 4 && Math.abs(h) < 4 && activeTool !== 'drawCircle' && activeTool !== 'drawLine') {{
                return;
            }}

            const newElem = createNewElement(startX, startY, w, h);
            elements.push(newElem);
            activeElementId = newElem.id;
            
            drawAll();
            updateLayersPanel();
        }});

        function hideReticle() {{
            document.getElementById('reticle-x').style.display = 'none';
            document.getElementById('reticle-y').style.display = 'none';
        }}

        // Dynamic Elements Constructors
        function createNewElement(x, y, w, h) {{
            let nx = w < 0 ? x + w : x;
            let ny = h < 0 ? y + h : y;
            let nw = Math.abs(w);
            let nh = Math.abs(h);

            const elem = {{
                id: Date.now() + Math.random(),
                type: activeTool,
                params: {{}}
            }};

            if (activeTool.startsWith('drawText')) {{
                elem.params = {{
                    x: nx,
                    y: ny,
                    w: nw || 200,
                    h: nh || 60,
                    text: document.getElementById('ctrl-text-content').value,
                    font: document.getElementById('ctrl-font-family').value,
                    size: document.getElementById('ctrl-font-size').value,
                    color: document.getElementById('ctrl-text-color-text').value,
                    anchor: document.getElementById('ctrl-text-anchor').value
                }};
            }} else if (activeTool === 'drawRect' || activeTool === 'drawRoundedRect' || activeTool === 'drawCircle' || activeTool === 'drawLine') {{
                const fillMode = document.getElementById('ctrl-fill-mode').value;
                let fill = 'none';
                if (fillMode === 'solid') fill = document.getElementById('ctrl-fill-color-text').value;
                else if (fillMode === 'gradient') fill = 'gradient';

                elem.params = {{
                    x: nx,
                    y: ny,
                    w: nw,
                    h: nh,
                    x1: x,
                    y1: y,
                    x2: currentX,
                    y2: currentY,
                    color: document.getElementById('ctrl-outline-color-text').value,
                    fill: fill,
                    lw: document.getElementById('ctrl-shape-lw').value,
                    radius: document.getElementById('ctrl-shape-radius').value,
                    gradType: document.getElementById('ctrl-grad-type').value,
                    gradStops: document.getElementById('ctrl-grad-stops').value,
                    gradAngle: document.getElementById('ctrl-grad-angle').value
                }};
                
                if (activeTool === 'drawCircle') {{
                    let dx = currentX - x;
                    let dy = currentY - y;
                    elem.params.radius = Math.floor(Math.sqrt(dx*dx + dy*dy));
                }}
            }} else if (activeTool === 'drawImage') {{
                elem.params = {{
                    x: nx,
                    y: ny,
                    w: nw || 150,
                    h: nh || 150,
                    path: document.getElementById('ctrl-image-path').value,
                    opacity: document.getElementById('ctrl-image-opacity').value
                }};
            }} else if (activeTool.startsWith('drawBarChart') || activeTool === 'drawLineChart' || activeTool === 'drawProgressBar') {{
                elem.params = {{
                    x: nx,
                    y: ny,
                    w: nw || 300,
                    h: nh || 180,
                    vals: document.getElementById('ctrl-chart-vals').value,
                    labels: document.getElementById('ctrl-chart-labels').value,
                    theme: document.getElementById('ctrl-chart-theme').value,
                    gap: parseInt(document.getElementById('ctrl-chart-gap').value) || 15,
                    radius: parseInt(document.getElementById('ctrl-chart-radius').value) || 6,
                    maxval: document.getElementById('ctrl-chart-maxval').value,
                    showlabels: document.getElementById('ctrl-chart-showlabels').checked
                }};
            }}

            return elem;
        }}

        // Update parameters on styling controls inputs
        function updateActiveElement() {{
            if (!activeElementId) return;
            const elem = elements.find(el => el.id === activeElementId);
            if (!elem) return;

            if (elem.type.startsWith('drawText')) {{
                elem.params.text = document.getElementById('ctrl-text-content').value;
                elem.params.font = document.getElementById('ctrl-font-family').value;
                elem.params.size = document.getElementById('ctrl-font-size').value;
                elem.params.color = document.getElementById('ctrl-text-color-text').value;
                elem.params.anchor = document.getElementById('ctrl-text-anchor').value;
            }} else if (elem.type === 'drawRect' || elem.type === 'drawRoundedRect' || elem.type === 'drawCircle' || elem.type === 'drawLine') {{
                const fillMode = document.getElementById('ctrl-fill-mode').value;
                let fill = 'none';
                if (fillMode === 'solid') fill = document.getElementById('ctrl-fill-color-text').value;
                else if (fillMode === 'gradient') fill = 'gradient';

                elem.params.color = document.getElementById('ctrl-outline-color-text').value;
                elem.params.fill = fill;
                elem.params.lw = document.getElementById('ctrl-shape-lw').value;
                elem.params.radius = document.getElementById('ctrl-shape-radius').value;
                elem.params.gradType = document.getElementById('ctrl-grad-type').value;
                elem.params.gradStops = document.getElementById('ctrl-grad-stops').value;
                elem.params.gradAngle = document.getElementById('ctrl-grad-angle').value;
            }} else if (elem.type === 'drawImage') {{
                elem.params.path = document.getElementById('ctrl-image-path').value;
                elem.params.opacity = document.getElementById('ctrl-image-opacity').value;
            }} else if (elem.type.startsWith('drawBarChart') || elem.type === 'drawLineChart' || elem.type === 'drawProgressBar') {{
                elem.params.vals = document.getElementById('ctrl-chart-vals').value;
                elem.params.labels = document.getElementById('ctrl-chart-labels').value;
                elem.params.theme = document.getElementById('ctrl-chart-theme').value;
                elem.params.gap = parseInt(document.getElementById('ctrl-chart-gap').value) || 15;
                elem.params.radius = parseInt(document.getElementById('ctrl-chart-radius').value) || 6;
                elem.params.maxval = document.getElementById('ctrl-chart-maxval').value;
                elem.params.showlabels = document.getElementById('ctrl-chart-showlabels').checked;
            }}

            drawAll();
            updateLayersPanel();
        }}

        // Delete elements
        function deleteElement(id) {{
            elements = elements.filter(el => el.id !== id);
            if (activeElementId === id) activeElementId = null;
            drawAll();
            updateLayersPanel();
        }}

        // Reorder layer indices
        function moveElement(id, direction) {{
            const idx = elements.findIndex(el => el.id === id);
            if (idx === -1) return;
            if (direction === 'up' && idx < elements.length - 1) {{
                let temp = elements[idx];
                elements[idx] = elements[idx+1];
                elements[idx+1] = temp;
            }} else if (direction === 'down' && idx > 0) {{
                let temp = elements[idx];
                elements[idx] = elements[idx-1];
                elements[idx-1] = temp;
            }}
            drawAll();
            updateLayersPanel();
        }}

        // Composed Elements drawing stack
        function drawAll() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            elements.forEach(elem => {{
                drawElement(elem);
            }});
        }}

        // Visual gradients constructors
        function createHTMLGradient(p, x, y, w, h) {{
            let grad;
            const px = parseCoord(x), py = parseCoord(y);
            const pw = parseCoord(w), ph = parseCoord(h);
            
            if (p.gradType === 'radial') {{
                const cx = px + pw/2, cy = py + ph/2;
                const r = Math.max(pw, ph) / 2;
                grad = ctx.createRadialGradient(cx, cy, 5, cx, cy, r);
            }} else {{
                // Linear gradient calculation with angle rotation
                const angle = (parseFloat(p.gradAngle) || 90) * Math.PI / 180;
                const x1 = px + pw/2 - Math.cos(angle) * pw/2;
                const y1 = py + ph/2 - Math.sin(angle) * ph/2;
                const x2 = px + pw/2 + Math.cos(angle) * pw/2;
                const y2 = py + ph/2 + Math.sin(angle) * ph/2;
                grad = ctx.createLinearGradient(x1, y1, x2, y2);
            }}

            // Parse color stops
            const stops = resolveVars(p.gradStops).split(';');
            stops.forEach(stop => {{
                const parts = stop.split(',');
                if (parts.length === 2) {{
                    const color = parts[0].trim();
                    const offset = parseFloat(parts[1].trim());
                    if (!isNaN(offset) && offset >= 0 && offset <= 1) {{
                        grad.addColorStop(offset, color);
                    }}
                }}
            }});
            return grad;
        }}

        // Visual Chart Themes
        function getChartThemeColors(theme) {{
            switch(theme) {{
                case 'green': return ['#10b981', '#34d399', '#059669', '#6ee7b7', '#047857'];
                case 'modern': return ['#a855f7', '#ec4899', '#8b5cf6', '#f472b6', '#6366f1'];
                case 'dark': return ['#d97706', '#f59e0b', '#b45309', '#fbbf24', '#78350f'];
                case 'neon': return ['#00f5ff', '#39ff14', '#ff007f', '#ffea00', '#9d00ff'];
                case 'blue':
                default: return ['#5865F2', '#3b82f6', '#1d4ed8', '#60a5fa', '#1e3a8a'];
            }}
        }}

        function drawElement(elem) {{
            const p = elem.params;
            
            // Parameter Resolving (Dynamic Mock Interpolations)
            const px = parseCoord(p.x), py = parseCoord(p.y);
            const pw = parseCoord(p.w), ph = parseCoord(p.h);
            const pcolor = resolveVars(p.color) || "#ffffff";
            const plw = parseCoord(p.lw) || 2;
            const pradius = parseCoord(p.radius) || 0;

            // Fill solver
            if (p.fill === 'gradient') {{
                ctx.fillStyle = createHTMLGradient(p, p.x, p.y, p.w, p.h);
            }} else {{
                ctx.fillStyle = p.fill === 'none' ? 'transparent' : (resolveVars(p.fill) || 'transparent');
            }}
            ctx.strokeStyle = pcolor;
            ctx.lineWidth = plw;

            if (elem.type === 'drawRect') {{
                ctx.beginPath();
                ctx.rect(px, py, pw, ph);
                if (p.fill !== 'none') ctx.fill();
                if (plw > 0) ctx.stroke();
            }} 
            else if (elem.type === 'drawRoundedRect') {{
                ctx.beginPath();
                ctx.roundRect(px, py, pw, ph, pradius);
                if (p.fill !== 'none') ctx.fill();
                if (plw > 0) ctx.stroke();
            }} 
            else if (elem.type === 'drawCircle') {{
                ctx.beginPath();
                const pcx = parseCoord(p.x1), pcy = parseCoord(p.y1);
                ctx.arc(pcx, pcy, pradius, 0, 2 * Math.PI);
                if (p.fill !== 'none') ctx.fill();
                if (plw > 0) ctx.stroke();
            }} 
            else if (elem.type === 'drawLine') {{
                ctx.beginPath();
                ctx.moveTo(parseCoord(p.x1), parseCoord(p.y1));
                ctx.lineTo(parseCoord(p.x2), parseCoord(p.y2));
                ctx.stroke();
            }} 
            else if (elem.type === 'drawImage') {{
                ctx.setLineDash([6, 6]);
                ctx.strokeStyle = '#5865F2';
                ctx.lineWidth = 2;
                ctx.strokeRect(px, py, pw, ph);
                ctx.setLineDash([]);
                
                ctx.fillStyle = 'rgba(88, 101, 242, 0.15)';
                ctx.fillRect(px, py, pw, ph);
                
                ctx.fillStyle = '#ffffff';
                ctx.font = '12px Outfit';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('🖼️ ' + resolveVars(p.path).split('/').pop(), px + pw/2, py + ph/2);
            }} 
            else if (elem.type === 'drawText') {{
                const psize = parseCoord(p.size) || 24;
                ctx.font = `${{psize}}px "${{p.font}}"`;
                ctx.fillStyle = pcolor;
                ctx.textAlign = p.anchor || 'left';
                ctx.textBaseline = 'top';
                ctx.fillText(resolveVars(p.text), px, py);
            }} 
            else if (elem.type === 'drawTextMid') {{
                const psize = parseCoord(p.size) || 24;
                ctx.font = `${{psize}}px "${{p.font}}"`;
                let displayStr = resolveVars(p.text);
                let textW = ctx.measureText(displayStr).width;
                if (textW > pw) {{
                    while (displayStr.length > 0) {{
                        displayStr = displayStr.slice(0, -1);
                        let checkW = ctx.measureText(displayStr + "...").width;
                        if (checkW <= pw) {{
                            displayStr += "...";
                            break;
                        }}
                    }}
                }}
                ctx.fillStyle = pcolor;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(displayStr, px + pw / 2, py + ph / 2);
                
                ctx.setLineDash([4, 4]);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.lineWidth = 1;
                ctx.strokeRect(px, py, pw, ph);
                ctx.setLineDash([]);
            }} 
            else if (elem.type === 'drawTextIn') {{
                const psize = parseCoord(p.size) || 24;
                let curSize = psize;
                const textStr = resolveVars(p.text);
                ctx.font = `${{curSize}}px "${{p.font}}"`;
                
                while (curSize > 4) {{
                    ctx.font = `${{curSize}}px "${{p.font}}"`;
                    let metrics = ctx.measureText(textStr);
                    if (metrics.width <= pw && curSize <= ph) {{
                        break;
                    }}
                    curSize--;
                }}
                
                ctx.fillStyle = pcolor;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.font = `${{curSize}}px "${{p.font}}"`;
                ctx.fillText(textStr, px + pw / 2, py + ph / 2);
                
                ctx.setLineDash([4, 4]);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.lineWidth = 1;
                ctx.strokeRect(px, py, pw, ph);
                ctx.setLineDash([]);
            }}
            // Advanced Data Charts Simulators
            else if (elem.type === 'drawProgressBar') {{
                // Outer bar background container
                ctx.beginPath();
                ctx.roundRect(px, py, pw, ph, pradius);
                ctx.fillStyle = 'rgba(255, 255, 255, 0.08)';
                ctx.fill();
                ctx.strokeStyle = 'rgba(255,255,255,0.15)';
                ctx.stroke();

                // Inner progress filled bar
                const vals = resolveVars(p.vals).split(',').map(Number);
                const curVal = vals[0] || 50;
                const maxVal = vals[1] || 100;
                const progressW = Math.max(10, Math.min(pw, (curVal / maxVal) * pw));
                
                ctx.beginPath();
                ctx.roundRect(px, py, progressW, ph, pradius);
                const colors = getChartThemeColors(p.theme);
                ctx.fillStyle = colors[0];
                ctx.fill();
            }}
            else if (elem.type === 'drawBarChart') {{
                const vals = resolveVars(p.vals).split(',').map(Number);
                const labels = resolveVars(p.labels).split(',');
                const maxVal = parseFloat(resolveVars(p.maxval)) || Math.max(...vals) || 100;
                
                const colors = getChartThemeColors(p.theme);
                const gap = parseInt(p.gap) || 15;
                const barW = (pw - (vals.length - 1) * gap) / vals.length;
                
                ctx.fillStyle = 'rgba(255, 255, 255, 0.02)';
                ctx.fillRect(px, py, pw, ph);
                ctx.strokeStyle = 'rgba(255,255,255,0.1)';
                ctx.strokeRect(px, py, pw, ph);

                for (let i = 0; i < vals.length; i++) {{
                    const val = vals[i];
                    const barH = (val / maxVal) * (ph - 30);
                    const barX = px + i * (barW + gap);
                    const barY = py + ph - 25 - barH;
                    
                    ctx.beginPath();
                    // Top rounding top-left & top-right only
                    ctx.roundRect(barX, barY, barW, barH, [pradius, pradius, 0, 0]);
                    ctx.fillStyle = colors[i % colors.length];
                    ctx.fill();

                    if (p.showlabels) {{
                        ctx.fillStyle = '#a5a5cc';
                        ctx.font = '10px Outfit';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'top';
                        ctx.fillText(labels[i] || '', barX + barW/2, py + ph - 20);
                        
                        // Value over bar
                        ctx.fillStyle = '#ffffff';
                        ctx.fillText(val, barX + barW/2, barY - 12);
                    }}
                }}
            }}
            else if (elem.type === 'drawLineChart') {{
                const vals = resolveVars(p.vals).split(',').map(Number);
                const labels = resolveVars(p.labels).split(',');
                const maxVal = parseFloat(resolveVars(p.maxval)) || Math.max(...vals) || 100;
                
                const colors = getChartThemeColors(p.theme);
                
                ctx.fillStyle = 'rgba(255, 255, 255, 0.02)';
                ctx.fillRect(px, py, pw, ph);
                ctx.strokeStyle = 'rgba(255,255,255,0.1)';
                ctx.strokeRect(px, py, pw, ph);

                const segW = pw / (vals.length - 1 || 1);
                const points = [];

                for (let i = 0; i < vals.length; i++) {{
                    const val = vals[i];
                    const pointX = px + i * segW;
                    const pointY = py + ph - 25 - (val / maxVal) * (ph - 40);
                    points.push({{x: pointX, y: pointY}});
                }}

                // Draw line connection segments
                ctx.beginPath();
                ctx.moveTo(points[0].x, points[0].y);
                for (let i = 1; i < points.length; i++) {{
                    ctx.lineTo(points[i].x, points[i].y);
                }}
                ctx.strokeStyle = colors[0];
                ctx.lineWidth = plw || 3;
                ctx.stroke();

                // Draw points and labels
                for (let i = 0; i < points.length; i++) {{
                    ctx.beginPath();
                    ctx.arc(points[i].x, points[i].y, 5, 0, 2*Math.PI);
                    ctx.fillStyle = colors[1 % colors.length];
                    ctx.fill();
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 1.5;
                    ctx.stroke();

                    if (p.showlabels) {{
                        ctx.fillStyle = '#a5a5cc';
                        ctx.font = '10px Outfit';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'top';
                        ctx.fillText(labels[i] || '', points[i].x, py + ph - 20);
                        
                        ctx.fillStyle = '#ffffff';
                        ctx.fillText(vals[i], points[i].x, points[i].y - 12);
                    }}
                }}
            }}
        }}

        // Live preview during mouse drag
        function drawPreviewShape() {{
            ctx.setLineDash([5, 5]);
            ctx.strokeStyle = '#57F287';
            ctx.lineWidth = 2;
            
            let w = currentX - startX;
            let h = currentY - startY;
            let nx = w < 0 ? startX + w : startX;
            let ny = h < 0 ? startY + h : startY;
            let nw = Math.abs(w);
            let nh = Math.abs(h);

            if (activeTool === 'drawRect' || activeTool === 'drawRoundedRect' || activeTool === 'drawImage' || activeTool.startsWith('drawText') || activeTool.startsWith('drawBarChart') || activeTool === 'drawLineChart' || activeTool === 'drawProgressBar') {{
                ctx.strokeRect(nx, ny, nw, nh);
            }} 
            else if (activeTool === 'drawCircle') {{
                ctx.beginPath();
                let r = Math.floor(Math.sqrt(w*w + h*h));
                ctx.arc(startX, startY, r, 0, 2*Math.PI);
                ctx.stroke();
            }} 
            else if (activeTool === 'drawLine') {{
                ctx.beginPath();
                ctx.moveTo(startX, startY);
                ctx.lineTo(currentX, currentY);
                ctx.stroke();
            }}
            ctx.setLineDash([]);
        }}

        // Code Generation Engine
        function generateCode(elem) {{
            if (!elem) return "";
            const p = elem.params;
            
            switch (elem.type) {{
                case 'drawText':
                    return `$drawText[${{p.x}};${{p.y}};${{p.text}};${{p.color}};${{p.size}};${{p.font}};${{p.anchor}}]`;
                case 'drawTextMid':
                    return `$drawTextMid[${{p.x}};${{p.y}};${{p.x + parseInt(p.w)}};${{p.y + parseInt(p.h)}};${{p.text}};${{p.color}};${{p.size}};${{p.font}}]`;
                case 'drawTextIn':
                    return `$drawTextIn[${{p.x}};${{p.y}};${{p.x + parseInt(p.w)}};${{p.y + parseInt(p.h)}};${{p.text}};${{p.color}};${{p.size}};${{p.font}}]`;
                case 'drawRect':
                    if (p.fill === 'gradient') {{
                        return `$drawRect[x=${{p.x}};y=${{p.y}};w=${{p.w}};h=${{p.h}};color=${{p.color}};fill=gradient;lw=${{p.lw}}]\\n$drawLinearGradient[x=${{p.x}};y=${{p.y}};w=${{p.w}};h=${{p.h}};stops="${{p.gradStops}}";angle=${{p.gradAngle}}]`;
                    }}
                    return `$drawRect[x=${{p.x}};y=${{p.y}};w=${{p.w}};h=${{p.h}};color=${{p.color}};fill=${{p.fill}};lw=${{p.lw}}]`;
                case 'drawRoundedRect':
                    if (p.fill === 'gradient') {{
                        return `$drawRoundedRect[x=${{p.x}};y=${{p.y}};w=${{p.w}};h=${{p.h}};radius=${{p.radius}};color=${{p.color}};fill=gradient;lw=${{p.lw}}]\\n$drawLinearGradient[x=${{p.x}};y=${{p.y}};w=${{p.w}};h=${{p.h}};stops="${{p.gradStops}}";angle=${{p.gradAngle}}]`;
                    }}
                    return `$drawRoundedRect[x=${{p.x}};y=${{p.y}};w=${{p.w}};h=${{p.h}};radius=${{p.radius}};color=${{p.color}};fill=${{p.fill}};lw=${{p.lw}}]`;
                case 'drawCircle':
                    return `$drawCircle[cx=${{p.x1}};cy=${{p.y1}};radius=${{p.radius}};color=${{p.color}};fill=${{p.fill}};lw=${{p.lw}}]`;
                case 'drawLine':
                    return `$drawLine[${{p.x1}};${{p.y1}};${{p.x2}};${{p.y2}};${{p.color}};${{p.lw}}]`;
                case 'drawImage':
                    return `$drawImage[${{p.x}};${{p.y}};${{p.path}};${{p.w}};${{p.h}};${{p.opacity}}]`;
                case 'drawProgressBar':
                    return `$drawProgressBar[${{p.x}};${{p.y}};${{p.w}};${{p.h}};val=${{p.vals}};max=${{p.maxval || 100}};theme=${{p.theme}};radius=${{p.radius}}]`;
                case 'drawBarChart':
                    return `$drawBarChart[${{p.x}};${{p.y}};${{p.w}};${{p.h}};vals=${{p.vals}};labels=${{p.labels}};theme=${{p.theme}};gap=${{p.gap}};show_lab=${{p.showlabels}};radius=${{p.radius}};max_val=${{p.maxval}}]`;
                case 'drawLineChart':
                    return `$drawLineChart[${{p.x}};${{p.y}};${{p.w}};${{p.h}};vals=${{p.vals}};labels=${{p.labels}};theme=${{p.theme}};lw=${{p.lw}};show_lab=${{p.showlabels}};max_val=${{p.maxval}}]`;
                default:
                    return "";
            }}
        }}

        // Reverse Template Parser (Import Code)
        function parseParams(paramStr) {{
            const parts = paramStr.split(';');
            const named = {{}};
            const positional = [];
            
            parts.forEach((part, index) => {{
                const trimmed = part.trim();
                if (trimmed.includes('=')) {{
                    const [k, v] = trimmed.split('=');
                    named[k.trim()] = v.trim();
                }} else {{
                    positional.push(trimmed);
                }}
            }});
            
            return {{ named, positional }};
        }}

        function importAlphaPILCode() {{
            const code = document.getElementById('import-code-area').value;
            if (!code.trim()) return;

            const lines = code.split('\\n');
            const funcRegex = /\\$(\\w+)\\s*\\[(.*?)\\]/g;
            
            elements = []; // Reset visual designer layers
            
            lines.forEach(line => {{
                let match;
                // Reset regex state
                funcRegex.lastIndex = 0;
                
                while ((match = funcRegex.exec(line)) !== null) {{
                    const func = match[1];
                    const paramStr = match[2];
                    const p = parseParams(paramStr);
                    
                    if (func === 'createCanvas') {{
                        const w = parseInt(p.positional[0]) || 1080;
                        const h = parseInt(p.positional[1]) || 1620;
                        document.getElementById('canvas-w').value = w;
                        document.getElementById('canvas-h').value = h;
                        resizeCanvasVisuals();
                    }}
                    else if (func === 'drawRect') {{
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawRect',
                            params: {{
                                x: p.named.x || p.positional[0] || '0',
                                y: p.named.y || p.positional[1] || '0',
                                w: parseInt(p.named.w || p.positional[2]) || 100,
                                h: parseInt(p.named.h || p.positional[3]) || 100,
                                color: p.named.color || p.named.outline || p.positional[4] || '#ffffff',
                                fill: p.named.fill || p.positional[6] || 'none',
                                lw: p.named.lw || p.positional[7] || '2',
                                radius: p.named.radius || p.positional[8] || '0'
                            }}
                        }});
                    }}
                    else if (func === 'drawRoundedRect') {{
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawRoundedRect',
                            params: {{
                                x: p.named.x || p.positional[0] || '0',
                                y: p.named.y || p.positional[1] || '0',
                                w: parseInt(p.named.w || p.positional[2]) || 100,
                                h: parseInt(p.named.h || p.positional[3]) || 100,
                                radius: p.named.radius || p.positional[4] || '12',
                                color: p.named.color || p.named.outline || p.positional[5] || '#ffffff',
                                fill: p.named.fill || p.positional[7] || 'none',
                                lw: p.named.lw || p.positional[8] || '2'
                            }}
                        }});
                    }}
                    else if (func === 'drawCircle') {{
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawCircle',
                            params: {{
                                x1: p.named.cx || p.positional[0] || '0',
                                y1: p.named.cy || p.positional[1] || '0',
                                cx: p.named.cx || p.positional[0] || '0',
                                cy: p.named.cy || p.positional[1] || '0',
                                radius: parseInt(p.named.radius || p.positional[2]) || 50,
                                color: p.named.color || p.positional[3] || '#ffffff',
                                fill: p.named.fill || p.positional[5] || 'none',
                                lw: p.named.lw || p.positional[6] || '2'
                            }}
                        }});
                    }}
                    else if (func === 'drawLine') {{
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawLine',
                            params: {{
                                x1: p.positional[0] || '0',
                                y1: p.positional[1] || '0',
                                x2: p.positional[2] || '100',
                                y2: p.positional[3] || '100',
                                color: p.positional[4] || '#ffffff',
                                lw: p.positional[5] || '2'
                            }}
                        }});
                    }}
                    else if (func === 'drawText') {{
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawText',
                            params: {{
                                x: p.positional[0] || '0',
                                y: p.positional[1] || '0',
                                text: p.positional[2] || 'Hello',
                                color: p.positional[3] || '#ffffff',
                                size: p.positional[4] || '24',
                                font: p.positional[5] || 'Arial',
                                anchor: p.positional[6] || 'left'
                            }}
                        }});
                    }}
                    else if (func === 'drawTextMid') {{
                        const x1 = parseInt(p.positional[0]) || 0;
                        const y1 = parseInt(p.positional[1]) || 0;
                        const x2 = parseInt(p.positional[2]) || 100;
                        const y2 = parseInt(p.positional[3]) || 100;
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawTextMid',
                            params: {{
                                x: x1,
                                y: y1,
                                w: x2 - x1,
                                h: y2 - y1,
                                text: p.positional[4] || 'Hello',
                                color: p.positional[5] || '#ffffff',
                                size: p.positional[6] || '24',
                                font: p.positional[7] || 'Arial'
                            }}
                        }});
                    }}
                    else if (func === 'drawTextIn') {{
                        const x1 = parseInt(p.positional[0]) || 0;
                        const y1 = parseInt(p.positional[1]) || 0;
                        const x2 = parseInt(p.positional[2]) || 100;
                        const y2 = parseInt(p.positional[3]) || 100;
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawTextIn',
                            params: {{
                                x: x1,
                                y: y1,
                                w: x2 - x1,
                                h: y2 - y1,
                                text: p.positional[4] || 'Hello',
                                color: p.positional[5] || '#ffffff',
                                size: p.positional[6] || '24',
                                font: p.positional[7] || 'Arial'
                            }}
                        }});
                    }}
                    else if (func === 'drawImage') {{
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawImage',
                            params: {{
                                x: p.positional[0] || '0',
                                y: p.positional[1] || '0',
                                path: p.positional[2] || 'resources/theme-irman.png',
                                w: parseInt(p.positional[3]) || 150,
                                h: parseInt(p.positional[4]) || 150,
                                opacity: p.positional[5] || '1.0'
                            }}
                        }});
                    }}
                    else if (func === 'drawBarChart') {{
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawBarChart',
                            params: {{
                                x: p.positional[0] || '0',
                                y: p.positional[1] || '0',
                                w: parseInt(p.positional[2]) || 300,
                                h: parseInt(p.positional[3]) || 180,
                                vals: p.named.vals || p.positional[4] || '10,20,30',
                                labels: p.named.labels || p.positional[5] || 'A,B,C',
                                theme: p.named.theme || p.positional[6] || 'blue',
                                gap: parseInt(p.named.gap || p.positional[8]) || 15,
                                radius: parseInt(p.named.radius || p.positional[12]) || 6,
                                maxval: p.named.max_val || p.positional[13] || '',
                                showlabels: true
                            }}
                        }});
                    }}
                    else if (func === 'drawLineChart') {{
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawLineChart',
                            params: {{
                                x: p.positional[0] || '0',
                                y: p.positional[1] || '0',
                                w: parseInt(p.positional[2]) || 300,
                                h: parseInt(p.positional[3]) || 180,
                                vals: p.named.vals || p.positional[4] || '10,20,30',
                                labels: p.named.labels || p.positional[5] || 'A,B,C',
                                theme: p.named.theme || p.positional[6] || 'blue',
                                lw: p.named.lw || p.positional[7] || '2',
                                maxval: p.named.max_val || p.positional[9] || '',
                                showlabels: true
                            }}
                        }});
                    }}
                    else if (func === 'drawProgressBar') {{
                        elements.push({{
                            id: Date.now() + Math.random(),
                            type: 'drawProgressBar',
                            params: {{
                                x: p.positional[0] || '0',
                                y: p.positional[1] || '0',
                                w: parseInt(p.positional[2]) || 200,
                                h: parseInt(p.positional[3]) || 24,
                                vals: p.named.val || p.positional[4] || '50',
                                maxval: p.named.max || p.positional[5] || '100',
                                theme: p.named.theme || p.positional[6] || 'blue',
                                radius: p.named.radius || p.positional[9] || '12'
                            }}
                        }});
                    }}
                }}
            }});

            drawAll();
            updateLayersPanel();
            showToast("Template imported and parsed successfully!");
        }}

        // Dynamic Layout listing
        function updateLayersPanel() {{
            const listContainer = document.getElementById('layers-list-container');
            const layersCard = document.getElementById('layers-card');
            const codeExportCard = document.getElementById('code-export-card');
            const fullTemplateArea = document.getElementById('full-template-code');
            const activeSnippet = document.getElementById('active-snippet-text');

            if (elements.length === 0) {{
                layersCard.style.display = 'none';
                codeExportCard.style.display = 'none';
                listContainer.innerHTML = '';
                return;
            }}

            layersCard.style.display = 'block';
            codeExportCard.style.display = 'block';
            listContainer.innerHTML = '';

            // Generate full template text
            let fullTemplate = `$createCanvas[${{canvas.width}};${{canvas.height}};#0c0c14;2;false;1]\\n\\n`;
            
            elements.forEach((elem, index) => {{
                fullTemplate += generateCode(elem) + "\\n";
                
                const item = document.createElement('div');
                item.className = 'layer-item';
                item.innerHTML = `
                    <div class="layer-info" onclick="selectLayer(${{elem.id}})" style="cursor:pointer; flex:1;">
                        <span>${{index + 1}}.</span>
                        <span>${{getLayerIcon(elem.type)}}</span>
                        <strong>${{elem.type}}</strong>
                        <span style="color:#8c8caf; font-size:9px;">(${{elem.params.x || elem.params.x1}}, ${{elem.params.y || elem.params.y1}})</span>
                    </div>
                    <div class="layer-actions">
                        <button class="layer-action-btn move" onclick="moveElement(${{elem.id}}, 'up')" title="Move Up">⬆️</button>
                        <button class="layer-action-btn move" onclick="moveElement(${{elem.id}}, 'down')" title="Move Down">⬇️</button>
                        <button class="layer-action-btn" onclick="deleteElement(${{elem.id}})" title="Delete Layer">🗑️</button>
                    </div>
                `;
                if (elem.id === activeElementId) {{
                    item.style.borderColor = '#5865F2';
                    item.style.backgroundColor = 'rgba(88, 101, 242, 0.08)';
                }}
                listContainer.appendChild(item);
            }});

            fullTemplate += `\\n$save[output.png]`;
            fullTemplateArea.value = fullTemplate;

            if (activeElementId) {{
                const actElem = elements.find(el => el.id === activeElementId);
                activeSnippet.innerText = generateCode(actElem);
            }} else {{
                activeSnippet.innerText = "Click and drag canvas to generate code";
            }}
        }}

        function selectLayer(id) {{
            activeElementId = id;
            const elem = elements.find(el => el.id === id);
            if (elem) {{
                setTool(elem.type);
                
                if (elem.type.startsWith('drawText')) {{
                    document.getElementById('ctrl-text-content').value = elem.params.text;
                    document.getElementById('ctrl-font-family').value = elem.params.font;
                    document.getElementById('ctrl-font-size').value = elem.params.size;
                    document.getElementById('ctrl-text-color-text').value = elem.params.color;
                    document.getElementById('ctrl-text-color-picker').value = elem.params.color.startsWith('#') ? elem.params.color : '#ffffff';
                    document.getElementById('ctrl-text-anchor').value = elem.params.anchor;
                }} else if (elem.type === 'drawRect' || elem.type === 'drawRoundedRect' || elem.type === 'drawCircle' || elem.type === 'drawLine') {{
                    document.getElementById('ctrl-outline-color-text').value = elem.params.color;
                    document.getElementById('ctrl-outline-color-picker').value = elem.params.color.startsWith('#') ? elem.params.color : '#ffffff';
                    
                    const fill = elem.params.fill;
                    if (fill === 'none') {{
                        document.getElementById('ctrl-fill-mode').value = 'none';
                    }} else if (fill === 'gradient') {{
                        document.getElementById('ctrl-fill-mode').value = 'gradient';
                    }} else {{
                        document.getElementById('ctrl-fill-mode').value = 'solid';
                        document.getElementById('ctrl-fill-color-text').value = fill;
                        if (fill.startsWith('#')) document.getElementById('ctrl-fill-color-picker').value = fill;
                    }}
                    
                    document.getElementById('ctrl-shape-lw').value = elem.params.lw;
                    document.getElementById('ctrl-shape-radius').value = elem.params.radius;
                    document.getElementById('ctrl-grad-type').value = elem.params.gradType || 'linear';
                    document.getElementById('ctrl-grad-stops').value = elem.params.gradStops || '#ff0000,0;#0000ff,1';
                    document.getElementById('ctrl-grad-angle').value = elem.params.gradAngle || '90';
                    
                    toggleFillMode(document.getElementById('ctrl-fill-mode').value);
                }} else if (elem.type === 'drawImage') {{
                    document.getElementById('ctrl-image-path').value = elem.params.path;
                    document.getElementById('ctrl-image-opacity').value = elem.params.opacity;
                }} else if (elem.type.startsWith('drawBarChart') || elem.type === 'drawLineChart' || elem.type === 'drawProgressBar') {{
                    document.getElementById('ctrl-chart-vals').value = elem.params.vals;
                    document.getElementById('ctrl-chart-labels').value = elem.params.labels;
                    document.getElementById('ctrl-chart-theme').value = elem.params.theme;
                    document.getElementById('ctrl-chart-gap').value = elem.params.gap;
                    document.getElementById('ctrl-chart-radius').value = elem.params.radius;
                    document.getElementById('ctrl-chart-maxval').value = elem.params.maxval;
                    document.getElementById('ctrl-chart-showlabels').checked = elem.params.showlabels;
                }}
            }}
            updateLayersPanel();
        }}

        function getLayerIcon(type) {{
            switch (type) {{
                case 'drawText': return '🔤';
                case 'drawTextMid': return '↔️';
                case 'drawTextIn': return '↕️';
                case 'drawRect': return '🟩';
                case 'drawRoundedRect': return '🟢';
                case 'drawCircle': return '🟡';
                case 'drawLine': return '➖';
                case 'drawImage': return '🖼️';
                case 'drawBarChart': return '📊';
                case 'drawLineChart': return '📈';
                case 'drawProgressBar': return '⏳';
                default: return '📍';
            }}
        }}

        // Clipboard copy controls
        function copyActiveCode() {{
            const code = document.getElementById('active-snippet-text').innerText;
            if (code && code !== "Click and drag canvas to generate code") {{
                copyText(code, "Copied active snippet!");
            }}
        }}

        function copyFullTemplate() {{
            const code = document.getElementById('full-template-code').value;
            if (code) {{
                copyText(code, "Copied full composed template!");
            }}
        }}

        function copyText(text, message) {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast(message);
            }}).catch(err => {{
                const textArea = document.createElement("textarea");
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand("copy");
                document.body.removeChild(textArea);
                showToast(message);
            }});
        }}

        function showToast(message) {{
            toastMessage.innerText = message;
            toast.classList.add('show');
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, 2200);
        }}

        // Dynamic Background swaps
        function loadFile(e) {{
            const file = e.target.files[0];
            if (file) {{
                const reader = new FileReader();
                reader.onload = function(event) {{
                    img.src = event.target.result;
                    elements = [];
                    activeElementId = null;
                    updateLayersPanel();
                }}
                reader.readAsDataURL(file);
            }}
        }}
    </script>
</body>
</html>"""
    
    html_path = os.path.join(output_dir, 'alphapil_ide_visualizer.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return html_path

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging server requests
        return

def open_picker(image_path: str):
    """
    Programmatic entry point to launch the coordinate picker for a given image.
    """
    if not os.path.exists(image_path):
        print(f"❌ Image path not found: {image_path}")
        return False

    abs_image_path = os.path.abspath(image_path)
    server_root = os.path.dirname(abs_image_path)
    
    # Generate HTML in the same directory as the image
    html_path = generate_html(abs_image_path, server_root, server_root)
    
    # Start server serving the directory containing the image
    port = find_free_port()
    
    # Change current working directory to the server root (safely restoring afterwards)
    orig_cwd = os.getcwd()
    os.chdir(server_root)
    
    try:
        httpd = socketserver.TCPServer(("", port), CustomHandler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Open browser relative to the server root
        filename = os.path.basename(html_path)
        url = f"http://localhost:{port}/{filename}"
        print(f"🌍 Opening Interactive Coordinator Webpage at: {url}")
        print("⏹️  Press Ctrl+C in this terminal to shut down the picker server.")
        webbrowser.open(url)
        
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Stopping Coordinate Picker Server...")
            httpd.shutdown()
            # Clean up generated html file
            if os.path.exists(html_path):
                os.remove(html_path)
            print("✅ Stopped successfully.")
    finally:
        os.chdir(orig_cwd)
    
    return True

def main():
    """CLI entry point."""
    image_path = None
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
    if not image_path:
        # Check standard default filenames
        default_choices = ["output.png", "output.jpg", "canvas.png"]
        for choice in default_choices:
            if os.path.exists(choice):
                image_path = choice
                break
                
    if not image_path:
        print("❌ Please specify an image path to open.")
        print("Usage: alphapil-picker <path_to_image>")
        sys.exit(1)
        
    open_picker(image_path)

if __name__ == "__main__":
    main()
