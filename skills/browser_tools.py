from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import os
from typing import Optional, Dict, List, Any

class BrowserTools:
    """
    Browser automation tools using Playwright.
    Provides web navigation, interaction, and data extraction capabilities.
    """
    
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self._is_initialized = False
    
    def _ensure_browser(self):
        """Ensures browser is initialized and ready."""
        if not self._is_initialized:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=False)  # Visible by default
            self.context = self.browser.new_context(
                viewport={'width': 1280, 'height': 720},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            self.page = self.context.new_page()
            self._is_initialized = True
    
    def navigate_to(self, url: str):
        """Navigate to a URL."""
        try:
            self._ensure_browser()
            self.page.goto(url, wait_until='domcontentloaded', timeout=30000)
            return f"Successfully navigated to {url}"
        except Exception as e:
            return f"Error navigating to {url}: {str(e)}"
    
    def click_element(self, selector: str):
        """Click an element by CSS selector."""
        try:
            self._ensure_browser()
            self.page.click(selector, timeout=10000)
            return f"Successfully clicked element: {selector}"
        except Exception as e:
            return f"Error clicking element {selector}: {str(e)}"
    
    def type_text(self, selector: str, text: str):
        """Type text into an input field."""
        try:
            self._ensure_browser()
            self.page.fill(selector, text, timeout=10000)
            return f"Successfully typed text into {selector}"
        except Exception as e:
            return f"Error typing into {selector}: {str(e)}"
    
    def get_text(self, selector: str):
        """Get text content from an element."""
        try:
            self._ensure_browser()
            text = self.page.text_content(selector, timeout=10000)
            return f"Text from {selector}: {text}"
        except Exception as e:
            return f"Error getting text from {selector}: {str(e)}"
    
    def get_attribute(self, selector: str, attribute: str):
        """Get an attribute value from an element."""
        try:
            self._ensure_browser()
            value = self.page.get_attribute(selector, attribute, timeout=10000)
            return f"{attribute} of {selector}: {value}"
        except Exception as e:
            return f"Error getting attribute {attribute} from {selector}: {str(e)}"
    
    def take_screenshot(self, filename: str = "screenshot.png"):
        """Take a screenshot of the current page."""
        try:
            self._ensure_browser()
            # Ensure screenshots directory exists
            os.makedirs("screenshots", exist_ok=True)
            filepath = os.path.join("screenshots", filename)
            self.page.screenshot(path=filepath, full_page=True)
            return f"Screenshot saved to {filepath}"
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"
    
    def wait_for_element(self, selector: str, timeout: int = 10000):
        """Wait for an element to appear."""
        try:
            self._ensure_browser()
            self.page.wait_for_selector(selector, timeout=timeout)
            return f"Element {selector} is now visible"
        except Exception as e:
            return f"Error waiting for {selector}: {str(e)}"
    
    def execute_script(self, js_code: str):
        """Execute JavaScript code on the page."""
        try:
            self._ensure_browser()
            result = self.page.evaluate(js_code)
            return f"Script executed. Result: {result}"
        except Exception as e:
            return f"Error executing script: {str(e)}"
    
    def get_page_content(self):
        """Get the full HTML content of the current page."""
        try:
            self._ensure_browser()
            content = self.page.content()
            # Truncate if too long
            if len(content) > 5000:
                content = content[:5000] + "\n...[Content Truncated]..."
            return f"Page content:\n{content}"
        except Exception as e:
            return f"Error getting page content: {str(e)}"
    
    def extract_links(self):
        """Extract all links from the current page."""
        try:
            self._ensure_browser()
            links = self.page.evaluate("""
                () => {
                    const anchors = Array.from(document.querySelectorAll('a'));
                    return anchors.map(a => ({
                        text: a.textContent.trim(),
                        href: a.href
                    })).filter(link => link.href && link.text);
                }
            """)
            # Limit to first 20 links
            links = links[:20]
            result = "Links found:\n"
            for link in links:
                result += f"- {link['text']}: {link['href']}\n"
            return result
        except Exception as e:
            return f"Error extracting links: {str(e)}"
    
    def fill_form(self, form_data: Dict[str, str]):
        """
        Fill a form with multiple fields.
        form_data should be a dict like: {'#email': 'user@example.com', '#password': 'pass123'}
        """
        try:
            self._ensure_browser()
            for selector, value in form_data.items():
                self.page.fill(selector, value, timeout=10000)
            return f"Successfully filled {len(form_data)} form fields"
        except Exception as e:
            return f"Error filling form: {str(e)}"
    
    def go_back(self):
        """Navigate back in browser history."""
        try:
            self._ensure_browser()
            self.page.go_back(wait_until='domcontentloaded')
            return "Navigated back"
        except Exception as e:
            return f"Error going back: {str(e)}"
    
    def go_forward(self):
        """Navigate forward in browser history."""
        try:
            self._ensure_browser()
            self.page.go_forward(wait_until='domcontentloaded')
            return "Navigated forward"
        except Exception as e:
            return f"Error going forward: {str(e)}"
    
    def reload_page(self):
        """Reload the current page."""
        try:
            self._ensure_browser()
            self.page.reload(wait_until='domcontentloaded')
            return "Page reloaded"
        except Exception as e:
            return f"Error reloading page: {str(e)}"
    
    def get_current_url(self):
        """Get the current page URL."""
        try:
            self._ensure_browser()
            return f"Current URL: {self.page.url}"
        except Exception as e:
            return f"Error getting URL: {str(e)}"
    
    def close_browser(self):
        """Close the browser and cleanup resources."""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            self._is_initialized = False
            return "Browser closed successfully"
        except Exception as e:
            return f"Error closing browser: {str(e)}"
    
    # ===== Form Handling Enhancements =====
    
    def submit_form(self, selector: str):
        """Submit a form by its selector."""
        try:
            self._ensure_browser()
            self.page.evaluate(f"document.querySelector('{selector}').submit()")
            return f"Form {selector} submitted successfully"
        except Exception as e:
            return f"Error submitting form {selector}: {str(e)}"
    
    def select_dropdown(self, selector: str, value: str):
        """Select an option from a dropdown by value or text."""
        try:
            self._ensure_browser()
            self.page.select_option(selector, value, timeout=10000)
            return f"Selected '{value}' in dropdown {selector}"
        except Exception as e:
            return f"Error selecting dropdown option: {str(e)}"
    
    def check_checkbox(self, selector: str, checked: bool = True):
        """Check or uncheck a checkbox."""
        try:
            self._ensure_browser()
            if checked:
                self.page.check(selector, timeout=10000)
                return f"Checked checkbox {selector}"
            else:
                self.page.uncheck(selector, timeout=10000)
                return f"Unchecked checkbox {selector}"
        except Exception as e:
            return f"Error toggling checkbox: {str(e)}"
    
    def upload_file(self, selector: str, filepath: str):
        """Upload a file to a file input element."""
        try:
            self._ensure_browser()
            self.page.set_input_files(selector, filepath, timeout=10000)
            return f"Uploaded file {filepath} to {selector}"
        except Exception as e:
            return f"Error uploading file: {str(e)}"
    
    # ===== Page Interaction Enhancements =====
    
    def scroll_to(self, x: int, y: int):
        """Scroll to specific coordinates on the page."""
        try:
            self._ensure_browser()
            self.page.evaluate(f"window.scrollTo({x}, {y})")
            return f"Scrolled to ({x}, {y})"
        except Exception as e:
            return f"Error scrolling: {str(e)}"
    
    def scroll_to_element(self, selector: str):
        """Scroll an element into view."""
        try:
            self._ensure_browser()
            self.page.locator(selector).scroll_into_view_if_needed(timeout=10000)
            return f"Scrolled to element {selector}"
        except Exception as e:
            return f"Error scrolling to element: {str(e)}"
    
    def hover_element(self, selector: str):
        """Hover over an element."""
        try:
            self._ensure_browser()
            self.page.hover(selector, timeout=10000)
            return f"Hovered over element {selector}"
        except Exception as e:
            return f"Error hovering: {str(e)}"
    
    def right_click(self, selector: str):
        """Right-click on an element."""
        try:
            self._ensure_browser()
            self.page.click(selector, button='right', timeout=10000)
            return f"Right-clicked element {selector}"
        except Exception as e:
            return f"Error right-clicking: {str(e)}"
    
    # ===== Tab Management =====
    
    def new_tab(self, url: str = "about:blank"):
        """Open a new tab and optionally navigate to a URL."""
        try:
            self._ensure_browser()
            new_page = self.context.new_page()
            if url != "about:blank":
                new_page.goto(url, wait_until='domcontentloaded', timeout=30000)
            self.page = new_page  # Switch to new tab
            return f"Opened new tab{' and navigated to ' + url if url != 'about:blank' else ''}"
        except Exception as e:
            return f"Error opening new tab: {str(e)}"
    
    def switch_tab(self, index: int):
        """Switch to a tab by index (0-based)."""
        try:
            self._ensure_browser()
            pages = self.context.pages
            if 0 <= index < len(pages):
                self.page = pages[index]
                return f"Switched to tab {index} (URL: {self.page.url})"
            else:
                return f"Invalid tab index {index}. Valid range: 0-{len(pages)-1}"
        except Exception as e:
            return f"Error switching tab: {str(e)}"
    
    def close_tab(self):
        """Close the current tab."""
        try:
            self._ensure_browser()
            pages = self.context.pages
            if len(pages) > 1:
                self.page.close()
                self.page = pages[0]  # Switch to first tab
                return "Closed current tab and switched to first tab"
            else:
                return "Cannot close the last tab. Use close_browser() instead."
        except Exception as e:
            return f"Error closing tab: {str(e)}"
    
    def list_tabs(self):
        """List all open tabs with their URLs."""
        try:
            self._ensure_browser()
            pages = self.context.pages
            result = f"Open tabs ({len(pages)}):\n"
            for i, page in enumerate(pages):
                current = " (current)" if page == self.page else ""
                result += f"{i}. {page.url}{current}\n"
            return result
        except Exception as e:
            return f"Error listing tabs: {str(e)}"
    
    # ===== Data Extraction Enhancements =====
    
    def extract_table(self, selector: str):
        """Extract table data as a structured format."""
        try:
            self._ensure_browser()
            table_data = self.page.evaluate(f"""
                () => {{
                    const table = document.querySelector('{selector}');
                    if (!table) return null;
                    const rows = Array.from(table.querySelectorAll('tr'));
                    return rows.map(row => {{
                        const cells = Array.from(row.querySelectorAll('th, td'));
                        return cells.map(cell => cell.textContent.trim());
                    }});
                }}
            """)
            if table_data:
                result = "Table data:\n"
                for row in table_data[:10]:  # Limit to 10 rows
                    result += " | ".join(row) + "\n"
                return result
            else:
                return f"No table found with selector {selector}"
        except Exception as e:
            return f"Error extracting table: {str(e)}"
    
    def get_all_text(self):
        """Get all visible text from the page."""
        try:
            self._ensure_browser()
            text = self.page.inner_text('body')
            # Truncate if too long
            if len(text) > 3000:
                text = text[:3000] + "\n...[Text Truncated]..."
            return f"Page text:\n{text}"
        except Exception as e:
            return f"Error getting page text: {str(e)}"
    
    def count_elements(self, selector: str):
        """Count the number of elements matching a selector."""
        try:
            self._ensure_browser()
            count = self.page.locator(selector).count()
            return f"Found {count} element(s) matching {selector}"
        except Exception as e:
            return f"Error counting elements: {str(e)}"
