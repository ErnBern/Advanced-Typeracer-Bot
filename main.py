import selenium
import customtkinter as ctk
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

app = ctk.CTk()
app.title("Advanced Typeracer Bot")

driver = ''

def set_driver(browser):
    global driver
    if browser == 'Brave':
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as BraveService
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.core.utils import ChromeType

        driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()))

    if browser == "Chrome":
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    if browser == 'Chromium':
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service as ChromiumService
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.core.utils import ChromeType

        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))

    if browser == 'Edge':
        from selenium import webdriver
        from selenium.webdriver.edge.service import Service as EdgeService
        from webdriver_manager.microsoft import EdgeChromiumDriverManager

        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

    if browser == 'FireFox':
        from selenium import webdriver
        from selenium.webdriver.firefox.service import Service as FirefoxService
        from webdriver_manager.firefox import GeckoDriverManager

        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))

    if browser == "Internet Explorer":
        from selenium import webdriver
        from selenium.webdriver.ie.service import Service as IEService
        from webdriver_manager.microsoft import IEDriverManager

        driver = webdriver.Ie(service=IEService(IEDriverManager().install()))

    if browser == 'Opera':
        from selenium import webdriver
        from selenium.webdriver.chrome import service
        from webdriver_manager.opera import OperaDriverManager

        webdriver_service = service.Service(OperaDriverManager().install())
        webdriver_service.start()

        options = webdriver.ChromeOptions()
        options.add_experimental_option('w3c', True)

        driver = webdriver.Remote(webdriver_service.service_url, options=options)

def change_browser(browser):
    set_driver(browser)

    #Writing the browser to a settings file
    with open('settings.txt', 'r') as file:
        settings = file.readlines()
    #Only runs if the settings file is blank
    if settings == []:
        with open('settings.txt', 'w+') as file:
            file.write("Do not modify this file!\n")
            file.write(f'BROWSER={browser}\n')
            file.write('START=E\n')
            file.write("END=F\n")
            file.write("APPEARANCE=SYSTEM\n")
        driver.get("https://play.typeracer.com/")
        return
    
    with open('settings.txt', 'r') as file:
        settings = file.readlines()
    settings[1] = f"BROWSER={browser}\n"

    with open('settings.txt', 'w+') as file:
        for setting in settings:
            file.write(setting)



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
            values = ['Brave', 'Chrome', 'Chromium', 'Edge', 'Firefox', 'Internet Explorer', 'Opera'],
            font=self.FONT,
        )
        #Set to 'Chrome' because it's the most common browser
        select_browser_combo.set('Chrome')
        select_browser_combo.pack()

        select_browser_button = ctk.CTkButton(
            master = app,
            command = lambda: change_browser(select_browser_combo.get()),
            text = 'Confirm',
            font = self.FONT,
        )
        select_browser_button.pack(pady=15)

class Main_Window():
    WIDTH = 500
    HEIGHT = 450
    FONT = (17, 17)
    def __init__(self):
        app.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        for widget in app.winfo_children(): #Refreshing the screen
            widget.destroy()
        #This is so the window size can not be modified
        app.minsize(self.WIDTH, self.HEIGHT)
        app.maxsize(self.WIDTH, self.HEIGHT)

        app.geometry(f"{self.WIDTH}x{self.HEIGHT}")


def main(): 
    try:
        #Checking if the settings file exists
        open('settings.txt', 'x')
        First_Screen()
        with open('settings.txt', 'r') as file:
            settings = file.readlines()

        with open("settings.txt", 'w+') as file:
            for setting in settings:
                file.write(setting)

        Main_Window()
        #To avoid issues before the main loop has started
        app.mainloop()
    except:
    #Getting the settings from the settings file
        with open('settings.txt', 'r') as file:
            settings = file.readlines()

        Main_Window()
        browser = settings[1].strip()
        browser = browser.split("BROWSER=")[1]
        set_driver(browser)
        driver.get("https://play.typeracer.com/")
        app.mainloop()

if __name__ == "__main__":
    main()