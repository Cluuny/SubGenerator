import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading


class SubtitleView:
    def __init__(self, root, controller):
        """
        Initialize the GUI.

        :param root: The root Tkinter window.
        :param controller: The controller instance to interact with the business logic.
        """
        self.root = root
        self.controller = controller

        # Configure the root window
        ctk.set_appearance_mode("dark")  # Modes: "dark", "light", "system"
        ctk.set_default_color_theme("green")  # Themes: "blue", "green", "dark-blue"

        self.root.title("MP4 Subtitle Generator")
        self.root.geometry("800x350")
        self.root.resizable(False, False)
        self.root.minsize(800, 350)
        self.root.maxsize(800, 350)
        self.root.update_idletasks()

        self.folder_path = ctk.StringVar()
        self.language = ctk.StringVar(value="English")

        self._setup_widgets()

    def _setup_widgets(self):
        """
        Setup all the widgets for the GUI.
        """
        # Main frame
        main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Title label
        title_label = ctk.CTkLabel(
            main_frame,
            text="MP4 Subtitle Generator",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.pack(pady=(10, 20))

        # Folder selection
        folder_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        folder_frame.pack(fill="x", pady=10, padx=20)

        ctk.CTkLabel(
            folder_frame, text="Select Folder:", font=("Arial", 14), anchor="w"
        ).grid(column=0, row=0, sticky="w", padx=15, pady=15)
        folder_entry = ctk.CTkEntry(
            folder_frame, textvariable=self.folder_path, width=400
        )
        folder_entry.grid(column=1, row=0, padx=10)
        ctk.CTkButton(folder_frame, text="Browse", command=self._browse_folder).grid(
            column=2, row=0, padx=15
        )

        # Language selection
        language_frame = ctk.CTkFrame(main_frame, corner_radius=15)
        language_frame.pack(fill="x", pady=10, padx=20)

        ctk.CTkLabel(
            language_frame, text="Language Code:", font=("Arial", 14), anchor="w"
        ).grid(column=0, row=0, sticky="w", padx=15, pady=15)

        # Create the OptionMenu for language selection
        language_options = ["English", "Spanish", "French"]
        language_menu = ctk.CTkOptionMenu(
            language_frame, variable=self.language, values=language_options
        )
        language_menu.grid(column=1, row=0, padx=10)

        # Start button
        start_button = ctk.CTkButton(
            main_frame,
            text="Start",
            command=self._start_subtitle_generation,
            font=("Arial", 16, "bold"),
            corner_radius=10,
        )
        start_button.pack(pady=25)

    def _browse_folder(self):
        """
        Open a folder dialog to select a folder.
        """
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def _start_subtitle_generation(self):
        """
        Start the subtitle generation process.
        """
        folder = self.folder_path.get()
        language = self.language.get()

        if not folder:
            self.show_error("Error", "Please select a folder.")
            return

        if not language:
            self.show_error("Error", "Please enter a language code.")
            return

        self.controller.start_subtitle_generation(folder, language)

    def update_progress(self, current, total, file_name):
        """
        Update the progress bar and label.

        :param current: Current progress count.
        :param total: Total number of files to process.
        :param file_name: Name of the file being processed.
        """
        progress = current / total
        self.progress_bar.set(progress)
        self.progress_label.configure(
            text=f"Processing {current}/{total}: {file_name}",
        )
        self._log_message(f"Processing: {file_name}")

    def _log_message(self, message):
        """
        Append a message to the log section.

        :param message: The message to append.
        """
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")

    def start_thread(self, target_function, *args):
        """
        Start a new thread to run the specified target function.

        :param target_function: The function to execute in the thread.
        :param args: Arguments to pass to the target function.
        """
        thread = threading.Thread(target=target_function, args=args)
        thread.daemon = True  # Ensures the thread exits when the main program exits
        thread.start()

    def show_message(self, title, message):
        """
        Show an information message box.

        :param title: Title of the message box.
        :param message: Message content.
        """
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        """
        Show an error message box.

        :param title: Title of the message box.
        :param message: Error content.
        """
        messagebox.showerror(title, message)
