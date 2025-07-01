
from PySide6.QtDBus import QDBusConnection, QDBusMessage
from PySide6.QtCore import QCoreApplication

def _get_dbus_connection():
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    return QDBusConnection.sessionBus()

def get_desktop_count():
    """
    Gets the number of virtual desktops using PySide6 D-Bus.

    Returns:
        int: The number of virtual desktops.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.KWin",
        "/VirtualDesktopManager",
        "org.kde.KWin.VirtualDesktopManager",
        "count"
    )
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ReplyMessage:
        return int(reply.arguments()[0]) if reply.arguments() else 0
    else:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")

def get_current_desktop():
    """
    Gets the ID of the current virtual desktop using PySide6 D-Bus.

    Returns:
        str: The ID of the current virtual desktop.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.KWin",
        "/VirtualDesktopManager",
        "org.kde.KWin.VirtualDesktopManager",
        "current"
    )
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ReplyMessage:
        return str(reply.arguments()[0]) if reply.arguments() else ""
    else:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")

def create_desktop(position, name):
    """
    Creates a new virtual desktop using PySide6 D-Bus.

    Args:
        position (int): The position of the new desktop.
        name (str): The name of the new desktop.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.KWin",
        "/VirtualDesktopManager",
        "org.kde.KWin.VirtualDesktopManager",
        "createDesktop"
    )
    message.setArguments([position, name])
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ErrorMessage:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")

def remove_desktop(desktop_id):
    """
    Removes a virtual desktop using PySide6 D-Bus.

    Args:
        desktop_id (str): The ID of the desktop to remove.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.KWin",
        "/VirtualDesktopManager",
        "org.kde.KWin.VirtualDesktopManager",
        "removeDesktop"
    )
    message.setArguments([desktop_id])
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ErrorMessage:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")

def set_desktop_name(desktop_id, name):
    """
    Sets the name of a virtual desktop using PySide6 D-Bus.

    Args:
        desktop_id (str): The ID of the desktop to rename.
        name (str): The new name of the desktop.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.KWin",
        "/VirtualDesktopManager",
        "org.kde.KWin.VirtualDesktopManager",
        "setDesktopName"
    )
    message.setArguments([desktop_id, name])
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ErrorMessage:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")
