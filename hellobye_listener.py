import socket
import re
import json
from os import path

FILEPATH = "autoscale.json"

def updater(action, hostname, ip):
    targets = []
    if path.isfile(FILEPATH) is False:
        print("[ERROR] File not found")
    else:
        with open(FILEPATH) as file:
            targets = json.load(file)
            print("[INFO] BEFORE append:\n",targets)
            ip = ip + ":9100"
            hostname = hostname[:len(hostname)-5] # REMOVE SUFFIX FOR AUTOSCALED SERVERS

            if action == "HELLO":
                targets.append({
                    "targets": [
                        ip
                    ],
                    "labels": {
                        "job": hostname
                    }
                })
                print("\n[INFO] AFTER append:\n",targets)
                with open(FILEPATH, 'w') as json_file:
                    json.dump(targets, json_file, 
                                        indent=4,  
                                        separators=(',',': '))
                
                print('[INFO] Successfully appended to the JSON file')

            elif action == "BYE":
                for idx, obj in enumerate(targets):
                    target = re.sub("['\[\]]","",str(obj['targets']))
                    if target == ip:
                        targets.pop(idx)
                
                print("[INFO] AFTER append:",targets)
                with open(FILEPATH, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(targets, indent=2))
                
                print('[INFO] Successfully appended to the JSON file')


def main():
    bind_ip = "0.0.0.0"
    bind_port = 56479    

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((bind_ip,bind_port))

    server.listen(5)
    print("[INFO] Listening on ", bind_ip, ":", bind_port)

    try:
        while True:
            client, address = server.accept()
            print("[INFO] Connected with : ", address[0], address[1])
            
            message = client.recv(1024).decode()
            hostname = ""
            ip = ""

            if (re.search(r'^HELLO_', message)):
                space = message.find(' ')
                hostname = message[6:space]
                ip = message[space+1:]

                updater("HELLO", hostname, ip)
                print("[INFO] HELLO received from",hostname,"[",ip,"]")

            elif (re.search(r'^BYE_', message)):
                space = message.find(' ')
                hostname = message[4:space]
                ip = message[space+1:]

                updater("BYE", hostname, ip)
                print("[INFO] BYE received from",hostname,"[",ip,"]")
            
            client.close()

    except Exception as e:
        print("[ERROR]",e)
        server.close()
        return


if __name__ == "__main__":
    main()