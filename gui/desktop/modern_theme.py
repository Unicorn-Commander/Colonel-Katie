# Modern cutting-edge theme for The Colonel GUI
# Inspired by next-generation design patterns

MODERN_STYLESHEET = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
            stop:0 #0a0a0f, stop:0.5 #1a1a2e, stop:1 #0f0f1a);
        color: #f8f9fa;
        border-radius: 12px;
        font-family: "Inter", "SF Pro Display", "Segoe UI Variable", "Helvetica Neue", system-ui, sans-serif;
        font-size: 11pt;
        font-weight: 400;
        letter-spacing: -0.01em;
    }
    
    QWidget#central_widget {
        background: transparent;
        border-radius: 12px;
    }
    
    /* Sidebar Styling - Glass morphism effect */
    ConversationHistory, QWidget#right_sidebar {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(255, 255, 255, 0.05),
            stop:1 rgba(255, 255, 255, 0.02));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        backdrop-filter: blur(20px);
        margin: 8px;
    }
    
    QLabel#sidebarLabel {
        color: #00f5ff;
        font-weight: 600;
        font-size: 12pt;
        padding: 16px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Chat Header Styling - Glassmorphism */
    ChatHeader {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(255, 255, 255, 0.05),
            stop:1 rgba(255, 255, 255, 0.02));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        backdrop-filter: blur(20px);
        margin: 8px;
        padding: 10px 15px;
    }

    QLabel#chatHeaderLabel {
        color: #00f5ff;
        font-weight: 500;
        font-size: 10pt;
        padding: 5px 10px;
        background: rgba(0, 245, 255, 0.1);
        border-radius: 8px;
    }

    /* Chat Message Bubbles */
    .user-message, .assistant-message, .computer-message, .error-message, .unknown-message {
        padding: 12px 18px;
        border-radius: 18px;
        margin-bottom: 10px;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 10.5pt;
        line-height: 1.5;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .user-message {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #8b5cf6, stop:1 #a855f7);
        color: #ffffff;
        margin-left: auto; /* Align to right */
        border-bottom-right-radius: 4px;
    }

    .assistant-message {
        background: rgba(255, 255, 255, 0.08);
        color: #f8f9fa;
        margin-right: auto; /* Align to left */
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom-left-radius: 4px;
    }

    .computer-message {
        background: rgba(0, 245, 255, 0.15);
        color: #e0e0e0;
        margin-right: auto;
        border: 1px solid rgba(0, 245, 255, 0.2);
        border-bottom-left-radius: 4px;
    }

    .error-message {
        background: rgba(255, 99, 71, 0.15);
        color: #ff6347;
        margin-right: auto;
        border: 1px solid rgba(255, 99, 71, 0.2);
        border-bottom-left-radius: 4px;
    }

    .unknown-message {
        background: rgba(255, 255, 0, 0.1);
        color: #ffff00;
        margin-right: auto;
        border: 1px solid rgba(255, 255, 0, 0.2);
        border-bottom-left-radius: 4px;
    }

    /* Code blocks within messages */
    .user-message pre, .assistant-message pre, .computer-message pre {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 8px;
        padding: 10px;
        overflow-x: auto;
        margin-top: 10px;
    }

    .user-message code, .assistant-message code, .computer-message code {
        font-family: "JetBrains Mono", "Fira Code", monospace;
        font-size: 9.5pt;
        line-height: 1.4;
    }

    /* Markdown elements within messages */
    .user-message h1, .assistant-message h1, .computer-message h1 { color: inherit; font-size: 1.5em; margin-top: 0.8em; margin-bottom: 0.4em; }
    .user-message h2, .assistant-message h2, .computer-message h2 { color: inherit; font-size: 1.3em; margin-top: 0.7em; margin-bottom: 0.3em; }
    .user-message h3, .assistant-message h3, .computer-message h3 { color: inherit; font-size: 1.1em; margin-top: 0.6em; margin-bottom: 0.2em; }
    .user-message strong, .assistant-message strong, .computer-message strong { font-weight: bold; }
    .user-message em, .assistant-message em, .computer-message em { font-style: italic; }
    .user-message ul, .assistant-message ul, .computer-message ul, .user-message ol, .assistant-message ol, .computer-message ol { margin-left: 20px; padding-left: 0; }
    .user-message li, .assistant-message li, .computer-message li { margin-bottom: 5px; }
    .user-message a, .assistant-message a, .computer-message a { color: #00f5ff; text-decoration: underline; }
    .user-message blockquote, .assistant-message blockquote, .computer-message blockquote {
        border-left: 4px solid rgba(255, 255, 255, 0.3);
        padding-left: 10px;
        margin-left: 0;
        font-style: italic;
        color: rgba(255, 255, 255, 0.7);
    }
    
    QListWidget {
        background: transparent;
        color: #f8f9fa;
        border: none;
        padding: 12px;
        outline: none;
    }
    
    QListWidget::item {
        padding: 14px 16px;
        border-radius: 12px;
        margin-bottom: 4px;
        font-weight: 450;
        font-size: 10.5pt;
        transition: all 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    QListWidget::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #8b5cf6, stop:1 #a855f7);
        color: #ffffff;
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }
    
    QListWidget::item:hover {
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Primary action buttons */
    QPushButton {
        background: rgba(255, 255, 255, 0.06);
        color: #f8f9fa;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: 500;
        font-size: 10pt;
        transition: all 150ms ease;
    }
    
    /* Dialog buttons (more prominent) */
    QDialog QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #8b5cf6, stop:1 #a855f7);
        color: #ffffff;
        border: none;
        padding: 10px 16px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 10pt;
        box-shadow: 0 2px 8px rgba(139, 92, 246, 0.2);
    }
    
    QPushButton:hover {
        background: rgba(255, 255, 255, 0.10);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    QPushButton:pressed {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 255, 255, 0.15);
    }
    
    QDialog QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #7a4cd5, stop:1 #9744e6);
        box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
    }
    
    QDialog QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #693bb4, stop:1 #8633c5);
        box-shadow: 0 1px 4px rgba(139, 92, 246, 0.15);
    }
    
    QPushButton:disabled {
        background: rgba(255, 255, 255, 0.05);
        color: rgba(255, 255, 255, 0.3);
        box-shadow: none;
    }
    
    /* Compact buttons for toolbars and menus */
    QPushButton[objectName*="compact"], QPushButton[objectName*="icon"] {
        padding: 6px 8px;
        min-width: 24px;
        min-height: 24px;
        border-radius: 4px;
        font-size: 9pt;
    }
    
    /* Send button style (like ChatGPT) */
    QPushButton[objectName*="send"] {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #8b5cf6, stop:1 #a855f7);
        color: #ffffff;
        border: none;
        padding: 8px 12px;
        border-radius: 6px;
        font-weight: 600;
        min-width: 60px;
    }
    
    QPushButton[objectName*="send"]:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #7a4cd5, stop:1 #9744e6);
    }
    
    QTextEdit#chatOutputDisplay {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(0, 0, 0, 0.3),
            stop:1 rgba(0, 0, 0, 0.1));
        color: #f8f9fa;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 24px;
        font-family: "JetBrains Mono", "Fira Code", "Menlo", "Consolas", monospace;
        font-size: 11pt;
        font-weight: 400;
        line-height: 1.6;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        selection-background-color: rgba(139, 92, 246, 0.3);
    }
    
    QTextEdit QScrollBar:vertical {
        border: none;
        background: transparent;
        width: 8px;
        margin: 4px;
    }
    
    QTextEdit QScrollBar::handle:vertical {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #8b5cf6, stop:1 #a855f7);
        min-height: 40px;
        border-radius: 4px;
        opacity: 0.7;
    }
    
    QTextEdit QScrollBar::handle:vertical:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #7c3aed, stop:1 #9333ea);
        opacity: 1.0;
    }
    
    QTextEdit QScrollBar::add-line:vertical, QTextEdit QScrollBar::sub-line:vertical {
        background: none;
        border: none;
    }
    
    QTextEdit QScrollBar::add-page:vertical, QTextEdit QScrollBar::sub-page:vertical {
        background: transparent;
    }
    
    QLineEdit#chatInputField, QDialog QLineEdit {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(255, 255, 255, 0.08),
            stop:1 rgba(255, 255, 255, 0.03));
        color: #f8f9fa;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 16px 20px;
        font-size: 11pt;
        font-weight: 400;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        transition: all 200ms cubic-bezier(0.25, 0.46, 0.45, 0.94);
        selection-background-color: rgba(139, 92, 246, 0.3);
    }
    
    QLineEdit#chatInputField:focus, QDialog QLineEdit:focus {
        border: 2px solid #00f5ff;
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(255, 255, 255, 0.12),
            stop:1 rgba(255, 255, 255, 0.06));
        box-shadow: 0 0 0 3px rgba(0, 245, 255, 0.1);
    }
    
    QMenuBar {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(255, 255, 255, 0.05),
            stop:1 rgba(255, 255, 255, 0.02));
        color: #f8f9fa;
        border: none;
        border-radius: 8px;
        padding: 4px;
        font-weight: 500;
    }
    
    QMenuBar::item {
        padding: 8px 16px;
        border-radius: 8px;
        margin: 2px;
    }
    
    QMenuBar::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #8b5cf6, stop:1 #a855f7);
    }
    
    QMenu {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(10, 10, 15, 0.95),
            stop:1 rgba(26, 26, 46, 0.95));
        color: #f8f9fa;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 8px;
        backdrop-filter: blur(20px);
    }
    
    QMenu::item {
        padding: 10px 16px;
        border-radius: 8px;
        margin: 2px;
    }
    
    QMenu::item:selected {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #8b5cf6, stop:1 #a855f7);
    }
    
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(10, 10, 15, 0.95),
            stop:1 rgba(26, 26, 46, 0.95));
        color: #f8f9fa;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        backdrop-filter: blur(30px);
    }
    
    QDialog QLabel {
        color: #f8f9fa;
        font-weight: 450;
    }
    
    QDialog QCheckBox {
        color: #f8f9fa;
        font-weight: 450;
        spacing: 8px;
    }
    
    QDialog QCheckBox::indicator {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        background: transparent;
    }
    
    QDialog QCheckBox::indicator:checked {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #8b5cf6, stop:1 #a855f7);
        border: 2px solid #8b5cf6;
    }
    
    QComboBox {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(255, 255, 255, 0.08),
            stop:1 rgba(255, 255, 255, 0.03));
        color: #f8f9fa;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 12px 16px;
        border-radius: 12px;
        font-weight: 450;
        backdrop-filter: blur(10px);
    }
    
    QComboBox:hover {
        border: 1px solid rgba(255, 255, 255, 0.2);
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(255, 255, 255, 0.12),
            stop:1 rgba(255, 255, 255, 0.06));
    }
    
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 30px;
        border: none;
        border-radius: 0;
    }
    
    QComboBox::down-arrow {
        width: 12px;
        height: 8px;
        background: #f8f9fa;
    }
    
    QComboBox QAbstractItemView {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(10, 10, 15, 0.95),
            stop:1 rgba(26, 26, 46, 0.95));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 8px;
        backdrop-filter: blur(20px);
        selection-background-color: rgba(139, 92, 246, 0.3);
    }
    
    /* Coming Soon Labels */
    QLabel#coming-soon {
        color: rgba(255, 255, 255, 0.5);
        font-style: italic;
        font-weight: 300;
        font-size: 9pt;
    }
    
    /* Collapsible Section Headers */
    QToolButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(255, 255, 255, 0.05),
            stop:1 rgba(255, 255, 255, 0.02));
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 600;
        font-size: 10pt;
        color: #f8f9fa;
        text-align: left;
    }
    
    QToolButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(255, 255, 255, 0.08),
            stop:1 rgba(255, 255, 255, 0.04));
    }
    
    /* Tooltips */
    QToolTip {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 rgba(10, 10, 15, 0.95),
            stop:1 rgba(26, 26, 46, 0.95));
        color: #f8f9fa;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 8px 12px;
        font-size: 10pt;
        backdrop-filter: blur(20px);
    }
"""