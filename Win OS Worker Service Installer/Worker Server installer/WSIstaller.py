from tkinter import Tk, ttk, filedialog
import subprocess

def select_folder():
    """Open a folder dialog and set the selected folder path."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        path_entry.delete(0, "end")  # Clear any existing text in the entry
        path_entry.insert(0, folder_selected)  # Insert the selected folder path

def install_service():
    """Install the worker service as a Windows service."""
    service_path = path_entry.get().strip()
    service_name = service_name_entry.get().strip()

    # Clear any previous message
    message_label.config(text="", foreground="black")

    # Validate inputs
    if not service_path or not service_name:
        message_label.config(text="Error: Both fields are required!", foreground="red")
        return

    # Simulate progress bar
    progress_bar.start(10)

    # Construct the command to install the service
    command = f'sc create "{service_name}" binPath= "{service_path}" start= auto'

    try:
        # Execute the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        progress_bar.stop()  # Stop progress bar

        # Check the result
        if result.returncode == 0:
            message_label.config(text=f"Service '{service_name}' installed successfully!", foreground="green")
        else:
            # Display detailed error information
            error_message = (
                f"Failed to install service.\n"
                f"Command: {command}\n"
                f"Error Code: {result.returncode}\n"
                f"Output: {result.stderr.strip() or 'No detailed error information available.'}"
            )
            message_label.config(text=error_message, foreground="red", wraplength=550, justify="left")
    except Exception as e:
        progress_bar.stop()  # Stop progress bar
        message_label.config(text=f"An unexpected error occurred:\n{e}", foreground="red")

# Create the app's main window
root = Tk()
root.title("Worker-Service Installer")
root.geometry("600x400")
root.resizable(False, False)

# Set the background color
root.configure(bg="#1E1E2F")  # Light blue-black color

# Set the app icon
root.iconbitmap("app_icon.ico")  # Make sure the .ico file is in the same directory or provide the full path

# Style configuration
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), background="#1E1E2F", foreground="white")
style.configure("TEntry", font=("Arial", 11), fieldbackground="white", foreground="black")
style.configure("TButton", font=("Arial", 11, "bold"), padding=5)
style.configure("TFrame", background="#1E1E2F")

# Create the main content frame
content_frame = ttk.Frame(root, padding="10")
content_frame.pack(expand=True, fill="both")

# Add widgets
path_label = ttk.Label(content_frame, text="Published Path:")
path_label.grid(row=0, column=0, sticky="w", pady=5)

path_entry = ttk.Entry(content_frame, width=40)
path_entry.grid(row=0, column=1, padx=5, pady=5)

browse_button = ttk.Button(content_frame, text="Browse", command=select_folder)
browse_button.grid(row=0, column=2, padx=5, pady=5)

service_name_label = ttk.Label(content_frame, text="Service Name:")
service_name_label.grid(row=1, column=0, sticky="w", pady=5)

service_name_entry = ttk.Entry(content_frame, width=40)
service_name_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

install_button = ttk.Button(content_frame, text="Install Service", command=install_service)
install_button.grid(row=2, column=0, columnspan=3, pady=10)

# Add progress bar
progress_bar = ttk.Progressbar(content_frame, mode="indeterminate")
progress_bar.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")

# Add a message label
message_label = ttk.Label(content_frame, text="", font=("Arial", 10), anchor="center", justify="center", foreground="white", wraplength=550)
message_label.grid(row=4, column=0, columnspan=3, pady=10)

# Add footer
footer_label = ttk.Label(content_frame, text="Worker-Service Installer © 2024", font=("Arial", 9, "italic"), anchor="center", foreground="white")
footer_label.grid(row=5, column=0, columnspan=3, pady=5)

# Run the app's main loop
root.mainloop()
