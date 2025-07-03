# Bug Report: AttributeError in AgentBuilderDialog

## Description
An `AttributeError` occurs in `gui/desktop/agent_builder_dialog.py` when attempting to initialize the `AgentBuilderDialog`. The error message indicates that `AgentBuilderDialog` object has no attribute `create_model_settings_group`, suggesting a potential issue with the order of method calls in the `__init__` method or a lingering state from previous `replace` operations.

## Steps to Reproduce
1.  Launch the application: `python3 /home/ucadmin/Development/Colonel-Katie/gui/desktop/main.py`
2.  Open the Agent Builder dialog from the 'Options' menu.
3.  Alternatively, run the programmatic test:
    `python3 -c "from PySide6.QtWidgets import QApplication; from gui.desktop.agent_builder_dialog import AgentBuilderDialog; import sys; app = QApplication(sys.argv); dialog = AgentBuilderDialog(); dialog.agent_name_edit.setText('TestAgent'); dialog.profile_pic_path_edit.setText('/path/to/test_pic.png'); dialog.system_prompt_edit.setPlainText('This is a test system prompt.'); dialog.custom_instructions_edit.setPlainText('These are test custom instructions.'); dialog.shell_tool_checkbox.setChecked(True); dialog.browser_tool_checkbox.setChecked(False); dialog.files_tool_checkbox.setChecked(True); dialog.save_agent_profile(); sys.exit(app.exec_())"`

## Expected Behavior
The `AgentBuilderDialog` should initialize without errors, and the programmatic test should successfully save an agent profile.

## Actual Behavior
The application crashes with an `AttributeError: 'AgentBuilderDialog' object has no attribute 'create_model_settings_group'. Did you mean: 'create_general_settings_group'?`

## Impact
Prevents the proper functioning and testing of the Agent Builder feature.

## Proposed Solution (if any)
Re-verify the `__init__` method's call order in `AgentBuilderDialog` to ensure `create_general_settings_group()` is called before any methods that rely on its initialized attributes. Consider a full rewrite of the `agent_builder_dialog.py` file to ensure no lingering syntax issues from previous `replace` operations.
