import pyautogui
import pywinauto
from pywinauto import Application, Desktop
from pywinauto.findwindows import ElementNotFoundError
import time
from typing import Optional, List, Dict, Tuple

class DesktopTools:
    """
    Desktop automation tools for Windows using pywinauto and PyAutoGUI.
    Provides window management, mouse/keyboard control, and UI element interaction.
    """
    
    def __init__(self):
        # Set PyAutoGUI safety features
        pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
        pyautogui.PAUSE = 0.5  # Pause between actions
    
    # ===== Window Management =====
    
    def list_windows(self):
        """List all visible windows with their titles."""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            window_list = []
            for win in windows:
                try:
                    title = win.window_text()
                    if title:  # Only include windows with titles
                        window_list.append(title)
                except:
                    continue
            
            if not window_list:
                return "No windows found."
            
            result = "Visible windows:\n"
            for i, title in enumerate(window_list[:20], 1):  # Limit to 20
                result += f"{i}. {title}\n"
            return result
        except Exception as e:
            return f"Error listing windows: {str(e)}"
    
    def focus_window(self, title: str):
        """Bring a window to the foreground by its title (partial match)."""
        try:
            desktop = Desktop(backend="uia")
            # Find window with partial title match
            windows = desktop.windows()
            for win in windows:
                try:
                    win_title = win.window_text()
                    if title.lower() in win_title.lower():
                        win.set_focus()
                        return f"Focused window: {win_title}"
                except:
                    continue
            return f"Window with title containing '{title}' not found."
        except Exception as e:
            return f"Error focusing window: {str(e)}"
    
    def minimize_window(self, title: str):
        """Minimize a window by its title."""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            for win in windows:
                try:
                    win_title = win.window_text()
                    if title.lower() in win_title.lower():
                        win.minimize()
                        return f"Minimized window: {win_title}"
                except:
                    continue
            return f"Window with title containing '{title}' not found."
        except Exception as e:
            return f"Error minimizing window: {str(e)}"
    
    def maximize_window(self, title: str):
        """Maximize a window by its title."""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            for win in windows:
                try:
                    win_title = win.window_text()
                    if title.lower() in win_title.lower():
                        win.maximize()
                        return f"Maximized window: {win_title}"
                except:
                    continue
            return f"Window with title containing '{title}' not found."
        except Exception as e:
            return f"Error maximizing window: {str(e)}"
    
    # ===== Mouse Control =====
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5):
        """Move mouse to specific coordinates."""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return f"Mouse moved to ({x}, {y})"
        except Exception as e:
            return f"Error moving mouse: {str(e)}"
    
    def click_at(self, x: int, y: int, button: str = "left"):
        """Click at specific coordinates."""
        try:
            pyautogui.click(x, y, button=button)
            return f"Clicked {button} button at ({x}, {y})"
        except Exception as e:
            return f"Error clicking: {str(e)}"
    
    def double_click_at(self, x: int, y: int):
        """Double-click at specific coordinates."""
        try:
            pyautogui.doubleClick(x, y)
            return f"Double-clicked at ({x}, {y})"
        except Exception as e:
            return f"Error double-clicking: {str(e)}"
    
    def get_mouse_position(self):
        """Get current mouse position."""
        try:
            x, y = pyautogui.position()
            return f"Mouse position: ({x}, {y})"
        except Exception as e:
            return f"Error getting mouse position: {str(e)}"
    
    # ===== Keyboard Control =====
    
    def press_key(self, key: str):
        """Press a single key."""
        try:
            pyautogui.press(key)
            return f"Pressed key: {key}"
        except Exception as e:
            return f"Error pressing key: {str(e)}"
    
    def hotkey(self, *keys):
        """Press a combination of keys (e.g., 'ctrl', 'c')."""
        try:
            pyautogui.hotkey(*keys)
            keys_str = '+'.join(keys)
            return f"Pressed hotkey: {keys_str}"
        except Exception as e:
            return f"Error pressing hotkey: {str(e)}"
    
    def type_text(self, text: str, interval: float = 0.05):
        """Type text with a delay between keystrokes."""
        try:
            pyautogui.write(text, interval=interval)
            return f"Typed text: {text[:50]}{'...' if len(text) > 50 else ''}"
        except Exception as e:
            return f"Error typing text: {str(e)}"
    
    # ===== Screen Analysis =====
    
    def find_on_screen(self, image_path: str, confidence: float = 0.8):
        """
        Find an image on the screen and return its coordinates.
        Requires opencv-python for image recognition.
        """
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                return f"Image found at: {center} (region: {location})"
            else:
                return f"Image not found on screen: {image_path}"
        except Exception as e:
            return f"Error finding image: {str(e)}"
    
    def get_screen_size(self):
        """Get the screen resolution."""
        try:
            width, height = pyautogui.size()
            return f"Screen size: {width}x{height}"
        except Exception as e:
            return f"Error getting screen size: {str(e)}"
    
    # ===== Advanced Window Interaction =====
    
    def click_button_in_window(self, window_title: str, button_name: str):
        """Click a button in a specific window using pywinauto."""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            
            for win in windows:
                try:
                    win_title = win.window_text()
                    if window_title.lower() in win_title.lower():
                        # Try to find and click the button
                        button = win.child_window(title=button_name, control_type="Button")
                        button.click()
                        return f"Clicked button '{button_name}' in window '{win_title}'"
                except:
                    continue
            
            return f"Could not find button '{button_name}' in window '{window_title}'"
        except Exception as e:
            return f"Error clicking button: {str(e)}"
    
    def type_in_field(self, window_title: str, field_name: str, text: str):
        """Type text into a specific field in a window."""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            
            for win in windows:
                try:
                    win_title = win.window_text()
                    if window_title.lower() in win_title.lower():
                        # Try to find and type in the field
                        field = win.child_window(title=field_name, control_type="Edit")
                        field.set_text(text)
                        return f"Typed text into field '{field_name}' in window '{win_title}'"
                except:
                    continue
            
            return f"Could not find field '{field_name}' in window '{window_title}'"
        except Exception as e:
            return f"Error typing in field: {str(e)}"
    
    def get_window_info(self, title: str):
        """Get detailed information about a window."""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            
            for win in windows:
                try:
                    win_title = win.window_text()
                    if title.lower() in win_title.lower():
                        rect = win.rectangle()
                        info = f"Window: {win_title}\n"
                        info += f"Position: ({rect.left}, {rect.top})\n"
                        info += f"Size: {rect.width()}x{rect.height()}\n"
                        info += f"Visible: {win.is_visible()}\n"
                        info += f"Enabled: {win.is_enabled()}"
                        return info
                except:
                    continue
            
            return f"Window with title containing '{title}' not found."
        except Exception as e:
            return f"Error getting window info: {str(e)}"
