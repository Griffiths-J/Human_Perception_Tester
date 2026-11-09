import customtkinter as ctk

# Configure appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Create application window
app = ctk.CTk()

# Window properties
app.title("Human Perception & Performance Tester")
app.geometry("800x500")

# Create heading
heading = ctk.CTkLabel(
    app,
    text="Human Perception & Performance Tester",
    font=("Arial", 24, "bold")
)

heading.pack(pady=40)

# Create a welcome message
message = ctk.CTkLabel(
    app,
    text="Welcome to our HCI testing application!",
    font=("Arial", 16)
)

message.pack(pady=50)

# Run application
app.mainloop()