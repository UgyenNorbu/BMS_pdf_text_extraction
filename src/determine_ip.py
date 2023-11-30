import socket
import requests

def get_local_ip():
    try:
        # Connect to an external server to determine the local IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except socket.error:
        return None

def determine_login_url():
    local_ip = get_local_ip()

    if local_ip:
        # Check if the local IP falls within a specific range for your office LAN
        if local_ip.startswith("192.168.20."):
            return "http://192.168.20.83/bms/public/p"
        else:
            return "http://202.144.157.83/bms/public/p"
    else:
        # Default to the internet URL if local IP cannot be determined
        return "http://202.144.157.83/bms/public/p"

# Get the appropriate login URL
login_url = determine_login_url()
