import socket

from main import main


def set_up_ps():
    s = socket.socket()
    s.bind(('127.0.0.1', 9090))
    s.listen(1)

    print(f'PS up on ')

    while True:
        data = s.recv(1024)
        print(data)
        if not data:
            break
        s.send(f'ANSWER: {data}')

    s.close()


def test_commands():


    """
    тесты, проверящие, что в результате вызова метода выдаются правильные команды через tcp-ip


    Поднять клиент имитирующий источник
    подключиться коннектором к нему
    послать команду коннектором
    проверить на клиенте, что пришла именно та комманда
    """

    set_up_ps()
    main()
