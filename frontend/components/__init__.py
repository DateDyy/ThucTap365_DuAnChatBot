# File này giúp Python nhận diện thư mục components là một package
# Cho phép import các module từ package này

from .chat_box import ChatBox
from .sidebar import Sidebar

__all__ = ['ChatBox', 'Sidebar']