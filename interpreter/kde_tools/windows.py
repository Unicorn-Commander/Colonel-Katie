
from PySide6.QtDBus import QDBusConnection, QDBusMessage
from PySide6.QtCore import QCoreApplication
import json

def _get_dbus_connection():
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    return QDBusConnection.sessionBus()

def get_window_info(window_id):
    """
    Gets information about a specific window using PySide6 D-Bus.

    Args:
        window_id (str): The ID of the window.

    Returns:
        dict: A dictionary containing information about the window.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.KWin",
        "/KWin",
        "org.kde.KWin",
        "getWindowInfo"
    )
    message.setArguments([window_id])
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ReplyMessage:
        result = reply.arguments()[0] if reply.arguments() else "{}"
        return json.loads(str(result))
    else:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")

def query_window_info():
    """
    Gets information about all windows using PySide6 D-Bus.

    Returns:
        dict: A dictionary containing information about all windows.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.KWin",
        "/KWin",
        "org.kde.KWin",
        "queryWindowInfo"
    )
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ReplyMessage:
        result = reply.arguments()[0] if reply.arguments() else "{}"
        return json.loads(str(result))
    else:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")

def set_current_desktop(desktop):
    """
    Switches to the specified virtual desktop using PySide6 D-Bus.

    Args:
        desktop (int): The number of the virtual desktop to switch to.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.KWin",
        "/KWin",
        "org.kde.KWin",
        "setCurrentDesktop"
    )
    message.setArguments([desktop])
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ErrorMessage:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")

def next_desktop():
    """
    Switches to the next virtual desktop using PySide6 D-Bus.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.KWin",
        "/KWin",
        "org.kde.KWin",
        "nextDesktop"
    )
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ErrorMessage:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")

def previous_desktop():
    """
    Switches to the previous virtual desktop using PySide6 D-Bus.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.KWin",
        "/KWin",
        "org.kde.KWin",
        "previousDesktop"
    )
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ErrorMessage:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")
