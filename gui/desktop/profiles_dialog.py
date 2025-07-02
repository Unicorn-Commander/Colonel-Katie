
import os
from PySide6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from dotenv import set_key

class ProfilesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Profiles")
        self.setGeometry(200, 200, 400, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint) # Remove help button

        self.layout = QVBoxLayout(self)
        self.profile_list_widget = QListWidget(self)
        self.layout.addWidget(self.profile_list_widget)

        self.set_default_button = QPushButton("Set as Default Profile")
        self.set_default_button.clicked.connect(self.set_default_profile)
        self.set_default_button.setToolTip("Set the selected profile as the default for new sessions.")
        self.layout.addWidget(self.set_default_button)

        self.load_profiles()
        self.highlight_default_profile()

    def load_profiles(self):
        profiles_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "interpreter", "terminal_interface", "profiles", "defaults")
        if not os.path.exists(profiles_dir):
            self.profile_list_widget.addItem("Error: Profiles directory not found.")
            return

        for filename in os.listdir(profiles_dir):
            if filename.endswith(".py") or filename.endswith(".yaml") or filename.endswith(".yml"):
                self.profile_list_widget.addItem(filename)

    def highlight_default_profile(self):
        default_profile = os.getenv("DEFAULT_PROFILE", "The_Colonel.py")
        items = self.profile_list_widget.findItems(default_profile, Qt.MatchExactly)
        if items:
            items[0].setSelected(True)
            self.profile_list_widget.scrollToItem(items[0])

    def set_default_profile(self):
        selected_items = self.profile_list_widget.selectedItems()
        if not selected_items:
            self.parent().output_display.append("Please select a profile to set as default.")
            return

        selected_profile = selected_items[0].text()
        try:
            set_key(os.getenv("DOTENV_PATH", ".env"), "DEFAULT_PROFILE", selected_profile)
            self.parent().chat_window.append_output(f"Default profile set to: {selected_profile}")
            self.accept() # Close dialog
        except Exception as e:
            self.parent().chat_window.append_output(f"Error setting default profile: {e}")
