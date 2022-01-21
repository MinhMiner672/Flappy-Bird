import pygame
from data import variables


class Pipe(pygame.sprite.Sprite):
    def __init__(self, direction: str, x_pos: int, y_pos: int, bird_class):
        super(Pipe, self).__init__()
        self.bird_class = bird_class
        self.direction = direction

        self.image = pygame.transform.scale(pygame.image.load(
            f'./data/images/graphics/pipe_{direction}.png').convert_alpha(), (90, 400))
        self.rect = self.image.get_rect(midbottom=(
            x_pos, y_pos)) if direction == 'down' else self.image.get_rect(midtop=(x_pos, y_pos))

        self.point_sound = pygame.mixer.Sound('./data/sound/point.mp3')
        self.hit_sound = pygame.mixer.Sound('./data/sound/hit.mp3')
        self.die_sound = pygame.mixer.Sound('./data/sound/die.mp3')

        self.die_sound.set_volume(0.5)
        self.point_sound.set_volume(0.5)

    def move_pipe(self):
        """
        Always moves the pipe to the left hand side
        """

        self.rect.x -= 2 if variables.bird_collision == False else 0
        # if variables.bird_collision == False or
        if self.rect.right <= 0:
            self.kill()

    def bird_touches_pipe(self):
        """
        If the bird touches one of the pipes
        """

        # If the pipe touches the bird / the bird y position is too high and
        # the bird has the same x position as the pipe
        if self.rect.colliderect(self.bird_class.sprite.rect) or all([self.bird_class.sprite.rect.bottom <= 0, self.bird_class.sprite.rect.left >= self.rect.left]):
            if not variables.hit_played:
                self.hit_sound.play()
                self.die_sound.play()
                variables.hit_played = True
            variables.bird_collision = True

    def get_point(self):
        """
        If the bird goes pass one pipe without hitting, then add 1 point
        we compare the self.direction to avoid double points
        """

        if self.rect.right == self.bird_class.sprite.rect.left and self.direction == 'down':
            variables.score += 1
            self.point_sound.play()

    def update(self):
        self.bird_touches_pipe()
        self.move_pipe()
        self.get_point()
