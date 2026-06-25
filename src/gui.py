"""Building the GUI"""

import time
import customtkinter as ctk
from PIL import Image
from automate import auto_forge


class ForgeApp(ctk.CTk):
    """The Main GUI Window"""

    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")

        ### Window Basics
        self.title("Pantheon Forge")
        self.iconbitmap("assets/favicon.ico")

        # self.configure(fg_color="#571322")
        self.bg_image=ctk.CTkImage(Image.open("assets/forge_background.png"), size=(300,300))
        self.bg_label = ctk.CTkLabel(self,text="", image=self.bg_image)
        self.bg_label.place(x=0,y=0)

        self.geometry("300x200")
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

        self.headline.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="ew")
        self.start_button.grid(row=1, column=0, pady=(8, 8))
        self.status_label.grid(row=2, column=0, pady=(8, 16))

    def start_automation(self):
        """Runs when the start button is pressed, activates the automation and updates the status label."""
        self.status_label.configure(text="STATUS: FORGING", fg_color="orange")
        self.update_idletasks()
        auto_forge()
        self.status_label.configure(text="STATUS: FINISHED", fg_color="green")


if __name__ == "__main__":
    app = ForgeApp()
    app.mainloop()
