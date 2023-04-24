import selenium
import customtkinter as ctk
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

app = ctk.CTk()
app.title("Advanced Typeracer Bot")

driver = ''

def change_browser(browser):
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