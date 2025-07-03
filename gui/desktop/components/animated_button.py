"""
Animated button component with hover effects and smooth transitions.
"""

from PySide6.QtWidgets import QPushButton
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QRect
from PySide6.QtGui import QColor, QPalette

class AnimatedButton(QPushButton):
    """A button with smooth hover animations and color transitions."""
    
    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # Remove color animation for now (requires custom property)
        # self._color_animation = QPropertyAnimation(self, b"color") 
        # self._color_animation.setDuration(200)
        
        # Store original geometry
        self._original_geometry = None
        
        # Default colors
        self._normal_color = QColor("#8A2BE2")  # Magic Unicorn Purple
        self._hover_color = QColor("#6A1BA0")   # Darker purple
        self._pressed_color = QColor("#4A0F70") # Even darker
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._normal_color.name()};
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                transition: all 0.2s ease-in-out;
            }}
            QPushButton:hover {{
                background-color: {self._hover_color.name()};
                transform: translateY(-2px);
            }}
            QPushButton:pressed {{
                background-color: {self._pressed_color.name()};
                transform: translateY(0px);
            }}
        """)
    
    def enterEvent(self, event):
        """Animate button on mouse enter."""
        super().enterEvent(event)
        if self._original_geometry is None:
            self._original_geometry = self.geometry()
        
        # Lift effect
        new_geometry = QRect(self._original_geometry)
        new_geometry.moveTop(new_geometry.top() - 2)
        
        self._animation.setStartValue(self.geometry())
        self._animation.setEndValue(new_geometry)
        self._animation.start()
    
    def leaveEvent(self, event):
        """Animate button on mouse leave."""
        super().leaveEvent(event)
        if self._original_geometry:
            self._animation.setStartValue(self.geometry())
            self._animation.setEndValue(self._original_geometry)
            self._animation.start()
    
    def mousePressEvent(self, event):
        """Handle mouse press with animation."""
        super().mousePressEvent(event)
        if self._original_geometry:
            # Return to original position on press
            self._animation.setStartValue(self.geometry())
            self._animation.setEndValue(self._original_geometry)
            self._animation.start()
    
    def set_colors(self, normal, hover, pressed):
        """Set custom colors for the button states."""
        self._normal_color = QColor(normal)
        self._hover_color = QColor(hover)
        self._pressed_color = QColor(pressed)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._normal_color.name()};
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                transition: all 0.2s ease-in-out;
            }}
            QPushButton:hover {{
                background-color: {self._hover_color.name()};
            }}
            QPushButton:pressed {{
                background-color: {self._pressed_color.name()};
            }}
        """)