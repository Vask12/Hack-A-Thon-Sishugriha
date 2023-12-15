import pygame
import random
from poly import P
from decimal import Decimal
from config import *
from sprites import MovableBox, TextBox, Button

pygame.init()

active_box: MovableBox = None
movable_boxes: list[MovableBox] = list()

textboxes: list[TextBox] = list()

_nextimg = pygame.image.load("images/nextbutton.png")
_nextimg2 = pygame.image.load("images/nextbuttonred.png")
next = Button(WIDTH - 100, HEIGHT - 100, 75, 75, _nextimg, _nextimg2)

background = pygame.image.load("images/background1.jpg")
eqn: P = None
rhs: P = None
lhs: P = None
magic: float = 0
allowed = True


def open(screen: Surface):
    screen.blit(
        get_titlefont(30).render("Hello", True, BLACK),
        (150, 100),
    )
    screen.blit(
        get_titlefont(30).render("Welcome to", True, BLACK),
        (125, 200),
    )
    screen.blit(
        get_titlefont(30).render("Completing the Square", True, BLACK),
        (100, 300),
    )


def close(screen: Surface):
    screen.blit(
        get_titlefont(50).render("Thank You!", True, BLACK),
        (300, 150),
    )


def lets(screen: Surface):
    screen.blit(
        get_font(30).render("Let's solve this equation:", True, BLACK),
        (100, 100),
    )
    screen.blit(
        get_font(50).render(str(eqn) + " = 0", True, BLACK),
        (100, 200),
    )


def represent(screen: Surface):
    global eqn, rhs, lhs, magic
    screen.blit(
        get_font(30).render("Let's Represent the Equation with Areas", True, BLACK),
        (150, 1),
    )

    if rhs is None and lhs is None:
        lhs = P([0, eqn.plist[1], eqn.plist[2]])
        rhs = P([-eqn.plist[0]])
        magic = Decimal(lhs.plist[1]) / Decimal(2)
    if len(movable_boxes) == 0:
        movable_boxes.append(MovableBox(25, 250, 200, 200, "x\u00b2", "x", "x", BLUE1))
        movable_boxes.append(
            MovableBox(
                300, 250, 150, 200, f"{lhs.plist[1]}x", "x", str(lhs.plist[1]), BLUE2
            )
        )
        movable_boxes.append(
            MovableBox(550, 250, 200, 200, str(rhs.plist[0]), "", "", "purple")
        )

    screen.blit(get_font(50).render("+", True, BLACK), (240, 345))
    display_boxes(screen)


def display_boxes(screen: Surface):
    display_eqn(screen)

    screen.blit(get_font(50).render("=", True, BLACK), (450, 300))

    for box in reversed(movable_boxes):
        box.draw(screen)


def display_eqn(screen):
    screen.blit(
        get_font(40).render(
            (str(lhs) + " = " + str(rhs)).replace(" ", "  "), True, BLACK
        ),
        (75, 100),
    )


def half(screen: Surface):
    screen.blit(
        get_font(30).render("Right Click the second term to halve it", True, BLACK),
        (50, 10),
    )
    screen.blit(
        get_font(30).render(
            "Then drag and drop each part to make an almost", True, BLACK
        ),
        (50, 40),
    )
    screen.blit(
        get_font(30).render("perfect square", True, BLACK),
        (50, 70),
    )

    if pygame.mouse.get_pressed()[2] and len(movable_boxes) == 3:
        rect = movable_boxes.pop(1)
        movable_boxes.append(
            MovableBox(
                rect.x, rect.y, rect.w / 2, rect.h, f"{magic}x", "x", f"{magic}", BLUE2
            )
        )
        movable_boxes.append(
            MovableBox(
                rect.x, rect.y, rect.h, rect.w / 2, f"{magic}x", f"{magic}", "x", BLUE2
            )
        )

    display_boxes(screen)


def missing(screen: Surface):
    global allowed
    screen.blit(
        get_font(30).render("How much area do you add to make it a", True, BLACK),
        (50, 10),
    )
    screen.blit(
        get_font(30).render(
            "perfect square? (You can press next only if ", True, BLACK
        ),
        (50, 40),
    )
    screen.blit(
        get_font(30).render("you enter the correct area)", True, BLACK),
        (50, 70),
    )
    if len(movable_boxes) == 4:
        movable_boxes[2].y = movable_boxes[0].y
        movable_boxes[2].x = movable_boxes[0].x + movable_boxes[0].width

        movable_boxes[3].x = movable_boxes[0].x
        movable_boxes[3].y = movable_boxes[0].y - movable_boxes[3].height

        movable_boxes.append(
            MovableBox(
                movable_boxes[0].x + movable_boxes[0].width,
                movable_boxes[0].y - 75,
                75,
                75,
                "?",
                "",
                "",
                GRAY,
            )
        )
        textboxes.append(TextBox(325, 174, 75, 75, text="", size=30))

    if textboxes[0].text != str(magic * magic):
        allowed = False

    else:
        allowed = True
    display_boxes(screen)
    for box in textboxes:
        box.update()
        box.draw(screen)


def middle(screen):
    global rhs, lhs
    if movable_boxes[-1].area == "?":
        _mgsqr = str(magic * magic)
        movable_boxes[-1].area = _mgsqr
        movable_boxes[-1].length = str(magic)
        movable_boxes[-1].breadth = str(magic)
        lhs += _mgsqr
        rhs += _mgsqr
    display_boxes(screen)


def final(screen):
    display_eqn(screen)
    if len(textboxes) > 1:
        textboxes.pop()

    r = Decimal(rhs.plist[0])
    screen.blit(
        get_font(40).render(f"(x + {magic})\u00b2 =  {r}", True, BLACK),
        (150, 160),
    )
    r = r.sqrt()
    screen.blit(
        get_font(40).render(f"x + {magic} ={r}", True, BLACK),
        (50, 220),
    )
    screen.blit(
        get_font(40).render(f"x + {magic} =-{r}", True, BLACK),
        (400, 220),
    )
    screen.blit(
        get_font(40).render(f"x = {r} - {magic}", True, BLACK),
        (50, 280),
    )
    screen.blit(
        get_font(40).render(f"x= -{r} - {magic}", True, BLACK),
        (400, 280),
    )
    screen.blit(
        get_font(50).render(f"x = {r - magic}", True, BLACK),
        (50, 340),
    )
    screen.blit(
        get_font(50).render(f"x = {-magic-r}", True, BLACK),
        (400, 340),
    )
    screen.blit(get_font(50).render("Yay! We solved it", True, BLACK), (200, 400))

    movable_boxes.clear()


slides = [open, lets, represent, half, missing, middle, final, close]
active_slide = 0


def event_handling(event: pygame.event.Event):
    global active_box, active_slide

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for box in movable_boxes:
            if box.collidepoint(event.pos):
                active_box = box

        if next.clicked(event.pos) and allowed:
            active_slide += 1

    if event.type == pygame.MOUSEMOTION and active_box is not None:
        active_box.move_ip(event.rel)

    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        active_box = None

    for box in textboxes:
        box.handle_event(event)


def main(screen: Surface, clock: pygame.time.Clock, eqn1: str = None):
    global active_slide, eqn, lhs, rhs, magic
    run = True
    active_slide = 0
    if eqn1 is None:
        _r1 = random.randint(-10, 10)
        _r2 = -_r1 - random.choice((-4, -2, 2, 4, 6))
        eqn = P([_r1 * _r2, -(_r1 + _r2), 1])
    else:
        eqn = P("x^2 + 2x - 15")
    lhs = P([0, eqn.plist[1], eqn.plist[2]])
    rhs = P([-eqn.plist[0]])
    magic = Decimal(lhs.plist[1]) / Decimal(2)

    while run:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            event_handling(event)

        if active_slide == len(slides):
            break

        slides[active_slide](screen)

        next.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Frame 1 Testing")
    clock = pygame.time.Clock()
    main(screen, clock)
