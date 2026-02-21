from langchain_core.tools import StructuredTool
from skills.web_search import WebSearch
from skills.organizer import Organizer
from skills.system_tools import SystemTools
from skills.web_tools import WebTools
from skills.browser_tools import BrowserTools
from skills.desktop_tools import DesktopTools

def get_viora_tools(category: str = "ALL"):
    search = WebSearch()
    org = Organizer()
    sys = SystemTools()
    web = WebTools()
    browser = BrowserTools()
    desktop = DesktopTools()

    # Define tool groups
    search_tools = [
        StructuredTool.from_function(name="web_search", func=search.run, description="Search the web.")
    ]

    todo_tools = [
        StructuredTool.from_function(name="add_todo", func=org.add_todo, description="Add a todo task."),
        StructuredTool.from_function(name="list_todos", func=org.list_todos, description="List all todos.")
    ]

    system_tools = [
        StructuredTool.from_function(name="get_time", func=sys.get_time, description="Get current date/time."),
        StructuredTool.from_function(name="get_os_info", func=sys.get_os_info, description="Get OS details."),
        StructuredTool.from_function(name="open_app", func=sys.open_application, description="Open a Windows app (edge, chrome, notepad, calc, etc)."),
        StructuredTool.from_function(name="list_files", func=sys.list_files, description="List files in a directory."),
        StructuredTool.from_function(name="read_file", func=sys.read_file, description="Read a text file."),
        StructuredTool.from_function(name="write_file", func=sys.write_file, description="Write text to a file (mode='w' or 'a')."),
        StructuredTool.from_function(name="get_system_status", func=sys.get_system_status, description="Get CPU, RAM, and Battery status."),
        StructuredTool.from_function(name="take_screenshot", func=sys.take_screenshot, description="Take and save a screenshot."),
        StructuredTool.from_function(name="get_clipboard", func=sys.get_clipboard_content, description="Get clipboard text."),
        StructuredTool.from_function(name="set_clipboard", func=sys.set_clipboard_content, description="Set clipboard text."),
        StructuredTool.from_function(name="set_volume", func=sys.set_volume, description="Set volume (0-100)."),
        StructuredTool.from_function(name="mute_volume", func=sys.mute_volume, description="Mute volume."),
        StructuredTool.from_function(name="unmute_volume", func=sys.unmute_volume, description="Unmute volume."),
        StructuredTool.from_function(name="media_control", func=sys.media_control, description="Media: play_pause, next, prev, stop, vol_up, vol_down, mute.")
    ]

    browser_tools = [
        StructuredTool.from_function(name="read_web_page", func=web.read_url, description="Fetch/read web page text."),
        StructuredTool.from_function(name="browser_navigate", func=browser.navigate_to, description="Navigate to a URL."),
        StructuredTool.from_function(name="browser_click", func=browser.click_element, description="Click an element (CSS selector)."),
        StructuredTool.from_function(name="browser_type", func=browser.type_text, description="Type text into an element (CSS selector)."),
        StructuredTool.from_function(name="browser_get_text", func=browser.get_text, description="Get element text (CSS selector)."),
        StructuredTool.from_function(name="browser_screenshot", func=browser.take_screenshot, description="Take browser screenshot."),
        StructuredTool.from_function(name="browser_extract_links", func=browser.extract_links, description="Extract all links from page."),
        StructuredTool.from_function(name="browser_get_url", func=browser.get_current_url, description="Get current URL."),
        StructuredTool.from_function(name="browser_go_back", func=browser.go_back, description="Navigate back."),
        StructuredTool.from_function(name="browser_reload", func=browser.reload_page, description="Reload current page."),
        StructuredTool.from_function(name="browser_close", func=browser.close_browser, description="Close browser."),
        StructuredTool.from_function(name="browser_submit_form", func=browser.submit_form, description="Submit form (selector)."),
        StructuredTool.from_function(name="browser_select_dropdown", func=browser.select_dropdown, description="Select dropdown option."),
        StructuredTool.from_function(name="browser_check_checkbox", func=browser.check_checkbox, description="Check/uncheck checkbox."),
        StructuredTool.from_function(name="browser_upload_file", func=browser.upload_file, description="Upload file (selector, path)."),
        StructuredTool.from_function(name="browser_scroll_to", func=browser.scroll_to, description="Scroll to (x, y)."),
        StructuredTool.from_function(name="browser_scroll_to_element", func=browser.scroll_to_element, description="Scroll element into view."),
        StructuredTool.from_function(name="browser_hover", func=browser.hover_element, description="Hover over element."),
        StructuredTool.from_function(name="browser_right_click", func=browser.right_click, description="Right-click on element."),
        StructuredTool.from_function(name="browser_new_tab", func=browser.new_tab, description="Open new tab."),
        StructuredTool.from_function(name="browser_switch_tab", func=browser.switch_tab, description="Switch tab by index."),
        StructuredTool.from_function(name="browser_close_tab", func=browser.close_tab, description="Close current tab."),
        StructuredTool.from_function(name="browser_list_tabs", func=browser.list_tabs, description="List all tabs."),
        StructuredTool.from_function(name="browser_extract_table", func=browser.extract_table, description="Extract table data."),
        StructuredTool.from_function(name="browser_get_all_text", func=browser.get_all_text, description="Get all page text."),
        StructuredTool.from_function(name="browser_count_elements", func=browser.count_elements, description="Count matching elements.")
    ]

    desktop_tools = [
        StructuredTool.from_function(name="desktop_list_windows", func=desktop.list_windows, description="List visible windows."),
        StructuredTool.from_function(name="desktop_focus_window", func=desktop.focus_window, description="Focus window by title."),
        StructuredTool.from_function(name="desktop_minimize_window", func=desktop.minimize_window, description="Minimize window."),
        StructuredTool.from_function(name="desktop_maximize_window", func=desktop.maximize_window, description="Maximize window."),
        StructuredTool.from_function(name="desktop_move_mouse", func=desktop.move_mouse, description="Move mouse to (x, y)."),
        StructuredTool.from_function(name="desktop_click_at", func=desktop.click_at, description="Click at (x, y). button: 'left', 'right', 'middle'."),
        StructuredTool.from_function(name="desktop_get_mouse_pos", func=desktop.get_mouse_position, description="Get mouse (x, y)."),
        StructuredTool.from_function(name="desktop_press_key", func=desktop.press_key, description="Press a key (enter, esc, a, b, etc)."),
        StructuredTool.from_function(name="desktop_hotkey", func=desktop.hotkey, description="Press key combo (e.g. 'ctrl', 'c')."),
        StructuredTool.from_function(name="desktop_type_text", func=desktop.type_text, description="Type text via keyboard."),
        StructuredTool.from_function(name="desktop_get_screen_size", func=desktop.get_screen_size, description="Get screen resolution."),
        StructuredTool.from_function(name="desktop_get_window_info", func=desktop.get_window_info, description="Get window details (pos, size)."),
        StructuredTool.from_function(name="desktop_drag_drop", func=desktop.drag_and_drop, description="Drag from (x1, y1) to (x2, y2)."),
        StructuredTool.from_function(name="desktop_scroll", func=desktop.scroll_mouse, description="Scroll mouse wheel (+up, -down)."),
        StructuredTool.from_function(name="desktop_right_click", func=desktop.right_click_at, description="Right-click at (x, y)."),
        StructuredTool.from_function(name="desktop_close_window", func=desktop.close_window, description="Close window by title."),
        StructuredTool.from_function(name="desktop_resize_window", func=desktop.resize_window, description="Resize window (w, h)."),
        StructuredTool.from_function(name="desktop_move_window", func=desktop.move_window_to, description="Move window to (x, y)."),
        StructuredTool.from_function(name="desktop_restore_window", func=desktop.restore_window, description="Restore minimized window."),
        StructuredTool.from_function(name="desktop_capture_region", func=desktop.capture_region, description="Capture screen region."),
        StructuredTool.from_function(name="desktop_get_pixel_color", func=desktop.get_pixel_color, description="Get pixel RGB at (x, y).")
    ]

    # Map categories to tool groups
    mapping = {
        "GREETING": [],
        "TODO": todo_tools,
        "SYSTEM": system_tools,
        "BROWSER": browser_tools,
        "DESKTOP": desktop_tools,
        "WEB_SEARCH": search_tools,
        "ALL": search_tools + todo_tools + system_tools + browser_tools + desktop_tools
    }

    return mapping.get(category, mapping["ALL"])
