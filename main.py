import time
import string
import random
import asyncio
import threading
import selenium
import customtkinter as ctk
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = ctk.CTk()
app.title("Advanced Typeracer Bot")

driver = ''
run = False

accuracy = ""
wpm = ""

end_typing_thread = False

#These have to be set as global variables to allow easy access between functions
start_button = None
end_button = None

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

        Main_Window()
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
        global start_button, end_button
        app.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        for widget in app.winfo_children(): #Refreshing the screen
            widget.destroy()
        #This is so the window size can not be modified
        app.minsize(self.WIDTH, self.HEIGHT)
        app.maxsize(self.WIDTH, self.HEIGHT)

        app.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        entry_frame = ctk.CTkFrame(app, 100,50, fg_color='transparent')
        entry_frame.pack()
        #Labels for the entries
        ctk.CTkLabel(
            entry_frame,
            font=self.FONT,
            text='Select Accuracy:'
        ).grid()
        ctk.CTkLabel(
            entry_frame,
            font=self.FONT,
            text='Select Typing Speed:'
        ).grid(row=0, column=1)

        #Creating the accuracy combo box
        accuracy = ctk.CTkComboBox(
            entry_frame,
            font=self.FONT,
            values=[
            "100%", "90%", "80%", 
            '70%', '60%', "50%",
            '40%', '30%', "20%", 
            "10%" 
            ],
            width=90
        )
        accuracy.grid(row=1, column=0)

        #Creating the typing speed entry box
        wpm = ctk.CTkEntry(
            entry_frame,
            font=self.FONT,
            placeholder_text="120",
            width=100,

        )
        wpm.grid(row=1, column=1)
        wpm.insert(0, "120")

        button_frame= ctk.CTkFrame(
            app,
            width=100,
            height=50,
            fg_color='transparent',
        )
        button_frame.pack(pady=10)

        with open('settings.txt', 'r') as f:
            settings = f.readlines()
            #Getting the keybinds and removing the "START=" and "END=", and also the "\n"
            start_keybind = settings[2].split("START=")[1].strip()
            end_keybind = settings[3].split("END=")[1].strip()
        
        start_button = ctk.CTkButton(
            button_frame,
            font = self.FONT,
            text=f"Start ({start_keybind})",
            width=110,
            command= lambda:self.start_button_handler(accuracy.get(), wpm.get()) 
        )
        start_button.grid(padx=10)

        end_button = ctk.CTkButton(
            button_frame,
            font=self.FONT,
            text=f"Stop ({end_keybind})",
            width=110,
            state='disabled',
            command= lambda:self.end_button_handler()
        )
        end_button.grid(row=0, column=1, padx=10)

    def start_button_handler(self, acc, WPM):
        global accuracy, wpm, run
        accuracy = acc
        wpm = WPM
        run = True
        start_button.configure(state='disabled')
        end_button.configure(state='normal')

    def end_button_handler(self):
        global run
        run = False
        start_button.configure(state='normal')
        end_button.configure(state='disabled')

async def typer():
    global accuracy, wpm, run
    last_text = None
    completed_text = []
    while True:
        #So the program does not use up all the CPU
        await asyncio.sleep(0.05)
        if end_typing_thread: break
        if not run: continue
        #Something to create an inaccuracy
        def create_inaccuracy(accuracy):
            #Python needs switch cases ;-;
            num = random.randint(1, 1)
            if accuracy == 100:
                return None
            if accuracy == 90:
                if num < 1:
                    return random.choice(string.ascii_letters)
            if accuracy == 80:
                if num < 2:
                    return random.choice(string.ascii_letters)
            if accuracy == 70:
                if num < 3:
                    return random.choice(string.ascii_letters)
            if accuracy == 60:
                if num < 4:
                    return random.choice(string.ascii_letters)
            if accuracy == 50:
                if num < 5:
                    return random.choice(string.ascii_letters)
            if accuracy == 40:
                if num <= 6:
                    return random.choice(string.ascii_letters)
            if accuracy == 30:
                if num <= 7:
                    return random.choice(string.ascii_letters)
            if accuracy == 20:
                if num <= 8:
                    return random.choice(string.ascii_letters)
            if accuracy == 10:
                if num <= 9:
                    return random.choice(string.ascii_letters)
            return None #If nothing happens return None
            
        accuracy = int(accuracy.split("%")[0])

        try: wpm = int(wpm) # If invalid input set WPM to 120
        except: wpm = 120

        #Getting the correct delay using different formulas
        if wpm >= 200:
            delay = 1 / (wpm * 7 / 60)
        if wpm < 60:
            delay = 1 / (wpm * 5 / 60)
        if 60 <= wpm <= 130:
            delay = 1 / (wpm * 6 / 60)
        if 130 < wpm <= 190:
            delay = 1 / (wpm * 6.5 / 60)

        src = driver.page_source
        soup = BeautifulSoup(src, "html.parser")
        text = ''
        span = soup.findAll("span")
        for i in span:
            if "unselectable" in str(i):
                text += i.text
        word_input = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.CLASS_NAME, "txtInput")))
        triggered = False
        #Turns the text from a string into a list of all the chars
        text = [*text]
        if text != last_text:
            completed_text = []
        if text == last_text:
            print("asd")
            triggered = True
            for char in completed_text:
                text.remove(char)
        if not triggered:
            word_input.clear()
        for word in text:
            if not run: break
            time.sleep(delay)
            char = create_inaccuracy(accuracy)
            if char is not None:
                word_input.send_keys(char)
                word_input.send_keys(Keys.BACKSPACE)
                word_input.send_keys(word)
                completed_text.append(word)
                continue
            word_input.send_keys(word)
            completed_text.append(word)
        #This is so if the user stops while in the same text it can continue
        if triggered:
            run =  False
            triggered = False
            continue
        last_text = text
        run = False

    
def main(): 
    global end_typing_thread
    typing_thread = threading.Thread(target=lambda:asyncio.run(typer()))
    typing_thread.start()
    try:
        #Checking if the settings file exists
        open('settings.txt', 'x')
        First_Screen()
        with open('settings.txt', 'r') as file:
            settings = file.readlines()

        with open("settings.txt", 'w+') as file:
            for setting in settings:
                file.write(setting)

        #To avoid issues before the main loop has started
        #app.mainloop()
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
    end_typing_thread = True
    driver.quit()

if __name__ == "__main__":
    main()