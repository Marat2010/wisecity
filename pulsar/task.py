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

import json


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


def package_split(package: bytearray) -> dict:  # Разбиение пакета
    addr = package[:4]  # ADDR - cетевой адрес устройства (4байта) в формате BCD, старшим байтом вперёд
    code_F = package[4]  # F - код функции запроса (1 байт);
    len_L = package[5]  # L - общая длина пакета (1 байт);
    data = package[6:-4]  # Либо DATA_IN(MASK) или DATA_OUT ...
    request_ID = package[-4:-2]  # ID - идентификатор запроса (любые 2 байта)
    crc16 = package[-2:]  # CRC16 - контрольная сумма (uint16_t) 2 байта младшим байтом вперёд.
    return {'ADDR': addr, 'F': code_F, 'L': len_L, 'CRC16': crc16, 'ID': request_ID, 'DATA': data}


def get_channel_name(channel_number: int) -> str:
    """ Получение имени канала по номеру """
    ch_name = {3: 'temperatureFlow',  # Температура под. [°C]
               4: 'temperatureReturn',  # Температура обр. [°C]
               5: 'temperatureDiff',  # Перепад температур, [°C]
               6: 'power',  # Мощность [Гкал/ч]
               7: 'energy',  # Энергия [Гкал]
               8: 'volume',  # Объем [м^3]
               9: 'consumption',  # Расход [м^3/ч]
               10: 'impInput1',  # Имп.вход 1, [м^3]
               11: 'impInput2',  # Имп.вход 2, [м^3]
               12: 'impInput3',  # Имп.вход 3, [м^3]
               13: 'impInput4',  # Имп.вход 4, [м^3]
               14: 'energyConsumption',  # Расход (по энергии) [м3/ч]
               20: 'normalWorkTime'  # Время нормальной работы [ч]
               }
    return ch_name[channel_number]


def parsing_request_mask(mask: bytearray) -> tuple:
    """ Парсинг маски каналов в запросе, полчуение списка (кортежа) номеров канала
        IN: mask, type(mask) => bytearray(b'\xfc?\x08\x00') <class 'bytearray'>
                    (fc 3f 08 00) => [252, 63, 8, 0] => [0, 8, 63, 252]
        => mask_bin => ['00000000', '00001000', '00111111', '11111100']
        => '00000000000010000011111111111100' => чтение с конца - mask_bin[::-1]
        OUT: => (3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 20)
    """
    mask_bin = [(bin(i)[2:]).rjust(8, '0') for i in reversed(mask)]
    mask_bin = ''.join(mask_bin)  # => '00000000000010000011111111111100'
    ch_list = []  # список каналов, будем добавлять номера в них
    [ch_list.append(_ + 1) for _, bit_val in enumerate(mask_bin[::-1]) if bit_val == '1']
    # ch_list => [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 20]
    return tuple(ch_list)


def data_split(data_bytes: bytearray) -> tuple:
    """ Разбиение данных "DATA" для каждого параметра (по 4 байта для канала) """
    values = []

    number_of_value = int(len(data_bytes)/4)  # Кол-во параметров(каналов) значений (одно значение = 4 байта)
    for i in range(1, number_of_value+1, 1):  # Берем сразу по 4 байта [0:4], [4:8] [8:12] ...
        values.append(tuple(data_bytes[i*4-4:i*4]))  # => [(149, 19, 97, 66), ... ]

    return tuple(values)


def check_package(package: dict) -> bool:
    """ Проверка пакета на соответствие кол-ва байт.
    Кол-во байтов в параметре "L" и фактическая длина пакетов данных в "DATA".
     Проверка что данные по 4 байта (кратность 4) """
    if int(package['L'])-10 != int(len(package['DATA'])) or\
            int(len(package['DATA'])) % 4 != 0:                  # сверка кол-ва байт
        raise ValueError('!!! Не верное кол-во байтов в данных!!!')
    return True


def get_readable_data(channel_data: tuple) -> float:
    """ Получает кортеж их 4-х байт, возвращает значение показания счетчика в человеко-читаемом виде.
    Формула вычисления взята отсюда: https://www.softelectro.ru/ieee754.html .
        Чтобы записать число в стандарте IEEE 754 или восстановить его, необходимо знать три параметра:
            S- бит знака (31-й бит)
            E- смещенная экспонента (30-23 биты)
            M - остаток от мантиссы (22-0 биты) """

    list_bytes = [(bin(i)[2:]).rjust(8, '0') for i in reversed(channel_data)]
    # переводим в двоичный формат младшим байтом вперёд
    # (149, 19, 97, 66) => list_bytes = ['01000010', '01100001', '00010011', '10010101']

    bits = ''.join(list_bytes)  # => 01000010011000010001001110010101

    sign_bit_S = int(bits[0])  # бит знака (31-й бит => 0 бит). => "=0"
    exp_E = int(bits[1:9], 2)  # Смещенная экспонента E (30-23 биты => 1-8 биты). => "=132"
    mantissa_M = int(bits[9:], 2)  # Остаток от мантиссы M (22-0 биты => 9-30 биты). => "=6362005"

    value = ((-1) ** sign_bit_S) * 2**(exp_E - 127) * (1 + mantissa_M / 2**23)  # формула расчета

    if value < 1e-38 or value > 1e+38:  # Отсечь -6.805646...e+38 => -∞ (0xff, ...) и 7.1333939...e-39 => 0 (0x00,  ...)
        value = 0.0
    value = round(value, 3)
    return value


def parse_response(response: bytearray) -> dict:
    """Ваша реализация здесь"""
    request_package = package_split(request_bytes)  # Распаковка пакета ЗАПРОСА (request) для получение маски
    channels = parsing_request_mask(request_package['DATA'])  # Получение кортежа номеров каналов из пакета запроса

    package = package_split(response)  # Распаковка пакета ОТВЕТА (response)

    check_package(package)  # Проверка в пакете кол-ва байт данных, иначе "raise ValueError"
    # функцию "check_package" необходимо расширить для проверки адресов "ADDR", кода функции "F" в двух
    # пакетах (request, response), вычисление CRC16.

    channels_data = data_split(package['DATA'])  # Разбиение данных "DATA" для каждого параметра (4 байта на канал)

    channels_values = []  # список показаний счетчика в человеко-читаемом виде
    [channels_values.append(get_readable_data(_)) for _ in channels_data]  # => [56.269, 45.59, 10.68, ..., 0.0]

    number_value = tuple(zip(channels, channels_values))  # кортеж (номер канала-значение) => ((3, 56.269)... (20, 0.0))

    sensorId = ''.join([hex(_)[2:] for _ in package['ADDR']])  # адрес устройства (4байта) в формате BCD
    result = {'sensorId': sensorId}  # Результируюший словарь

    for i, ch in enumerate(number_value):  # Добавление в словарь значений каналов
        result[get_channel_name(ch[0])] = channels_values[i]  # по ключу (номер канала) вытаскиваем имя канала

    return result


# ------------- результат -----------------------------
if __name__ == '__main__':
    request = parse_response(response_bytes)
    print(f'***** РЕЗУЛЬТАТ **** :')
    print(json.dumps(request, indent=4, sort_keys=True))


# -------------------------------------------------------------
    # import pprint
    # pprint.pprint(request)
# -------------------
# mask_bin => ['00000000', '00001000', '00111111', '11111100']
#     # ----- Временно для просмотра в разнох форматах ----
# values_h = []
# values_b = []
#     val_h = (hex(b) for b in data_bytes[(4*i-4):(4*i)])  # => ('0x95', '0x13', '0x61', '0x42')
#     values_h.append(tuple(val_h))
#
#     val_b = bytearray(b for b in data_bytes[(4*i-4):(4*i)])  # => bytearray(b'\x95\x13aB')'
#     values_b.append(val_b)
#
# print(f"-- Value в 16-ричном: {values_h}")
# print(f"-- Value в byte: {values_b}")
# value = ''
# list_bytes = [(bin(i)[2:]).rjust(8, '0') for i in channel_data]
# bits = ''.join(list_bytes)[::-1]
# print(f'==== 16h: {channel_data}, обратный порядок: {tuple(reversed(channel_data))}')
# print(f'==== 2-ый: {list_bytes}, склеинные биты: {bits}', len(bits))

# exp_E = bits[23:30]
# exp_E = int(bits[23:31], 2)
# exp_E = int(bits[23:31][::-1], 2)

# print(f'==== 2-ый склеинный: {"".join(res)}, обратный порядок: {"".join(tuple(reversed(res)))}')

# res = []
# for b in channel_data:   # [::-1]
#     res.append((bin(b)[2:]).rjust(8, '0'))
# value = []  # список каналов, будем добавлять номера в них
# [value.append(_ + 1) for _, bit_val in enumerate(mask_bin[::-1]) if bit_val == '1']
# print(f'==VALUE: {value}')
# print(f"Кол-во байтов в L (L-10): {int(package['L']) - 10}, в самих даннных: {int(len(package['DATA']))}")

# print(f' --- Кол-во параметров значений: {number_of_value}')
# print(f' --- Кортеж параметров : {values}')
# print(f' === Пакет ответа: {package} \n\t === Длина пакета: {len(package)}')
# print(f'=== Номера каналов: {channels}')
# for _ in channels_data:
#     channels_values.append(get_readable_data(_))
# print(f"=== ZIP: {tuple(z1)}")
# print(f'==Cетевой адрес: {sensorId}')
# print(f"==Канал: {ch[0]:2} : {get_channel_name(ch[0]):20} = {channels_values[i]} => {ch[1]}")

# --------------------------------------------------------

# # ---------------- получение десятичных данных ------------------
# print(' ---------------- получение десятичных данных ------------------')
# data_decimal = get_decimal_data(val[4:8])
# print(f'== десятичное : {data_decimal}')
# print('--0-- ', mask, type(mask))  # bytearray(b'\xfc?\x08\x00') <class 'bytearray'>


# print('----------- Ответ------------------------------------------')
# parse = parse_response(response_bytes)
# print(parse, '\n')
# val = parse['DATA']
# print(f' данные: {val}')

# ------------------------------------------------------------------
# val = response_bytes[6:-4]  # можно не переводить в список ...?
# val
# raise Exception("!!! Не верное кол-во байтов в данных!!!")

# Разбивка по каналам, надо перевернуть мл.байт вперед

# number_of_channels = int(len(val)/4)
# new_data = []
# for channel in range(1, number_of_channels+1, 1):
#     print(channel, val[channel], tuple(val[channel*4-4:channel*4]))
#     new_data.append(tuple(val[channel*4-4:channel*4]))
# print('новый список', new_data)
# new_data.reverse()
# print('новый список перевернут', new_data)
# -----------------------------------------------------------------------
# raise Exception("Boo!")
# val_h = map(lambda b: hex(b), data_bytes[(i*4-4):(i*4)])  # генератор ( list(...) )
# val_h = (hex(b) for b in data_bytes[(4 * i - 4):(4 * i)])  # генератор ( [...] )
# val_b = bytes(b for b in data_bytes[(4*i-4):(4*i)])  # => b'\x95\x13aB'
# ----------------------------------------------
# print(f"--i: {i} , {(bin(i)[2:]).rjust(8, '0')}, {hex(i)} ")
# print(f'------ байтареа: {values}, 16-рич: {i}, двоич: {i}')
    # print(f'--3-- Кортеж каналов: {tuple(ch_list)}')

# number_of_channels = int(len(val)/4)
# new_data = []
# for channel in range(1, number_of_channels+1, 1):
#     print(channel, val[channel], tuple(val[channel*4-4:channel*4]))
#     new_data.append(tuple(val[channel*4-4:channel*4]))
# print('новый список', new_data)
# new_data.reverse()
# print('новый список перевернут', new_data)

# def get_decimal_data(data_bytes: bytearray):
# print('--1-- ', mask_bin)
# -----------------------------------------------
# print('----------- запрос временно ------------------------------------------')
# request = parse_response(request_bytes)
# print(f'*** Пакет запрос: {request}\n-----------------')

# -----------------------------------------------
# ----------------------------------------------
# input_as_uint32 = np.frombuffer(val[0:4])
# # input_as_uint32 = np.frombuffer(val[0:4], dtype='> u4')
# print(input_as_uint32)
# ----------------------------------------------
# print(f'-- значение: {val[4:8]}')
# print(f'-- Обрат значение: {request_mask_parse(val[4:8])}')
# ----------------------------------------------
# mask_ch = request['DATA']  # Маска каналов
# print(f'---- Маска каналов: {mask_ch}')
# print(f'Маска: {mask_ch}')
# print(f'---- Номера каналов: {request_mask_parse(mask_ch)}')
# ----------------------------------------------
# mask_list = [(bin(i)) for i in reversed(mask)]
# print(mask_list)
#
# mask_list = ''.join(mask_list).split('0b')
# mask_str = ''.join(mask_list)
# -----------------------------------------------
# for _, bit_val in enumerate(mask_bin[::-1]):
#     if bit_val == '1':
#         ch_list.append(_ + 1)
# -----------------------------------------------
# mask_bin = [f'{(bin(i)[2:]):>8}'.replace(' ', '0') for i in reversed(mask)]
# response_list = list(response)
# print(response_list)
# # addr = response_list[:4]  # проба со списком
# addr = response[:4]  # проба с bytearray, можно не переводить в список
# code_F = response_list[4]
# len_L = response_list[5]
# crc16 = response_list[-2:]
# req_ID = response_list[-4:-2]

# data_out:
# Для запроса: битовая маска запрашиваемых каналов (uint32_t) 4 байта, младшим байтом вперёд
# Для ответа: CH[n] - массив значений каналов, согласно установленным битам во входной маске,
# в формате IEEE 754 (float32_t) младшим байтом вперёд.

# data_out = response_list[6:-4]  # проба со списком
# data_out = response[6:-4]  # проба с bytearray, можно не переводить в список
# -----------------------------------------------
# list(reversed(new_data))
# tuple(reversed(new_data))
# ---------------------------------------------------------------

# 4.2 Преобразования числа формата 32 бит IEEE 754 в десятичное число
# Чтобы записать число в стандарте IEEE 754 или восстановить его, необходимо знать три параметра:
# S- бит знака (31-й бит)
# E- смещенная экспонента (30-23 биты)
# M - остаток от мантиссы (22-0 биты)
# Это целые числа которые записанные в числе IEEE 754 в двоичном виде.
#
# Приведём формулу для получения десятичного числа из числа IEEE754 одинарной точности:
#
# Формула для 32 нормализованных бит IEEE754  где F - десятичное число
# Проверяем наш пример:
# F =(-1)0∙2(134-127)∙(1+ 1810432 / 223)= 27∙(1+0,2158203125)=128∙1,2158203125=155,625