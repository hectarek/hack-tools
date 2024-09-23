import socket
from threading import Thread

def port_scan(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Timeout for the socket connection
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port}: Open")
        sock.close()
    except Exception as e:
        print(f"Error scanning port {port}: {e}")

def main():
    host = input("Enter the target host IP address: ")
    start_port = int(input("Enter the start port number: "))
    end_port = int(input("Enter the end port number: "))
    
    threads = []
    for port in range(start_port, end_port + 1):
        t = Thread(target=port_scan, args=(host, port))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    main()