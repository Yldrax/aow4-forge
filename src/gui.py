"""Building the GUI"""

import customtkinter as ctk
from PIL import Image
from src.automate import auto_forge


class ForgeApp(ctk.CTk):
    """The Main GUI Window"""

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")

        ### Window Basics
        self.title("Pantheon Forge")
        self.iconbitmap("assets/favicon.ico")

        # self.configure(fg_color="#571322")
        self.bg_image = ctk.CTkImage(
            Image.open("assets/forge_background.png"), size=(300, 300)
        )
        self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
        self.bg_label.place(x=0, y=0)

        self.geometry("300x300")
        self.resizable(False, False)

        ### Widgets
        # Header
        self.headline = ctk.CTkLabel(
            self,
            text="Pantheon Forge",
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
            text_color=("#F2F0EF"),
            fg_color="#005484",
        )

        # Speed Slider
        self.speed = 3
        self.speed_slider = ctk.CTkSlider(
            self, from_=1, to=5, number_of_steps=4, command=self.slider_changed
        )
        self.speed_slider.set(3)

        self.delay_label = ctk.CTkLabel(
            self,
            text="Speed: 3",
            font=ctk.CTkFont(family="Arial", size=16, weight="bold"),
            padx=8,
            text_color="#F2F0EF",
            fg_color="black",
        )

        # Start Button
        self.start_button = ctk.CTkButton(
            self,
            command=self.start_automation,
            text="START",
            fg_color="#135748",
            hover_color="#1f7c6a",
            text_color="#F2F0EF",
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
        )

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="STATUS: READY",
            text_color="black",
            fg_color="#F2F0EF",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            padx=2,
            corner_radius=16,
        )

        ### Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        self.headline.grid(row=0, column=0, pady=(16, 8), padx=16, sticky="ew")
        self.speed_slider.grid(row=1, column=0, pady=(8, 0))
        self.delay_label.grid(row=2, column=0, pady=(0, 8))
        self.start_button.grid(row=3, column=0, pady=(8, 8))
        self.status_label.grid(row=4, column=0, pady=(8, 16))

    def slider_changed(self, value):
        """Tracking the Delay Slider"""
        self.speed = round(value)
        self.delay_label.configure(text=f"Speed: {self.speed}")

    def start_automation(self):
        """Runs on pressing start button, activates the automation and updates the status label."""
        self.update_status(1)
        self.update_idletasks()
        self.update_status(auto_forge(self.speed))
        self.focus_force()

    def update_status(self, status: int):
        """Update the Status Label"""
        match status:
            case 0:
                status_string = "STATUS: READY"
                status_color = "white"
            case 1:
                status_string = "STATUS: FORGING"
                status_color = "orange"
            case 2:
                status_string = "STATUS: COMPLETE"
                status_color = "green"
            case -1:
                status_string = "STATUS: ABORTED"
                status_color = "red"

        self.status_label.configure(text=status_string, fg_color=status_color)


if __name__ == "__main__":
    app = ForgeApp()
    app.mainloop()
