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
    
    # ===== Advanced Mouse Enhancements =====
    
    def drag_and_drop(self, x1: int, y1: int, x2: int, y2: int, duration: float = 1.0):
        """Drag from (x1, y1) to (x2, y2)."""
        try:
            pyautogui.moveTo(x1, y1, duration=duration/2)
            pyautogui.dragTo(x2, y2, duration=duration/2, button='left')
            return f"Dragged from ({x1}, {y1}) to ({x2}, {y2})"
        except Exception as e:
            return f"Error dragging: {str(e)}"
    
    def scroll_mouse(self, clicks: int):
        """Scroll with mouse wheel. Positive = up, negative = down."""
        try:
            pyautogui.scroll(clicks)
            direction = "up" if clicks > 0 else "down"
            return f"Scrolled {abs(clicks)} clicks {direction}"
        except Exception as e:
            return f"Error scrolling: {str(e)}"
    
    def right_click_at(self, x: int, y: int):
        """Right-click at specific coordinates."""
        try:
            pyautogui.rightClick(x, y)
            return f"Right-clicked at ({x}, {y})"
        except Exception as e:
            return f"Error right-clicking: {str(e)}"
    
    # ===== Window Control Enhancements =====
    
    def close_window(self, title: str):
        """Close a window by its title."""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            for win in windows:
                try:
                    win_title = win.window_text()
                    if title.lower() in win_title.lower():
                        win.close()
                        return f"Closed window: {win_title}"
                except:
                    continue
            return f"Window with title containing '{title}' not found."
        except Exception as e:
            return f"Error closing window: {str(e)}"
    
    def resize_window(self, title: str, width: int, height: int):
        """Resize a window to specific dimensions."""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            for win in windows:
                try:
                    win_title = win.window_text()
                    if title.lower() in win_title.lower():
                        rect = win.rectangle()
                        win.move_window(rect.left, rect.top, width, height)
                        return f"Resized window '{win_title}' to {width}x{height}"
                except:
                    continue
            return f"Window with title containing '{title}' not found."
        except Exception as e:
            return f"Error resizing window: {str(e)}"
    
    def move_window_to(self, title: str, x: int, y: int):
        """Move a window to specific coordinates."""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            for win in windows:
                try:
                    win_title = win.window_text()
                    if title.lower() in win_title.lower():
                        rect = win.rectangle()
                        win.move_window(x, y, rect.width(), rect.height())
                        return f"Moved window '{win_title}' to ({x}, {y})"
                except:
                    continue
            return f"Window with title containing '{title}' not found."
        except Exception as e:
            return f"Error moving window: {str(e)}"
    
    def restore_window(self, title: str):
        """Restore a minimized window."""
        try:
            desktop = Desktop(backend="uia")
            windows = desktop.windows()
            for win in windows:
                try:
                    win_title = win.window_text()
                    if title.lower() in win_title.lower():
                        win.restore()
                        return f"Restored window: {win_title}"
                except:
                    continue
            return f"Window with title containing '{title}' not found."
        except Exception as e:
            return f"Error restoring window: {str(e)}"
    
    # ===== Screen Capture Enhancements =====
    
    def capture_region(self, x: int, y: int, width: int, height: int, filename: str = "region.png"):
        """Capture a specific region of the screen."""
        try:
            import os
            os.makedirs("screenshots", exist_ok=True)
            filepath = os.path.join("screenshots", filename)
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            screenshot.save(filepath)
            return f"Region screenshot saved to {filepath}"
        except Exception as e:
            return f"Error capturing region: {str(e)}"
    
    def get_pixel_color(self, x: int, y: int):
        """Get the RGB color of a pixel at specific coordinates."""
        try:
            pixel = pyautogui.pixel(x, y)
            return f"Pixel color at ({x}, {y}): RGB{pixel}"
        except Exception as e:
            return f"Error getting pixel color: {str(e)}"
