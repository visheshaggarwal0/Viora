from langchain_core.tools import StructuredTool
from skills.web_search import WebSearch
from skills.organizer import Organizer
from skills.system_tools import SystemTools
from skills.web_tools import WebTools
from skills.browser_tools import BrowserTools
from skills.desktop_tools import DesktopTools

def get_viora_tools():
    search = WebSearch()
    org = Organizer()
    sys = SystemTools()
    web = WebTools()
    browser = BrowserTools()
    desktop = DesktopTools()

    return [

        StructuredTool.from_function(
            name="web_search",
            func=search.run,
            description="Search the web for current events or information."
        ),

        StructuredTool.from_function(
            name="add_todo",
            func=org.add_todo,
            description="Add a task to the todo list."
        ),

        StructuredTool.from_function(
            name="list_todos",
            func=org.list_todos,
            description="List all todo tasks."
        ),

        StructuredTool.from_function(
            name="get_time",
            func=sys.get_time,
            description="Get current date and time."
        ),

        StructuredTool.from_function(
            name="get_os_info",
            func=sys.get_os_info,
            description="Get operating system information."
        ),

        StructuredTool.from_function(
            name="open_app",
            func=sys.open_application,
            description="Open an application on Windows. Supports aliases like 'edge', 'chrome', 'notepad', 'calc', 'solitaire', 'settings', etc."
        ),

        StructuredTool.from_function(
            name="list_files",
            func=sys.list_files,
            description="List files and directories in a given path (default is current directory)."
        ),

        StructuredTool.from_function(
            name="read_file",
            func=sys.read_file,
            description="Read the content of a text file."
        ),

        StructuredTool.from_function(
            name="write_file",
            func=sys.write_file,
            description="Write content to a file. Defaults to overwrite ('w'), use mode='a' to append."
        ),

        StructuredTool.from_function(
            name="get_system_status",
            func=sys.get_system_status,
            description="Get current system status (CPU, RAM, Battery)."
        ),

        StructuredTool.from_function(
            name="take_screenshot",
            func=sys.take_screenshot,
            description="Take a screenshot and save it to a file. Default is 'screenshot.png'."
        ),

        StructuredTool.from_function(
            name="get_clipboard",
            func=sys.get_clipboard_content,
            description="Get text content from the clipboard."
        ),

        StructuredTool.from_function(
            name="set_clipboard",
            func=sys.set_clipboard_content,
            description="Set text content to the clipboard."
        ),

        StructuredTool.from_function(
            name="set_volume",
            func=sys.set_volume,
            description="Set system volume to a specific percentage (0-100)."
        ),

        StructuredTool.from_function(
            name="mute_volume",
            func=sys.mute_volume,
            description="Mute system volume."
        ),

        StructuredTool.from_function(
            name="unmute_volume",
            func=sys.unmute_volume,
            description="Unmute system volume."
        ),

        StructuredTool.from_function(
            name="media_control",
            func=sys.media_control,
            description="Control media playback. Actions: 'play_pause', 'next', 'prev', 'stop', 'vol_up', 'vol_down', 'mute'."
        ),

        StructuredTool.from_function(
            name="read_web_page",
            func=web.read_url,
            description="Read and summarize the text content of a web page URL."
        ),

        # Browser Automation Tools
        StructuredTool.from_function(
            name="browser_navigate",
            func=browser.navigate_to,
            description="Navigate to a URL in the browser. Opens a visible browser window if not already open."
        ),

        StructuredTool.from_function(
            name="browser_click",
            func=browser.click_element,
            description="Click an element on the current web page using a CSS selector (e.g., '#submit-button', '.login-link')."
        ),

        StructuredTool.from_function(
            name="browser_type",
            func=browser.type_text,
            description="Type text into an input field using a CSS selector (e.g., '#email', 'input[name=\"password\"]')."
        ),

        StructuredTool.from_function(
            name="browser_get_text",
            func=browser.get_text,
            description="Get text content from an element using a CSS selector."
        ),

        StructuredTool.from_function(
            name="browser_screenshot",
            func=browser.take_screenshot,
            description="Take a full-page screenshot of the current browser page. Saves to screenshots/ folder."
        ),

        StructuredTool.from_function(
            name="browser_extract_links",
            func=browser.extract_links,
            description="Extract all links (text and URLs) from the current page."
        ),

        StructuredTool.from_function(
            name="browser_get_url",
            func=browser.get_current_url,
            description="Get the current URL of the browser page."
        ),

        StructuredTool.from_function(
            name="browser_go_back",
            func=browser.go_back,
            description="Navigate back in browser history."
        ),

        StructuredTool.from_function(
            name="browser_reload",
            func=browser.reload_page,
            description="Reload the current browser page."
        ),

        StructuredTool.from_function(
            name="browser_close",
            func=browser.close_browser,
            description="Close the browser and cleanup resources. Use this when done with browser automation."
        ),

        # Desktop Automation Tools
        StructuredTool.from_function(
            name="desktop_list_windows",
            func=desktop.list_windows,
            description="List all visible windows with their titles."
        ),

        StructuredTool.from_function(
            name="desktop_focus_window",
            func=desktop.focus_window,
            description="Bring a window to the foreground by its title (partial match works)."
        ),

        StructuredTool.from_function(
            name="desktop_minimize_window",
            func=desktop.minimize_window,
            description="Minimize a window by its title."
        ),

        StructuredTool.from_function(
            name="desktop_maximize_window",
            func=desktop.maximize_window,
            description="Maximize a window by its title."
        ),

        StructuredTool.from_function(
            name="desktop_move_mouse",
            func=desktop.move_mouse,
            description="Move mouse to specific screen coordinates (x, y)."
        ),

        StructuredTool.from_function(
            name="desktop_click_at",
            func=desktop.click_at,
            description="Click at specific screen coordinates. Specify button: 'left', 'right', or 'middle'."
        ),

        StructuredTool.from_function(
            name="desktop_get_mouse_pos",
            func=desktop.get_mouse_position,
            description="Get the current mouse position coordinates."
        ),

        StructuredTool.from_function(
            name="desktop_press_key",
            func=desktop.press_key,
            description="Press a single key (e.g., 'enter', 'esc', 'tab', 'space', 'a', 'b', etc.)."
        ),

        StructuredTool.from_function(
            name="desktop_hotkey",
            func=desktop.hotkey,
            description="Press a combination of keys. Pass keys as separate arguments (e.g., 'ctrl', 'c' for copy)."
        ),

        StructuredTool.from_function(
            name="desktop_type_text",
            func=desktop.type_text,
            description="Type text using the keyboard with a delay between keystrokes."
        ),

        StructuredTool.from_function(
            name="desktop_get_screen_size",
            func=desktop.get_screen_size,
            description="Get the screen resolution (width x height)."
        ),

        StructuredTool.from_function(
            name="desktop_get_window_info",
            func=desktop.get_window_info,
            description="Get detailed information about a window (position, size, visibility)."
        ),

        # Browser Enhancements
        StructuredTool.from_function(
            name="browser_submit_form",
            func=browser.submit_form,
            description="Submit a form by its CSS selector."
        ),

        StructuredTool.from_function(
            name="browser_select_dropdown",
            func=browser.select_dropdown,
            description="Select an option from a dropdown menu by value or text."
        ),

        StructuredTool.from_function(
            name="browser_check_checkbox",
            func=browser.check_checkbox,
            description="Check or uncheck a checkbox. Pass checked=True to check, checked=False to uncheck."
        ),

        StructuredTool.from_function(
            name="browser_upload_file",
            func=browser.upload_file,
            description="Upload a file to a file input element. Provide selector and absolute file path."
        ),

        StructuredTool.from_function(
            name="browser_scroll_to",
            func=browser.scroll_to,
            description="Scroll to specific coordinates (x, y) on the page."
        ),

        StructuredTool.from_function(
            name="browser_scroll_to_element",
            func=browser.scroll_to_element,
            description="Scroll an element into view using its CSS selector."
        ),

        StructuredTool.from_function(
            name="browser_hover",
            func=browser.hover_element,
            description="Hover over an element using its CSS selector."
        ),

        StructuredTool.from_function(
            name="browser_right_click",
            func=browser.right_click,
            description="Right-click on an element using its CSS selector."
        ),

        StructuredTool.from_function(
            name="browser_new_tab",
            func=browser.new_tab,
            description="Open a new browser tab, optionally navigate to a URL."
        ),

        StructuredTool.from_function(
            name="browser_switch_tab",
            func=browser.switch_tab,
            description="Switch to a tab by index (0-based)."
        ),

        StructuredTool.from_function(
            name="browser_close_tab",
            func=browser.close_tab,
            description="Close the current tab and switch to the first tab."
        ),

        StructuredTool.from_function(
            name="browser_list_tabs",
            func=browser.list_tabs,
            description="List all open tabs with their URLs."
        ),

        StructuredTool.from_function(
            name="browser_extract_table",
            func=browser.extract_table,
            description="Extract table data from a table element using CSS selector."
        ),

        StructuredTool.from_function(
            name="browser_get_all_text",
            func=browser.get_all_text,
            description="Get all visible text content from the current page."
        ),

        StructuredTool.from_function(
            name="browser_count_elements",
            func=browser.count_elements,
            description="Count the number of elements matching a CSS selector."
        ),

        # Desktop Enhancements
        StructuredTool.from_function(
            name="desktop_drag_drop",
            func=desktop.drag_and_drop,
            description="Drag from coordinates (x1, y1) to (x2, y2)."
        ),

        StructuredTool.from_function(
            name="desktop_scroll",
            func=desktop.scroll_mouse,
            description="Scroll with mouse wheel. Positive clicks = up, negative = down."
        ),

        StructuredTool.from_function(
            name="desktop_right_click",
            func=desktop.right_click_at,
            description="Right-click at specific screen coordinates."
        ),

        StructuredTool.from_function(
            name="desktop_close_window",
            func=desktop.close_window,
            description="Close a window by its title (partial match works)."
        ),

        StructuredTool.from_function(
            name="desktop_resize_window",
            func=desktop.resize_window,
            description="Resize a window to specific width and height."
        ),

        StructuredTool.from_function(
            name="desktop_move_window",
            func=desktop.move_window_to,
            description="Move a window to specific screen coordinates (x, y)."
        ),

        StructuredTool.from_function(
            name="desktop_restore_window",
            func=desktop.restore_window,
            description="Restore a minimized window by its title."
        ),

        StructuredTool.from_function(
            name="desktop_capture_region",
            func=desktop.capture_region,
            description="Capture a screenshot of a specific screen region (x, y, width, height)."
        ),

        StructuredTool.from_function(
            name="desktop_get_pixel_color",
            func=desktop.get_pixel_color,
            description="Get the RGB color value of a pixel at specific coordinates."
        )

    ]
