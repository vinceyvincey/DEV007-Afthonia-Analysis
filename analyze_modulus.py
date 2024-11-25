import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import glob
import os
from tkinter import messagebox

class ModulusAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Setup main window
        self.title("Flexural Modulus Analyzer")
        self.geometry("1300x800")
        
        # Initialize strain variables with default values
        self.strain_min = tk.DoubleVar(value=0.01)
        self.strain_max = tk.DoubleVar(value=0.2)
        
        # Load files
        self.files = glob.glob('raw_data/*.csv')
        self.file_names = [os.path.basename(f) for f in self.files]
        
        self.current_file_index = 0
        self.dragging_line = None
        self.left_line = None
        self.right_line = None
        
        # Add progress tracking
        self.progress_var = tk.StringVar(value="File 1 of 0")
        
        # Add data storage
        self.results = []
        
        self.setup_gui()
        self.current_modulus = None
        
    def setup_gui(self):
        # Create main container
        main_container = ttk.Frame(self)
        main_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Create left panel for plot and controls
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side='left', fill='both', expand=True)
        
        # Move existing controls to left panel
        controls = ttk.Frame(left_panel)
        controls.pack(fill='x', padx=5, pady=5)
        
        # Add strain control frame
        strain_frame = ttk.Frame(controls)
        strain_frame.pack(side='left', padx=5)
        
        # Add strain min/max entry boxes with bindings
        ttk.Label(strain_frame, text="Min Strain:").pack(side='left')
        strain_min_entry = ttk.Entry(strain_frame, width=6, textvariable=self.strain_min)
        strain_min_entry.pack(side='left', padx=2)
        
        ttk.Label(strain_frame, text="Max Strain:").pack(side='left', padx=(10,0))
        strain_max_entry = ttk.Entry(strain_frame, width=6, textvariable=self.strain_max)
        strain_max_entry.pack(side='left', padx=2)
        
        # Bind update events to entries
        strain_min_entry.bind('<Return>', self.update_plot)
        strain_min_entry.bind('<FocusOut>', self.update_plot)
        strain_max_entry.bind('<Return>', self.update_plot)
        strain_max_entry.bind('<FocusOut>', self.update_plot)
        
        # Progress indicator
        ttk.Label(controls, textvariable=self.progress_var).pack(side='left', padx=5)
        
        # Accept button
        self.accept_button = ttk.Button(controls, text="Accept (Enter)", command=self.accept_and_advance)
        self.accept_button.pack(side='left', padx=5)
        
        # Modulus display
        self.modulus_var = tk.StringVar(value="Modulus: --")
        ttk.Label(controls, textvariable=self.modulus_var).pack(side='right', padx=5)
        
        # File selector
        ttk.Label(controls, text="Select File:").pack(side='left', padx=5)
        self.file_var = tk.StringVar()
        file_select = ttk.Combobox(controls, textvariable=self.file_var, values=self.file_names)
        file_select.pack(side='left', padx=5)
        file_select.bind('<<ComboboxSelected>>', self.update_plot)
        
        # Add export button next to other controls
        export_button = ttk.Button(controls, text="Export Data", command=self.export_results)
        export_button.pack(side='left', padx=5)
        
        # Move matplotlib canvas to left panel
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=left_panel)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
        
        # Load first file automatically
        if self.file_names:
            self.file_var.set(self.file_names[0])
            self.update_progress()
            self.update_plot()
        
        # Add keyboard binding for Enter key
        self.bind('<Return>', lambda event: self.accept_and_advance())
    
    def calculate_modulus(self, strain_min, strain_max, df):
        """Calculate modulus for selected strain range"""
        # Convert both columns to numeric values
        df['Strain (%)'] = pd.to_numeric(df['Strain (%)'], errors='coerce')
        df['Stress (MPa)'] = pd.to_numeric(df['Stress (MPa)'], errors='coerce')
        
        mask = (df['Strain (%)'] >= strain_min) & (df['Strain (%)'] <= strain_max)
        strain = df['Strain (%)'][mask] / 100  # Convert to decimal
        stress = df['Stress (MPa)'][mask]
        
        if len(strain) < 2:
            return None, None
            
        # Print debug info
        print(f"Strain range: {strain.min():.4f} to {strain.max():.4f}")
        print(f"Stress range: {stress.min():.2f} to {stress.max():.2f} MPa")
        
        coefficients = np.polyfit(strain, stress, 1)
        modulus = coefficients[0]  # This is the slope of the line
        
        # Print calculated modulus
        print(f"Calculated modulus: {modulus:.0f} MPa")
        
        fit_line = np.poly1d(coefficients)
        return modulus, fit_line
    
    def update_plot(self, *args):
        if not self.file_var.get():
            return
            
        # Clear previous plot
        self.ax.clear()
        
        # Load selected file
        file_path = os.path.join('raw_data', self.file_var.get())
        df = pd.read_csv(file_path)
        
        # Calculate modulus
        strain_min = self.strain_min.get()
        strain_max = self.strain_max.get()
        modulus, fit_line = self.calculate_modulus(strain_min, strain_max, df)
        
        # Plot data
        self.ax.plot(df['Strain (%)'], df['Stress (MPa)'], 'b-', label='Data')
        
        if modulus is not None:
            # Plot fit line
            mask = (df['Strain (%)'] >= strain_min) & (df['Strain (%)'] <= strain_max)
            strain_fit = df['Strain (%)'][mask] / 100
            self.ax.plot(df['Strain (%)'][mask], 
                        fit_line(strain_fit), 
                        'r-', 
                        label=f'Fit (Modulus = {modulus:.0f} MPa)')
            
            # Highlight selected region
            self.ax.axvspan(strain_min, strain_max, alpha=0.2, color='yellow')
            
            # Update modulus display
            self.modulus_var.set(f"Modulus: {modulus:.0f} MPa")
        
        # Set labels and title
        self.ax.set_xlabel('Strain (%)')
        self.ax.set_ylabel('Stress (MPa)')
        self.ax.set_title(f'Stress-Strain Curve: {self.file_var.get()}')
        self.ax.grid(True)
        self.ax.legend()
        
        # Add or update vertical lines
        if self.left_line is None:
            self.left_line = self.ax.axvline(x=strain_min, color='r', linestyle='--', picker=True)
            self.right_line = self.ax.axvline(x=strain_max, color='r', linestyle='--', picker=True)
            
            # Connect the mouse events
            self.canvas.mpl_connect('button_press_event', self.on_click)
            self.canvas.mpl_connect('motion_notify_event', self.on_motion)
            self.canvas.mpl_connect('button_release_event', self.on_release)
        else:
            # Remove old lines
            self.left_line.remove()
            self.right_line.remove()
            # Create new lines
            self.left_line = self.ax.axvline(x=strain_min, color='r', linestyle='--', picker=True)
            self.right_line = self.ax.axvline(x=strain_max, color='r', linestyle='--', picker=True)
        
        self.canvas.draw()
    
    def on_click(self, event):
        if event.inaxes != self.ax:
            return
        
        # Check if click is near either line
        left_x = self.left_line.get_xdata()[0]
        right_x = self.right_line.get_xdata()[0]
        
        if abs(event.xdata - left_x) < 0.1:
            self.dragging_line = self.left_line
        elif abs(event.xdata - right_x) < 0.1:
            self.dragging_line = self.right_line
    
    def on_motion(self, event):
        if event.inaxes != self.ax or self.dragging_line is None:
            return
        
        self.dragging_line.set_xdata([event.xdata, event.xdata])
        if self.dragging_line == self.left_line:
            self.strain_min.set(event.xdata)
        else:
            self.strain_max.set(event.xdata)
        self.canvas.draw()
    
    def on_release(self, event):
        self.dragging_line = None
        self.update_plot()
    
    def update_progress(self):
        self.progress_var.set(f"File {self.current_file_index + 1} of {len(self.file_names)}")
    
    def accept_and_advance(self):
        # Save current results
        current_file = self.file_var.get()
        modulus = float(self.modulus_var.get().split(': ')[1].split(' ')[0])
        result = {
            'filename': current_file,
            'strain_min': self.strain_min.get(),
            'strain_max': self.strain_max.get(),
            'modulus': modulus
        }
        
        # Add to results list
        self.results.append(result)
        
        # Move to next file
        self.current_file_index += 1
        if self.current_file_index < len(self.file_names):
            self.file_var.set(self.file_names[self.current_file_index])
            self.update_progress()
            self.update_plot()
    
    def export_results(self):
        """Export results to CSV file"""
        if not self.results:
            tk.messagebox.showwarning("No Data", "No results to export!")
            return
        
        df = pd.DataFrame(self.results)
        df.to_csv('modulus_results.csv', index=False)
        tk.messagebox.showinfo("Success", "Results exported to 'modulus_results.csv'")
    
if __name__ == "__main__":
    app = ModulusAnalyzer()
    app.mainloop() 