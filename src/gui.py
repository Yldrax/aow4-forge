"""Building the GUI"""

import time
from PIL import Image
import customtkinter as ctk


class ImageButton(ctk.CTkButton):
    """Custom Button with Hover Effect"""

    def __init__(self, root, img1, img2, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.img1 = ctk.CTkImage(Image.open(img1), size=(64, 64))
        self.img2 = ctk.CTkImage(Image.open(img2), size=(64, 64))

        self.image = self.img1

        self.bind("<Enter>", self.enter)
        self.bind("<Leave>", self.leave)

    def enter(self, event):
        self.configure(image=self.img2)

    def leave(self, event):
        self.configure(image=self.img1)


class ForgeApp(ctk.CTk):
    """The Main GUI Window"""

    def __init__(self):
        super().__init__()

        ### Window Basics
        self.title("Pantheon Forge")
        self.iconbitmap("assets/favicon.ico")

        self.geometry("300x200")
        self.resizable(False, False)
        ### Widgets
        # Header
        self.headline = ctk.CTkLabel(
            self,
            text="Pantheon Forge",
            font=ctk.CTkFont(family="Arial", size=32, weight="bold"),
        )

        # Start Button
        self.start_button = ImageButton(
            self,
            command=self.start_automation,
            img1="assets/forge_extinguished.png",
            img2="assets/forge_upscaled.png",
            text="",
        )

        # Status label
        self.status_label = ctk.CTkLabel(
            self,
            text="READY",
            text_color="black",
            fg_color="white",
            font=ctk.CTkFont(family="Arial", size=24, weight="bold"),
            padx=2,
            corner_radius=16,
        )

        ### Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(index=1, weight=1)

        self.headline.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="ew")
        self.start_button.grid(row=1, column=0, pady=(8, 8))
        self.status_label.grid(row=2, column=0, pady=(8, 8))

    def start_automation(self):
        """Runs when the start button is pressed, activates the automation and updates the status label."""
        self.status_label.configure(text="FORGING", fg_color="orange")
        self.update_idletasks()
        time.sleep(5)
        self.status_label.configure(text="FINISHED", fg_color="green")


if __name__ == "__main__":
    app = ForgeApp()
    app.mainloop()
