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
            conn.sendall('4.10466677,-3.13684184,1.75743178\n'.encode())
    except Exception as error:
        print(f'Error: {error}')
    finally:
        sock.close()


if __name__ == '__main__':
    ps_run()
