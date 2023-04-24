import selenium
import customtkinter as ctk
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

app = ctk.CTk()
app.title("Advanced Typeracer Bot")

class First_Screen():
    WIDTH = 300
    HEIGHT = 150
    FONT = (17,17)
    def __init__(self):
        app.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        #This is so the window size can not be modified
        app.minsize(self.WIDTH, self.HEIGHT)
        app.maxsize(self.WIDTH, self.HEIGHT)

        #Creating the label that tells the user to select their browser
        ctk.CTkLabel(
            master=app,
            text = "Select your preferred browser",
            font=self.FONT,
        ).pack(pady=10)

        select_browser_combo = ctk.CTkComboBox(
            master=app,
            values = ['Brave', 'Chrome', 'Firefox', 'Internet Explorer', 'Opera'],
            font=self.FONT,
        )
        #Set to 'Chrome' because it's the most common browser
        select_browser_combo.set('Chrome')
        select_browser_combo.pack()

        select_browser_button = ctk.CTkButton(
            master = app,
            command = lambda: print(select_browser_combo.get()),
            text = 'Confirm',
            font = self.FONT,
        )
        select_browser_button.pack(pady=15)
        

def main():
    First_Screen()
    app.mainloop()

if __name__ == "__main__":
    main()