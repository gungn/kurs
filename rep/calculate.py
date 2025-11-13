import math

def calculate_geometry(shape_combobox, input_frame, result_label):
    shape = shape_combobox.get()
    
    try:
        if shape == "Triangle":
            values = get_triangle_inputs(input_frame)
            perimeter, area = calculate_triangle(**values)
        elif shape == "Rectangle":
            values = get_rectangle_inputs(input_frame)
            perimeter, area = calculate_rectangle(**values)
        elif shape == "Trapezoid":
            values = get_trapezoid_inputs(input_frame)
            perimeter, area = calculate_trapezoid(**values)
        else:
            result_label.config(text="Please select a shape")
            return
        
        result_text = f"Perimeter: {perimeter:.2f}\nArea: {area:.2f}"
        result_label.config(text=result_text)
    
    except ValueError as e:
        result_label.config(text=str(e))
    except Exception as e:
        result_label.config(text="Error in calculation")

def get_triangle_inputs(input_frame):
    from gui import get_input_values
    values = get_input_values(input_frame, ['a', 'b', 'c'])
    a = float(values['a'])
    b = float(values['b'])
    c = float(values['c'])
    return {'a': a, 'b': b, 'c': c}

def get_rectangle_inputs(input_frame):
    from gui import get_input_values
    values = get_input_values(input_frame, ['a', 'b'])
    a = float(values['a'])
    b = float(values['b'])
    return {'a': a, 'b': b}

def get_trapezoid_inputs(input_frame):
    from gui import get_input_values
    values = get_input_values(input_frame, ['a', 'b', 'c', 'd', 'h'])
    a = float(values['a'])
    b = float(values['b'])
    c = float(values['c'])
    d = float(values['d'])
    h = float(values['h'])
    return {'a': a, 'b': b, 'c': c, 'd': d, 'h': h}

def calculate_triangle(a, b, c):
    # Validate triangle inequality
    if a + b <= c or a + c <= b or b + c <= a:
        raise ValueError("Invalid triangle sides")
    
    perimeter = a + b + c
    s = perimeter / 2
    area = math.sqrt(s * (s - a) * (s - b) * (s - c))
    return perimeter, area

def calculate_rectangle(a, b):
    if a <= 0 or b <= 0:
        raise ValueError("Sides must be positive")
    
    perimeter = 2 * (a + b)
    area = a * b
    return perimeter, area

def calculate_trapezoid(a, b, c, d, h):
    if a <= 0 or b <= 0 or c <= 0 or d <= 0 or h <= 0:
        raise ValueError("All values must be positive")
    
    perimeter = a + b + c + d
    area = (a + b) * h / 2
    return perimeter, area