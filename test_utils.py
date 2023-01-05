import socket

from config import POWER_SUPPLY_HOST, POWER_SUPPLY_PORT


def ps_run():
    sock = socket.socket()
    sock.bind((POWER_SUPPLY_HOST, POWER_SUPPLY_PORT))

    sock.listen(1)
    conn, address = sock.accept()
    print(f'PS connected with {address}')

    try:
        while True:
            data = conn.recv(1024)
            print(f'Request: {data}')
            if not data:
                break

            conn.sendall('4.10466677,-3.13684184,1.75743178\n'.encode())
            print(f'Response: 4.10466677,-3.13684184,1.75743178\n')
    except:
        pass
    finally:
        sock.close()


if __name__ == '__main__':
    ps_run()
