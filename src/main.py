import os
import sys
from controller.controller import SubtitleController
from view.cli_view import print_message, print_error
from tkinter import Tk
from view.gui_view import SubtitleView
import ctypes
import customtkinter as ctk


def cli_main():
    """
    Entry point for the Command Line Interface (CLI).
    """
    input_file = os.path.join(os.path.dirname(__file__), "videos.txt")
    subtitles_dir = "sub"
    language = "English"
    exclude_files = ["videos.txt", "requirements.txt"]

    try:
        # Leer directorios desde el archivo de entrada
        with open(input_file, "r") as file:
            directories = [
                line.strip().strip('"').strip("'") for line in file if line.strip()
            ]

        # Crear una instancia del controlador
        controller = SubtitleController(
            view=None, subtitles_dir=subtitles_dir, exclude_files=exclude_files
        )

        # Procesar videos y limpiar archivos
        print_message("Processing videos...")
        for folder in directories:
            controller.start_subtitle_generation(folder, language)
        print_message("All tasks completed successfully.")
    except FileNotFoundError:
        print_error(f"Input file '{input_file}' not found.")
    except Exception as e:
        print_error(f"An error occurred: {e}")


def gui_main():
    """
    Entry point for the Graphical User Interface (GUI).
    """
    subtitles_dir = "sub"
    exclude_files = ["videos.txt", "requirements.txt"]

    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(
            1
        )  # Habilitar DPI-aware (Modo Per-Monitor v2)
    except Exception:
        pass

    # Inicializar la ventana principal de Tkinter
    root = ctk.CTk()

    # Escalado para HiDPI (CustomTkinter)
    ctk.set_widget_scaling(
        1
    )  # Ajusta el tamaño de los widgets (1.0 = normal, 1.2 = más grande)
    ctk.set_window_scaling(1)  # Escala también el tamaño de la ventan

    # Crear una instancia del controlador
    controller = SubtitleController(
        view=None, subtitles_dir=subtitles_dir, exclude_files=exclude_files
    )

    # Crear una instancia de la vista y pasarle el controlador
    app = SubtitleView(root, controller)

    # Conectar la vista con el controlador
    controller.view = app

    # Ejecutar el bucle principal de la GUI
    root.mainloop()


def main():
    """
    Main function to choose between CLI and GUI.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        cli_main()
    else:
        gui_main()


if __name__ == "__main__":
    main()
