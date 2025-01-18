import logging
import threading
from tkinter.scrolledtext import ScrolledText
import customtkinter as ctk
from tkinter import filedialog, messagebox


class LoggingHandler(logging.Handler):
    """
    Custom handler to redirect logging messages
    to the text widget in the GUI, with colors based on the log level.
    """

    def __init__(self, log_widget):
        super().__init__()
        self.log_widget = log_widget

    def emit(self, record):
        log_entry = self.format(record) + "\n"
        self.log_widget.configure(state="normal")  # Temporarily enable editing

        # Configure colors based on log level
        level_colors = {
            logging.INFO: "green",
            logging.WARNING: "orange",
            logging.ERROR: "red",
        }
        color = level_colors.get(record.levelno, "white")  # Default color

        # Insert formatted text
        self.log_widget.insert("end", log_entry, record.levelname)
        self.log_widget.tag_config(record.levelname, foreground=color)

        # Auto-scroll to the end
        self.log_widget.see("end")
        self.log_widget.configure(state="disabled")  # Disable editing


class SubtitleView:
    """
    Class representing the view in the MVC pattern for a subtitle generation application.
    Manages the user interface and user interactions.
    """

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # Initial GUI configuration
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")
        self.root.title("MP4 Subtitle Generator")

        # GUI variables
        self.folder_path = ctk.StringVar()
        self.language = ctk.StringVar(value="English")

        # Widget and logging configuration
        self._setup_widgets()
        self._setup_logging()

    def _setup_widgets(self):
        """
        Configures all the widgets in the user interface.
        """
        # Main frame
        main_frame = ctk.CTkFrame(self.root, corner_radius=20)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="MP4 Subtitle Generator",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title_label.pack(pady=(10, 20))

        # Folder selection
        self._create_folder_selection(main_frame)

        # Language selection
        self._create_language_selection(main_frame)

        # Start button
        ctk.CTkButton(
            main_frame, text="Start", command=self._start_subtitle_generation
        ).pack(pady=20)

        # Log window
        self.log_text = ScrolledText(
            main_frame,
            height=10,
            state="disabled",
            wrap="word",
            bg="black",  # Black background
            fg="white",  # Default white text
        )
        self.log_text.pack(fill="both", padx=10, pady=(10, 20))

    def _create_folder_selection(self, parent):
        """
        Creates the frame and widgets for folder selection.
        """
        folder_frame = ctk.CTkFrame(parent, corner_radius=15)
        folder_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(folder_frame, text="Select Folder:").grid(
            column=0, row=0, padx=10, pady=10
        )
        ctk.CTkEntry(folder_frame, textvariable=self.folder_path, width=400).grid(
            column=1, row=0, padx=10
        )
        ctk.CTkButton(folder_frame, text="Browse", command=self._browse_folder).grid(
            column=2, row=0, padx=10
        )

    def _create_language_selection(self, parent):
        """
        Creates the frame and widgets for language selection.
        """
        language_frame = ctk.CTkFrame(parent, corner_radius=15)
        language_frame.pack(fill="x", pady=10, padx=10)
        ctk.CTkLabel(language_frame, text="Language Code:").grid(
            column=0, row=0, padx=10, pady=10
        )
        ctk.CTkOptionMenu(
            language_frame,
            variable=self.language,
            values=["English", "Spanish", "French"],
        ).grid(column=1, row=0, padx=10)

    def _setup_logging(self):
        """
        Configures the logging system to redirect logs to the text widget.
        """
        handler = LoggingHandler(self.log_text)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        logging.getLogger().addHandler(handler)
        logging.getLogger().setLevel(logging.INFO)

    def start_thread(self, target_function, *args):
        """
        Starts a thread to execute a target function with the given arguments.
        """
        thread = threading.Thread(target=target_function, args=args)
        thread.daemon = True  # Allow the thread to terminate with the application
        thread.start()

    def _browse_folder(self):
        """
        Opens a dialog to select a folder.
        """
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def _start_subtitle_generation(self):
        """
        Validates user input and calls the controller to start subtitle generation.
        """
        folder = self.folder_path.get()
        language = self.language.get()

        # Input validations
        if not folder:
            self.show_error("Error", "Please select a folder.")
            return
        if not language:
            self.show_error("Error", "Please select a language.")
            return

        # Call the controller to start the process
        self.controller.start_subtitle_generation(folder, language)

    def show_error(self, title, message):
        """
        Displays an error dialog.
        """
        messagebox.showerror(title, message)


if __name__ == "__main__":
    # Initial application setup
    root = ctk.CTk()

    # The actual controller should be implemented and passed here
    app = SubtitleView(root, None)  # Replace None with the controller

    root.mainloop()
