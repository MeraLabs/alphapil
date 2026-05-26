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

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AlphaPIL Visual Designer 🎯</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
        }}

        body {{
            background: radial-gradient(circle at top right, #1a1a2e, #08080f);
            color: #f1f1f7;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }}

        header {{
            background: rgba(10, 10, 20, 0.8);
            backdrop-filter: blur(16px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding: 14px 40px;
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
            padding: 24px 40px;
            gap: 30px;
            max-width: 1800px;
            margin: 0 auto;
            width: 100%;
        }}

        .picker-area {{
            flex: 1;
            background: rgba(10, 10, 20, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 24px;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            position: relative;
            min-height: 600px;
            max-height: 85vh;
            overflow: auto;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}

        .image-wrapper {{
            position: relative;
            cursor: crosshair;
            display: inline-block;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.12);
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
            width: 440px;
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
            border-radius: 18px;
            padding: 20px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
        }}

        .panel-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 14px;
            color: #a5a5cc;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            padding-bottom: 8px;
        }}

        .coordinate-display {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 14px;
        }}

        .coord-box {{
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 10px;
            text-align: center;
        }}

        .coord-label {{
            font-size: 10px;
            font-weight: 600;
            color: #7d7db5;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 4px;
        }}

        .coord-value {{
            font-size: 26px;
            font-weight: 800;
            color: #ffffff;
        }}

        /* Tool Grid */
        .tool-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
            margin-bottom: 10px;
        }}

        .tool-btn {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            padding: 10px 6px;
            color: #b5b5d5;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 6px;
            transition: all 0.2s ease;
        }}

        .tool-btn:hover {{
            background: rgba(255, 255, 255, 0.07);
            color: #ffffff;
            border-color: rgba(88, 101, 242, 0.4);
        }}

        .tool-btn.active {{
            background: rgba(88, 101, 242, 0.15);
            border-color: #5865F2;
            color: #ffffff;
            box-shadow: 0 0 12px rgba(88, 101, 242, 0.25);
        }}

        .tool-icon {{
            font-size: 18px;
        }}

        /* Settings Forms */
        .input-group {{
            margin-bottom: 12px;
        }}

        .input-label {{
            display: block;
            font-size: 12px;
            color: #8c8caf;
            margin-bottom: 6px;
            font-weight: 600;
        }}

        .input-field {{
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 8px 12px;
            color: white;
            font-size: 13px;
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
            width: 32px;
            height: 32px;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.2);
            cursor: pointer;
            padding: 0;
            background: none;
        }}

        /* Layer List */
        .layer-list {{
            max-height: 180px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .layer-item {{
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 8px 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
        }}

        .layer-info {{
            display: flex;
            align-items: center;
            gap: 8px;
            color: #d1d1e0;
        }}

        .layer-actions {{
            display: flex;
            gap: 6px;
        }}

        .layer-action-btn {{
            background: none;
            border: none;
            color: #8c8caf;
            cursor: pointer;
            padding: 2px;
            border-radius: 4px;
            font-size: 12px;
            transition: all 0.2s ease;
        }}

        .layer-action-btn:hover {{
            color: #ff4d4d;
            background: rgba(255, 77, 77, 0.1);
        }}

        .layer-action-btn.move:hover {{
            color: #57F287;
            background: rgba(87, 242, 135, 0.1);
        }}

        /* Code snippets */
        .clipboard-box {{
            background: rgba(0, 0, 0, 0.3);
            border: 1px dashed rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            padding: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: monospace;
            font-size: 12px;
            color: #e2e2f0;
            cursor: pointer;
            transition: border 0.3s ease;
            margin-top: 8px;
        }}

        .clipboard-box:hover {{
            border-color: #5865F2;
            background: rgba(88, 101, 242, 0.05);
        }}

        .copy-tag {{
            font-size: 10px;
            color: #5865F2;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}

        .full-code-area {{
            width: 100%;
            height: 120px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 8px;
            padding: 10px;
            color: #57F287;
            font-family: monospace;
            font-size: 11px;
            resize: none;
            outline: none;
            margin-bottom: 8px;
        }}

        .primary-btn {{
            width: 100%;
            background: linear-gradient(135deg, #5865F2, #4752c4);
            border: none;
            border-radius: 8px;
            color: white;
            padding: 10px;
            font-weight: 600;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
        }}

        .primary-btn:hover {{
            background: linear-gradient(135deg, #6c78ff, #5865F2);
            box-shadow: 0 4px 15px rgba(88, 101, 242, 0.3);
        }}

        .toast {{
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: #57F287;
            color: #0c0c14;
            padding: 12px 24px;
            border-radius: 30px;
            font-weight: 600;
            font-size: 15px;
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
            border-radius: 14px;
            padding: 16px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .upload-area:hover {{
            border-color: #5865F2;
            background: rgba(88, 101, 242, 0.05);
        }}

        .upload-icon {{
            font-size: 20px;
            margin-bottom: 4px;
        }}

        .upload-text {{
            font-size: 12px;
            color: #a5a5cc;
        }}
    </style>
</head>
<body>

    <header>
        <div class="logo">
            <div class="logo-dot"></div>
            AlphaPIL Designer 🎯
        </div>
        <div style="font-size: 14px; color: #a5a5cc;">Active: <span style="color: white; font-weight: 600;">{os.path.basename(image_path)}</span></div>
    </header>

    <div class="main-container">
        <div class="picker-area">
            <div class="image-wrapper" id="img-wrapper">
                <img id="target-img" src="/{rel_image_path}" alt="Rendered Canvas">
                <canvas id="overlay-canvas"></canvas>
                <div class="reticle-x" id="reticle-x"></div>
                <div class="reticle-y" id="reticle-y"></div>
            </div>
        </div>

        <div class="control-panel">
            <!-- Coordinates Card -->
            <div class="panel-card">
                <div class="panel-title">
                    <span>🎯 Live Coordinates</span>
                </div>
                <div class="coordinate-display">
                    <div class="coord-box" id="box-x">
                        <div class="coord-label">X Axis</div>
                        <div class="coord-value" id="val-x">0</div>
                    </div>
                    <div class="coord-box" id="box-y">
                        <div class="coord-label">Y Axis</div>
                        <div class="coord-value" id="val-y">0</div>
                    </div>
                </div>
            </div>

            <!-- Visual Tools Selector -->
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
                        <span>drawText</span>
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
                        <span>drawRect</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawRoundedRect')">
                        <span class="tool-icon">🟢</span>
                        <span>RoundRect</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawCircle')">
                        <span class="tool-icon">🟡</span>
                        <span>drawCircle</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawLine')">
                        <span class="tool-icon">➖</span>
                        <span>drawLine</span>
                    </button>
                    <button class="tool-btn" onclick="setTool('drawImage')">
                        <span class="tool-icon">🖼️</span>
                        <span>drawImage</span>
                    </button>
                </div>
                <div style="font-size: 11px; color: #8c8caf; text-align: center; margin-top: 4px;">
                    * For Box/Line/Circle tools, Click & Drag on canvas to draw.
                </div>
            </div>

            <!-- Dynamic Settings Config Box -->
            <div class="panel-card" id="settings-card" style="display: none;">
                <div class="panel-title" id="settings-title">
                    <span>⚙️ Styling Controls</span>
                </div>
                
                <!-- Text Inputs Group -->
                <div id="settings-group-text" style="display: none;">
                    <div class="input-group">
                        <label class="input-label">Text Content</label>
                        <input type="text" class="input-field" id="ctrl-text-content" value="Hello AlphaPIL" oninput="updateActiveElement()">
                    </div>
                    <div class="inline-inputs">
                        <div class="input-group">
                            <label class="input-label">Font Family</label>
                            <input type="text" class="input-field" id="ctrl-font-family" value="Arial" oninput="updateActiveElement()">
                        </div>
                        <div class="input-group">
                            <label class="input-label">Font Size (px)</label>
                            <input type="number" class="input-field" id="ctrl-font-size" value="32" min="6" max="250" oninput="updateActiveElement()">
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

                <!-- Shapes Inputs Group -->
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
                            <label class="input-label">Fill Color</label>
                            <div class="color-picker-wrapper" style="gap: 4px;">
                                <input type="color" class="color-input-preview" id="ctrl-fill-color-picker" value="#5865F2" oninput="document.getElementById('ctrl-fill-none').checked = false; syncColorInput('ctrl-fill-color-picker', 'ctrl-fill-color-text')">
                                <input type="text" class="input-field" id="ctrl-fill-color-text" value="#5865F2" oninput="document.getElementById('ctrl-fill-none').checked = false; syncColorText('ctrl-fill-color-text', 'ctrl-fill-color-picker')">
                            </div>
                            <label style="display: flex; align-items: center; gap: 4px; font-size: 11px; color: #8c8caf; margin-top: 4px; cursor: pointer;">
                                <input type="checkbox" id="ctrl-fill-none" onchange="toggleFillNone(this.checked)"> Transparent Fill
                            </label>
                        </div>
                    </div>
                    <div class="inline-inputs">
                        <div class="input-group">
                            <label class="input-label">Line/Stroke Width (`lw`)</label>
                            <input type="number" class="input-field" id="ctrl-shape-lw" value="2" min="0" max="50" oninput="updateActiveElement()">
                        </div>
                        <div class="input-group" id="radius-wrapper">
                            <label class="input-label">Corner Radius (`radius`)</label>
                            <input type="number" class="input-field" id="ctrl-shape-radius" value="12" min="0" max="500" oninput="updateActiveElement()">
                        </div>
                    </div>
                </div>

                <!-- Image Inputs Group -->
                <div id="settings-group-image" style="display: none;">
                    <div class="input-group">
                        <label class="input-label">Local Image Path</label>
                        <input type="text" class="input-field" id="ctrl-image-path" value="resources/theme-irman.png" oninput="updateActiveElement()">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Opacity (0.0 to 1.0)</label>
                        <input type="number" class="input-field" id="ctrl-image-opacity" value="1.0" min="0.0" max="1.0" step="0.1" oninput="updateActiveElement()">
                    </div>
                </div>

                <!-- Copied Snippet Box inside configuration -->
                <div style="margin-top: 14px;">
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
                    <span>📚 Composed Layers ({os.path.basename(image_path)})</span>
                </div>
                <div class="layer-list" id="layers-list-container">
                    <!-- Dynamic Layer items here -->
                </div>
            </div>

            <!-- Full Template Code Export Card -->
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
                    <span>📁 Load Different Background</span>
                </div>
                <div class="upload-area" onclick="document.getElementById('file-input').click()">
                    <div class="upload-icon">📷</div>
                    <div class="upload-text">Drag & Drop Image or Click to Browse</div>
                    <input type="file" id="file-input" style="display: none;" accept="image/*" onchange="loadFile(event)">
                </div>
            </div>
        </div>
    </div>

    <div class="toast" id="toast">
        <span id="toast-message">✅ Coordinates copied to clipboard!</span>
    </div>

    <script>
        const wrapper = document.getElementById('img-wrapper');
        const img = document.getElementById('target-img');
        const canvas = document.getElementById('overlay-canvas');
        const ctx = canvas.getContext('2d');
        const valX = document.getElementById('val-x');
        const valY = document.getElementById('val-y');
        const boxX = document.getElementById('box-x');
        const boxY = document.getElementById('box-y');
        const rx = document.getElementById('reticle-x');
        const ry = document.getElementById('reticle-y');
        const toast = document.getElementById('toast');
        const toastMessage = document.getElementById('toast-message');

        // Designer States
        let elements = []; // Array of drawn visual elements
        let activeTool = 'inspector'; // 'inspector', 'drawText', 'drawRect', etc.
        let isDrawing = false;
        let startX = 0, startY = 0;
        let currentX = 0, currentY = 0;
        let activeElementId = null;

        // On Image Load, configure visual canvas and dimensions
        img.onload = () => {{
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            drawAll();
        }};
        
        // Safety trigger if image is already cached/loaded
        if (img.complete) {{
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            setTimeout(drawAll, 200);
        }}

        // Translate mouse Client positions to native pixel dimensions
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

        // Handle active tool selection
        function setTool(toolName) {{
            activeTool = toolName;
            
            // Toggle active visual states on grid buttons
            document.querySelectorAll('.tool-btn').forEach(btn => {{
                btn.classList.remove('active');
                if (btn.querySelector('.tool-icon').parentElement.onclick.toString().includes(toolName)) {{
                    btn.classList.add('active');
                }}
            }});

            // Show / Hide Styling Cards
            const settingsCard = document.getElementById('settings-card');
            const gText = document.getElementById('settings-group-text');
            const gShape = document.getElementById('settings-group-shape');
            const gImg = document.getElementById('settings-group-image');
            
            if (toolName === 'inspector') {{
                settingsCard.style.display = 'none';
            }} else {{
                settingsCard.style.display = 'block';
                gText.style.display = (toolName.startsWith('drawText')) ? 'block' : 'none';
                gShape.style.display = (toolName.startsWith('drawRect') || toolName === 'drawRoundedRect' || toolName === 'drawCircle' || toolName === 'drawLine') ? 'block' : 'none';
                gImg.style.display = (toolName === 'drawImage') ? 'block' : 'none';

                // Display anchors only on point text drawText
                document.getElementById('anchor-wrapper').style.display = (toolName === 'drawText') ? 'block' : 'none';
                // Display radius only on rounded rects
                document.getElementById('radius-wrapper').style.display = (toolName === 'drawRoundedRect') ? 'block' : 'none';
                
                document.getElementById('settings-title').querySelector('span').innerText = `⚙️ ${{toolName}} Controls`;
                document.getElementById('active-snippet-text').innerText = "Click and drag canvas to generate code";
            }}
            drawAll();
        }}

        // Synchronization color utilities
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

        function toggleFillNone(isNone) {{
            if (isNone) {{
                document.getElementById('ctrl-fill-color-text').value = 'none';
            }} else {{
                document.getElementById('ctrl-fill-color-text').value = document.getElementById('ctrl-fill-color-picker').value;
            }}
            updateActiveElement();
        }}

        // Canvas Interactions (Drawing/Mousedowns)
        canvas.addEventListener('mousedown', (e) => {{
            const coord = getCoords(e);
            
            if (activeTool === 'inspector') {{
                const coordinates = `${{coord.x}};${{coord.y}}`;
                copyText(coordinates, "Coordinates copied to clipboard!");
                boxX.classList.add('highlight');
                boxY.classList.add('highlight');
                setTimeout(() => {{
                    boxX.classList.remove('highlight');
                    boxY.classList.remove('highlight');
                }}, 1200);
                return;
            }}

            isDrawing = true;
            startX = coord.x;
            startY = coord.y;
            currentX = startX;
            currentY = startY;

            if (activeTool === 'drawText') {{
                // Point placing tool
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
            
            // Reticle positioning
            const rect = canvas.getBoundingClientRect();
            if (coord.x >= 0 && coord.x <= canvas.width && coord.y >= 0 && coord.y <= canvas.height) {{
                valX.innerText = coord.x;
                valY.innerText = coord.y;
                
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
            
            // Render immediate overlay preview
            drawAll();
            drawPreviewShape();
        }});

        window.addEventListener('mouseup', (e) => {{
            if (!isDrawing) return;
            isDrawing = false;
            
            const w = currentX - startX;
            const h = currentY - startY;
            
            // Avoid creating tiny empty boxes
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
            rx.style.display = 'none';
            ry.style.display = 'none';
        }}

        // Dynamic Elements Constructors
        function createNewElement(x, y, w, h) {{
            // Normalize values for rectangles
            let nx = w < 0 ? x + w : x;
            let ny = h < 0 ? y + h : y;
            let nw = Math.abs(w);
            let nh = Math.abs(h);

            const elem = {{
                id: Date.now(),
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
                    size: parseInt(document.getElementById('ctrl-font-size').value) || 24,
                    color: document.getElementById('ctrl-text-color-text').value,
                    anchor: document.getElementById('ctrl-text-anchor').value
                }};
            }} else if (activeTool === 'drawRect' || activeTool === 'drawRoundedRect' || activeTool === 'drawCircle' || activeTool === 'drawLine') {{
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
                    fill: document.getElementById('ctrl-fill-color-text').value,
                    lw: parseInt(document.getElementById('ctrl-shape-lw').value) || 2,
                    radius: parseInt(document.getElementById('ctrl-shape-radius').value) || 12
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
                    opacity: parseFloat(document.getElementById('ctrl-image-opacity').value) || 1.0
                }};
            }}

            return elem;
        }}

        // Updates selected element fields on input changes
        function updateActiveElement() {{
            if (!activeElementId) return;
            const elem = elements.find(el => el.id === activeElementId);
            if (!elem) return;

            if (elem.type.startsWith('drawText')) {{
                elem.params.text = document.getElementById('ctrl-text-content').value;
                elem.params.font = document.getElementById('ctrl-font-family').value;
                elem.params.size = parseInt(document.getElementById('ctrl-font-size').value) || 24;
                elem.params.color = document.getElementById('ctrl-text-color-text').value;
                elem.params.anchor = document.getElementById('ctrl-text-anchor').value;
            }} else if (elem.type === 'drawRect' || elem.type === 'drawRoundedRect' || elem.type === 'drawCircle' || elem.type === 'drawLine') {{
                elem.params.color = document.getElementById('ctrl-outline-color-text').value;
                elem.params.fill = document.getElementById('ctrl-fill-color-text').value;
                elem.params.lw = parseInt(document.getElementById('ctrl-shape-lw').value) || 2;
                elem.params.radius = parseInt(document.getElementById('ctrl-shape-radius').value) || 12;
            }} else if (elem.type === 'drawImage') {{
                elem.params.path = document.getElementById('ctrl-image-path').value;
                elem.params.opacity = parseFloat(document.getElementById('ctrl-image-opacity').value) || 1.0;
            }}

            drawAll();
            updateLayersPanel();
        }}

        // Deletes an element
        function deleteElement(id) {{
            elements = elements.filter(el => el.id !== id);
            if (activeElementId === id) activeElementId = null;
            drawAll();
            updateLayersPanel();
        }}

        // Reorders layers up or down
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

        // Re-renders all elements onto Visual HTML overlay
        function drawAll() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            
            elements.forEach(elem => {{
                drawElement(elem);
            }});
        }}

        function drawElement(elem) {{
            const p = elem.params;
            ctx.strokeStyle = p.color || "#ffffff";
            ctx.fillStyle = p.fill === 'none' ? 'transparent' : (p.fill || 'transparent');
            ctx.lineWidth = p.lw || 2;
            
            if (elem.type === 'drawRect') {{
                ctx.beginPath();
                ctx.rect(p.x, p.y, p.w, p.h);
                if (p.fill !== 'none') ctx.fill();
                if (p.lw > 0) ctx.stroke();
            }} 
            else if (elem.type === 'drawRoundedRect') {{
                ctx.beginPath();
                ctx.roundRect(p.x, p.y, p.w, p.h, p.radius || 0);
                if (p.fill !== 'none') ctx.fill();
                if (p.lw > 0) ctx.stroke();
            }} 
            else if (elem.type === 'drawCircle') {{
                ctx.beginPath();
                ctx.arc(p.x1, p.y1, p.radius, 0, 2 * Math.PI);
                if (p.fill !== 'none') ctx.fill();
                if (p.lw > 0) ctx.stroke();
            }} 
            else if (elem.type === 'drawLine') {{
                ctx.beginPath();
                ctx.moveTo(p.x1, p.y1);
                ctx.lineTo(p.x2, p.y2);
                ctx.stroke();
            }} 
            else if (elem.type === 'drawImage') {{
                // Draw dotted boundary representation
                ctx.setLineDash([6, 6]);
                ctx.strokeStyle = '#5865F2';
                ctx.lineWidth = 2;
                ctx.strokeRect(p.x, p.y, p.w, p.h);
                ctx.setLineDash([]);
                
                // Overlay text
                ctx.fillStyle = 'rgba(88, 101, 242, 0.15)';
                ctx.fillRect(p.x, p.y, p.w, p.h);
                
                ctx.fillStyle = '#ffffff';
                ctx.font = '12px Outfit';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('🖼️ ' + p.path.split('/').pop(), p.x + p.w/2, p.y + p.h/2);
            }} 
            else if (elem.type === 'drawText') {{
                ctx.font = `${{p.size}}px "${{p.font}}"`;
                ctx.fillStyle = p.color;
                ctx.textAlign = p.anchor || 'left';
                ctx.textBaseline = 'top';
                ctx.fillText(p.text, p.x, p.y);
            }} 
            else if (elem.type === 'drawTextMid') {{
                // Box Mid Centering with auto-truncation simulation
                ctx.font = `${{p.size}}px "${{p.font}}"`;
                let displayStr = p.text;
                let textW = ctx.measureText(displayStr).width;
                if (textW > p.w) {{
                    while (displayStr.length > 0) {{
                        displayStr = displayStr.slice(0, -1);
                        let checkW = ctx.measureText(displayStr + "...").width;
                        if (checkW <= p.w) {{
                            displayStr += "...";
                            break;
                        }}
                    }}
                }}
                ctx.fillStyle = p.color;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(displayStr, p.x + p.w / 2, p.y + p.h / 2);
                
                // Draw text box bounding limit dashed
                ctx.setLineDash([4, 4]);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.lineWidth = 1;
                ctx.strokeRect(p.x, p.y, p.w, p.h);
                ctx.setLineDash([]);
            }} 
            else if (elem.type === 'drawTextIn') {{
                // Box In Centering with dynamic scaling simulation
                let curSize = p.size;
                ctx.font = `${{curSize}}px "${{p.font}}"`;
                
                while (curSize > 4) {{
                    ctx.font = `${{curSize}}px "${{p.font}}"`;
                    let metrics = ctx.measureText(p.text);
                    if (metrics.width <= p.w && curSize <= p.h) {{
                        break;
                    }}
                    curSize--;
                }}
                
                ctx.fillStyle = p.color;
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.font = `${{curSize}}px "${{p.font}}"`;
                ctx.fillText(p.text, p.x + p.w / 2, p.y + p.h / 2);
                
                // Draw text box bounding limit dashed
                ctx.setLineDash([4, 4]);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.2)';
                ctx.lineWidth = 1;
                ctx.strokeRect(p.x, p.y, p.w, p.h);
                ctx.setLineDash([]);
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

            if (activeTool === 'drawRect' || activeTool === 'drawRoundedRect' || activeTool === 'drawImage' || activeTool === 'drawTextMid' || activeTool === 'drawTextIn') {{
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
                    return `$drawTextMid[${{p.x}};${{p.y}};${{p.x + p.w}};${{p.y + p.h}};${{p.text}};${{p.color}};${{p.size}};${{p.font}}]`;
                case 'drawTextIn':
                    return `$drawTextIn[${{p.x}};${{p.y}};${{p.x + p.w}};${{p.y + p.h}};${{p.text}};${{p.color}};${{p.size}};${{p.font}}]`;
                case 'drawRect':
                    return `$drawRect[x=${{p.x}};y=${{p.y}};w=${{p.w}};h=${{p.h}};color=${{p.color}};fill=${{p.fill}};lw=${{p.lw}}]`;
                case 'drawRoundedRect':
                    return `$drawRoundedRect[x=${{p.x}};y=${{p.y}};w=${{p.w}};h=${{p.h}};radius=${{p.radius}};color=${{p.color}};fill=${{p.fill}};lw=${{p.lw}}]`;
                case 'drawCircle':
                    return `$drawCircle[cx=${{p.x1}};cy=${{p.y1}};radius=${{p.radius}};color=${{p.color}};fill=${{p.fill}};lw=${{p.lw}}]`;
                case 'drawLine':
                    return `$drawLine[${{p.x1}};${{p.y1}};${{p.x2}};${{p.y2}};${{p.color}};${{p.lw}}]`;
                case 'drawImage':
                    return `$drawImage[${{p.x}};${{p.y}};${{p.path}};${{p.w}};${{p.h}};${{p.opacity}}]`;
                default:
                    return "";
            }}
        }}

        // Composed Layers & Cards list UI updates
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
            
            // Loop backwards (bottom-up index drawing)
            elements.forEach((elem, index) => {{
                fullTemplate += generateCode(elem) + "\\n";
                
                // Add list layer item
                const activeClass = elem.id === activeElementId ? 'style="border-color:#5865F2; background:rgba(88,101,242,0.06)"' : '';
                const item = document.createElement('div');
                item.className = 'layer-item';
                item.innerHTML = `
                    <div class="layer-info" onclick="selectLayer(${{elem.id}})" style="cursor:pointer; flex:1;">
                        <span>${{index + 1}}.</span>
                        <span>${{getLayerIcon(elem.type)}}</span>
                        <strong>${{elem.type}}</strong>
                        <span style="color:#8c8caf; font-size:10px;">(${{elem.params.x || elem.params.x1}}, ${{elem.params.y || elem.params.y1}})</span>
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

            // Update active snippet display
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
                
                // Load params into settings panel
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
                    document.getElementById('ctrl-fill-color-text').value = elem.params.fill;
                    document.getElementById('ctrl-fill-none').checked = elem.params.fill === 'none';
                    if (elem.params.fill !== 'none' && elem.params.fill.startsWith('#')) {{
                        document.getElementById('ctrl-fill-color-picker').value = elem.params.fill;
                    }}
                    document.getElementById('ctrl-shape-lw').value = elem.params.lw;
                    document.getElementById('ctrl-shape-radius').value = elem.params.radius;
                }} else if (elem.type === 'drawImage') {{
                    document.getElementById('ctrl-image-path').value = elem.params.path;
                    document.getElementById('ctrl-image-opacity').value = elem.params.opacity;
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
                default: return '📍';
            }}
        }}

        // Copy utilities
        function copyActiveCode() {{
            const code = document.getElementById('active-snippet-text').innerText;
            if (code && code !== "Click and drag canvas to generate code") {{
                copyText(code, "Copied active snippet code to clipboard!");
            }}
        }}

        function copyFullTemplate() {{
            const code = document.getElementById('full-template-code').value;
            if (code) {{
                copyText(code, "Copied full composed template to clipboard!");
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

        // Image drag and drop dynamic load
        function loadFile(e) {{
            const file = e.target.files[0];
            if (file) {{
                const reader = new FileReader();
                reader.onload = function(event) {{
                    img.src = event.target.result;
                    // Reset elements array
                    elements = [];
                    activeElementId = null;
                    updateLayersPanel();
                }}
                reader.readAsDataURL(file);
            }}
        }}

        const dropArea = document.querySelector('.upload-area');
        dropArea.addEventListener('dragover', (e) => {{
            e.preventDefault();
            dropArea.style.borderColor = '#5865F2';
        }});

        dropArea.addEventListener('dragleave', () => {{
            dropArea.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        }});

        dropArea.addEventListener('drop', (e) => {{
            e.preventDefault();
            dropArea.style.borderColor = 'rgba(255, 255, 255, 0.1)';
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith('image/')) {{
                const reader = new FileReader();
                reader.onload = function(event) {{
                    img.src = event.target.result;
                    elements = [];
                    activeElementId = null;
                    updateLayersPanel();
                }}
                reader.readAsDataURL(file);
            }}
        }});
    </script>
</body>
</html>"""
    
    html_path = os.path.join(output_dir, 'alphapil_coordinate_picker.html')
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
