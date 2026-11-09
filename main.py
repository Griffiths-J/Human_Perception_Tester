import tkinter as tk
from datetime import datetime

import customtkinter as ctk

if __package__:
    from .data_logging import CSV_FILE, create_csv
    from .identification_task import IdentificationTaskMixin
    from .target_hitting_task import TargetHittingTaskMixin
    from .visual_settings import VisualSettingsMixin
else:
    from data_logging import CSV_FILE, create_csv
    from identification_task import IdentificationTaskMixin
    from target_hitting_task import TargetHittingTaskMixin
    from visual_settings import VisualSettingsMixin


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class HumanPerformanceTester(
    VisualSettingsMixin,
    IdentificationTaskMixin,
    TargetHittingTaskMixin,
    ctk.CTk
):

    def __init__(self):

        super().__init__()

        self.title("Human Perception & Performance Tester")

        self.geometry("1000x720")

        self.minsize(900, 650)

        self.contrast = "Medium"
        self.size = "Medium"
        self.brightness = 80

        self.participant_id = tk.StringVar(self)

        self.current_frame = None

        self.show_dashboard()


    def clear_page(self):

        if self.current_frame is not None:

            self.current_frame.destroy()

        self.current_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.current_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )


    def title_block(self, title, subtitle):

        ctk.CTkLabel(
            self.current_frame,
            text=title,
            font=("Arial", 27, "bold")
        ).pack(pady=(10, 5))

        ctk.CTkLabel(
            self.current_frame,
            text=subtitle,
            font=("Arial", 14)
        ).pack(pady=(0, 15))


    def get_visual_condition(self):

        return (
            f"Contrast={self.contrast}; "
            f"Size={self.size}; "
            f"Brightness={self.brightness}%"
        )


    def get_font_size(self, original_size=16):

        sizes = {
            "Small": 0.8,
            "Medium": 1.0,
            "Large": 1.3
        }

        return int(original_size * sizes[self.size])


    def get_visual_colors(self):

        shade = int(
            35 + (self.brightness / 100) * 210
        )

        background = (
            f"#{shade:02x}{shade:02x}{shade:02x}"
        )

        if self.contrast == "High":

            difference = 190

            text_color = (
                "#111111" if shade >= 128 else "#FFFFFF"
            )

        elif self.contrast == "Medium":

            difference = 105

            text_color = (
                "#555555" if shade >= 128 else "#C8C8C8"
            )

        else:

            difference = 38

            text_color = (
                "#999999" if shade >= 128 else "#777777"
            )

        if shade >= 128:

            target_shade = max(0, shade - difference)

        else:

            target_shade = min(255, shade + difference)

        target_color = (
            f"#{target_shade:02x}"
            f"{target_shade:02x}"
            f"{target_shade:02x}"
        )

        return background, text_color, target_color


    def rating_control(self, parent):

        rating_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )

        rating_frame.pack(pady=8)

        ctk.CTkLabel(
            rating_frame,
            text="Ease of use (1 = Difficult, 5 = Easy):"
        ).pack(side="left", padx=5)

        rating = ctk.CTkOptionMenu(
            rating_frame,
            values=["1", "2", "3", "4", "5"],
            width=75
        )

        rating.set("3")

        rating.pack(side="left", padx=5)

        return rating


    def create_result(
        self,
        task,
        elapsed,
        rating,
        response="",
        target_size="",
        distance="",
        trial=""
    ):

        return {
            "timestamp": datetime.now().isoformat(
                timespec="seconds"
            ),
            "participant_id": self.participant_id.get().strip(),
            "visual_condition": self.get_visual_condition(),
            "contrast_level": self.contrast,
            "size_level": self.size,
            "brightness_percent": self.brightness,
            "task_type": task,
            "time_taken_seconds": round(elapsed, 3),
            "ease_of_use_rating": rating,
            "identification_response": response,
            "target_size_px": target_size,
            "target_distance_px": distance,
            "trial_number": trial
        }


    def show_dashboard(self):

        self.clear_page()

        self.title_block(
            "Human Perception & Performance Tester",
            "Explore how visual design affects human performance."
        )

        dashboard = ctk.CTkFrame(
            self.current_frame
        )

        dashboard.pack(
            fill="both",
            expand=True,
            padx=55,
            pady=10
        )

        ctk.CTkLabel(
            dashboard,
            text="Select an Experiment",
            font=("Arial", 21, "bold")
        ).pack(pady=(30, 10))

        ctk.CTkLabel(
            dashboard,
            text="Choose an experiment or adjust your visual settings.",
            font=("Arial", 14)
        ).pack(pady=5)

        ctk.CTkLabel(
            dashboard,
            text="Anonymous participant ID (use the same ID for each task):",
            font=("Arial", 12)
        ).pack(pady=(12, 3))

        ctk.CTkEntry(
            dashboard,
            textvariable=self.participant_id,
            width=280,
            placeholder_text="For example, P01"
        ).pack(pady=3)

        self.dashboard_status = ctk.CTkLabel(
            dashboard,
            text="Do not enter participant names.",
            font=("Arial", 11)
        )

        self.dashboard_status.pack(pady=(2, 5))

        ctk.CTkButton(
            dashboard,
            text="Identification Task",
            width=280,
            height=48,
            command=self.begin_identification
        ).pack(pady=12)

        ctk.CTkButton(
            dashboard,
            text="Target Hitting Task (Fitts' Law)",
            width=280,
            height=48,
            command=self.begin_fitts
        ).pack(pady=12)

        ctk.CTkButton(
            dashboard,
            text="Visual Settings",
            width=280,
            height=48,
            fg_color="gray",
            hover_color="dimgray",
            command=self.show_settings
        ).pack(pady=12)

        ctk.CTkLabel(
            dashboard,
            text=f"Current settings: {self.get_visual_condition()}",
            font=("Arial", 12)
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            dashboard,
            text=f"Results are saved automatically in {CSV_FILE.name}",
            font=("Arial", 11)
        ).pack(pady=5)


    def require_participant_id(self):

        participant_id = self.participant_id.get().strip()

        if not participant_id:

            self.dashboard_status.configure(
                text="Enter an anonymous participant ID before starting a task."
            )

            return False

        self.participant_id.set(participant_id)

        return True


    def begin_identification(self):

        if self.require_participant_id():

            self.show_identification()


    def begin_fitts(self):

        if self.require_participant_id():

            self.start_fitts()


if __name__ == "__main__":

    create_csv()

    app = HumanPerformanceTester()

    app.mainloop()
