import socket
import threading
import datetime

IP_ADDR = '0.0.0.0'
PORT = 9001
MAX_BYTE = 4049

server_addr  = (IP_ADDR, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# サーバーからのメッセージを受信
def receive_messages():
    while True:
        
        rx_data, addr = sock.recvfrom(MAX_BYTE)
        
        # ヘッダーからユーザー名長を取得
        username_length = int.from_bytes(rx_data[:1], 'big')
    
        # ユーザー名とメッセージを分離
        username = rx_data[1:username_length+1].decode('utf-8')
        message = rx_data[username_length+1:].decode('utf-8')
        
        print(f"{username} > {message}")

# スレッドを開始
receive_thread = threading.Thread(target=receive_messages, daemon=True)
receive_thread.start()

print('ユーザー名を入力してください')
username = input()

if username != '':
    
    while True:

        try:
            
            message = input(' > ')
            
            # protocol_header()関数を用いてヘッダ情報を作成し、ユーザー名をヘッダーに設定
            username_length = len(username.encode('utf-8'))
            
            # ヘッダーを作成
            # to_bytes()メソッドを用いてバイナリに変換され、1つの64ビットバイナリに結合されます。
            header = username_length.to_bytes(1, 'big') + username.encode('utf-8')
                
            # メッセージにヘッダーを付与する
            data = header + message.encode('utf-8')                
                
            sock.sendto(data, server_addr)
                        
        except KeyboardInterrupt:
            print('closing socket')
            sock.close()
            print('done')
            break
        
else:
    sock.close()
    print('bye')