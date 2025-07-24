#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as patches

class SimpleMouseViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("USB Mouse Drawing Viewer")
        self.root.geometry("800x600")
        
        self.mouse_data = []
        self.setup_gui()
        
    def setup_gui(self):
        # Control frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="Load File", command=self.load_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Show Drawing", command=self.show_drawing).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Clear", command=self.clear_plot).pack(side=tk.LEFT, padx=5)
        
        # Plot frame
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, self.root)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
    def load_file(self):
        file_path = filedialog.askopenfilename(
            title="Select USB data file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            self.parse_mouse_data(file_path)
            messagebox.showinfo("Success", f"Loaded {len(self.mouse_data)} mouse packets")
    
    def parse_mouse_data(self, file_path):
        self.mouse_data = []
        try:
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            for i in range(0, len(lines), 2):
                if i + 1 < len(lines):
                    data_line = lines[i].strip()
                    if len(data_line) >= 8 and data_line != "0":
                        # Parse HID mouse data
                        buttons = int(data_line[0:2], 16)
                        x_raw = int(data_line[2:4], 16)
                        y_raw = int(data_line[4:6], 16)
                        
                        # Convert to signed bytes
                        x_move = x_raw if x_raw < 128 else x_raw - 256
                        y_move = y_raw if y_raw < 128 else y_raw - 256
                        left_click = bool(buttons & 0x01)
                        
                        self.mouse_data.append({
                            'left_click': left_click,
                            'x_move': x_move,
                            'y_move': y_move
                        })
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse file: {str(e)}")
    
    def show_drawing(self):
        if not self.mouse_data:
            messagebox.showwarning("Warning", "Please load a file first")
            return
            
        self.ax.clear()
        
        # Reconstruct drawing path
        x_pos, y_pos = 0, 0
        current_stroke = []
        strokes = []
        
        for data in self.mouse_data:
            x_pos += data['x_move']
            y_pos += data['y_move']
            
            if data['left_click']:
                current_stroke.append((x_pos, y_pos))
            else:
                if current_stroke:
                    strokes.append(current_stroke)
                    current_stroke = []
        
        if current_stroke:
            strokes.append(current_stroke)
        
        # Draw all strokes
        for stroke in strokes:
            if len(stroke) > 1:
                x_coords = [point[0] for point in stroke]
                y_coords = [point[1] for point in stroke]
                self.ax.plot(x_coords, y_coords, 'black', linewidth=3, alpha=0.8)
        
        self.ax.set_title('USB Mouse Drawing Reconstruction', fontsize=14, fontweight='bold')
        self.ax.axis('equal')
        self.ax.invert_yaxis()  # Invert Y for screen coordinates
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('X Position')
        self.ax.set_ylabel('Y Position')
        
        self.canvas.draw()
        
        # Show stats
        total_strokes = len(strokes)
        total_clicks = sum(1 for d in self.mouse_data if d['left_click'])
        print(f"Drawing complete: {total_strokes} strokes, {total_clicks} click packets")
    
    def clear_plot(self):
        self.ax.clear()
        self.ax.set_title('USB Mouse Drawing Viewer - Ready')
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleMouseViewer(root)
    
    # Auto-load the extracted file if it exists
    try:
        app.parse_mouse_data('extracted_1.txt')
        app.show_drawing()
        print("Auto-loaded extracted_1.txt")
    except:
        print("No extracted_1.txt found - use Load File button")
    
    root.mainloop() 
