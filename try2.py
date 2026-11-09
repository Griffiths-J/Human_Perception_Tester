import customtkinter as ctk

# Application appearance
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Main application window
app = ctk.CTk()
app.title("Human Perception & Performance Tester")
app.geometry("900x600")
app.resizable(False, False)

# Main heading
heading = ctk.CTkLabel(
    app,
    text="Human Perception & Performance Tester",
    font=("Arial", 26, "bold")
)
heading.pack(pady=(30, 5))

# Introduction
subtitle = ctk.CTkLabel(
    app,
    text="Explore how visual design affects human performance.",
    font=("Arial", 14)
)
subtitle.pack(pady=5)

# Main content frame
main_frame = ctk.CTkFrame(app)
main_frame.pack(fill="both", expand=True, padx=40, pady=25)

# Dashboard heading
section_title = ctk.CTkLabel(
    main_frame,
    text="Select an Experiment",
    font=("Arial", 20, "bold")
)
section_title.pack(pady=25)

# Information label
info_label = ctk.CTkLabel(
    main_frame,
    text="Choose one of the experiments below to get started.",
    font=("Arial", 14)
)
info_label.pack(pady=10)


# Button functions
def identification_task():
    info_label.configure(
        text="Identification Task selected. Visual perception testing."
    )


def target_hitting_task():
    info_label.configure(
        text="Target Hitting Task selected. Fitts' Law testing."
    )


# Identification button
identification_button = ctk.CTkButton(
    main_frame,
    text="Identification Task",
    width=250,
    height=45,
    command=identification_task
)
identification_button.pack(pady=15)

# Target hitting button
target_button = ctk.CTkButton(
    main_frame,
    text="Target Hitting Task",
    width=250,
    height=45,
    command=target_hitting_task
)
target_button.pack(pady=15)

# Settings button
settings_button = ctk.CTkButton(
    main_frame,
    text="Visual Settings",
    width=250,
    height=45,
    fg_color="gray",
    hover_color="dimgray",
    command=lambda: info_label.configure(
        text="Visual Settings will be implemented next."
    )
)
settings_button.pack(pady=15)

# Run application
app.mainloop()