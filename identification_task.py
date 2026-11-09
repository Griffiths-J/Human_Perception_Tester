import time
import tkinter as tk

import customtkinter as ctk

if __package__:
    from .data_logging import save_result
else:
    from data_logging import save_result


class IdentificationTaskMixin:

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
            text=""
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

        if not any(character.isalpha() for character in response):

            self.identification_status.configure(
                text="Please describe what you see using words, not only numbers."
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

        self.identification_start = time.perf_counter()
