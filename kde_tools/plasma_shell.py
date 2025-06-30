
from PySide6.QtDBus import QDBusConnection, QDBusMessage
from PySide6.QtCore import QCoreApplication

def _get_dbus_connection():
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication([])
    return QDBusConnection.sessionBus()

def evaluate_script(script):
    """
    Evaluates a JavaScript script in the Plasma Shell using PySide6 D-Bus.

    Args:
        script (str): The JavaScript script to evaluate.

    Returns:
        str: The result of the script evaluation.
    """
    connection = _get_dbus_connection()
    message = QDBusMessage.createMethodCall(
        "org.kde.plasmashell",
        "/PlasmaShell",
        "org.kde.PlasmaShell",
        "evaluateScript"
    )
    message.setArguments([script])
    
    reply = connection.call(message)
    if reply.type() == QDBusMessage.Type.ReplyMessage:
        return reply.arguments()[0] if reply.arguments() else ""
    else:
        raise Exception(f"D-Bus Plasma Shell call failed: {reply.errorMessage()}")
