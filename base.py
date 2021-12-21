import pygame
import variables


class Base(pygame.sprite.Sprite):
    """
    The ground instance
    """

    def __init__(self, x_pos: int, y_pos: int, base_group):
        super(Base, self).__init__()
        self.image = pygame.transform.scale(pygame.image.load(
            './images/graphics/base.png').convert(), (700, 100))
        self.rect = self.image.get_rect(bottomleft=(x_pos, y_pos))

        self.base_group = base_group

    def move_ground(self):
        """
        Always moves the base to the left
        """

        self.rect.x -= 2 if not variables.bird_collision else 0

    def base_reaches_limit(self):
        """
        If the right side of the base reaches the limit of the screen (x = 500)
        Or if the base goes beyond the screen (x = 0)
        """

        if self.rect.right == 500:
            self.base_group.add(
                Base(500, 710, self.base_group))
        if self.rect.right < 0:
            self.kill()
        return self.base_group

    def update(self):
        self.move_ground()
        self.base_reaches_limit()
