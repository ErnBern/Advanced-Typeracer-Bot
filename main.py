import time
import string
import random
import asyncio
import threading
import customtkinter as ctk
from bs4 import BeautifulSoup
from pynput.keyboard import Listener
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

changing_keybind = False # used to check if a keybind is being changed
keybind_display = None # entry box used to display the keybind

#Variables used to get the accuracy and wpm values when using keybinds
accuracy_ComboBox = None
wpm_Entry = None

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

class Preferences(ctk.CTkToplevel):
    WIDTH = 500
    HEIGHT = 300
    FONT= (17, 17)
    def __init__(self, *args, **kwargs):
        global keybind_display
        super().__init__(*args, **kwargs)
        self.title('Change Preferences')
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.minsize(self.WIDTH, self.HEIGHT)
        self.maxsize(self.WIDTH, self.HEIGHT)
        with open("settings.txt", 'r') as f:
            #Variable before the \n is removed
            temp_settings = f.readlines()
            self.settings = []
            for setting in temp_settings:
                #Try statement to ignore the first line
                try: self.settings.append(setting.strip().split('=')[1]) #Removes all the unnecessary characters 
                except: continue
        keybind_frame = ctk.CTkFrame(
            master=self,
            fg_color= 'transparent',
        )
        keybind_frame.pack()
        #Entry that displays the current keybind
        keybind_display = ctk.CTkEntry(
            master=keybind_frame,
            font=self.FONT,
            width=200,
            height=30,
            justify="center"
        )
        keybind_display.grid(pady=10, columnspan=5,sticky='ew')
        self.grid_rowconfigure((0), weight=1) #Centres the entry window
        #Inserting the text into the entry
        keybind_display.insert(0, f"SELECT KEYBIND")
        keybind_display.configure(state="disabled")

        self.change_start_button = ctk.CTkButton(
            master=keybind_frame,
            text="Change Start Keybind",
            font=self.FONT,
            command=self.change_start_keybind,
        )
        self.change_start_button.grid(row=1, column=0, padx=10, sticky='e')

        self.change_stop_button = ctk.CTkButton(
            master=keybind_frame,
            text="Change Stop Keybind",
            font=self.FONT,
            command=self.change_stop_keybind,
        )
        self.change_stop_button.grid(row=1, column=1, padx=10, sticky='w')

        self.grid_columnconfigure((0, 1), weight=1) #Creates and equal distance between the 2 buttons

        self.confirm_keybind = ctk.CTkButton(
            master=keybind_frame,
            text="Confirm Keybind",
            state='disabled',
            command=self.confirm_keybind_change,
            font=self.FONT,
        )
        self.grid_rowconfigure(2, weight=1)
        self.confirm_keybind.grid(row=2, pady=(5, 0), columnspan=2, sticky='w', padx=(40, 0))

        self.cancel_keybind = ctk.CTkButton(
            master=keybind_frame,
            text="Cancel",
            command=self.cancel_keybind_change,
            font=self.FONT,
            state='disabled',
        )
        self.cancel_keybind.grid(row=2, column=1, pady=(5,0),columnspan=2, sticky='e', padx=(0, 40))

        #Themes frame
        themes_frame = ctk.CTkFrame(
            master=self,
            fg_color='transparent',
        )
        themes_frame.pack(pady=10)

        #Radio Buttons for the themes/modes
        self.theme_radio_var = ctk.IntVar(value=0)
        light_mode = ctk.CTkRadioButton(
            themes_frame,
            font=self.FONT,
            text="Light Mode",
            value=1,
            variable=self.theme_radio_var,
            command=self.change_theme,
            )
        dark_mode = ctk.CTkRadioButton(
            themes_frame,
            font=self.FONT,
            text="Dark Mode",
            value=2,
            variable=self.theme_radio_var,
            command=self.change_theme,
        )
        system_mode = ctk.CTkRadioButton(
            themes_frame,
            font=self.FONT,
            text="System Mode",
            value=3,
            variable=self.theme_radio_var,
            command=self.change_theme,
        )
        themes_frame.grid_rowconfigure((1,2,3), weight=1)
        light_mode.grid(row=0, pady=5, columnspan=2, sticky='ew')
        dark_mode.grid(row=1, pady=5, columnspan=2, sticky='ew')
        system_mode.grid(row=2, pady=5, columnspan=2, sticky='ew')

        #Selects the current theme
        if self.settings[3] == 'LIGHT':
            light_mode.select()
        if self.settings[3] == 'SYSTEM':
            system_mode.select()
        if self.settings[3] == 'DARK':
            dark_mode.select()

        browser_combobox = ctk.CTkComboBox(
            master=self,
            values = ['Brave', 'Chrome', 'Chromium', 'Edge', 'FireFox', 'Internet Explorer', 'Opera'],
            font=self.FONT,
            command=self.change_browser,
        )
        browser_combobox.pack(pady=5)
        browser_combobox.set(self.settings[0])


    def change_start_keybind(self):
        global changing_keybind
        self.change_start_button.configure(state="disabled")
        keybind_display.configure(state="normal")
        keybind_display.delete(0, ctk.END) # Clears the Entry Box
        keybind_display.insert(0, f"Keybind: {self.settings[1]}")
        keybind_display.configure(state="disabled")
        self.change_stop_button.configure(state="normal")
        self.confirm_keybind.configure(state="normal")# Enables the confirm button
        self.cancel_keybind.configure(state='normal')# Enables the cancel button
        changing_keybind = True #Starts recording the keystrokes

    def change_stop_keybind(self):
        global changing_keybind
        self.change_stop_button.configure(state="disabled")
        keybind_display.configure(state="normal")
        keybind_display.delete(0, ctk.END) # Clears the Entry Box
        keybind_display.insert(0, f"Keybind: {self.settings[2]}")
        keybind_display.configure(state="disabled")
        self.change_start_button.configure(state="normal")
        self.confirm_keybind.configure(state="normal")
        self.cancel_keybind.configure(state='normal')
        changing_keybind = True

    def write_changes(self):
        #Can't use a for loop to write changes because each line needs to be written differently
        with open('settings.txt', 'w+') as f:
            f.write("Do not modify this file!\n")
            f.write(f'BROWSER={self.settings[0]}\n')
            f.write(f'START={self.settings[1]}\n')
            f.write(f"END={self.settings[2]}\n")
            f.write(f"APPEARANCE={self.settings[3]}\n")

    def confirm_keybind_change(self):
        global changing_keybind

        if self.change_start_button.cget('state') == 'disabled': #Checks if the start key is being changed by seeing if its button is disabled
            keybind = keybind_display.get().split('Keybind: ')[1]
            self.settings[1] = keybind
            self.change_start_button.configure(state="normal")
            start_button.configure(text=f"Start ({keybind})")

        if self.change_stop_button.cget('state') == 'disabled': #Checks if the stop key is being change by checking if its button is disabled
            keybind = keybind_display.get().split('Keybind: ')[1]
            self.settings[2] = keybind
            self.change_stop_button.configure(state="normal")
            end_button.configure(text=f"Stop ({keybind})")

        self.write_changes()
        
        #Reverts the keybind display entry back to normal
        keybind_display.configure(state='normal')
        keybind_display.delete(0, ctk.END)
        keybind_display.insert(0, 'SELECT KEYBIND')
        keybind_display.configure(state='disabled')

        #Reverts the confirm and cancel button back to their orignal states
        self.confirm_keybind.configure(state='disabled')
        self.cancel_keybind.configure(state='disabled')
        
    
    def change_theme(self):
        theme_value = self.theme_radio_var.get()
        theme = None
        if theme_value == 1:
            theme = "light"
        if theme_value == 2:
            theme = "dark"
        if theme_value == 3:
            theme = "system"

        ctk.set_appearance_mode(theme)

        self.settings[3] = theme.upper()
        
        self.write_changes()

    def change_browser(self, browser):
        self.settings[0] = browser

        self.write_changes()
        
        driver.quit()
        set_driver(browser)     
        driver.get("https://play.typeracer.com/")

    def cancel_keybind_change(self):
        global changing_keybind
        
        self.change_stop_button.configure(state="normal")# Re-enables the start and stop buttons
        self.change_start_button.configure(state="normal")

        changing_keybind = False #Stops Recording keystrokes
        self.cancel_keybind.configure(state='disabled') #Disables the Cancel and Confirm Button
        self.confirm_keybind.configure(state='disabled')
        
        keybind_display.configure(state='normal')
        keybind_display.delete(0, ctk.END)
        keybind_display.insert(0, 'SELECT KEYBIND')
        keybind_display.configure(state='disabled')


        
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
            values = ['Brave', 'Chrome', 'Chromium', 'Edge', 'FireFox', 'Internet Explorer', 'Opera'],
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
    WIDTH = 425
    HEIGHT = 200
    FONT = (17, 17)
    def __init__(self):
        global start_button, end_button, accuracy_ComboBox, wpm_Entry
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
            text='Accuracy:',
            justify="center",
        ).grid(sticky='w', columnspan=2)
        entry_frame.grid_columnconfigure((0,1), weight=1)
        entry_frame.grid_rowconfigure((0), weight=1)
        ctk.CTkLabel(
            entry_frame,
            font=self.FONT,
            text='Speed:',
            justify='center',
        ).grid(row=0, column=1, columnspan=2,sticky='w', padx=(20,0))

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
        accuracy.grid(row=1, column=0, padx=(0, 40))
        accuracy_ComboBox = accuracy

        #Creating the typing speed entry box
        wpm = ctk.CTkEntry(
            entry_frame,
            font=self.FONT,
            placeholder_text="120",
            width=90,

        )
        wpm.grid(row=1, column=1)
        wpm.insert(0, "120")
        wpm_Entry = wpm

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

        preferences_button = ctk.CTkButton(
            app,
            font = self.FONT,
            text="Preferences",
            width=110,
            command=self.open_preferences_window
        )
        preferences_button.pack()
        self.top_level_window = None


    def open_preferences_window(self):
        #Checks if the Windows already 
        if self.top_level_window is None or not self.top_level_window.winfo_exists():
            self.TOP_LEVEL_EXISTS = True
            self.top_level_window = Preferences(app)
            return
        #If window exists, focus it
        self.top_level_window.focus()


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
        #This is so if the user stops while in the same text it can continue, sadly it doesn't work if the user types on their own too
        if triggered:
            run =  False
            triggered = False
            continue
        last_text = text
        run = False

#Function for listening for the starting and ending keys
async def on_press(key):
    global changing_keybind
    await asyncio.sleep(0.05)
    try: key = str(key).split('Key.')[1]
    #Stopping the char from being wrapped in ""
    except: key = str(key.char).split()[0]

    if changing_keybind:
        keybind_display.configure(state='normal')
        keybind_display.delete(0, ctk.END)
        keybind_display.insert(0, f"Keybind: {key.upper()}")
        keybind_display.configure(state='disabled')
        

    with open('settings.txt', 'r') as f:
        settings = f.readlines()
        #Getting the keybinds and removing the "START=" and "END=", and also the "\n"
        start_keybind = settings[2].split("START=")[1].strip().lower()
        end_keybind = settings[3].split("END=")[1].strip().lower()
    
    if key == start_keybind:
        Main_Window.start_button_handler(None, accuracy_ComboBox.get(), wpm_Entry.get)
    
    if key == end_keybind:
        Main_Window.end_button_handler(None)

def main(): 
    global end_typing_thread
    typing_thread = threading.Thread(target=lambda:asyncio.run(typer()))
    typing_thread.start()
    keybind_listener = Listener(on_press=lambda key: asyncio.run(on_press(key)))
    keybind_listener.start()
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

        #sets the theme/mode from the from the settings file
        theme = settings[4].strip()
        theme = theme.split("APPEARANCE=")[1]
        ctk.set_appearance_mode(theme.lower())

    app.mainloop()
    end_typing_thread = True
    driver.quit()

if __name__ == "__main__":
    main()