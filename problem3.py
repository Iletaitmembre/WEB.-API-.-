import os
import sys
import pygame
import requests
import time

pygame.init()
screen = pygame.display.set_mode((650, 450))
pygame.display.set_caption('Maps API')

# ДАННЫЕ
ll = [37.6521910, 55.6482380]
params = {"ll": ",".join([str(el) for el in ll]),
          "z": 16,
          "l": "map",
          "size": ",".join(["650", "450"])
          }


# ДАННЫЕ


def terminate():
    pygame.quit()
    sys.exit()


def map():
    global params, ll
    params["ll"] = ",".join([str(el) for el in ll])
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=params)
    try:
        with open("map.png", "wb") as file:
            file.write(response.content)
    except Exception:
        print("Ошибка")
        exit()
    return "map.png"


def main():
    global params, ll
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(map_file)
                terminate()
            if pygame.key.get_pressed()[pygame.K_PAGEDOWN]:
                if params["z"] > 2:
                    params["z"] -= 1
                    if not (85 >= ll[1] + 1.5 * 0.008 * (2 ** (15 - params["z"]))):
                        ll[1] = -85 + 0.008 * (2 ** (15 - params["z"])) / 2
                    if not (ll[1] + 1.5 * 0.008 * (2 ** (15 - params["z"])) >= -85):
                        ll[1] = 85 - 0.5 * 0.008 * (2 ** (15 - params["z"]))
            if pygame.key.get_pressed()[pygame.K_PAGEUP]:
                if params["z"] < 19:
                    params["z"] += 1
            if pygame.key.get_pressed()[pygame.K_UP]:
                if 85 >= ll[1] + 1.5 * 0.008 * (2 ** (15 - params["z"])) >= -85:
                    ll[1] += 0.008 * (2 ** (15 - params["z"]))
                else:
                    ll[1] = -85 + 0.008 * (2 ** (15 - params["z"])) / 2
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                if 85 >= ll[1] - 1.5 * 0.008 * (2 ** (15 - params["z"])) >= -85:
                    ll[1] -= 0.008 * (2 ** (15 - params["z"]))
                else:
                    ll[1] = 85 - 0.5 * 0.008 * (2 ** (15 - params["z"]))
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                if 180 >= ll[0] + 1.5 * 0.008 * (2 ** (15 - params["z"])) >= -180:
                    ll[0] += 0.008 * (2 ** (15 - params["z"]))
                else:
                    ll[0] = -180 + 0.008 * (2 ** (15 - params["z"])) * 0.5
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                if 180 >= ll[0] - 1.5 * 0.008 * (2 ** (15 - params["z"])) >= -180:
                    ll[0] -= 0.008 * (2 ** (15 - params["z"]))
                else:
                    ll[0] = 180 - 0.008 * (2 ** (15 - params["z"])) * 0.5
        screen.fill("Black")
        map_file = map()

        try:
            screen.blit(pygame.image.load(map_file), (0, 0))
            pygame.display.flip()
        except Exception:
            print("Ошибка в запросе! Запрос:",
                  requests.get("http://static-maps.yandex.ru/1.x/", params=params).url)
            time.sleep(3)


if __name__ == "__main__":
    main()
