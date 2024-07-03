import pygame

width, height = 1200, 680
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Program Simulasi")

class InputBox:
    def __init__(self, x, y, width, height, label='', default_text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('white')
        self.color_active = pygame.Color('grey')
        self.color = self.color_inactive
        self.text = default_text
        self.label_color = pygame.Color('white')
        self.font_size = 20  # Sesuaikan ukuran font
        self.font = pygame.font.Font(None, self.font_size)
        self.active = False
        self.label = label

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    try:
                        return int(self.text)
                    except ValueError:
                        return None
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        return None

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(85, self.rect.w)
        self.rect.w = width
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

        # Menampilkan label di sebelah input box
        label_surface = self.font.render(self.label, True, self.label_color)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 20))

    def update(self):
        # Sesuaikan ukuran kotak input
        width = max(50, self.font.size(self.text)[0] + 10)
        height = max(15, self.font_size + 5)
        self.rect.w = width
        self.rect.h = height

        # Menampilkan label di sebelah input box
        label_surface = self.font.render(self.label, True, self.color)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 20))