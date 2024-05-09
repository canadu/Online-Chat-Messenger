import socket
IP_ADDR = '0.0.0.0'
PORT = 9001
MAX_BYTE = 4049

# udpで接続
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f'接続開始します。{IP_ADDR}')

sock.bind((IP_ADDR, PORT))

try:
    while True:
        
        try:
            # 一度に最大4096バイトを処理する
            message, cli_addr = sock.recvfrom(MAX_BYTE)
            
            client_data = message.decode(encoding='utf-8')
            
            print('from username > ' + client_data, cli_addr)
            
            if message:
                response = 'hello > ' + client_data
                sock.sendto(response.encode(encoding='utf-8'), cli_addr)
            else:
                print('no data from', IP_ADDR)
                break
            
        except Exception as e:
            print('エラー > ' + str(e))
            break
        except KeyboardInterrupt:
            sock.close()
            break
                
except Exception as ex:
    print(ex)
finally:
    sock.close()
    