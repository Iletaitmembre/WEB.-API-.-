import os
import sys
import pygame
import requests

pygame.init()
screen = pygame.display.set_mode((650, 450))
pygame.display.set_caption('Maps API')

# ДАННЫЕ
params = {"ll": ",".join(["37.6521910", "55.6482380"]),
          "spn": ",".join(["0.002", "0.002"]),
          "z": 16,
          "l": "map",
          "size": ",".join(["650", "450"])
          }


# ДАННЫЕ


def terminate():
    pygame.quit()
    sys.exit()


def map():
    global params
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=params)

    map = "map.png"
    try:
        with open(map, "wb") as file:
            file.write(response.content)
    except IOError:
        print("Ошибка")
        exit()
    return map


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(map_file)
                terminate()
            if pygame.key.get_pressed()[pygame.K_LEFT]:
                pass
            if pygame.key.get_pressed()[pygame.K_RIGHT]:
                pass
            if pygame.key.get_pressed()[pygame.K_UP]:
                pass
            if pygame.key.get_pressed()[pygame.K_DOWN]:
                pass
        map_file = map()
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()
