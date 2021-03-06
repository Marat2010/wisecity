'''
Описание задачи

Контекст:
Есть счетчик тепла. Счетчик тепла ставится в квартиру и позволяет получать сколько тепла было потреблено квартирой.
Счетчик измеряет температуру воды на входе в квартиру и температуру воды на выходе из квартиры.
Имея эти данные и объем воды, который прошел через квартиру, счетчик расчитывает сколько именно энергии было потреблено квартирой для отопления.

Счетчик позволяет получать с него данные удаленно, передавая команды по проводному интерфейсу (RS-485),
в ответ на эти команды счетчик возвращает результат выполнения команды (например, текущие показания). 
Команды имеют определенную структуру и описаны в pdf-файле, приложеном к письму.

Среди команд есть команда для получения текущих показаний. В pdf-файле есть описание команды и ответа счетчика в разделе
“3. Чтение текущих значений по измерительным каналам.”

Мы сформировали байтовую последовательность для получения текущих показаний, которую отправили счетчику.
Байтовая последовательность команды: 02 27 21 35 01 0e fc 3f 08 00 ba 1c 49 73
На эту команду счетчик ответил такой байтовой последовательностью: 
02 27 21 35 01 3e 95 13 61 42 c3 5b 36 42 48 df 2a 41 81 36 1e 3b 37 d1 80 41 89 3b c1 44 66 30 6a 3e ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff ff c7 3f 6a 3e 6c 2d 00 00 ba 1c 57 d2

Задача:
Разобрать ответ от счетчика на основе документации.
Результатом выполнения задачи должна быть функция, которая принимает на вход байтовую последовательность ответа счетчика, и возвращает значения текущих показаний счетчика в человеко-читаемом виде.
'''



request_bytes = bytearray([0x02, 0x27, 0x21, 0x35, 0x01, 0x0e, 0xfc, 0x3f, 0x08, 0x00, 0xba, 0x1c, 0x49, 0x73])
response_bytes = bytearray([
    0x02, 0x27, 0x21, 0x35, 0x01, 0x3e, 0x95, 0x13, 0x61, 0x42, 0xc3, 0x5b, 0x36, 0x42, 0x48, 0xdf, 0x2a, 0x41, 0x81,
    0x36, 0x1e, 0x3b, 0x37, 0xd1, 0x80, 0x41, 0x89, 0x3b, 0xc1, 0x44, 0x66, 0x30, 0x6a, 0x3e, 0xff, 0xff, 0xff, 0xff,
    0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xc7, 0x3f, 0x6a, 0x3e, 0x6c, 0x2d, 0x00,
    0x00, 0xba, 0x1c, 0x57, 0xd2
])

"""
Ответ, который у нас получился при разборе данного ответа от счетчика

{   
    'consumption': 0.229,
    'energy': 16.102,
    'energyConsumption': 0.229,
    'impInput1': 0,
    'impInput2': 0,
    'impInput3': 0,
    'impInput4': 0,
    'normalWorkTime': 0.0,
    'power': 0.002,
    'sensorId': '2272135',
    'temperatureDiff': 10.68,
    'temperatureFlow': 56.269,
    'temperatureReturn': 45.59,
    'volume': 1545.86
}

"""


def parse_response(response: bytearray) -> dict:
    '''Ваша реализация здесь'''
    return {}



# результат


print(parse_response(response_bytes))
