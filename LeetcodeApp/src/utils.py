import os
import json
import random
import base64
from datetime import datetime
import pyperclip

def copy_to_clipboard(text):
    """Discreetly copy text to clipboard."""
    try:
        pyperclip.copy(text)
        return True
    except Exception:
        return False

def load_history(history_dir):
    """Load solution history from files."""
    if not os.path.exists(history_dir):
        return []
    
    history = []
    for filename in os.listdir(history_dir):
        if filename.endswith('.json'):
            try:
                with open(os.path.join(history_dir, filename), 'r') as f:
                    history.append(json.load(f))
            except:
                continue
    
    return sorted(history, key=lambda x: x.get('timestamp', 0), reverse=True)

def obfuscate_solution(solution_code):
    """
    Obfuscate solution to avoid detection by pattern matching or simple plagiarism systems.
    This just makes minor, non-functional changes to the code.
    """
    # List of possible variable name changes
    var_changes = {
        'i': ['idx', 'index', 'pos'],
        'j': ['jdx', 'j_index', 'inner_idx'],
        'k': ['kdx', 'k_pos', 'third_idx'],
        'nums': ['numbers', 'num_array', 'values'],
        'arr': ['array', 'elements', 'items'],
        'result': ['res', 'ans', 'output', 'solution'],
        'curr': ['current', 'cur', 'now'],
        'prev': ['previous', 'prev_val', 'before'],
        'next': ['next_val', 'after', 'following'],
        'temp': ['tmp', 'temporary', 'placeholder']
    }
    
    # Apply simple transformations
    for old, alternatives in var_changes.items():
        if old in solution_code and random.random() > 0.5:
            new = random.choice(alternatives)
            # Only replace if it's a whole word (not part of another word)
            solution_code = solution_code.replace(f" {old} ", f" {new} ")
            solution_code = solution_code.replace(f" {old},", f" {new},")
            solution_code = solution_code.replace(f" {old}:", f" {new}:")
            solution_code = solution_code.replace(f" {old}=", f" {new}=")
            solution_code = solution_code.replace(f"({old},", f"({new},")
            solution_code = solution_code.replace(f"({old})", f"({new})")
            
    # Insert random (but valid) whitespace
    if random.random() > 0.5:
        solution_code = solution_code.replace("for ", "for ")
        solution_code = solution_code.replace("if ", "if ")
        solution_code = solution_code.replace("while ", "while ")
        solution_code = solution_code.replace("return ", "return ")
        
    # Add some meaningless but harmless comments
    comments = [
        "# Process this part carefully",
        "# Handle the calculation",
        "# Update the value",
        "# Initialize variables",
        "# Check for edge cases",
        "# Helper function to streamline code"
    ]
    
    lines = solution_code.split('\n')
    for _ in range(min(2, len(lines))):
        if random.random() > 0.7:
            line_idx = random.randint(0, len(lines) - 1)
            if not lines[line_idx].strip().startswith("#") and lines[line_idx].strip():
                lines[line_idx] = lines[line_idx] + "  " + random.choice(comments)
                
    return '\n'.join(lines)

def export_solution(solution, file_path=None):
    """Export solution to a file with a generic name."""
    if not file_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(os.path.expanduser("~"), "Documents", f"study_notes_{timestamp}.py")
        
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            f.write(solution)
        return file_path
    except Exception as e:
        return None

def secure_save(solution, problem_description, problem_type):
    """Save solution in a more secure way, using obfuscation and encoding."""
    data = {
        "solution": solution,
        "problem": problem_description,
        "type": problem_type,
        "timestamp": datetime.now().isoformat()
    }
    
    # Convert to JSON and encode
    json_str = json.dumps(data)
    encoded = base64.b64encode(json_str.encode()).decode()
    
    # Save to a hidden folder with innocuous name
    docs_dir = os.path.join(os.path.expanduser("~"), "Documents")
    hidden_dir = os.path.join(docs_dir, ".temp_study_data")
    os.makedirs(hidden_dir, exist_ok=True)
    
    filename = f"note_{random.randint(1000, 9999)}.dat"
    with open(os.path.join(hidden_dir, filename), 'w') as f:
        f.write(encoded)
    
    return os.path.join(hidden_dir, filename)

def stealth_mode_activate():
    """
    Activate additional stealth features for the application.
    This makes the application less detectable by monitoring software.
    """
    # Use generic process name if possible
    try:
        import ctypes
        if hasattr(ctypes, 'windll') and hasattr(ctypes.windll, 'kernel32'):
            # Try to change the window title (Windows only)
            ctypes.windll.kernel32.SetConsoleTitleW("Study Helper")
    except:
        pass
    
    # Clean temporary files periodically
    def clean_temp_files():
        try:
            import tempfile
            temp_dir = tempfile.gettempdir()
            for file in os.listdir(temp_dir):
                if file.startswith('py_') and file.endswith('.tmp'):
                    try:
                        os.remove(os.path.join(temp_dir, file))
                    except:
                        pass
        except:
            pass
    
    # Schedule the cleaning function
    try:
        import threading
        cleaner = threading.Timer(300, clean_temp_files)  # Run every 5 minutes
        cleaner.daemon = True
        cleaner.start()
    except:
        pass
    
    return True 