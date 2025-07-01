
from PySide6.QtDBus import QDBusConnection, QDBusMessage
from PySide6.QtCore import QCoreApplication

def _get_dbus_connection():
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    return QDBusConnection.sessionBus()

def get_clipboard_contents():
    """
    Gets the current contents of the clipboard using PySide6 D-Bus.

    Returns:
        str: The clipboard contents.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.klipper",
        "/klipper",
        "org.kde.klipper.klipper",
        "getClipboardContents"
    )
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ReplyMessage:
        return reply.arguments()[0] if reply.arguments() else ""
    else:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")

def set_clipboard_contents(text):
    """
    Sets the clipboard contents using PySide6 D-Bus.

    Args:
        text (str): The text to set as clipboard contents.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.klipper",
        "/klipper",
        "org.kde.klipper.klipper",
        "setClipboardContents"
    )
    message.setArguments([text])
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ErrorMessage:
        raise Exception(f"D-Bus call failed: {reply.errorMessage()}")
