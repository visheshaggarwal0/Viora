import platform
import datetime
import os
import subprocess

class SystemTools:
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
        Example: 'notepad', 'calculator', or a full path.
        """
        try:
            # os.startfile is Windows-specific and handles both app names in PATH and full paths
            os.startfile(app_name)
            return f"Successfully attempted to open {app_name}."
        except Exception as e:
            return f"Failed to open {app_name}: {str(e)}"

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
