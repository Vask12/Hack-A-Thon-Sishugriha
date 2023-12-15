import pygame
import enter
from sprites import Button
from config import *
import custom


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Completing the Square")


background = pygame.image.load("images/background1.jpg")

play = Button(
    250,
    300,
    200,
    35,
    get_titlefont(35).render(">PLAY", True, BLACK),
    get_titlefont(35).render(">PLAY", True, RED),
)
eqn = Button(
    250,
    400,
    300,
    35,
    get_titlefont(30).render(">CUSTOM EQUATION", True, BLACK),
    get_titlefont(30).render(">CUSTOM EQUATION", True, RED),
)
gen = Button(
    250,
    200,
    300,
    35,
    get_titlefont(30).render(">TUTORIAL", True, BLACK),
    get_titlefont(30).render(">TUTORIAL", True, RED),
)


def main_menu(screen: Surface):
    screen.blit(
        get_titlefont(40).render("COMPLETING THE SQUARE", True, BLACK), (100, 100)
    )
    play.draw(screen)
    eqn.draw(screen)
    gen.draw(screen)


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play.clicked(pygame.mouse.get_pos()):
                    enter.main(screen, clock)
                if eqn.clicked(pygame.mouse.get_pos()):
                    custom.main(screen, clock)
                if gen.clicked(pygame.mouse.get_pos()):
                    enter.main(screen, clock, 1)

        screen.blit(background, (0, 0))

        # display_s(screen)
        main_menu(screen)
        # enter(screen, "x\u00b2 + 2x = 15")

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
