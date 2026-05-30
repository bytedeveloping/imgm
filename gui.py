"""GUI mode for imgm."""
import tkinter as tk
from tkinter import filedialog, messagebox, Scale
from pathlib import Path
from PIL import Image, ImageTk
import processor
from presets import list_presets


class ImgmGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("imgm - Image Processor")
        self.root.geometry("800x600")
        
        self.current_image = None
        self.current_image_path = None
        self.preview_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI elements."""
        # File selection
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Open Image", command=self.open_image).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=5)
        
        # Preview
        self.preview_label = tk.Label(self.root, text="No image loaded", bg="gray")
        self.preview_label.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Filters section
        filters_frame = tk.LabelFrame(self.root, text="Filters")
        filters_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(filters_frame, text="Brightness:").pack()
        self.brightness_slider = Scale(filters_frame, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.brightness_slider.set(1.0)
        self.brightness_slider.pack(fill=tk.X)
        
        tk.Label(filters_frame, text="Contrast:").pack()
        self.contrast_slider = Scale(filters_frame, from_=0.0, to=2.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.contrast_slider.set(1.0)
        self.contrast_slider.pack(fill=tk.X)
        
        tk.Label(filters_frame, text="Blur:").pack()
        self.blur_slider = Scale(filters_frame, from_=0, to=20, orient=tk.HORIZONTAL)
        self.blur_slider.set(0)
        self.blur_slider.pack(fill=tk.X)
        
        # Presets
        presets_frame = tk.LabelFrame(self.root, text="Presets")
        presets_frame.pack(pady=10, padx=10, fill=tk.X)
        
        for preset in list_presets():
            tk.Button(presets_frame, text=preset, command=lambda p=preset: self.apply_preset(p)).pack(side=tk.LEFT, padx=5)
        
        # Apply button
        tk.Button(self.root, text="Apply & Preview", command=self.apply_preview, bg="green", fg="white").pack(pady=10)
    
    def open_image(self):
        """Open image dialog."""
        filetypes = [("Images", "*.png *.jpg *.jpeg *.gif *.bmp *.webp *.tiff"), ("All Files", "*.*")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        if filepath:
            self.current_image_path = filepath
            self.current_image = Image.open(filepath).convert('RGBA')
            self.display_preview(self.current_image)
    
    def save_image(self):
        """Save image dialog."""
        if self.current_image is None:
            messagebox.showerror("Error", "No image loaded")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("GIF", "*.gif"), ("All Files", "*.*")]
        )
        if filepath:
            processor.save_image(self.current_image, filepath)
            messagebox.showinfo("Success", f"Image saved: {filepath}")
    
    def display_preview(self, img):
        """Display preview of image."""
        # Resize for preview
        preview_img = img.copy()
        preview_img.thumbnail((400, 400))
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(preview_img)
        self.preview_label.config(image=photo, text="")
        self.preview_label.image = photo
    
    def apply_preview(self):
        """Apply filters and show preview."""
        if self.current_image is None:
            messagebox.showerror("Error", "No image loaded")
            return
        
        filter_dict = {
            'brightness': self.brightness_slider.get(),
            'contrast': self.contrast_slider.get(),
        }
        
        if self.blur_slider.get() > 0:
            filter_dict['blur'] = self.blur_slider.get()
        
        processed = processor.apply_filters(self.current_image, filter_dict)
        if processed:
            self.current_image = processed
            self.display_preview(processed)
    
    def apply_preset(self, preset_name):
        """Apply a preset."""
        if self.current_image is None:
            messagebox.showerror("Error", "No image loaded")
            return
        
        from presets import get_preset
        preset = get_preset(preset_name)
        if preset:
            processed = processor.apply_filters(self.current_image, preset)
            if processed:
                self.current_image = processed
                self.display_preview(processed)


def launch_gui():
    """Launch GUI."""
    root = tk.Tk()
    app = ImgmGUI(root)
    root.mainloop()


if __name__ == '__main__':
    launch_gui()
