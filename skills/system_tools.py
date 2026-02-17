import platform
import datetime
import os
import subprocess
import difflib
import psutil
import pyperclip
from PIL import ImageGrab
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import ctypes
import math

class SystemTools:
    # Common Windows App Aliases
    APP_ALIASES = {
        "edge": "msedge",
        "chrome": "chrome",
        "firefox": "firefox",
        "notepad": "notepad",
        "calculator": "calc",
        "calc": "calc",
        "cmd": "cmd",
        "terminal": "wt",
        "explorer": "explorer",
        "settings": "start ms-settings:",
        "solitaire": "explorer.exe shell:AppsFolder\\Microsoft.MicrosoftSolitaireCollection_8wekyb3d8bbwe!App",
        "store": "explorer.exe shell:AppsFolder\\Microsoft.WindowsStore_8wekyb3d8bbwe!App",
        "photos": "explorer.exe shell:AppsFolder\\Microsoft.Windows.Photos_8wekyb3d8bbwe!App",
        "spotify": "spotify",
        "code": "code",
        "vscode": "code"
    }

    @staticmethod
    def get_time():
        """Returns the current date and time."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_os_info():
        """Returns operating system information."""
        return f"{platform.system()} {platform.release()} ({platform.version()})"

    @staticmethod
    def open_application(app_name: str):
        """
        Opens an application on Windows. 
        Example: 'notepad', 'calculator', 'edge', 'solitaire' or a full path.
        """
        app_name_lower = app_name.lower().strip()
        
        # Check aliases
        command = SystemTools.APP_ALIASES.get(app_name_lower)
        
        # If not an exact alias match, try to find a close match
        if not command:
            matches = difflib.get_close_matches(app_name_lower, SystemTools.APP_ALIASES.keys(), n=1, cutoff=0.7)
            if matches:
                suggestion = matches[0]
                command = SystemTools.APP_ALIASES[suggestion]
                print(f"Assuming '{app_name}' means '{suggestion}'...")
        
        # If still no command, use the input as is (it might be a path or exact name)
        if not command:
            command = app_name

        try:
            # Handle 'start' commands explicitly for shell integration
            if command.startswith("start "):
                 os.system(command)
            else:
                # os.startfile is Windows-specific
                os.startfile(command)
            return f"Successfully attempted to open '{app_name}' (Command: {command})."
        except Exception as e:
            return f"Failed to open '{app_name}': {str(e)}"

    @staticmethod
    def list_files(directory: str = "."):
        """Lists files and directories in the specified path."""
        try:
            files = os.listdir(directory)
            return f"Files in '{directory}':\n" + "\n".join(files)
        except Exception as e:
            return f"Error listing files in '{directory}': {str(e)}"

    @staticmethod
    def read_file(file_path: str):
        """Reads the content of a file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"Content of '{file_path}':\n{content}"
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"

    @staticmethod
    def write_file(file_path: str, content: str, mode: str = "w"):
        """Writes content to a file. Mode 'w' for overwrite, 'a' for append."""
        try:
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to '{file_path}' (mode: {mode})."
        except Exception as e:
            return f"Error writing to file '{file_path}': {str(e)}"

    @staticmethod
    def get_system_status():
        """Returns CPU, Memory, and Battery status."""
        try:
            cpu = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            battery = psutil.sensors_battery()
            
            status = [
                f"CPU Usage: {cpu}%",
                f"Memory: {memory.percent}% used ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)"
            ]
            
            if battery:
                plugged = "Plugged In" if battery.power_plugged else "Running on Battery"
                status.append(f"Battery: {battery.percent}% ({plugged})")
            else:
                status.append("Battery: Not deteced (Desktop?)")
                
            return "\n".join(status)
        except Exception as e:
            return f"Error getting system status: {str(e)}"

    @staticmethod
    def take_screenshot(filename: str = "screenshot.png"):
        """Takes a screenshot and saves it to the specified filename."""
        try:
            # Ensure screenshots directory exists if path has one
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                
            screenshot = ImageGrab.grab()
            screenshot.save(filename)
            return f"Screenshot saved to '{filename}'."
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"

    @staticmethod
    def get_clipboard_content():
        """Returns the content of the clipboard."""
        try:
            return pyperclip.paste()
        except Exception as e:
            return f"Error reading clipboard: {str(e)}"

    @staticmethod
    def set_clipboard_content(text: str):
        """Sets the content of the clipboard."""
        try:
            pyperclip.copy(text)
            return "Content copied to clipboard."
        except Exception as e:
            return f"Error setting clipboard: {str(e)}"

    @staticmethod
    def _get_volume_interface():
        devices = AudioUtilities.GetSpeakers()
        return devices.EndpointVolume

    @staticmethod
    def set_volume(level: int):
        """Sets the system volume to a specific level (0-100)."""
        try:
            volume = SystemTools._get_volume_interface()
            # Convert 0-100 to scalar (0.0 to 1.0)
            scalar = max(0.0, min(1.0, level / 100.0))
            volume.SetMasterVolumeLevelScalar(scalar, None)
            return f"Volume set to {level}%."
        except Exception as e:
            return f"Error setting volume: {str(e)}"

    @staticmethod
    def mute_volume():
        """Mutes the system volume."""
        try:
            volume = SystemTools._get_volume_interface()
            volume.SetMute(1, None)
            return "Volume muted."
        except Exception as e:
            return f"Error muting volume: {str(e)}"

    @staticmethod
    def unmute_volume():
        """Unmutes the system volume."""
        try:
            volume = SystemTools._get_volume_interface()
            volume.SetMute(0, None)
            return "Volume unmuted."
        except Exception as e:
            return f"Error unmuting volume: {str(e)}"

    @staticmethod
    def media_control(action: str):
        """
        Controls media playback.
        Actions: 'play_pause', 'next', 'prev', 'stop', 'vol_up', 'vol_down', 'mute'
        """
        # Virtual Key Codes
        VK_MEDIA_NEXT_TRACK = 0xB0
        VK_MEDIA_PREV_TRACK = 0xB1
        VK_MEDIA_STOP = 0xB2
        VK_MEDIA_PLAY_PAUSE = 0xB3
        VK_VOLUME_MUTE = 0xAD
        VK_VOLUME_DOWN = 0xAE
        VK_VOLUME_UP = 0xAF

        action_map = {
            "play_pause": VK_MEDIA_PLAY_PAUSE,
            "next": VK_MEDIA_NEXT_TRACK,
            "prev": VK_MEDIA_PREV_TRACK,
            "stop": VK_MEDIA_STOP,
            "vol_up": VK_VOLUME_UP,
            "vol_down": VK_VOLUME_DOWN,
            "mute": VK_VOLUME_MUTE
        }

        vk_code = action_map.get(action.lower())
        if not vk_code:
            return f"Invalid media action: {action}. Valid actions: {list(action_map.keys())}"

        try:
            # keybd_event(bVk, bScan, dwFlags, dwExtraInfo)
            # KEYEVENTF_KEYUP = 0x0002
            ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0) # Press
            ctypes.windll.user32.keybd_event(vk_code, 0, 0x0002, 0) # Release
            return f"Media action successfully sent: {action}"
        except Exception as e:
            return f"Error sending media control: {str(e)}"
