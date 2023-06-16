import socket

TARGET_IP = '10.19.20.98'
TARGET_PORT = 56479

def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print("Hostname :  ", host_name)
        print("IP : ", host_ip)
        return host_name, host_ip

    except:
        print("Unable to get Hostname and IP")
        return "",""
 
def main():
    global TARGET_IP, TARGET_PORT

    hostname, ip = get_Host_name_IP()
    
    message = "BYE_" + hostname + " " + ip
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    client.connect((TARGET_IP, TARGET_PORT))
    client.send(message.encode())
    client.close()

if __name__ == "__main__":
    main()

