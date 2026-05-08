"""
AlphaPIL - An asynchronous, template-based image generation engine.

This package provides a powerful recursive parser for handling nested functions
in image generation templates, with support for asynchronous operations.
"""

__version__ = "0.1.6"
__author__ = "MeraLabs"

from .engine import CanvasEngine
from .interpreter import CanvasInterpreter
from .modules import AlphaMixin, ShapesMixin, TextMixin, ImagesMixin, UtilsMixin, MaskingMixin

__all__ = [
    "CanvasEngine", 
    "CanvasInterpreter", 
    "AlphaMixin", 
    "ShapesMixin", 
    "TextMixin", 
    "ImagesMixin",
    "UtilsMixin",
    "MaskingMixin"
]
