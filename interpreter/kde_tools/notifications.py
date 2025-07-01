
from PySide6.QtDBus import QDBusConnection, QDBusMessage
from PySide6.QtCore import QCoreApplication

def _get_dbus_connection():
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    return QDBusConnection.sessionBus()

def send_notification(summary, body="", app_name="The Colonel", app_icon="", timeout=5000):
    """
    Sends a desktop notification using PySide6 D-Bus.

    Args:
        summary (str): The summary text of the notification.
        body (str, optional): The body text of the notification. Defaults to "".
        app_name (str, optional): The name of the application sending the notification. Defaults to "The Colonel".
        app_icon (str, optional): The icon to display with the notification. Defaults to "".
        timeout (int, optional): The timeout in milliseconds. Defaults to 5000.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.freedesktop.Notifications",
        "/org/freedesktop/Notifications",
        "org.freedesktop.Notifications",
        "Notify"
    )
    
    # Arguments for Notify: app_name, replaces_id, app_icon, summary, body, actions, hints, timeout
    message.setArguments([
        app_name,           # app_name
        0,                  # replaces_id (0 = new notification)
        app_icon,           # app_icon
        summary,            # summary
        body,               # body
        [],                 # actions (empty list)
        {},                 # hints (empty dict)
        timeout             # timeout
    ])
    
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ErrorMessage:
        raise Exception(f"D-Bus notification call failed: {reply.errorMessage()}")
