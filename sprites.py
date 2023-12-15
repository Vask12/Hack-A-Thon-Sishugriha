from pygame import Rect
from config import *


class MovableBox(Rect):
    def __init__(
        self,
        x: int,
        y: int,
        w: int,
        h: int,
        area: str,
        length: str,
        breadth: str,
        color: str,
    ):
        super().__init__(x, y, w, h)
        self.area = area
        self.length = length
        self.breadth = breadth
        self.color = color

    def draw(self, screen: Surface):
        pygame.draw.rect(screen, self.color, self)
        pygame.draw.rect(screen, "white", self, width=3)
        screen.blit(
            get_font(25).render(self.area, True, BLACK),
            (self.center[0] - 25, self.center[1] - 25),
        )
        screen.blit(
            get_font(20).render(self.length, True, BLACK),
            (self.x, self.centery),
        )
        screen.blit(
            get_font(20).render(self.breadth, True, BLACK), (self.centerx, self.y - 20)
        )


class Button:
    def __init__(
        self,
        x: int,
        y: float,
        width: int,
        height: int,
        image: Surface,
        image2: Surface,
        color: rgb = GREEN,
    ):
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height
        self.color = color
        self.image = image
        self.image2 = image2
        self.rect = pygame.rect.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen: Surface):
        on_button = self.rect.collidepoint(pygame.mouse.get_pos())
        if on_button:
            screen.blit(self.image2, (self.x, self.y))
        else:
            screen.blit(self.image, (self.x, self.y))

    def clicked(self, pos: tuple[int, int]) -> bool:
        x, y = pos
        return (x >= self.x and x <= self.x + self.width) and (
            y >= self.y and y <= self.y + self.height
        )


class TextBox:
    def __init__(self, x, y, w, h, text="", size=25):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.size = size
        self.txt_surface = get_font(self.size).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = get_font(self.size).render(
                    self.text, True, self.color
                )

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
