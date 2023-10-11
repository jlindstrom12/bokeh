#-----------------------------------------------------------------------------
# Copyright (c) 2012 - 2023, Anaconda, Inc., and Bokeh Contributors.
# All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------
'''

'''

#-----------------------------------------------------------------------------
# Boilerplate
#-----------------------------------------------------------------------------
from __future__ import annotations

import logging # isort:skip
log = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

# Standard library imports
from typing import Any

# Bokeh imports
from ...core.enums import (
    AngleUnits,
    CoordinateUnits,
    TextAlign,
    VerticalAlign,
)
from ...core.has_props import abstract
from ...core.properties import (
    Angle,
    CoordinateLike,
    Enum,
    Float,
    Include,
    Override,
    Required,
    TextLike,
)
from ...core.property_mixins import ScalarFillProps, ScalarLineProps, ScalarTextProps
from ...util.deprecation import deprecated
from .. import glyphs
from ..renderers import GlyphRenderer
from .annotation import Annotation
from .common import build_glyph_renderer

#-----------------------------------------------------------------------------
# Globals and constants
#-----------------------------------------------------------------------------

__all__ = (
    "Label",
    "LabelSet",
    "Title",
    "TextAnnotation",
)

#-----------------------------------------------------------------------------
# General API
#-----------------------------------------------------------------------------

@abstract
class TextAnnotation(Annotation):
    ''' Base class for text annotation models such as labels and titles.

    '''

    # explicit __init__ to support Init signatures
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    text = TextLike(default="", help="""
    A text or LaTeX notation to render.
    """)

    text_props = Include(ScalarTextProps, help="""
    The {prop} values for the text.
    """)

    background_props = Include(ScalarFillProps, prefix="background", help="""
    The {prop} values for the text bounding box.
    """)

    background_fill_color = Override(default=None)

    border_props = Include(ScalarLineProps, prefix="border", help="""
    The {prop} values for the text bounding box.
    """)

    border_line_color = Override(default=None)

class Label(TextAnnotation):
    ''' Render a single text label as an annotation.

    ``Label`` will render a single text label at given ``x`` and ``y``
    coordinates, which can be in either screen (pixel) space, or data (axis
    range) space.

    The label can also be configured with a screen space offset from ``x`` and
    ``y``, by using the ``x_offset`` and ``y_offset`` properties.

    Additionally, the label can be rotated with the ``angle`` property.

    There are also standard text, fill, and line properties to control the
    appearance of the text, its background, as well as the rectangular bounding
    box border.

    See :ref:`ug_basic_annotations_labels` for information on plotting labels.

    '''

    # explicit __init__ to support Init signatures
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    x = Required(CoordinateLike, help="""
    The x-coordinate in screen coordinates to locate the text anchors.
    """)

    x_units = Enum(CoordinateUnits, default='data', help="""
    The unit type for the x attribute. Interpreted as |data units| by
    default.
    """)

    y = Required(CoordinateLike, help="""
    The y-coordinate in screen coordinates to locate the text anchors.
    """)

    y_units = Enum(CoordinateUnits, default='data', help="""
    The unit type for the y attribute. Interpreted as |data units| by
    default.
    """)

    angle = Angle(default=0, help="""
    The angle to rotate the text, as measured from the horizontal.
    """)

    angle_units = Enum(AngleUnits, default='rad', help="""
    Acceptable values for units are ``"rad"`` and ``"deg"``
    """)

    x_offset = Float(default=0, help="""
    Offset value to apply to the x-coordinate.

    This is useful, for instance, if it is desired to "float" text a fixed
    distance in |screen units| from a given data position.
    """)

    y_offset = Float(default=0, help="""
    Offset value to apply to the y-coordinate.

    This is useful, for instance, if it is desired to "float" text a fixed
    distance in |screen units| from a given data position.
    """)

class Title(TextAnnotation):
    ''' Render a single title box as an annotation.

    See :ref:`ug_basic_annotations_titles` for information on plotting titles.

    '''

    # explicit __init__ to support Init signatures
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    vertical_align = Enum(VerticalAlign, default='bottom', help="""
    Alignment of the text in its enclosing space, *across* the direction of the text.
    """)

    align = Enum(TextAlign, default='left', help="""
    Alignment of the text in its enclosing space, *along* the direction of the text.
    """)

    offset = Float(default=0, help="""
    Offset the text by a number of pixels (can be positive or negative). Shifts the text in
    different directions based on the location of the title:

        * above: shifts title right
        * right: shifts title down
        * below: shifts title right
        * left: shifts title up

    """)

    standoff = Float(default=10, help="""
    """)

    text_font_size = Override(default="13px")

    text_font_style = Override(default="bold")

    text_line_height = Override(default=1.0)

#-----------------------------------------------------------------------------
# Legacy API
#-----------------------------------------------------------------------------

def LabelSet(**kwargs: Any) -> GlyphRenderer:
    """ Render multiple text labels as annotations.

    .. note::
        This is a legacy API and will be removed at some point. Prefer using
        ``bokeh.glyphs.Text`` model or ``figure.text()`` method.

    """
    deprecated((3, 4, 0), "bokeh.annotations.LabelSet", "bokeh.glyphs.Text or figure.text()")

    if "y_offset" in kwargs:
        kwargs["y_offset"] = -kwargs["y_offset"]

    return build_glyph_renderer(glyphs.Text, kwargs)

#-----------------------------------------------------------------------------
# Dev API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Private API
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# Code
#-----------------------------------------------------------------------------
