import socket
IP_ADDR = '0.0.0.0'
PORT = 9001
MAX_BYTE = 4049

# UNIXドメインソケットとデータグラム（非接続）ソケットを作成します
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        print('ユーザー名を入力してください')
        username = input()
        if username != '':
            name_length = len(username)
            username = str(name_length) + username
            send_len = sock.sendto(username.encode('utf-8'), (IP_ADDR, PORT))

            print('Waiting response from server')
            rx_message, addr = sock.recvfrom(MAX_BYTE)
            print(f"[Server]:{rx_message.decode(encoding='utf-8')}")
        else:
            print('closing socket')
            sock.close()
            print('done')
            break
        
    except KeyboardInterrupt:
        print('closing socket')
        sock.close()
        print('done')
        break          


