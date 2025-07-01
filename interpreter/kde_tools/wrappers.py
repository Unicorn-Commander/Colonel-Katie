import os
import shutil
from datetime import datetime
import json

from PySide6.QtDBus import QDBusConnection, QDBusMessage
from PySide6.QtCore import QCoreApplication

# Import the original global functions
from . import clipboard
from . import file_operations
from . import notifications
from . import plasma_shell
from . import virtual_desktops
from . import windows

def _get_dbus_connection():
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    return QDBusConnection.sessionBus()

class KDEClipboardWrapper:
    def __init__(self, computer):
        self.computer = computer

    def get_contents(self):
        """
        Gets the current contents of the clipboard using PySide6 D-Bus.
        Returns:
            str: The clipboard contents.
        """
        return clipboard.get_clipboard_contents()

    def set_contents(self, text: str):
        """
        Sets the clipboard contents using PySide6 D-Bus.
        Args:
            text (str): The text to set as clipboard contents.
        """
        clipboard.set_clipboard_contents(text)

class KDEFileOperationsWrapper:
    def __init__(self, computer):
        self.computer = computer

    def write_file_content(self, path: str, content: str):
        """
        Writes content to a file. Creates the file if it doesn't exist.
        Args:
            path (str): The absolute path to the file.
            content (str): The content to write to the file.
        """
        file_operations.write_file_content(path, content)

    def read_file_content(self, path: str):
        """
        Reads content from a file.
        Args:
            path (str): The absolute path to the file.
        Returns:
            str: The content of the file.
        """
        return file_operations.read_file_content(path)

    def append_file_content(self, path: str, content: str):
        """
        Appends content to a file. Creates the file if it doesn't exist.
        Args:
            path (str): The absolute path to the file.
            content (str): The content to append to the file.
        """
        file_operations.append_file_content(path, content)

    def create_directory(self, path: str):
        """
        Creates a new directory.
        Args:
            path (str): The absolute path to the directory to create.
        """
        file_operations.create_directory(path)

    def delete_file(self, path: str):
        """
        Deletes a file.
        Args:
            path (str): The absolute path to the file to delete.
        """
        file_operations.delete_file(path)

    def delete_directory(self, path: str):
        """
        Deletes a directory and all its contents.
        Args:
            path (str): The absolute path to the directory to delete.
        """
        file_operations.delete_directory(path)

    def list_directory_contents(self, path: str):
        """
        Lists the contents of a directory.
        Args:
            path (str): The absolute path to the directory.
        Returns:
            list: A list of file and directory names within the specified path.
        """
        return file_operations.list_directory_contents(path)

    def move_item(self, source_path: str, destination_path: str):
        """
        Moves a file or directory from source to destination.
        Args:
            source_path (str): The absolute path of the item to move.
            destination_path (str): The absolute path to the destination.
        """
        file_operations.move_item(source_path, destination_path)

    def copy_item(self, source_path: str, destination_path: str):
        """
        Copies a file or directory from source to destination.
        Args:
            source_path (str): The absolute path of the item to copy.
            destination_path (str): The absolute path to the destination.
        """
        file_operations.copy_item(source_path, destination_path)

class KDENotificationsWrapper:
    def __init__(self, computer):
        self.computer = computer

    def send_notification(self, summary: str, body: str = "", app_name: str = "The Colonel", app_icon: str = "", timeout: int = 5000):
        """
        Sends a desktop notification using PySide6 D-Bus.
        Args:
            summary (str): The summary text of the notification.
            body (str, optional): The body text of the notification. Defaults to "".
            app_name (str, optional): The name of the application sending the notification. Defaults to "The Colonel".
            app_icon (str, optional): The icon to display with the notification. Defaults to "".
            timeout (int, optional): The timeout in milliseconds. Defaults to 5000.
        """
        notifications.send_notification(summary, body, app_name, app_icon, timeout)

class KDEPlasmaShellWrapper:
    def __init__(self, computer):
        self.computer = computer

    def evaluate_script(self, script: str):
        """
        Evaluates a JavaScript script in the Plasma Shell using PySide6 D-Bus.
        Args:
            script (str): The JavaScript script to evaluate.
        Returns:
            str: The result of the script evaluation.
        """
        return plasma_shell.evaluate_script(script)

class KDEVirtualDesktopsWrapper:
    def __init__(self, computer):
        self.computer = computer

    def get_desktop_count(self):
        """
        Gets the number of virtual desktops using PySide6 D-Bus.
        Returns:
            int: The number of virtual desktops.
        """
        return virtual_desktops.get_desktop_count()

    def get_current_desktop(self):
        """
        Gets the ID of the current virtual desktop using PySide6 D-Bus.
        Returns:
            str: The ID of the current virtual desktop.
        """
        return virtual_desktops.get_current_desktop()

    def create_desktop(self, position: int, name: str):
        """
        Creates a new virtual desktop using PySide6 D-Bus.
        Args:
            position (int): The position of the new desktop.
            name (str): The name of the new desktop.
        """
        virtual_desktops.create_desktop(position, name)

    def remove_desktop(self, desktop_id: str):
        """
        Removes a virtual desktop using PySide6 D-Bus.
        Args:
            desktop_id (str): The ID of the desktop to remove.
        """
        virtual_desktops.remove_desktop(desktop_id)

    def set_desktop_name(self, desktop_id: str, name: str):
        """
        Sets the name of a virtual desktop using PySide6 D-Bus.
        Args:
            desktop_id (str): The ID of the desktop to rename.
            name (str): The new name of the desktop.
        """
        virtual_desktops.set_desktop_name(desktop_id, name)

class KDEWindowsWrapper:
    def __init__(self, computer):
        self.computer = computer

    def get_window_info(self, window_id: str):
        """
        Gets information about a specific window using PySide6 D-Bus.
        Args:
            window_id (str): The ID of the window.
        Returns:
            dict: A dictionary containing information about the window.
        """
        return windows.get_window_info(window_id)

    def query_window_info(self):
        """
        Gets information about all windows using PySide6 D-Bus.
        Returns:
            dict: A dictionary containing information about all windows.
        """
        return windows.query_window_info()

    def set_current_desktop(self, desktop: int):
        """
        Switches to the specified virtual desktop using PySide6 D-Bus.
        Args:
            desktop (int): The number of the virtual desktop to switch to.
        """
        windows.set_current_desktop(desktop)

    def next_desktop(self):
        """
        Switches to the next virtual desktop using PySide6 D-Bus.
        """
        windows.next_desktop()

    def previous_desktop(self):
        """
        Switches to the previous virtual desktop using PySide6 D-Bus.
        """
        windows.previous_desktop()
