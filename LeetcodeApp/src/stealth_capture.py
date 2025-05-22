import os
import time
import json
import base64
import threading
import subprocess
import tempfile
import random
import sys
import requests
from datetime import datetime
from PIL import ImageGrab, Image
import pytesseract
import keyboard
import numpy as np
import cv2

# Anthropic Claude API key (replace with actual key when in use)
CLAUDE_API_KEY = "YOUR_CLAUDE_API_KEY"

# Configure paths
USER_HOME = os.path.expanduser("~")
APP_DIR = os.path.join(USER_HOME, "Documents", ".temp_study_data")
LOG_FILE = os.path.join(APP_DIR, "system.log")
TEMP_DIR = os.path.join(APP_DIR, "temp")
PYTESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update as needed

# Ensure directories exist
os.makedirs(APP_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Configure pytesseract
if os.path.exists(PYTESSERACT_PATH):
    pytesseract.pytesseract.tesseract_cmd = PYTESSERACT_PATH

# ===================== STEALTH FUNCTIONS =====================

def stealth_log(message):
    """Log message in an encrypted format to avoid detection"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        encoded_msg = base64.b64encode(f"{timestamp}: {message}".encode()).decode()
        
        with open(LOG_FILE, "a") as f:
            f.write(f"{encoded_msg}\n")
    except Exception:
        pass  # Silent failure

def hide_window():
    """Hide console window using Windows API"""
    try:
        import ctypes
        user32 = ctypes.WinDLL('user32')
        hwnd = user32.GetForegroundWindow()
        user32.ShowWindow(hwnd, 0)  # SW_HIDE = 0
    except Exception:
        pass

def disguise_process_name():
    """Attempt to disguise the process name in task manager"""
    try:
        import ctypes
        if hasattr(ctypes, 'windll'):
            ctypes.windll.kernel32.SetConsoleTitleW("Windows Security Monitor")
    except Exception:
        pass

def clean_temp_files(max_age_minutes=30):
    """Clean temporary files older than specified minutes"""
    try:
        now = time.time()
        for filename in os.listdir(TEMP_DIR):
            file_path = os.path.join(TEMP_DIR, filename)
            if os.path.isfile(file_path):
                # If file is older than max_age_minutes, delete it
                if now - os.path.getmtime(file_path) > max_age_minutes * 60:
                    os.remove(file_path)
    except Exception:
        pass

# ===================== SCREEN CAPTURE FUNCTIONS =====================

def capture_screen():
    """Capture full screen and return PIL Image"""
    return ImageGrab.grab()

def save_temp_image(image):
    """Save image to temporary location with random name"""
    random_name = f"img_{random.randint(1000, 9999)}_{int(time.time())}.png"
    file_path = os.path.join(TEMP_DIR, random_name)
    image.save(file_path)
    return file_path

def extract_text_from_image(image_path):
    """Extract text from image using OCR"""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        stealth_log(f"OCR error: {str(e)}")
        return ""

def detect_leetcode_problem(text):
    """Detect if text contains a LeetCode problem based on patterns"""
    leetcode_markers = [
        "LeetCode", "leetcode", "Leetcode",
        "Example 1:", "Input:", "Output:", 
        "class Solution:", "def ", 
        "Constraints:", "Follow-up:", "Return",
        "Example 2:"
    ]
    
    score = 0
    for marker in leetcode_markers:
        if marker in text:
            score += 1
    
    return score >= 3, text if score >= 3 else ""

# ===================== AI INTEGRATION FUNCTIONS =====================

def query_claude_api(problem_text):
    """Send problem to Claude API and get solution"""
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "Content-Type": "application/json"
    }
    
    prompt = f"""
You are a coding expert specializing in solving LeetCode problems. I'll provide you with a problem description, and you should return the most efficient solution with clear explanations. 

Here's the problem:

{problem_text}

Please provide:
1. Your analysis of the problem
2. The time and space complexity of your solution
3. The full working solution code in Python
4. Any edge cases or optimizations to consider
"""
    
    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers=headers,
            json={
                "model": "claude-3-opus-20240229",
                "max_tokens": 4000,
                "temperature": 0,
                "system": "You are a coding expert who specializes in solving algorithm problems efficiently and explaining them clearly.",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        
        response_data = response.json()
        return response_data['content'][0]['text']
    except Exception as e:
        stealth_log(f"Claude API error: {str(e)}")
        return f"Error: {str(e)}"

def format_solution(claude_response):
    """Extract and format the solution from Claude's response"""
    # Just return the full response for now
    return claude_response

# ===================== CLIPBOARD AND INTERACTION FUNCTIONS =====================

def copy_to_clipboard(text):
    """Copy text to clipboard silently"""
    try:
        import pyperclip
        pyperclip.copy(text)
    except Exception as e:
        stealth_log(f"Clipboard error: {str(e)}")

def background_monitor():
    """Background thread to monitor screen and detect problems"""
    last_capture_time = 0
    capture_interval = 5  # Seconds between captures
    
    while True:
        try:
            current_time = time.time()
            
            # Only capture every capture_interval seconds
            if current_time - last_capture_time < capture_interval:
                time.sleep(0.5)
                continue
                
            last_capture_time = current_time
            
            # Check if hotkey is pressed
            if not is_hotkey_active():
                time.sleep(0.5)
                continue
                
            # Capture screen
            screen = capture_screen()
            img_path = save_temp_image(screen)
            
            # Extract text from image
            text = extract_text_from_image(img_path)
            
            # Detect if text contains a LeetCode problem
            is_problem, problem_text = detect_leetcode_problem(text)
            
            if is_problem:
                stealth_log("LeetCode problem detected")
                
                # Get solution from Claude
                solution = query_claude_api(problem_text)
                
                # Format solution and store it for hotkey-based paste
                formatted_solution = format_solution(solution)
                store_solution(formatted_solution)
                
                # Send notification (very subtle, only visible to user)
                notify_user()
            
            # Clean up
            clean_temp_files()
            
        except Exception as e:
            stealth_log(f"Monitor error: {str(e)}")
            time.sleep(5)  # Wait before retrying

def is_hotkey_active():
    """Check if the activation hotkey is pressed"""
    # Ctrl+Alt+L is the activation hotkey
    return keyboard.is_pressed('ctrl+alt+l')

def store_solution(solution):
    """Store solution for later pasting"""
    solution_file = os.path.join(APP_DIR, "last_solution.dat")
    
    # Encode and store
    encoded = base64.b64encode(solution.encode()).decode()
    with open(solution_file, 'w') as f:
        f.write(encoded)

def get_stored_solution():
    """Get the stored solution"""
    solution_file = os.path.join(APP_DIR, "last_solution.dat")
    
    if os.path.exists(solution_file):
        try:
            with open(solution_file, 'r') as f:
                encoded = f.read()
            decoded = base64.b64decode(encoded.encode()).decode()
            return decoded
        except:
            return None
    return None

def notify_user():
    """Send a very subtle notification to user"""
    try:
        # Flash the title bar briefly
        import ctypes
        user32 = ctypes.WinDLL('user32')
        hwnd = user32.GetForegroundWindow()
        user32.FlashWindow(hwnd, 1)
    except:
        pass

def paste_solution_hotkey():
    """Monitor for the paste solution hotkey"""
    while True:
        try:
            # Ctrl+Alt+P is the paste solution hotkey
            if keyboard.is_pressed('ctrl+alt+p'):
                solution = get_stored_solution()
                if solution:
                    copy_to_clipboard(solution)
                    # Wait to prevent multiple pastes
                    time.sleep(0.5)
                    # Simulate Ctrl+V to paste
                    keyboard.press_and_release('ctrl+v')
                
                # Wait before checking again to prevent multiple triggers
                time.sleep(0.5)
            
            time.sleep(0.1)  # Reduce CPU usage
        except Exception as e:
            stealth_log(f"Paste hotkey error: {str(e)}")
            time.sleep(1)

# ===================== MAIN FUNCTION =====================

def run_stealth_capture():
    """Main function to run the stealth capture system"""
    try:
        # Apply stealth measures
        disguise_process_name()
        hide_window()
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=background_monitor, daemon=True)
        monitor_thread.start()
        
        # Start paste hotkey monitoring
        paste_thread = threading.Thread(target=paste_solution_hotkey, daemon=True)
        paste_thread.start()
        
        # Log startup
        stealth_log("Stealth capture system started")
        
        # Keep alive
        while True:
            time.sleep(60)
            clean_temp_files()
    
    except Exception as e:
        stealth_log(f"Fatal error: {str(e)}")

if __name__ == "__main__":
    run_stealth_capture() 