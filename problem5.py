import os
import sys
import pygame
import requests
import time

pygame.init()
screen = pygame.display.set_mode((900, 450))
pygame.display.set_caption('Maps API')


class Data:
    """
    данные
    """
    # карта
    pt = ''
    temp_tag = ''
    ll = [37.6521910, 55.6482380]
    map_params = {"ll": ",".join([str(el) for el in ll]),
                  "z": 5,
                  "l": "map",
                  "size": ",".join(["650", "450"]),
                  "pt": ""
                  }

    # для форм
    search_form = pygame.Rect(670, 400, 200, 50)
    input_form = pygame.Rect(670, 0, 210, 40)
    tag_form = pygame.Rect(670, 350, 200, 50)
    font = pygame.font.Font(None, 50)
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('blue')
    color = color_inactive
    active = False
    text = ''
    # поиск объектов с помощью геокодера яндекса

    geocoder_params = {"apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                       "format": "json",
                       "geocode": "",
                       "lang": "ru_RU",
                       "ll": ",".join([str(el) for el in ll]),
                       "results": 10
                       }
    # lля работы с метками и выбором нужного варианта поиска при совпадении
    data = False
    choice = []
    add_a_tag = False


def terminate():
    """
    завершает работу pygame при выходе из приложения
    """
    pygame.quit()
    sys.exit()


def map_image():
    """
    получение снимка карт с помощью api яндекса
    :return: имя файла с картинкой в формате .png
    """
    Data.map_params["ll"] = ",".join([str(el) for el in Data.ll])
    if Data.add_a_tag:
        Data.map_params["pt"] = Data.temp_tag
    else:
        Data.map_params["pt"] = Data.pt[:-1]

    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=Data.map_params)
    try:
        with open("map.png", "wb") as file:
            file.write(response.content)
    except Exception:
        print("Ошибка")
        exit()
    return "map.png"


def map_keys(event):
    """
    управление запросами api карт с помощью клавиш
    :param event: события в pygame
    """
    if Data.active:
        return
    if pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
        if Data.map_params["z"] > 2:
            Data.map_params["z"] -= 1
            if not (85 >= Data.ll[1] + 1.5 * 0.008 * (2 ** (15 - Data.map_params["z"]))):
                Data.ll[1] = 88 - 0.008 * (2 ** (15 - Data.map_params["z"])) / 2
            if not (Data.ll[1] + 1.5 * 0.008 * (2 ** (15 - Data.map_params["z"])) >= -85):
                Data.ll[1] = -88 + 0.5 * 0.008 * (2 ** (15 - Data.map_params["z"]))

    if pygame.key.get_pressed()[pygame.K_PAGEUP]:
        if Data.map_params["z"] < 19:
            Data.map_params["z"] += 1
    if pygame.key.get_pressed()[pygame.K_UP]:
        if 85 >= Data.ll[1] + 1.5 * 0.008 * (2 ** (15 - Data.map_params["z"])) >= -85:
            Data.ll[1] += 0.008 * (2 ** (15 - Data.map_params["z"]))
        else:
            Data.ll[1] = 88 - 0.008 * (2 ** (15 - Data.map_params["z"])) / 2
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        if 85 >= Data.ll[1] - 1.5 * 0.008 * (2 ** (15 - Data.map_params["z"])) >= -85:
            Data.ll[1] -= 0.008 * (2 ** (15 - Data.map_params["z"]))
        else:
            Data.ll[1] = -88 + 0.5 * 0.008 * (2 ** (15 - Data.map_params["z"]))
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if 180 >= Data.ll[0] + 1.5 * 0.008 * (2 ** (15 - Data.map_params["z"])) >= -180:
            Data.ll[0] += 0.008 * (2 ** (15 - Data.map_params["z"]))
        else:
            Data.ll[0] = -180 + 0.008 * (2 ** (15 - Data.map_params["z"])) * 0.5
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if 180 >= Data.ll[0] - 1.5 * 0.008 * (2 ** (15 - Data.map_params["z"])) >= -180:
            Data.ll[0] -= 0.008 * (2 ** (15 - Data.map_params["z"]))
        else:
            Data.ll[0] = 180 - 0.008 * (2 ** (15 - Data.map_params["z"])) * 0.5
    if pygame.key.get_pressed()[pygame.K_m] and event.type == pygame.KEYDOWN:
        layers = ["map", "sat", "sat,skl"]
        if Data.map_params["l"] == layers[2]:
            Data.map_params["l"] = layers[0]
        else:
            Data.map_params["l"] = layers[layers.index(Data.map_params["l"]) + 1]


def draw_forms():
    """
    рисует формы для поиска
    """
    pygame.draw.rect(screen, Data.color, Data.input_form, 1)
    text = Data.font.render(Data.text[-6:], True, pygame.Color('red'))
    screen.blit(text, (Data.input_form.x + 5, Data.input_form.y + 5))

    pygame.draw.rect(screen, pygame.Color('red'), Data.search_form)
    text = Data.font.render("Искать!", True, pygame.Color('white'))
    screen.blit(text, (Data.search_form.x + 35, Data.search_form.y + 10))


def object_search(event):
    """
    обработка действий клавиатуры и мыши при работе с геокодером
    :param event: события в pygame
    """
    if event.type == pygame.MOUSEBUTTONDOWN:
        if Data.input_form.collidepoint(event.pos):
            Data.active = 1 - Data.active
        else:
            Data.active = False
        if Data.search_form.collidepoint(event.pos) and Data.text:
            Data.data = geocoder_api(Data.text)
            geocoder_data_processing()
            Data.text = ''
            Data.add_a_tag = False
        for i in range(len(Data.choice)):
            if Data.choice[i].collidepoint(event.pos):
                change_ll(i)
        if Data.tag_form.collidepoint(event.pos):
            Data.add_a_tag = False
            Data.pt += Data.temp_tag + '~'
    Data.color = Data.color_active if Data.active else Data.color_inactive
    if event.type == pygame.KEYDOWN:
        if Data.active:
            if event.key == pygame.K_RETURN and Data.text:
                Data.data = geocoder_api(Data.text)
                geocoder_data_processing()
                Data.text = ''
                Data.add_a_tag = False
            elif event.key == pygame.K_BACKSPACE:
                Data.text = Data.text[:-1]
            else:
                Data.text += event.unicode


def geocoder_api(text):
    """
    получение данных о адресе с помощью api геокодера
    :param text: запрос
    :return: список с адресами и координатами
    """
    Data.geocoder_params["geocode"] = text
    Data.geocoder_params["ll"] = ",".join([str(el) for el in Data.ll])
    api_server = "http://geocode-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=Data.geocoder_params)
    if response.json()['response']['GeoObjectCollection']['featureMember']:
        return [(element["GeoObject"]['Point']["pos"], element["GeoObject"]['description'])
                if 'description' in element["GeoObject"]
                else (element["GeoObject"]['Point']["pos"], element["GeoObject"]['name'])
                for element in response.json()['response']['GeoObjectCollection']['featureMember']]
    else:
        # ничего не найдено
        return False


def geocoder_data_processing():
    """
    обработка данных, получаемых из функции geocoder_api
    (данные в формате json (response.json()['response']['GeoObjectCollection']['featureMember']))
    """
    if not Data.data:
        Data.data = ['Ничего не найдено!']
    else:
        Data.choice.clear()
        for i in range(len(Data.data)):
            temp = pygame.Rect(Data.input_form.bottomleft[0] - 30,
                               Data.input_form.bottomleft[1] + (i * 30) - 4, 30, 30)
            Data.choice.append(temp)


def geocoder_forms():
    """
    вывод полученной информации с геокодера; рисование кружочков (нажатие - выбор соответственного им места)
    """
    if Data.data == ['Ничего не найдено!']:
        text = pygame.font.Font(None, 32).render(Data.data[0], True, pygame.Color('green'))
        screen.blit(text, (Data.input_form.bottomleft[0], Data.input_form.bottomleft[1] + 30))
    else:
        for i in range(len(Data.data)):
            text = pygame.font.Font(None, 32).render(Data.data[i][1], True, pygame.Color('green'))
            screen.blit(text, (Data.input_form.bottomleft[0], Data.input_form.bottomleft[1] + (i * 30)))
            pygame.draw.circle(screen, pygame.Color("blue"),
                               (Data.choice[i].center[0], Data.choice[i].center[1]), 5)


def change_ll(i):
    """
    при нажатии кружочка около элемента списка переносит положение карты на ll элемента списка
    :param i: элемент списка в Data.data
    """
    if Data.data:
        Data.ll = [float(el) for el in Data.data[i][0].split()]
        Data.temp_tag = ",".join(Data.data[i][0].split()) + ",flag"
        Data.add_a_tag = True


def draw_add_a_tag_button():
    """
    рисует кнопку, нажатие которой сохраняет метку
    """
    pygame.draw.rect(screen, pygame.Color('violet'), Data.tag_form)
    text = pygame.font.Font(None, 32).render("Добавить", True, pygame.Color('white'))
    screen.blit(text, (Data.tag_form.x + 50, Data.tag_form.y + 5))
    text = pygame.font.Font(None, 32).render("Метку!", True, pygame.Color('white'))
    screen.blit(text, (Data.tag_form.x + 60, Data.tag_form.y + 25))


def color():
    """
    :return: цвет для запроса поверх карты
    """
    global screen
    r = 0
    g = 0
    b = 0
    for y in range(100):
        for x in range(100):
            r += screen.get_at((x, y))[0]
            g += screen.get_at((x, y))[1]
            b += screen.get_at((x, y))[2]
    r //= 10000
    g //= 10000
    b //= 10000
    # противоположный среднему не всегда читаем
    # return 255 - r, 255 - g, 255 - b, 1
    # преобразование цвета в серую шкалу, проверка: ближе ли он к черному или белому.
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    if y < 128:
        return "white"
    return "black"


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(map_file)
                terminate()
            # использование клавиш для управления картой
            map_keys(event)
            # набор текста для поиска объекта
            object_search(event)

        screen.fill("Black")
        draw_forms()

        map_file = map_image()
        try:
            screen.blit(pygame.image.load(map_file), (0, 0))
        except Exception:
            print("Ошибка в запросе! Запрос:",
                  requests.get("http://static-maps.yandex.ru/1.x/", params=Data.map_params).url)
            time.sleep(3)

        if Data.text:
            request = pygame.font.Font(None, 32).render(Data.text, True, pygame.Color(color()))
            screen.blit(request, (0, 0))
        if Data.data:
            geocoder_forms()
        if Data.add_a_tag:
            draw_add_a_tag_button()
        pygame.display.flip()


if __name__ == "__main__":
    main()
