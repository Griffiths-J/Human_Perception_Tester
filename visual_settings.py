import customtkinter as ctk


class VisualSettingsMixin:

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
