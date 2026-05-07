#!/usr/bin/env python3
"""
AlphaPIL Live Previewer

This script monitors the templates/ folder and automatically renders
templates when they are saved, providing instant visual feedback.
"""

import os
import sys
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image

# Add src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, os.path.join(project_root, 'src'))

from alphapil import CanvasEngine


class TemplatePreviewer(FileSystemEventHandler):
    """Handler for template file changes."""
    
    def __init__(self, templates_dir: str, dummy_data: dict):
        """
        Initialize the previewer.
        
        Args:
            templates_dir: Path to templates directory
            dummy_data: Dictionary of mock variables for rendering
        """
        self.templates_dir = templates_dir
        self.dummy_data = dummy_data
        self.engine = CanvasEngine()
        
        # Set up dummy variables
        for key, value in dummy_data.items():
            self.engine.set_variable(key, value)
        
        print("🎨 AlphaPIL Live Previewer Started")
        print(f"📁 Monitoring: {templates_dir}")
        print(f"🔧 Using dummy data: {list(dummy_data.keys())}")
        print("⏹️  Press Ctrl+C to stop")
        print("-" * 50)
    
    def on_modified(self, event):
        """Handle file modification events."""
        if event.is_directory:
            return
        
        # Only process .txt files
        if not event.src_path.endswith('.txt'):
            return
        
        # Small delay to avoid multiple triggers
        time.sleep(0.1)
        
        try:
            self.render_template(event.src_path)
        except Exception as e:
            print(f"❌ Error rendering {os.path.basename(event.src_path)}: {e}")
    
    def render_template(self, template_path: str):
        """
        Render a template file and display the result.
        
        Args:
            template_path: Path to the template file
        """
        filename = os.path.basename(template_path)
        print(f"🔄 Rendering: {filename}")
        
        try:
            # Read template file
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Reset canvas
            self.engine.reset()
            
            # Re-set dummy variables (in case they were modified during rendering)
            for key, value in self.dummy_data.items():
                self.engine.set_variable(key, value)
            
            # Process each line
            lines = template_content.strip().split('\n')
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                
                try:
                    result = self.engine.parse(line)
                    if result and not result.startswith("Canvas created"):
                        print(f"   ✓ {result}")
                except Exception as e:
                    print(f"   ❌ Line {line_num}: {e}")
                    print(f"      Content: {line}")
            
            # Display the result
            if self.engine.canvas:
                self.display_image(self.engine.canvas, filename)
            else:
                print(f"⚠️  No canvas generated for {filename}")
                
        except Exception as e:
            print(f"❌ Failed to render {filename}: {e}")
    
    def display_image(self, canvas, filename: str):
        """
        Display the rendered canvas.
        
        Args:
            canvas: PIL Image object
            filename: Original template filename
        """
        try:
            # Create a copy to avoid modifying the original
            display_img = canvas.copy()
            
            # Add filename as watermark for identification
            from PIL import ImageDraw, ImageFont
            draw = ImageDraw.Draw(display_img)
            
            try:
                font = ImageFont.truetype("arial.ttf", 12)
            except:
                font = ImageFont.load_default()
            
            # Add semi-transparent background for text
            text_bbox = draw.textbbox((0, 0), f"Preview: {filename}", font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Draw background rectangle
            draw.rectangle(
                [(5, 5), (15 + text_width, 15 + text_height)],
                fill=(255, 255, 255, 200),
                outline=(0, 0, 0)
            )
            
            # Draw text
            draw.text((10, 10), f"Preview: {filename}", fill=(0, 0, 0), font=font)
            
            # Show the image
            display_img.show()
            print(f"🖼️  Preview displayed for {filename}")
            
        except Exception as e:
            print(f"❌ Failed to display image: {e}")


def get_dummy_data() -> dict:
    """
    Get comprehensive dummy data for template rendering.
    
    Returns:
        Dictionary of mock variables
    """
    return {
        # User data
        'name': 'AlphaUser',
        'username': 'alpha_dev',
        'display_name': 'Alpha Developer',
        'avatar_url': 'https://i.imgur.com/8f8vXoU.png',
        'xp': '80',
        'level': '5',
        'rank': 'Developer',
        
        # Colors
        'primary_color': '#5865F2',  # Discord blurple
        'secondary_color': '#57F287',  # Discord green
        'accent_color': '#FEE75C',     # Discord yellow
        'danger_color': '#ED4245',     # Discord red
        
        # Text content
        'title': 'AlphaPIL Demo',
        'subtitle': 'Template-Based Image Generation',
        'description': 'This is a demonstration of AlphaPIL capabilities',
        'footer': 'Generated with AlphaPIL v0.1.0',
        
        # Dimensions
        'canvas_width': '800',
        'canvas_height': '600',
        'card_width': '300',
        'card_height': '150',
        
        # Status
        'status': 'online',
        'is_premium': 'true',
        'is_verified': 'true',
        
        # Numbers
        'followers': '1234',
        'posts': '567',
        'likes': '8901',
        
        # URLs
        'profile_url': 'https://example.com/profile',
        'website_url': 'https://alphapil.dev',
        
        # Dates
        'join_date': '2024-01-15',
        'last_active': '2024-02-16',
        
        # Random data for testing
        'random_number': '42',
        'random_color': 'blurple',
        'random_size': '24',
    }


def main():
    """Main function to run the live previewer."""
    # Get paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    templates_dir = os.path.join(project_root, 'templates')
    
    # Check if templates directory exists
    if not os.path.exists(templates_dir):
        print(f"❌ Templates directory not found: {templates_dir}")
        sys.exit(1)
    
    # Get dummy data
    dummy_data = get_dummy_data()
    
    # Create event handler
    event_handler = TemplatePreviewer(templates_dir, dummy_data)
    
    # Create observer
    observer = Observer()
    observer.schedule(event_handler, templates_dir, recursive=False)
    
    # Start monitoring
    observer.start()
    
    try:
        # Initial render of test.txt if it exists
        test_file = os.path.join(templates_dir, 'test.txt')
        if os.path.exists(test_file):
            print(f"🎬 Initial render of test.txt")
            event_handler.render_template(test_file)
        
        # Keep running
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n👋 Stopping previewer...")
        observer.stop()
    
    observer.join()
    print("✅ Previewer stopped")


if __name__ == "__main__":
    main()
