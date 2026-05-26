#!/usr/bin/env python3
"""
AlphaPIL Interactive Coordinate Picker

This script starts a premium interactive local web application 
to easily inspect, find, and copy pixel coordinates from your rendered images.
"""

import os
import sys
import http.server
import socketserver
import webbrowser
import threading
import socket
import re

def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def generate_html(image_path, project_root):
    # Determine the path of the image relative to the project root (where the server runs)
    try:
        rel_image_path = os.path.relpath(image_path, project_root)
    except ValueError:
        # If on a different drive/volume, fallback to absolute path
        rel_image_path = os.path.abspath(image_path)

    # Use forward slashes for HTML URLs
    rel_image_path = rel_image_path.replace(os.sep, '/')

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AlphaPIL Coordinate Picker 🎯</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Outfit', sans-serif;
        }}

        body {{
            background: radial-gradient(circle at top right, #1e1e30, #0c0c14);
            color: #f1f1f7;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }}

        header {{
            background: rgba(15, 15, 27, 0.7);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding: 16px 40px;
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
            padding: 40px;
            gap: 40px;
            max-width: 1600px;
            margin: 0 auto;
            width: 100%;
        }}

        .picker-area {{
            flex: 1;
            background: rgba(15, 15, 27, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 24px;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 30px;
            position: relative;
            min-height: 500px;
            overflow: auto;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }}

        .image-wrapper {{
            position: relative;
            cursor: crosshair;
            display: inline-block;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}

        #target-img {{
            max-width: 100%;
            height: auto;
            display: block;
            user-select: none;
            -webkit-user-drag: none;
        }}

        .reticle-x, .reticle-y {{
            position: absolute;
            background: rgba(88, 101, 242, 0.4);
            pointer-events: none;
            display: none;
        }}
        .reticle-x {{ height: 100%; width: 1px; top: 0; }}
        .reticle-y {{ width: 100%; height: 1px; left: 0; }}

        .control-panel {{
            width: 380px;
            display: flex;
            flex-direction: column;
            gap: 30px;
        }}

        .panel-card {{
            background: rgba(25, 25, 45, 0.65);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}

        .panel-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #a5a5cc;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .coordinate-display {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 25px;
        }}

        .coord-box {{
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            position: relative;
        }}

        .coord-label {{
            font-size: 12px;
            font-weight: 600;
            color: #7d7db5;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
        }}

        .coord-value {{
            font-size: 36px;
            font-weight: 800;
            color: #ffffff;
        }}

        .coord-box.highlight .coord-value {{
            color: #57F287;
            text-shadow: 0 0 10px rgba(87, 242, 135, 0.3);
        }}

        .clipboard-box {{
            background: rgba(0, 0, 0, 0.25);
            border: 1px dashed rgba(255, 255, 255, 0.15);
            border-radius: 12px;
            padding: 14px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: monospace;
            font-size: 14px;
            color: #ffffff;
            cursor: pointer;
            transition: border 0.3s ease;
        }}

        .clipboard-box:hover {{
            border-color: #5865F2;
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
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .upload-area:hover {{
            border-color: #5865F2;
            background: rgba(88, 101, 242, 0.05);
        }}

        .upload-icon {{
            font-size: 24px;
            margin-bottom: 8px;
        }}

        .upload-text {{
            font-size: 14px;
            color: #a5a5cc;
        }}
    </style>
</head>
<body>

    <header>
        <div class="logo">
            <div class="logo-dot"></div>
            AlphaPIL Coordinator 🎯
        </div>
        <div style="font-size: 14px; color: #a5a5cc;">Active Image: <span style="color: white; font-weight: 600;">{os.path.basename(image_path)}</span></div>
    </header>

    <div class="main-container">
        <div class="picker-area">
            <div class="image-wrapper" id="img-wrapper">
                <img id="target-img" src="/{rel_image_path}" alt="Rendered Canvas">
                <div class="reticle-x" id="reticle-x"></div>
                <div class="reticle-y" id="reticle-y"></div>
            </div>
        </div>

        <div class="control-panel">
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

                <div style="margin-bottom: 12px; font-size: 14px; color: #a5a5cc; font-weight: 500;">Saved Click Point (Semicolon Separated):</div>
                <div class="clipboard-box" id="clipboard-box" onclick="copySaved()">
                    <span id="saved-text">Click anywhere on image</span>
                    <span style="font-size: 12px; color: #5865F2; font-weight: 600;">COPY</span>
                </div>
            </div>

            <div class="panel-card">
                <div class="panel-title">
                    <span>📁 Load Different Image</span>
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
        <span>✅ Coordinates copied to clipboard!</span>
    </div>

    <script>
        const wrapper = document.getElementById('img-wrapper');
        const img = document.getElementById('target-img');
        const valX = document.getElementById('val-x');
        const valY = document.getElementById('val-y');
        const boxX = document.getElementById('box-x');
        const boxY = document.getElementById('box-y');
        const rx = document.getElementById('reticle-x');
        const ry = document.getElementById('reticle-y');
        const clipboard = document.getElementById('clipboard-box');
        const savedText = document.getElementById('saved-text');
        const toast = document.getElementById('toast');

        let lastClickedCoord = "";

        // Track mouse position over the image wrapper
        wrapper.addEventListener('mousemove', (e) => {{
            const rect = img.getBoundingClientRect();
            
            // Calculate relative pixel coordinate based on original image dimensions
            const scaleX = img.naturalWidth / rect.width;
            const scaleY = img.naturalHeight / rect.height;
            
            const px = Math.floor((e.clientX - rect.left) * scaleX);
            const py = Math.floor((e.clientY - rect.top) * scaleY);
            
            // Boundary validation
            if (px >= 0 && px <= img.naturalWidth && py >= 0 && py <= img.naturalHeight) {{
                valX.innerText = px;
                valY.innerText = py;
                
                // Position reticle lines
                rx.style.left = (e.clientX - rect.left) + 'px';
                rx.style.display = 'block';
                
                ry.style.top = (e.clientY - rect.top) + 'px';
                ry.style.display = 'block';
            }} else {{
                hideReticle();
            }}
        }});

        wrapper.addEventListener('mouseleave', () => {{
            hideReticle();
        }});

        function hideReticle() {{
            rx.style.display = 'none';
            ry.style.display = 'none';
        }}

        // Handle Click to Save/Copy Coordinates
        wrapper.addEventListener('click', () => {{
            const x = valX.innerText;
            const y = valY.innerText;
            lastClickedCoord = `${{x}};${{y}}`;
            
            savedText.innerText = lastClickedCoord;
            boxX.classList.add('highlight');
            boxY.classList.add('highlight');
            
            setTimeout(() => {{
                boxX.classList.remove('highlight');
                boxY.classList.remove('highlight');
            }}, 1500);

            copyToClipboard(lastClickedCoord);
        }});

        function copySaved() {{
            if (lastClickedCoord) {{
                copyToClipboard(lastClickedCoord);
            }}
        }}

        function copyToClipboard(text) {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast();
            }}).catch(err => {{
                // Fallback method
                const textArea = document.createElement("textarea");
                textArea.value = text;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand("copy");
                document.body.removeChild(textArea);
                showToast();
            }});
        }}

        function showToast() {{
            toast.classList.add('show');
            setTimeout(() => {{
                toast.classList.remove('show');
            }}, 2000);
        }}

        // Allow loading other local files via browser file dialog
        function loadFile(e) {{
            const file = e.target.files[0];
            if (file) {{
                const reader = new FileReader();
                reader.onload = function(event) {{
                    img.src = event.target.result;
                    savedText.innerText = "Click anywhere on image";
                    lastClickedCoord = "";
                }}
                reader.readAsDataURL(file);
            }}
        }}

        // Drag & Drop support
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
                    savedText.innerText = "Click anywhere on image";
                    lastClickedCoord = "";
                }}
                reader.readAsDataURL(file);
            }}
        }});
    </script>
</body>
</html>"""
    
    html_path = os.path.join(project_root, 'tools', 'coordinate_picker.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    return html_path

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging server requests to the console
        return

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    # 1. Resolve image path
    image_path = None
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
    
    if not image_path:
        # Default choices
        possible_paths = [
            "/home/yogeswar/Desktop/Projects/youtube/alphapil/pil/output.png",
            os.path.join(project_root, "output.png"),
            os.path.join(project_root, "youtube", "alphapil", "pil", "output.png")
        ]
        for path in possible_paths:
            if os.path.exists(path):
                image_path = path
                break
                
    if not image_path:
        print("❌ Image path not found. Please provide an image path as argument.")
        print("Usage: python tools/coordinate_picker.py <path_to_image>")
        sys.exit(1)
        
    print(f"🎯 Target Image: {image_path}")
    
    # 2. Generate HTML Page
    html_path = generate_html(image_path, project_root)
    
    # 3. Start local HTTP server
    port = find_free_port()
    # Change cwd to project root so the server serves relative paths
    os.chdir(project_root)
    
    # SimpleHTTPRequestHandler serves files relative to current directory
    httpd = socketserver.TCPServer(("", port), CustomHandler)
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # 4. Open browser
    url = f"http://localhost:{port}/tools/coordinate_picker.html"
    print(f"🌍 Opening Interactive Coordinator Webpage at: {url}")
    print("⏹️  Press Ctrl+C in this terminal to shut down the coordinator server.")
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

if __name__ == "__main__":
    main()
