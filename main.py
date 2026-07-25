import platform
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

SERVER_URL = "https://mint-license-server.onrender.com/api/verify"

def get_hwid():
    return platform.node() + "-" + platform.system()

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 30
        self.spacing = 15

        # Tytuł
        self.add_widget(Label(
            text="=== MINT LICENSE CLIENT ===", 
            font_size=20, 
            size_hint_y=None, 
            height=40
        ))

        # Login
        self.add_widget(Label(text="Login:", size_hint_y=None, height=30))
        self.username_input = TextInput(
            text='', 
            multiline=False, 
            size_hint_y=None, 
            height=40
        )
        self.add_widget(self.username_input)

        # Hasło
        self.add_widget(Label(text="Hasło:", size_hint_y=None, height=30))
        self.password_input = TextInput(
            text='', 
            password=True, 
            multiline=False, 
            size_hint_y=None, 
            height=40
        )
        self.add_widget(self.password_input)

        # Przycisk logowania
        self.login_btn = Button(text="Zaloguj się", size_hint_y=None, height=50)
        self.login_btn.bind(on_press=self.verify_license)
        self.add_widget(self.login_btn)

        # Status / Wynik
        self.status_label = Label(
            text="", 
            halign='center', 
            valign='middle'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        self.add_widget(self.status_label)

    def verify_license(self, instance):
        username = self.username_input.text.strip()
        password = self.password_input.text.strip()

        if not username or not password:
            self.status_label.text = "[BŁĄD] Wprowadź login i hasło!"
            return

        self.status_label.text = "Logowanie do serwera..."

        payload = {
            "username": username,
            "password": password,
            "hwid": get_hwid()
        }

        try:
            response = requests.post(SERVER_URL, json=payload, timeout=10)
            data = response.json()

            if data.get("status") == "valid":
                role = data.get('role', 'Brak')
                announcement = data.get('announcement', '')
                msg = f"[SUKCES] Zalogowano pomyślnie!\nRola: {role}"
                if announcement:
                    msg += f"\n\n📢 Ogłoszenie:\n{announcement}"
                self.status_label.text = msg
            else:
                err = data.get('error', 'Nieznany błąd')
                self.status_label.text = f"[BŁĄD] {err}"
        except Exception as e:
            self.status_label.text = f"[BŁĄD SIECI] Nie udało się połączyć:\n{e}"

class MintClientApp(App):
    def build(self):
        self.title = "Mint Client"
        return LoginScreen()

if __name__ == "__main__":
    MintClientApp().run()
