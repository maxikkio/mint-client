import platform
import requests

SERVER_URL = "https://mint-license-server.onrender.com/api/verify"

def get_hwid():
    return platform.node() + "-" + platform.system()

def main():
    print("=== MINT LICENSE CLIENT ===")
    username = input("Podaj login: ").strip()
    password = input("Podaj hasło: ").strip()

    payload = {
        "username": username,
        "password": password,
        "hwid": get_hwid()
    }

    print("\nLogowanie do serwera...")
    try:
        response = requests.post(SERVER_URL, json=payload)
        data = response.json()

        if data.get("status") == "valid":
            print("\n[SUKCES] Zalogowano pomyślnie!")
            print(f"Rola: {data.get('role')}")
            if data.get("announcement"):
                print(f"📢 Ogłoszenie od Właściciela: {data.get('announcement')}")
            
            print("\nTutaj uruchamia się właściwy kod Twojego programu...")
            input("\nNaciśnij Enter, aby zamknąć...")
        else:
            print(f"\n[BŁĄD] {data.get('error', 'Nieznany błąd')}")
            input("\nNaciśnij Enter, aby zamknąć...")
    except Exception as e:
        print(f"\n[BŁĄD SIECI] Nie udało się połączyć z serwerem: {e}")
        input("\nNaciśnij Enter, aby zamknąć...")

if __name__ == "__main__":
    main()
