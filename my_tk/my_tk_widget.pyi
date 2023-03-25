import tkinter as tk
from typing import Any, Literal,  overload
from tkinter import _Color

@overload
class Scrollbar(tk.Frame):
    def __init__(
        self,
        master: tk.Misc | None = None,
        cnf: dict[str, Any] | None = ...,
        *,
        activebackground: _Color = ...,
        activeforeground: _Color = ...,
        anchor: Any = ...,
        background: Any = ...,
        bd: Any = ...,  # same as borderwidth
        bg: Any = ...,  # same as background
        bitmap: Any = ...,
        border: Any = ...,  # same as borderwidth
        borderwidth: Any = ...,
        command: Any = ...,
        compound: Any = ...,
        cursor: Any = ...,
        default: Literal["normal", "active", "disabled"] = ...,
        disabledforeground: Any = ...,
        fg: Any = ...,  # same as foreground
        font: Any = ...,
        foreground: Any = ...,
        # width and height must be int for buttons containing just text, but
        # ints are also valid _ScreenUnits
        height: Any = ...,
        highlightbackground: Any = ...,
        highlightcolor: Any = ...,
        highlightthickness: Any = ...,
        image: Any = ...,
        justify: Literal["left", "center", "right"] = ...,
        name: str = ...,
        overrelief: Any = ...,
        padx: Any = ...,
        pady: Any = ...,
        relief: Any = ...,
        repeatdelay: int = ...,
        repeatinterval: int = ...,
        state: Literal["normal", "active", "disabled"] = ...,
        takefocus: Any = ...,
        text: float | str = ...,
        # We allow the textvariable to be any Variable, not necessarily
        # StringVar. This is useful for e.g. a button that displays the value
        # of an IntVar.
        textvariable: Any = ...,
        underline: int = ...,
        width: Any = ...,
        wraplength: Any = ...,
    ) -> None: ...