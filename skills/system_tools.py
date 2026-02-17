import platform
import datetime

class SystemTools:
    @staticmethod
    def get_time():
        """Returns the current date and time."""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_os_info():
        """Returns operating system information."""
        return f"{platform.system()} {platform.release()} ({platform.version()})"
