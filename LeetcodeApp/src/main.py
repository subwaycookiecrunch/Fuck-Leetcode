import tkinter as tk
from tkinter import scrolledtext, messagebox, Menu
import json
import os
import sys

# Add the current directory to path to make imports work
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from solver import get_solution
    from utils import copy_to_clipboard, obfuscate_solution, secure_save, stealth_mode_activate
except ImportError as e:
    print(f"Error importing modules: {e}")

class LeetCodeHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Assistant")  # Innocent name
        self.root.geometry("800x600")
        
        # Activate stealth mode
        try:
            stealth_mode_activate()
        except Exception as e:
            print(f"Stealth mode error: {e}")
        
        # Create problem input area
        self.problem_frame = tk.LabelFrame(root, text="Problem Description")
        self.problem_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.problem_text = scrolledtext.ScrolledText(self.problem_frame, height=10)
        self.problem_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        # Create a frame for problem tags/type
        self.config_frame = tk.Frame(root)
        self.config_frame.pack(padx=10, pady=5, fill="x")
        
        tk.Label(self.config_frame, text="Problem Type:").grid(row=0, column=0, padx=5, pady=5)
        self.problem_type = tk.StringVar(value="array")
        problem_types = ["array", "string", "linked-list", "tree", "dynamic-programming", "graph", "math"]
        self.type_menu = tk.OptionMenu(self.config_frame, self.problem_type, *problem_types)
        self.type_menu.grid(row=0, column=1, padx=5, pady=5)
        
        # Checkboxes for additional options
        self.obfuscate_var = tk.BooleanVar(value=True)
        tk.Checkbutton(self.config_frame, text="Obfuscate Solution", variable=self.obfuscate_var).grid(row=0, column=2, padx=5, pady=5)
        
        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)
        
        self.solve_button = tk.Button(self.button_frame, text="Generate Solution", command=self.solve_problem)
        self.solve_button.grid(row=0, column=0, padx=5)
        
        self.copy_button = tk.Button(self.button_frame, text="Copy to Clipboard", command=self.copy_solution)
        self.copy_button.grid(row=0, column=1, padx=5)
        
        self.secure_save_button = tk.Button(self.button_frame, text="Secure Save", command=self.save_secure)
        self.secure_save_button.grid(row=0, column=2, padx=5)
        
        # Create solution display area
        self.solution_frame = tk.LabelFrame(root, text="Solution")
        self.solution_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.solution_text = scrolledtext.ScrolledText(self.solution_frame, height=15)
        self.solution_text.pack(padx=5, pady=5, fill="both", expand=True)
        
        # History management
        self.history_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "history")
        os.makedirs(self.history_dir, exist_ok=True)
        
        # Create a menu
        self.menu = Menu(root)
        root.config(menu=self.menu)
        
        file_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.clear_all)
        file_menu.add_command(label="Save", command=self.save_secure)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)
        
        help_menu = Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def solve_problem(self):
        problem_desc = self.problem_text.get("1.0", tk.END).strip()
        problem_type = self.problem_type.get()
        
        if not problem_desc:
            messagebox.showerror("Error", "Please enter a problem description")
            return
        
        try:
            # Get solution from the solver module
            solution = get_solution(problem_desc, problem_type)
            
            # Obfuscate if requested
            if self.obfuscate_var.get():
                solution = obfuscate_solution(solution)
            
            # Display the solution
            self.solution_text.delete("1.0", tk.END)
            self.solution_text.insert(tk.END, solution)
            
            # Save to history
            self.save_to_history(problem_desc, problem_type, solution)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate solution: {str(e)}")
    
    def save_to_history(self, problem, prob_type, solution):
        timestamp = os.path.join(self.history_dir, f"{prob_type}_{len(os.listdir(self.history_dir))}.json")
        with open(timestamp, 'w') as f:
            json.dump({
                "problem": problem,
                "type": prob_type,
                "solution": solution
            }, f, indent=2)
    
    def copy_solution(self):
        solution = self.solution_text.get("1.0", tk.END).strip()
        if not solution:
            messagebox.showinfo("Info", "No solution to copy")
            return
        
        if copy_to_clipboard(solution):
            messagebox.showinfo("Success", "Solution copied to clipboard")
        else:
            messagebox.showerror("Error", "Failed to copy to clipboard")
    
    def save_secure(self):
        problem_desc = self.problem_text.get("1.0", tk.END).strip()
        problem_type = self.problem_type.get()
        solution = self.solution_text.get("1.0", tk.END).strip()
        
        if not solution:
            messagebox.showinfo("Info", "No solution to save")
            return
        
        file_path = secure_save(solution, problem_desc, problem_type)
        if file_path:
            messagebox.showinfo("Success", f"Solution securely saved")
        else:
            messagebox.showerror("Error", "Failed to save solution")
    
    def clear_all(self):
        self.problem_text.delete("1.0", tk.END)
        self.solution_text.delete("1.0", tk.END)
    
    def show_about(self):
        messagebox.showinfo("About Study Assistant", 
            "Study Assistant v1.0\n\n"
            "A tool to help with algorithm practice and problem solving.\n\n"
            "This application provides solution templates for common algorithm problems.")

def main():
    try:
        root = tk.Tk()
        app = LeetCodeHelper(root)
        root.mainloop()
    except Exception as e:
        print(f"Error running application: {e}")

if __name__ == "__main__":
    main() 