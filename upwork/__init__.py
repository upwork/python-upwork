"""Top-level package for python-upwork."""

from upwork.config import Config
from upwork.client import Client
from . import routers

__author__ = """Maksym Novozhylov"""
__email__ = "mnovozhilov@upwork.com"
__version__ = "2.0.0"

__all__ = ("Config", "Client", "routers")
