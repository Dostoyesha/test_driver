ОПИСАНИЕ
-------------------------
Драйвер для работы с промышленным 4-х канальным источником питания.
Поддерживает несколько операций с каналами, запрашивает телеметрию. Внешний API - REST, с источником общается по TCP/IP протоколу.

Документация на источник питания: https://www.gwinstek.com/en-global/products/downloadSeriesDownNew/14242/1737


КАК ПОЛЬЗОВАТЬСЯ
-------------------------

Запуск приложения из терминала:

`python main.py`

Запрос текущего состояния всех каналов питания. 
Указать хост и порт, на котором поднялся драйвер. Задать можно в `config.py` в `APP_API_HOST`, `APP_API_PORT`:

`curl -X GET http://127.0.0.1:8080/condition`

Пример ответа в json:
```
{
    'conditions': [
        {
            'channel': 1,
            'current': 4.10466677,
            'voltage': -3.13684184,
            'power': 1.75743178
        },
        {
            'channel': 2,
            'current': 4.10466677,
            'voltage': -3.13684184,
            'power': 1.75743178
        },
        {
            'channel': 3,
            'current': 4.10466677,
            'voltage': -3.13684184,
            'power': 1.75743178
        },
        {
            'channel': 4,
            'current': 4.10466677,
            'voltage': -3.13684184,
            'power': 1.75743178
        }
    ]
}
```

Запрос на отключение канала питания (параметр ch - номер канала): 

`curl -X POST http://127.0.0.1:8080/channel_off?ch=1`

Лог регулярного опроса телеметрии каналов записывается в `logs/telemetry_log.txt`.
Период в секундах, через который происходит опрос можно задать в `config.py` `TELEMETRY_REQUEST_TASK_SEC_PERIOD`. По умолчанию стоит 10 секунд.
Задача реализована в корутине `task_get_condition(ps_conn)`.

ЧТО СДЕЛАНО
-------------------------

В `handlers.py` лежат апи, обрабатывающие запросы и реализующие бизнес-алгоритмы.
Не успела доделать метод включения канала питания с заданными параметрами (пункт 3 в задании).

Не нашла в документации адекватный пример ответа устройства на запрос телеметрии.
Предположила, что на команду 
`MEASure1:ALL?\n`
он выглядит так (ток, напряжение и мощность соответственно):
`4.10466677,-3.13684184,1.75743178\n`

Тесты написала только проверяющие обработку данных с источника (пункт 3 в задании). Лежат в `tests/test_data_processing_from_ps.py`.

Локально для разработки и тестирования прохождения запросов поднимала сервер-имитацию источника питания. Оставила его в `test_utils.py` `ps_run()`.
Написать тесты не успела.

ЧТО БЫ СДЕЛАЛА ЕЩЕ
-------------------------

1. Добавила бы больше нормальных логов: запуск/ошибки приложения, коннект/дисконект к источнику питания.
2. Потестировав на реальном источнике питания, обернула бы код больше в try/except с конкретными классами ошибок, а не общим Exception. 
И в целом, так как делала вслепую, где-то код может быть неэффективным.
3. Предполагаю, что у драйвера большой потенциал использования с разными источниками, отличающимися количеством каналов и возможно алгоритмом выполнения комманд. А также использования множеством клиентов по REST. Можно притянуть уже вебфреймворк, например, fastapi, чтобы в дальнейшем упростить разработку: снять вопросы по обработке и валидации запросов и т.д.. 

ЗАДАНИЕ
-------------------------

Разработать приложение («драйвер») для работы с промышленным 4-х канальным источником питания со следующими возможностями:

1. Постоянный опрос телеметрии источника питания (текущее напряжение, ток, мощность по каждому каналу);
2. Логгирование телеметрии - в файл. Каждое измерение - с меткой времени;
3. Имеет команду на включение канала питания (параметры: номер канала питания, заданное напряжение, заданный ток);
4. Имеет команду на отключение канала питания(параметры: номер канала питания);
5. Имеет команду на запрос текущего состояния всех каналов питания (время измерения, значение напряжений, токов по всем каналам питания). Выходной формат - json.
6. Внешний API для программы - REST
7. Использовать asyncio

ПО обменивается с источником питания по tcp/ip по протоколу scpi (текстовый формат с разделителем \n).

Алгоритм включения канала питания. Выдать команды:
1. Задать ток для канала питания (подсистема SOURCE)
2. Задать напряжение для канала питания (подсистема SOURCE)
3. Включить выход канала питания (подсистема OUTPUT)

Алгоритм отключения канала питания:
1. Отключить выход канала питания (подсистема OUTPUT)

Алгоритм опроса канала питания:
1. Запросить состояние канала питания (подсистема MEASURE)

Документация на источник питания: https://www.gwinstek.com/en-global/products/downloadSeriesDownNew/14242/1737

Тесты предлагается разбить на 3 части:
1. Тесты, проверяющие, что при обращении на url будет вызываться нужный метод нужного класса (типа роутинг до методов)
2. Тесты, проверящие, что в результате вызова метода выдаются правильные команды на через tcp-ip
3. Тесты, проверяющие корректность обработки данных, полученных от прибора

Примечание: во время тестов не должно происходить передачи данных по сети. Прибор “мокаем”.
