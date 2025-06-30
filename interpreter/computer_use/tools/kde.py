
import subprocess
from ..kde_tools.notifications import send_notification
from ..kde_tools.windows import (
    get_window_info,
    query_window_info,
    set_current_desktop,
    next_desktop,
    previous_desktop,
)
from ..kde_tools.virtual_desktops import (
    get_desktop_count,
    get_current_desktop,
    create_desktop,
    remove_desktop,
    set_desktop_name,
)
from ..kde_tools.plasma_shell import evaluate_script
from ..kde_tools.clipboard import get_clipboard_contents, set_clipboard_contents
from ..kde_tools.file_operations import (
    write_file_content,
    read_file_content,
    append_file_content,
    create_directory,
    delete_file,
    delete_directory,
    list_directory_contents,
    move_item,
    copy_item,
)
from ..kde_tools.screensaver import set_screensaver_active


class Kde:
    def notification(self, summary, body=""):
        """
        Sends a desktop notification.

        Args:
            summary (str): The summary text of the notification.
            body (str, optional): The body text of the notification. Defaults to "".
        """
        send_notification(summary, body)

    def get_window_info(self, window_id):
        """
        Gets information about a specific window.

        Args:
            window_id (str): The ID of the window.

        Returns:
            dict: A dictionary containing information about the window, with keys such as:
                  'caption': The window title.
                  'geometry': Dictionary with 'x', 'y', 'width', 'height'.
                  'pid': The process ID of the application.
                  'desktop': The desktop number the window is on.
                  'active': Boolean indicating if the window is active.
                  'minimized': Boolean indicating if the window is minimized.
                  'maximized': Boolean indicating if the window is maximized.
                  'fullscreen': Boolean indicating if the window is fullscreen.
        """
        return get_window_info(window_id)

    def query_window_info(self):
        """
        Gets information about all windows.

        Returns:
            dict: A dictionary where keys are window IDs and values are dictionaries
                  containing information about each window, with keys such as:
                  'caption': The window title.
                  'geometry': Dictionary with 'x', 'y', 'width', 'height'.
                  'pid': The process ID of the application.
                  'desktop': The desktop number the window is on.
                  'active': Boolean indicating if the window is active.
                  'minimized': Boolean indicating if the window is minimized.
                  'maximized': Boolean indicating if the window is maximized.
                  'fullscreen': Boolean indicating if the window is fullscreen.
        """
        return query_window_info()

    def set_current_desktop(self, desktop):
        """
        Switches to the specified virtual desktop.

        Args:
            desktop (int): The number of the virtual desktop to switch to.
        """
        set_current_desktop(desktop)

    def next_desktop(self):
        """
        Switches to the next virtual desktop.
        """
        next_desktop()

    def previous_desktop(self):
        """
        Switches to the previous virtual desktop.
        """
        previous_desktop()

    def get_desktop_count(self):
        """
        Gets the number of virtual desktops.

        Returns:
            int: The number of virtual desktops.
        """
        return get_desktop_count()

    def get_current_desktop(self):
        """
        Gets the ID of the current virtual desktop.

        Returns:
            str: The ID of the current virtual desktop.
        """
        return get_current_desktop()

    def create_desktop(self, position, name):
        """
        Creates a new virtual desktop.

        Args:
            position (int): The position of the new desktop.
            name (str): The name of the new desktop.
        """
        create_desktop(position, name)

    def remove_desktop(self, desktop_id):
        """
        Removes a virtual desktop.

        Args:
            desktop_id (str): The ID of the desktop to remove.
        """
        remove_desktop(desktop_id)

    def set_desktop_name(self, desktop_id, name):
        """
        Sets the name of a virtual desktop.

        Args:
            desktop_id (str): The ID of the desktop to rename.
            name (str): The new name of the desktop.
        """
        set_desktop_name(desktop_id, name)

    def evaluate_script(self, script):
        """
        Evaluates a JavaScript script in the Plasma Shell.

        Args:
            script (str): The JavaScript script to evaluate.

        Returns:
            str: The result of the script evaluation.
        """
        try:
            result = subprocess.run([
                "qdbus6",
                "org.kde.plasmashell",
                "/PlasmaShell",
                "org.kde.PlasmaShell.evaluateScript",
                script
            ], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to evaluate script: {e.stderr}")
        except FileNotFoundError:
            raise Exception("qdbus6 command not found. Is qdbus installed and in PATH?")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")

    def get_clipboard_contents(self):
        """
        Gets the current contents of the clipboard.

        Returns:
            str: The clipboard contents.
        """
        return get_clipboard_contents()

    def set_clipboard_contents(self, text):
        """
        Sets the clipboard contents.

        Args:
            text (str): The text to set as clipboard contents.
        """
        set_clipboard_contents(text)

    def krunner_query(self, term):
        """
        Queries KRunner with the given term.

        Args:
            term (str): The search term for KRunner.
        """
        subprocess.run([
            "qdbus6",
            "org.kde.krunner",
            "/App",
            "org.kde.krunner.App.query",
            term
        ])

    def krunner_toggle_display(self):
        """
        Toggles the display of KRunner.
        """
        subprocess.run([
            "qdbus6",
            "org.kde.krunner",
            "/App",
            "org.kde.krunner.App.toggleDisplay"
        ])

    def get_battery_remaining_time(self):
        """
        Gets the remaining battery time in milliseconds.

        Returns:
            int: The remaining battery time in milliseconds.
        """
        result = subprocess.run([
            "qdbus6",
            "org.kde.Solid.PowerManagement",
            "/org/kde/Solid/PowerManagement",
            "org.kde.Solid.PowerManagement.batteryRemainingTime"
        ], capture_output=True, text=True)
        return int(result.stdout.strip())

    def get_current_power_profile(self):
        """
        Gets the current power profile.

        Returns:
            str: The current power profile.
        """
        result = subprocess.run([
            "qdbus6",
            "org.kde.Solid.PowerManagement",
            "/org/kde/Solid/PowerManagement",
            "org.kde.Solid.PowerManagement.currentProfile"
        ], capture_output=True, text=True)
        return result.stdout.strip()

    def is_lid_closed(self):
        """
        Checks if the laptop lid is closed.

        Returns:
            bool: True if the lid is closed, False otherwise.
        """
        result = subprocess.run([
            "qdbus6",
            "org.kde.Solid.PowerManagement",
            "/org/kde/Solid/PowerManagement",
            "org.kde.Solid.PowerManagement.isLidClosed"
        ], capture_output=True, text=True)
        return result.stdout.strip().lower() == "true"

    def konsole_run_command(self, command, session_id="1"):
        """
        Runs a command in a Konsole session.

        Args:
            command (str): The command to run.
            session_id (str, optional): The ID of the Konsole session. Defaults to "1".
        """
        # Discover the active Konsole instance dynamically
        result = subprocess.run(["qdbus6", "--session", "--literal", "org.kde.konsole", "/", "org.freedesktop.DBus.ListNames"], capture_output=True, text=True)
        konsole_service = ""
        for line in result.stdout.splitlines():
            if "org.kde.konsole-" in line:
                konsole_service = line.strip()
                break

        if not konsole_service:
            raise Exception("No active Konsole instance found.")

        subprocess.run([
            "qdbus6",
            konsole_service,
            f"/Sessions/{session_id}",
            "org.kde.konsole.Session.runCommand",
            command
        ])

    def konsole_send_text(self, text, session_id="1"):
        """
        Sends text to a Konsole session.

        Args:
            text (str): The text to send.
            session_id (str, optional): The ID of the Konsole session. Defaults to "1".
        """
        # Discover the active Konsole instance dynamically
        result = subprocess.run(["qdbus6", "--session", "--literal", "org.kde.konsole", "/", "org.freedesktop.DBus.ListNames"], capture_output=True, text=True)
        konsole_service = ""
        for line in result.stdout.splitlines():
            if "org.kde.konsole-" in line:
                konsole_service = line.strip()
                break

        if not konsole_service:
            raise Exception("No active Konsole instance found.")

        subprocess.run([
            "qdbus6",
            konsole_service,
            f"/Sessions/{session_id}",
            "org.kde.konsole.Session.sendText",
            text
        ])

    def lock_screen(self):
        """
        Locks the screen.
        """
        subprocess.run([
            "qdbus6",
            "org.freedesktop.ScreenSaver",
            "/ScreenSaver",
            "org.freedesktop.ScreenSaver.Lock"
        ])

    

    def show_folders(self, uri_list):
        """
        Shows folders in the file manager.

        Args:
            uri_list (list): A list of URIs (e.g., file:///home/user/Documents).
        """
        subprocess.run([
            "qdbus6",
            "org.freedesktop.FileManager1",
            "/org/freedesktop/FileManager1",
            "org.freedesktop.FileManager1.ShowFolders",
            " ".join(uri_list),
            ""
        ])

    def show_item_properties(self, uri_list):
        """
        Shows properties of items in the file manager.

        Args:
            uri_list (list): A list of URIs (e.g., file:///home/user/Documents/file.txt).
        """
        subprocess.run([
            "qdbus6",
            "org.freedesktop.FileManager1",
            "/org/freedesktop/FileManager1",
            "org.freedesktop.FileManager1.ShowItemProperties",
            " ".join(uri_list),
            ""
        ])

    def show_items(self, uri_list):
        """
        Shows items in the file manager.

        Args:
            uri_list (list): A list of URIs (e.g., file:///home/user/Documents/file.txt).
        """
        subprocess.run([
            "qdbus6",
            "org.freedesktop.FileManager1",
            "/org/freedesktop/FileManager1",
            "org.freedesktop.FileManager1.ShowItems",
            " ".join(uri_list),
            ""
        ])

    def close_notification(self, notification_id):
        """
        Closes a specific notification.

        Args:
            notification_id (int): The ID of the notification to close.
        """
        subprocess.run([
            "qdbus6",
            "org.freedesktop.Notifications",
            "/org/freedesktop/Notifications",
            "org.freedesktop.Notifications.CloseNotification",
            str(notification_id)
        ])

    def take_screenshot(self, parent_window="", options="{}"):
        """
        Takes a screenshot and returns the base64 encoded image data.

        Args:
            parent_window (str, optional): The parent window. Defaults to "".
            options (str, optional): JSON string of options. Defaults to "{}".

        Returns:
            str: The base64 encoded image data of the screenshot.
        """
        import base64
        import os
        import tempfile

        # Call the D-Bus method to take a screenshot
        result = subprocess.run([
            "qdbus6",
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.Screenshot.Screenshot",
            parent_window,
            options
        ], capture_output=True, text=True)

        # The result contains the path to the screenshot file (e.g., "file:///tmp/screenshot_XXXXXX.png")
        screenshot_uri = result.stdout.strip()
        if not screenshot_uri:
            raise Exception("Failed to take screenshot: No URI returned.")

        # Convert file URI to local path
        screenshot_path = screenshot_uri.replace("file://", "")

        if not os.path.exists(screenshot_path):
            raise Exception(f"Screenshot file not found at {screenshot_path}")

        # Read the image file and encode it to base64
        with open(screenshot_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # Clean up the temporary screenshot file
        os.remove(screenshot_path)

        return encoded_string

    def read_setting(self, namespace, key):
        """
        Reads a setting from the desktop portal.

        Args:
            namespace (str): The namespace of the setting.
            key (str): The key of the setting.

        Returns:
            str: The value of the setting.
        """
        result = subprocess.run([
            "qdbus6",
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.Settings.Read",
            namespace,
            key
        ], capture_output=True, text=True)
        return result.stdout.strip()

    def read_all_settings(self, namespaces):
        """
        Reads all settings from the desktop portal for given namespaces.

        Args:
            namespaces (list): A list of namespaces.

        Returns:
            str: A JSON string of settings.
        """
        result = subprocess.run([
            "qdbus6",
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.Settings.ReadAll",
            " ".join(namespaces)
        ], capture_output=True, text=True)
        return result.stdout.strip()

    def open_uri(self, uri, parent_window="", options="{}"):
        """
        Opens a URI using the desktop portal.

        Args:
            uri (str): The URI to open.
            parent_window (str, optional): The parent window. Defaults to "".
            options (str, optional): JSON string of options. Defaults to "{}".
        """
        subprocess.run([
            "qdbus6",
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.OpenURI.OpenURI",
            parent_window,
            uri,
            options
        ])

    def trash_file(self, fd):
        """
        Moves a file to the trash using the desktop portal.

        Args:
            fd (str): The file descriptor of the file to trash.
        """
        subprocess.run([
            "qdbus6",
            "org.freedesktop.portal.Desktop",
            "/org/freedesktop/portal/desktop",
            "org.freedesktop.portal.Trash.TrashFile",
            fd
        ])

    def write_file(self, path, content):
        """
        Writes content to a file. Creates the file if it doesn't exist.

        Args:
            path (str): The absolute path to the file.
            content (str): The content to write to the file.
        """
        write_file_content(path, content)

    def read_file(self, path):
        """
        Reads content from a file.

        Args:
            path (str): The absolute path to the file.

        Returns:
            str: The content of the file.
        """
        return read_file_content(path)

    def append_file(self, path, content):
        """
        Appends content to a file. Creates the file if it doesn't exist.

        Args:
            path (str): The absolute path to the file.
            content (str): The content to append to the file.
        """
        append_file_content(path, content)

    def create_dir(self, path):
        """
        Creates a new directory.

        Args:
            path (str): The absolute path to the directory to create.
        """
        create_directory(path)

    def delete_file(self, path):
        """
        Deletes a file.

        Args:
            path (str): The absolute path to the file to delete.
        """
        delete_file(path)

    def delete_dir(self, path):
        """
        Deletes a directory and all its contents.

        Args:
            path (str): The absolute path to the directory to delete.
        """
        delete_directory(path)

    def list_dir(self, path):
        """
        Lists the contents of a directory.

        Args:
            path (str): The absolute path to the directory.

        Returns:
            list: A list of file and directory names within the specified path.
        """
        return list_directory_contents(path)

    def move_item(self, source_path, destination_path):
        """
        Moves a file or directory from source to destination.

        Args:
            source_path (str): The absolute path of the item to move.
            destination_path (str): The absolute path to the destination.
        """
        move_item(source_path, destination_path)

    def copy_item(self, source_path, destination_path):
        """
        Copies a file or directory from source to destination.

        Args:
            source_path (str): The absolute path of the item to copy.
            destination_path (str): The absolute path to the destination.
        """
        copy_item(source_path, destination_path)

    def konsole_run_command(self, command, session_id="1"):
        """
        Runs a command in a Konsole session.

        Args:
            command (str): The command to run.
            session_id (str, optional): The ID of the Konsole session. Defaults to "1".
        """
        # Discover the active Konsole instance dynamically
        result = subprocess.run(["qdbus6", "--session", "--literal", "org.kde.konsole", "/", "org.freedesktop.DBus.ListNames"], capture_output=True, text=True)
        konsole_service = ""
        for line in result.stdout.splitlines():
            if "org.kde.konsole-" in line:
                konsole_service = line.strip()
                break

        if not konsole_service:
            raise Exception("No active Konsole instance found.")

        subprocess.run([
            "qdbus6",
            konsole_service,
            f"/Sessions/{session_id}",
            "org.kde.konsole.Session.runCommand",
            command
        ])

    def konsole_send_text(self, text, session_id="1"):
        """
        Sends text to a Konsole session.

        Args:
            text (str): The text to send.
            session_id (str, optional): The ID of the Konsole session. Defaults to "1".
        """
        # Discover the active Konsole instance dynamically
        result = subprocess.run(["qdbus6", "--session", "--literal", "org.kde.konsole", "/", "org.freedesktop.DBus.ListNames"], capture_output=True, text=True)
        konsole_service = ""
        for line in result.stdout.splitlines():
            if "org.kde.konsole-" in line:
                konsole_service = line.strip()
                break

        if not konsole_service:
            raise Exception("No active Konsole instance found.")

        subprocess.run([
            "qdbus6",
            konsole_service,
            f"/Sessions/{session_id}",
            "org.kde.konsole.Session.sendText",
            text
        ])

    def lock_screen(self):
        """
        Locks the screen.
        """
        subprocess.run([
            "qdbus6",
            "org.freedesktop.ScreenSaver",
            "/ScreenSaver",
            "org.freedesktop.ScreenSaver.Lock"
        ])

    def list_processes(self):
        """
        Lists all running processes with their PIDs, names, and CPU/memory usage.

        Returns:
            list: A list of dictionaries, each representing a process.
        """
        try:
            # Using 'ps aux' for a comprehensive list of processes
            result = subprocess.run(["ps", "aux"], capture_output=True, text=True, check=True)
            lines = result.stdout.strip().split('\n')
            
            processes = []
            # Skip header line
            for line in lines[1:]:
                parts = line.split(None, 10) # Split into at most 11 parts
                if len(parts) >= 11:
                    user, pid, cpu, mem, vsz, rss, tty, stat, start, time_str, command = parts
                    processes.append({
                        "user": user,
                        "pid": int(pid),
                        "cpu_usage": float(cpu),
                        "memory_usage": float(mem),
                        "command": command
                    })
            return processes
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to list processes: {e.stderr}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while listing processes: {e}")

    def kill_process(self, pid):
        """
        Kills a process by its PID.

        Args:
            pid (int): The Process ID to kill.
        """
        try:
            subprocess.run(["kill", str(pid)], check=True)
            return f"Process {pid} killed successfully."
        except subprocess.CalledProcessError as e:
            raise Exception(f"Failed to kill process {pid}: {e.stderr}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while killing process {pid}: {e}")

    def find_process(self, name):
        """
        Finds processes by name.

        Args:
            name (str): The name or part of the name of the process to find.

        Returns:
            list: A list of dictionaries, each representing a found process.
        """
        try:
            # Using 'pgrep -l' to find processes by name and list their PID and name
            result = subprocess.run(["pgrep", "-l", name], capture_output=True, text=True, check=False)
            
            processes = []
            if result.returncode == 0: # pgrep returns 0 if matches are found
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split(None, 1)
                        if len(parts) == 2:
                            pid, cmd = parts
                            processes.append({"pid": int(pid), "name": cmd})
            elif result.returncode == 1: # pgrep returns 1 if no matches are found
                return []
            else: # Other error codes
                raise Exception(f"pgrep command failed with error: {result.stderr}")
            
            return processes
        except Exception as e:
            raise Exception(f"An unexpected error occurred while finding process '{name}': {e}")

    def launch_application(self, app_name, args=None):
        """
        Launches an application.

        Args:
            app_name (str): The name of the application to launch (e.g., 'firefox', 'konsole').
            args (list, optional): A list of arguments to pass to the application. Defaults to None.
        """
        command = [app_name]
        if args:
            command.extend(args)
        try:
            subprocess.Popen(command) # Use Popen to launch without waiting
            return f"Application '{app_name}' launched successfully."
        except FileNotFoundError:
            raise Exception(f"Application '{app_name}' not found. Is it installed and in PATH?")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while launching '{app_name}': {e}")

    def open_file_with_application(self, file_path, app_name):
        """
        Opens a file with a specific application.

        Args:
            file_path (str): The absolute path to the file.
            app_name (str): The name of the application to open the file with.
        """
        try:
            subprocess.Popen([app_name, file_path])
            return f"File '{file_path}' opened with '{app_name}' successfully."
        except FileNotFoundError:
            raise Exception(f"Application '{app_name}' not found. Is it installed and in PATH?")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while opening '{file_path}' with '{app_name}': {e}")

    def set_screensaver_active(self, active):
        """
        Sets the screensaver active state.

        Args:
            active (bool): True to activate, False to deactivate.
        """
        subprocess.run([
            "qdbus6",
            "org.freedesktop.ScreenSaver",
            "/ScreenSaver",
            "org.freedesktop.ScreenSaver.SetActive",
            str(active).lower()
        ])

    def list_activities(self):
        """
        Lists all KDE activities.

        Returns:
            list: A list of activity IDs.
        """
        result = subprocess.run([
            "qdbus6",
            "org.kde.ActivityManager",
            "/ActivityManager/Activities",
            "org.kde.ActivityManager.Activities.ListActivities"
        ], capture_output=True, text=True)
        return result.stdout.strip().split('\n')

    def get_current_activity(self):
        """
        Gets the ID of the current KDE activity.

        Returns:
            str: The ID of the current activity.
        """
        result = subprocess.run([
            "qdbus6",
            "org.kde.ActivityManager",
            "/ActivityManager/Activities",
            "org.kde.ActivityManager.Activities.CurrentActivity"
        ], capture_output=True, text=True)
        return result.stdout.strip()

    def set_current_activity(self, activity_id):
        """
        Sets the current KDE activity.

        Args:
            activity_id (str): The ID of the activity to set as current.
        """
        subprocess.run([
            "qdbus6",
            "org.kde.ActivityManager",
            "/ActivityManager/Activities",
            "org.kde.ActivityManager.Activities.SetCurrentActivity",
            activity_id
        ])

    def add_activity(self, name):
        """
        Adds a new KDE activity.

        Args:
            name (str): The name of the new activity.

        Returns:
            str: The ID of the newly created activity.
        """
        result = subprocess.run([
            "qdbus6",
            "org.kde.ActivityManager",
            "/ActivityManager/Activities",
            "org.kde.ActivityManager.Activities.AddActivity",
            name
        ], capture_output=True, text=True)
        return result.stdout.strip()

    def remove_activity(self, activity_id):
        """
        Removes a KDE activity.

        Args:
            activity_id (str): The ID of the activity to remove.
        """
        subprocess.run([
            "qdbus6",
            "org.kde.ActivityManager",
            "/ActivityManager/Activities",
            "org.kde.ActivityManager.Activities.RemoveActivity",
            activity_id
        ])

    

    

    
