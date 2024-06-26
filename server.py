import socket
import time

# ブロードキャストするときは空文字
IP_ADDR = ''
PORT = 9001
MAX_BYTE = 4049
TIME_OUT = 60

clients = []

# udpで接続
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f'接続開始します。{IP_ADDR}')

sock.bind((IP_ADDR, PORT))

send_time = time.time()

try:

    while True:
        
        try:
            
            # 一度に最大4096バイトを処理する
            data, addr = sock.recvfrom(MAX_BYTE)
            
            # ヘッダーからユーザー名長を取得
            username_length = int.from_bytes(data[:1], 'big')
    
            # ユーザー名とメッセージを分離
            username = data[1:username_length+1].decode('utf-8')
            message = data[username_length+1:].decode('utf-8')
            
            # 現在時刻を取得
            current_time = time.time()
            
            # メッセージの受信時間を保持
            client_info = (addr, username, send_time)
            
            client_found = False
            
            for i, client in enumerate(clients):
                # ある場合
                if client[:2] == client_info[:2]:
                    clients[i] = client_info
                    client_found = True
                    break
            if not client_found:
                # ない場合
                clients.append(client_info)
                print(f'New client connected: {username}')
                                
            print(f"> from {username} > {message}", addr)
            
            if data:
                
                # 接続中のクライアントに送信
                for client in clients[:]:
                    
                    # 最後の投稿から差分と現在時刻の差分を取得し、メッセージ送信対象か判定する
                    client_addr, client_username, last_msg_time = client
                    
                    if time.time() - last_msg_time > TIME_OUT:
                        clients.remove(client)
                        print(f'Client {client_username} timed out')
                    else:
                        # ヘッダーを作成
                        username_length = len(client_username.encode('utf-8'))
                        header = username_length.to_bytes(1, 'big') + client_username.encode('utf-8')
                
                        # メッセージにヘッダーを付与する
                        data = header + message.encode('utf-8')                
                
                        c_addr, c_port = client_addr
                    
                        sock.sendto(data, (c_addr, c_port))
                    
            else:
                print('no data from', IP_ADDR)
                break
            
        except KeyboardInterrupt:
            print('Interrupted.')
            sock.close()
            break
        
        except socket.error:
            print('Has error occurred.')
            sock.close()
            break
        
except Exception as ex:
    print(ex)
finally:
    sock.close()
    