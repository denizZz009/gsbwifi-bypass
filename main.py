import requests
import time
import os
import subprocess
import configparser
import urllib3
import platform

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

if os.name == 'nt':
    os.system('')

LOGIN_URL = "https://wifi.gsb.gov.tr/j_spring_security_check" 
CONFIG_FILE = "config.ini"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Content-Type": "application/x-www-form-urlencoded"
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    GREEN = '\033[92m'
    RESET = '\033[0m'
    
    banner = f"""{GREEN}
    ╔═════════════════════════════════════════════════════╗
    ║                                                     ║
    ║    ____  ____  ____  __        _____ _____ ___      ║
    ║   / ___|/ ___|| __ ) \ \      / /_ _|  ___|_ _|     ║
    ║  | |  _ \___ \|  _ \  \ \ /\ / / | || |_   | |      ║
    ║  | |_| | ___) | |_) |  \ V  V /  | ||  _|  | |      ║
    ║   \____||____/|____/    \_/\_/  |___|_|   |___|     ║
    ║                                                     ║
    ║         [ GSBWIFI Auto-Auth & Bypass Tool ]         ║
    ║         [ Credit: @denizegemenemare       ]         ║
    ║                                                     ║
    ╚═════════════════════════════════════════════════════╝{RESET}
    """
    print(banner)

def load_credentials():
    config = configparser.ConfigParser()
    
    if not os.path.exists(CONFIG_FILE):
        print_banner()
        print(f"[*] İlk kurulum tespit edildi. '{CONFIG_FILE}' dosyası oluşturuluyor...")
        config['Credentials'] = {
            'TC_KIMLIK': 'BURAYA_TC_YAZIN',
            'SIFRE': 'BURAYA_SIFRE_YAZIN'
        }
        with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
            config.write(configfile)
            
        print(f"[!] '{CONFIG_FILE}' dosyası başarıyla oluşturuldu.")
        print("[!] Lütfen bu dosyanın içine TC ve Şifre bilgilerinizi yazıp aracı tekrar çalıştırın.")
        input("\nÇıkmak için Enter'a bas...")
        exit()
        
    config.read(CONFIG_FILE, encoding='utf-8')
    tc = config['Credentials'].get('TC_KIMLIK', '').strip()
    sifre = config['Credentials'].get('SIFRE', '').strip()
    
    if tc in ['BURAYA_TC_YAZIN', ''] or sifre in ['BURAYA_SIFRE_YAZIN', '']:
        print_banner()
        print(f"[-] HATA: Lütfen '{CONFIG_FILE}' dosyasının içindeki bilgileri kendi bilgilerinizle değiştirin!")
        input("\nÇıkmak için Enter'a bas...")
        exit()
        
    return tc, sifre

def aggressive_login(tc, sifre):
    print("\n[*] GSBWIFI kapısı zorlanıyor. Arkana yaslan...")
    attempts = 0
    
    payload = {
        "j_username": tc,
        "j_password": sifre
    }
    
    with requests.Session() as session:
        while True:
            attempts += 1
            try:
                response = session.post(LOGIN_URL, data=payload, headers=HEADERS, timeout=2, allow_redirects=False, verify=False)
                
                if response.status_code == 302 and 'Location' in response.headers:
                    print(f"\n[+] BOOM! {attempts}. denemede içeri girildi! İnternet aktif.")
                    return True 
                
                elif response.status_code == 200 and "giriş başarılı" in response.text.lower():
                    print(f"\n[+] BOOM! {attempts}. denemede içeri girildi! İnternet aktif.")
                    return True
                
                else:
                    print(f"\r[-] {attempts}. deneme başarısız. Sistem yanıt verdi ama giriş onaylanmadı...", end="")            
            
            except requests.exceptions.Timeout:
                print(f"\r[-] {attempts}. deneme: Sunucu dolu (Timeout). Tekrar vuruluyor...", end="")
            except requests.exceptions.RequestException:
                print(f"\r[-] {attempts}. deneme: Ağ hatası. Tekrar vuruluyor...", end="")
                
            time.sleep(0.3)

def check_warp_installed():
    try:
        result = subprocess.run(["warp-cli", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
    except FileNotFoundError:
        return False
    return False

def install_warp():
    os_name = platform.system()
    
    if os_name == "Windows":
        print("\n[*] Windows tespit edildi. Winget ile WARP kuruluyor. Lütfen bekle...")
        os.system("winget install -e --id Cloudflare.Warp")
        print("\n[+] Kurulum tamamlandı! Lütfen uygulamanın ilk ayarlarını yap.")
        
    elif os_name == "Linux":
        try:
            with open("/etc/os-release") as f:
                os_info = f.read().lower()
                
            if "cachyos" in os_info or "arch" in os_info:
                print("\n[*] Arch/CachyOS tabanlı sistem tespit edildi. 'yay' ile kuruluyor...")
                os.system("yay -S cloudflare-warp-bin --noconfirm")
                print("\n[+] Kurulum tamamlandı. Servisi başlatmak gerekebilir: sudo systemctl enable --now warp-svc")
                
            elif "debian" in os_info or "ubuntu" in os_info:
                print("\n[*] Debian/Ubuntu tabanlı sistem tespit edildi. APT ile kuruluyor...")
                print("[!] Not: Cloudflare GPG anahtarı ve deposunun sisteme daha önceden eklenmiş olduğu varsayılmaktadır.")
                os.system("sudo apt update && sudo apt install cloudflare-warp -y")
                
            elif "fedora" in os_info:
                print("\n[*] Fedora tespit edildi. DNF ile kuruluyor...")
                os.system("sudo dnf install cloudflare-warp -y")
                
            else:
                print("\n[-] Desteklenmeyen veya tanımlanamayan Linux dağıtımı. Lütfen warp-cli paketini manuel kurun.")
                
        except FileNotFoundError:
            print("\n[-] '/etc/os-release' dosyası okunamadı. Lütfen WARP'ı manuel kurun.")
            
    elif os_name == "Darwin":
        print("\n[*] macOS tespit edildi. Homebrew ile kuruluyor...")
        os.system("brew install --cask cloudflare-warp")
        
    else:
        print(f"\n[-] {os_name} işletim sistemi için otomatik kurulum desteklenmiyor.")

def manage_warp():
    print("\n[*] Cloudflare WARP durumu kontrol ediliyor...")
    
    if check_warp_installed():
        print("[+] WARP sistemde kurulu!")
        print("[*] WARP bağlantısı başlatılıyor...")
        subprocess.run(["warp-cli", "connect"], capture_output=True)
        print("[+] Trafik şu an Cloudflare üzerinden tünelleniyor. Hız kısıtlamaları aşıldı.")
    else:
        print("[-] Cloudflare WARP (warp-cli) bilgisayarında bulunamadı.")
        ans = input("[?] WARP'ı otomatik olarak indirmemi ve kurmamı ister misin? (E/H): ")
        if ans.lower() == 'e':
            install_warp()
        else:
            print("[!] WARP kurulumu iptal edildi.")

def main_menu():
    tc, sifre = load_credentials() 
    
    while True:
        print_banner()
        print(f"[*] Aktif Kullanıcı TC: {tc[:3]}********") 
        print("\nSeçenekler:")
        print("  [1] GSBWIFI Ağına Bağlan (Agresif Login)")
        print("  [2] Ağa Bağlan ve Cloudflare WARP'ı Aktif Et (Bypass)")
        print("  [3] Cloudflare WARP Kontrol / Kurulum")
        print("  [0] Çıkış\n")
        
        choice = input(">> Seçiminiz: ")
        
        if choice == '1':
            aggressive_login(tc, sifre)
            input("\nMenüye dönmek için Enter'a bas...")
            
        elif choice == '2':
            success = aggressive_login(tc, sifre)
            if success:
                time.sleep(1) 
                manage_warp()
            input("\nMenüye dönmek için Enter'a bas...")
            
        elif choice == '3':
            manage_warp()
            input("\nMenüye dönmek için Enter'a bas...")
            
        elif choice == '0':
            print("\n[!] Çıkış yapılıyor. Kendine iyi bak!")
            break
        else:
            print("\n[-] Geçersiz seçim, tekrar dene.")
            time.sleep(1)

if __name__ == "__main__":
    main_menu()
