import customtkinter as ctk
import tkinter as tk
import csv
import math
import random
import time
from pathlib import Path
from datetime import datetime


# ==========================================================
# 1. APPLICATION CONFIGURATION
# ==========================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

APP_FOLDER = Path(__file__).resolve().parent
CSV_FILE = APP_FOLDER / "experiment_results.csv"

CSV_COLUMNS = [
    "timestamp",
    "participant_id",
    "visual_condition",
    "contrast_level",
    "size_level",
    "brightness_percent",
    "task_type",
    "time_taken_seconds",
    "ease_of_use_rating",
    "identification_response",
    "target_size_px",
    "target_distance_px",
    "trial_number"
]


# ==========================================================
# 2. CSV DATA LOGGING
# ==========================================================

def create_csv():

    if not CSV_FILE.exists() or CSV_FILE.stat().st_size == 0:

        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=CSV_COLUMNS
            )

            writer.writeheader()

        return

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        existing_columns = reader.fieldnames or []

        if existing_columns == CSV_COLUMNS:

            return

        if not set(existing_columns).issubset(CSV_COLUMNS):

            raise ValueError(
                "The results CSV contains columns that this app does not recognize."
            )

        existing_results = list(reader)

    temporary_file = CSV_FILE.with_suffix(".csv.tmp")

    with open(temporary_file, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_COLUMNS
        )

        writer.writeheader()

        writer.writerows(existing_results)

    temporary_file.replace(CSV_FILE)


def save_result(result):

    create_csv()

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=CSV_COLUMNS
        )

        writer.writerow(result)


# ==========================================================
# 3. MAIN APPLICATION CLASS
# ==========================================================

class HumanPerformanceTester(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Human Perception & Performance Tester")

        self.geometry("1000x720")

        self.minsize(900, 650)

        # Default visual settings
        self.contrast = "Medium"
        self.size = "Medium"
        self.brightness = 80

        self.participant_id = tk.StringVar(self)

        self.current_frame = None

        self.show_dashboard()


    # ======================================================
    # GENERAL PAGE FUNCTIONS
    # ======================================================

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


    # ======================================================
    # 4. DASHBOARD
    # ======================================================

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


    # ======================================================
    # 5. VISUAL SETTINGS
    # ======================================================

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


    def show_settings(self):

        self.clear_page()

        self.title_block(
            "Visual Settings",
            "Adjust the visual conditions used in the experiments."
        )

        panel = ctk.CTkFrame(
            self.current_frame
        )

        panel.pack(
            fill="both",
            expand=True,
            padx=80,
            pady=5
        )

        background, text_color, _ = self.get_visual_colors()

        self.preview_frame = ctk.CTkFrame(
            panel,
            fg_color=background,
            height=105
        )

        self.preview_frame.pack(
            fill="x",
            padx=35,
            pady=(25, 15)
        )

        self.preview_frame.pack_propagate(False)

        self.preview_label = ctk.CTkLabel(
            self.preview_frame,
            text="Visual Preview: Sample Text",
            text_color=text_color,
            font=("Arial", self.get_font_size(20), "bold")
        )

        self.preview_label.pack(expand=True)

        # Contrast
        ctk.CTkLabel(
            panel,
            text="Contrast Level",
            font=("Arial", 14, "bold")
        ).pack(pady=(5, 3))

        contrast_menu = ctk.CTkOptionMenu(
            panel,
            values=["High", "Medium", "Low"],
            width=220,
            command=self.change_contrast
        )

        contrast_menu.set(self.contrast)

        contrast_menu.pack(pady=5)

        # Size
        ctk.CTkLabel(
            panel,
            text="Text / Icon Size",
            font=("Arial", 14, "bold")
        ).pack(pady=(10, 3))

        size_menu = ctk.CTkOptionMenu(
            panel,
            values=["Small", "Medium", "Large"],
            width=220,
            command=self.change_size
        )

        size_menu.set(self.size)

        size_menu.pack(pady=5)

        # Brightness
        self.brightness_label = ctk.CTkLabel(
            panel,
            text=f"Brightness: {self.brightness}%"
        )

        self.brightness_label.pack(pady=(15, 3))

        brightness_slider = ctk.CTkSlider(
            panel,
            from_=0,
            to=100,
            number_of_steps=100,
            width=320,
            command=self.change_brightness
        )

        brightness_slider.set(self.brightness)

        brightness_slider.pack(pady=5)

        ctk.CTkLabel(
            panel,
            text="Brightness is simulated using background colours. "
                 "It does not change your physical screen brightness.",
            wraplength=650,
            font=("Arial", 11)
        ).pack(pady=12)

        ctk.CTkButton(
            self.current_frame,
            text="Back to Dashboard",
            width=190,
            command=self.show_dashboard
        ).pack(pady=10)


    def refresh_preview(self):

        background, text_color, _ = self.get_visual_colors()

        self.preview_frame.configure(
            fg_color=background
        )

        self.preview_label.configure(
            text_color=text_color,
            font=("Arial", self.get_font_size(20), "bold")
        )


    def change_contrast(self, value):

        self.contrast = value

        self.refresh_preview()


    def change_size(self, value):

        self.size = value

        self.refresh_preview()


    def change_brightness(self, value):

        self.brightness = int(float(value))

        self.brightness_label.configure(
            text=f"Brightness: {self.brightness}%"
        )

        self.refresh_preview()


    # ======================================================
    # 6. IDENTIFICATION TASK
    # ======================================================

    def show_identification(self):

        self.clear_page()

        self.title_block(
            "Identification Task",
            "Look carefully at the silhouette and describe what you see."
        )

        background, text_color, _ = self.get_visual_colors()

        figure_frame = ctk.CTkFrame(
            self.current_frame
        )

        figure_frame.pack(pady=5)

        self.figure_canvas = tk.Canvas(
            figure_frame,
            width=620,
            height=300,
            bg=background,
            highlightthickness=1,
            highlightbackground="#888888"
        )

        self.figure_canvas.pack(
            padx=12,
            pady=12
        )

        self.draw_ambiguous_figure(
            background,
            text_color
        )

        ctk.CTkLabel(
            self.current_frame,
            text="What do you see in the figure?",
            font=("Arial", self.get_font_size(17), "bold")
        ).pack(pady=(10, 4))

        self.answer_entry = ctk.CTkEntry(
            self.current_frame,
            width=360,
            height=38,
            placeholder_text="Type your answer here"
        )

        self.answer_entry.pack(pady=5)

        self.identification_status = ctk.CTkLabel(
            self.current_frame,
            text="Ask someone other than the developer to complete this task."
        )

        self.identification_status.pack(pady=5)

        self.identification_rating = self.rating_control(
            self.current_frame
        )

        ctk.CTkButton(
            self.current_frame,
            text="Submit Answer and Save Result",
            width=260,
            command=self.submit_identification
        ).pack(pady=8)

        ctk.CTkButton(
            self.current_frame,
            text="Back to Dashboard",
            fg_color="gray",
            command=self.show_dashboard
        ).pack(pady=5)

        self.identification_start = time.perf_counter()


    def draw_ambiguous_figure(self, background, text_color):

        canvas = self.figure_canvas

        canvas.delete("all")

        canvas.configure(
            bg=background
        )

        # Combine a duck-like bill and rabbit-like ears in one silhouette.
        canvas.create_polygon(
            165, 137,
            215, 132,
            233, 112,
            257, 99,
            287, 92,
            314, 96,
            330, 48,
            350, 29,
            367, 40,
            361, 99,
            381, 35,
            402, 25,
            416, 40,
            398, 111,
            427, 120,
            447, 143,
            450, 174,
            438, 201,
            412, 220,
            373, 230,
            326, 226,
            283, 211,
            250, 190,
            228, 166,
            165, 157,
            smooth=True,
            splinesteps=24,
            fill=text_color,
            outline=text_color
        )

        canvas.create_oval(
            280, 124,
            292, 136,
            fill=background,
            outline=background
        )

        canvas.create_text(
            310,
            270,
            text="One silhouette, more than one possible interpretation",
            fill=text_color,
            font=("Arial", self.get_font_size(13))
        )


    def submit_identification(self):

        response = self.answer_entry.get().strip()

        if not response:

            self.identification_status.configure(
                text="Please enter the participant's answer."
            )

            return

        elapsed = (
            time.perf_counter() - self.identification_start
        )

        result = self.create_result(
            task="Identification",
            elapsed=elapsed,
            rating=self.identification_rating.get(),
            response=response
        )

        save_result(result)

        self.identification_status.configure(
            text=f"Result saved! Answer: {response}. "
                 f"Time: {elapsed:.2f} seconds."
        )

        self.answer_entry.delete(0, "end")

        # Start a fresh timer for the next identification attempt.
        self.identification_start = time.perf_counter()


    # ======================================================
    # 7. TARGET HITTING TASK - FITTS' LAW
    # ======================================================

    def start_fitts(self):

        # Target size and distance combinations.
        # Each combination is repeated twice.

        self.fitts_trials = [
            (24, 120),
            (24, 240),
            (60, 120),
            (60, 240),
            (24, 120),
            (24, 240),
            (60, 120),
            (60, 240)
        ]

        random.shuffle(self.fitts_trials)

        self.fitts_trial_index = 0

        self.show_fitts_trial()


    def show_fitts_trial(self):

        self.clear_page()

        if self.fitts_trial_index >= len(self.fitts_trials):

            self.show_fitts_complete()

            return

        self.fitts_size, self.fitts_distance = (
            self.fitts_trials[self.fitts_trial_index]
        )

        trial_number = self.fitts_trial_index + 1

        self.title_block(
            f"Target Hitting Task — Trial {trial_number} of 8",
            "Click the START marker first, then click the target."
        )

        ctk.CTkLabel(
            self.current_frame,
            text=f"Target size: {self.fitts_size}px     "
                 f"Distance: {self.fitts_distance}px",
            font=("Arial", 14, "bold")
        ).pack(pady=3)

        background, text_color, target_color = (
            self.get_visual_colors()
        )

        self.fitts_canvas = tk.Canvas(
            self.current_frame,
            width=760,
            height=430,
            bg=background,
            highlightthickness=1,
            highlightbackground="#888888"
        )

        self.fitts_canvas.pack(pady=10)

        # Starting point
        self.start_x = 380
        self.start_y = 215

        # Choose an angle that keeps the complete target
        # inside the canvas, including its radius.
        valid_angles = [
            0, 30, 150, 180, 210, 330
        ]

        angle = math.radians(
            random.choice(valid_angles)
        )

        self.target_x = (
            self.start_x
            + self.fitts_distance * math.cos(angle)
        )

        self.target_y = (
            self.start_y
            + self.fitts_distance * math.sin(angle)
        )

        self.target_radius = self.fitts_size / 2

        # Draw start marker
        self.fitts_canvas.create_oval(
            self.start_x - 12,
            self.start_y - 12,
            self.start_x + 12,
            self.start_y + 12,
            fill=text_color,
            outline=text_color
        )

        self.fitts_canvas.create_text(
            self.start_x,
            self.start_y + 25,
            text="START",
            fill=text_color,
            font=("Arial", 11, "bold")
        )

        # Draw target
        self.fitts_canvas.create_oval(
            self.target_x - self.target_radius,
            self.target_y - self.target_radius,
            self.target_x + self.target_radius,
            self.target_y + self.target_radius,
            fill=target_color,
            outline=text_color,
            width=2
        )

        self.fitts_status = ctk.CTkLabel(
            self.current_frame,
            text="Click the START marker to begin."
        )

        self.fitts_status.pack(pady=3)

        self.fitts_rating = self.rating_control(
            self.current_frame
        )

        self.fitts_rating.configure(
            state="disabled"
        )

        self.fitts_started = False

        self.fitts_elapsed = None

        self.fitts_canvas.bind(
            "<Button-1>",
            self.handle_fitts_click
        )

        ctk.CTkButton(
            self.current_frame,
            text="Cancel / Back to Dashboard",
            fg_color="gray",
            command=self.show_dashboard
        ).pack(pady=5)


    def handle_fitts_click(self, event):

        # Distance between click and start marker
        start_dx = event.x - self.start_x

        start_dy = event.y - self.start_y

        start_distance = math.sqrt(
            start_dx ** 2 + start_dy ** 2
        )

        # Distance between click and target centre
        target_dx = event.x - self.target_x

        target_dy = event.y - self.target_y

        target_distance = math.sqrt(
            target_dx ** 2 + target_dy ** 2
        )

        # First click: start marker
        if not self.fitts_started:

            if start_distance <= 18:

                self.fitts_started = True

                self.fitts_start_time = time.perf_counter()

                self.fitts_status.configure(
                    text="Timing started! Click the target."
                )

            else:

                self.fitts_status.configure(
                    text="Please click the START marker first."
                )

            return

        # Second click: target
        if target_distance <= self.target_radius:

            self.fitts_elapsed = (
                time.perf_counter()
                - self.fitts_start_time
            )

            self.fitts_status.configure(
                text=f"Target hit! Movement time: "
                     f"{self.fitts_elapsed:.3f} seconds. "
                     f"Rate the ease of use."
            )

            self.fitts_rating.configure(
                state="normal"
            )

            self.fitts_canvas.unbind(
                "<Button-1>"
            )

            self.fitts_canvas.create_text(
                380,
                25,
                text="TARGET HIT",
                fill="#16803C",
                font=("Arial", 15, "bold")
            )

            ctk.CTkButton(
                self.current_frame,
                text="Save Rating & Next Trial",
                width=230,
                command=self.save_fitts_trial
            ).pack(pady=5)

        else:

            self.fitts_status.configure(
                text="You missed the target. Try clicking inside it."
            )


    def save_fitts_trial(self):

        result = self.create_result(
            task="Target Hitting",
            elapsed=self.fitts_elapsed,
            rating=self.fitts_rating.get(),
            target_size=self.fitts_size,
            distance=self.fitts_distance,
            trial=self.fitts_trial_index + 1
        )

        save_result(result)

        self.fitts_trial_index += 1

        self.show_fitts_trial()


    def show_fitts_complete(self):

        self.clear_page()

        self.title_block(
            "Target Hitting Task Complete",
            "All eight trials have been completed."
        )

        ctk.CTkLabel(
            self.current_frame,
            text=f"Your results have been saved in {CSV_FILE.name}.",
            font=("Arial", 15)
        ).pack(pady=20)

        ctk.CTkLabel(
            self.current_frame,
            text="You can repeat the experiment with another participant.",
            font=("Arial", 13)
        ).pack(pady=5)

        ctk.CTkButton(
            self.current_frame,
            text="Back to Dashboard",
            command=self.show_dashboard,
            width=190
        ).pack(pady=15)


# ==========================================================
# 8. START APPLICATION
# ==========================================================

if __name__ == "__main__":

    create_csv()

    app = HumanPerformanceTester()

    app.mainloop()