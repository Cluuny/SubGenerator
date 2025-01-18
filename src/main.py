import os
import sys
from controller.controller import SubtitleController
from tkinter import Tk
from view.gui_view import SubtitleView
import ctypes
import customtkinter as ctk


def gui_main():
    """
    Entry point for the Graphical User Interface (GUI).
    """
    exclude_files = ["videos.txt", "requirements.txt"]

    try:
        # Enable DPI awareness (Per-Monitor v2 mode)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    # Initialize the main Tkinter window
    root = ctk.CTk()

    # Set initial window size and prevent resizing
    root.geometry("750x500")
    root.resizable(False, False)

    # Scaling adjustments for HiDPI displays (CustomTkinter)
    ctk.set_widget_scaling(1)  # Adjust widget scaling
    ctk.set_window_scaling(1)  # Adjust window scaling

    # Create an instance of the controller
    controller = SubtitleController(view=None, exclude_files=exclude_files)

    # Create an instance of the view and link it with the controller
    app = SubtitleView(root, controller)

    # Connect the view to the controller
    controller.view = app

    # Start the main GUI loop
    root.mainloop()


def main():
    """
    Main entry point for the application.
    """
    gui_main()


if __name__ == "__main__":
    main()
