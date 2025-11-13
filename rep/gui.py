import tkinter as tk
from tkinter import ttk
from calculate import calculate_geometry
from docx_export import save_calculation_to_docx

# Global variable to store last calculation results
last_calculation = None

def create_main_window():
    root = tk.Tk()
    root.title("Geometry Calculator")
    root.resizable(False, False)
    
    # Shape selection
    tk.Label(root, text="Select shape:").grid(row=0, column=0, padx=5, pady=5)
    shape_combobox = ttk.Combobox(root, values=["Triangle", "Rectangle", "Trapezoid"])
    shape_combobox.grid(row=0, column=1, padx=5, pady=5)
    shape_combobox.bind('<<ComboboxSelected>>', lambda e: show_fields(input_frame, shape_combobox))
    
    # Input fields frame
    input_frame = tk.Frame(root)
    input_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    
    # Calculate button
    calculate_button = tk.Button(
        root, 
        text="Calculate", 
        command=lambda: calculate_and_store(shape_combobox, input_frame, result_label)
    )
    calculate_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
    
    # Save button
    save_button = tk.Button(
        root,
        text="Save to DOCX",
        command=lambda: save_to_docx(result_label)
    )
    save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    
    # Result display
    result_label = tk.Label(root, text="", justify=tk.LEFT)
    result_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    
    root.mainloop()

def calculate_and_store(shape_combobox, input_frame, result_label):
    """
    Calculate and store results for potential saving
    """
    global last_calculation
    
    # Call existing calculate_geometry function
    calculate_geometry(shape_combobox, input_frame, result_label)
    
    # Extract results from label text for saving
    result_text = result_label.cget("text")
    if "Perimeter:" in result_text and "Area:" in result_text:
        try:
            # Parse the results from the label text
            lines = result_text.split('\n')
            perimeter = float(lines[0].split(": ")[1])
            area = float(lines[1].split(": ")[1])
            
            # Get shape and parameters
            shape = shape_combobox.get()
            parameters = get_current_parameters(input_frame, shape)
            
            # Store for saving
            last_calculation = {
                'shape': shape,
                'parameters': parameters,
                'perimeter': perimeter,
                'area': area
            }
        except:
            last_calculation = None

def get_current_parameters(input_frame, shape):
    """
    Get current parameters from input fields
    """
    try:
        if shape == "Triangle":
            values = get_input_values(input_frame, ['a', 'b', 'c'])
            return {k: float(v) for k, v in values.items()}
        elif shape == "Rectangle":
            values = get_input_values(input_frame, ['a', 'b'])
            return {k: float(v) for k, v in values.items()}
        elif shape == "Trapezoid":
            values = get_input_values(input_frame, ['a', 'b', 'c', 'd', 'h'])
            return {k: float(v) for k, v in values.items()}
    except:
        return {}

def save_to_docx(result_label):
    """
    Save last calculation to DOCX file
    """
    global last_calculation
    if last_calculation is None:
        result_label.config(text="No calculation to save. Please calculate first.")
        return
    
    try:
        filename = save_calculation_to_docx(
            last_calculation['shape'],
            last_calculation['parameters'],
            last_calculation['perimeter'],
            last_calculation['area']
        )
        current_text = result_label.cget("text")
        result_label.config(text=f"{current_text}\n\nSaved to: {filename}")
    except Exception as e:
        result_label.config(text=f"Error saving file: {str(e)}")

# Keep the existing functions unchanged
def show_fields(input_frame, shape_combobox):
    # Clear previous input fields
    for widget in input_frame.winfo_children():
        widget.destroy()
    
    shape = shape_combobox.get()
    
    if shape == "Triangle":
        tk.Label(input_frame, text="Side a:").grid(row=0, column=0)
        tk.Entry(input_frame, name="entry_a").grid(row=0, column=1)
        
        tk.Label(input_frame, text="Side b:").grid(row=1, column=0)
        tk.Entry(input_frame, name="entry_b").grid(row=1, column=1)
        
        tk.Label(input_frame, text="Side c:").grid(row=2, column=0)
        tk.Entry(input_frame, name="entry_c").grid(row=2, column=1)
        
    elif shape == "Rectangle":
        tk.Label(input_frame, text="Length:").grid(row=0, column=0)
        tk.Entry(input_frame, name="entry_a").grid(row=0, column=1)
        
        tk.Label(input_frame, text="Width:").grid(row=1, column=0)
        tk.Entry(input_frame, name="entry_b").grid(row=1, column=1)
        
    elif shape == "Trapezoid":
        tk.Label(input_frame, text="Base a:").grid(row=0, column=0)
        tk.Entry(input_frame, name="entry_a").grid(row=0, column=1)
        
        tk.Label(input_frame, text="Base b:").grid(row=1, column=0)
        tk.Entry(input_frame, name="entry_b").grid(row=1, column=1)
        
        tk.Label(input_frame, text="Side c:").grid(row=2, column=0)
        tk.Entry(input_frame, name="entry_c").grid(row=2, column=1)
        
        tk.Label(input_frame, text="Side d:").grid(row=3, column=0)
        tk.Entry(input_frame, name="entry_d").grid(row=3, column=1)
        
        tk.Label(input_frame, text="Height h:").grid(row=4, column=0)
        tk.Entry(input_frame, name="entry_h").grid(row=4, column=1)

def get_input_values(input_frame, field_names):
    values = {}
    for field in field_names:
        entry_widget = input_frame.nametowidget(f"entry_{field}")
        values[field] = entry_widget.get()
    return values