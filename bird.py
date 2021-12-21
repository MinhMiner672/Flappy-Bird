import pygame
import variables


class Bird(pygame.sprite.Sprite):
    """
    A Class for Flappy Bird

    Args:
        pygame (list): The list of obstacle group for the bird
        to detect whether it collides something that will make 
        user lose the game
    """

    def __init__(self, obstacles: list):
        super(Bird, self).__init__()

        # All bird states
        self.bird_flap_up = pygame.transform.scale(pygame.image.load(
            './images/bird/bird_up.png').convert_alpha(), (55, 40))
        self.bird_flap_mid = pygame.transform.scale(pygame.image.load(
            './images/bird/bird_mid.png').convert_alpha(), (55, 40))
        self.bird_flap_down = pygame.transform.scale(pygame.image.load(
            './images/bird/bird_down.png').convert_alpha(), (55, 40))
        self.bird_state_surfaces = [self.bird_flap_up,
                                    self.bird_flap_mid, self.bird_flap_down]
        self.state_index = 0
        self.rotate_index = 3

        self.image = self.bird_state_surfaces[self.state_index]

        self.rect = self.image.get_rect(center=(100, 370))
        self.gravity_count = 2

        self.lost_rotation = False

        self.y_index_for_animation = 0
        self.up_or_down = 'up'

        # Create an obstacles list to check if the bird collides any of them
        # this list includes pipes, ground
        self.obstacles = obstacles

    def animation(self):
        """
        If user has not started the game, the bird will go up and then 
        go down a little bit, to make animation
        """

        if not variables.user_started:
            if not self.y_index_for_animation > 2 and self.up_or_down == 'up':
                self.y_index_for_animation += 0.2
                if self.y_index_for_animation > 2:
                    self.up_or_down = 'down'

            elif not self.y_index_for_animation < -2 and self.up_or_down == 'down':
                self.y_index_for_animation -= 0.2
                if self.y_index_for_animation < -2:
                    self.up_or_down = 'up'

            self.rect.y += int(self.y_index_for_animation)

    def change_state(self):
        """
        Change flapping state of the bird
        """

        # If the bird is not colliding anything
        if not variables.bird_collision:
            self.state_index += 0.2
            if self.state_index > 3:
                self.state_index = 0
            # Changes the bird's state
            self.image = self.bird_state_surfaces[int(self.state_index)]
            # Rotates the bird as it falls
            self.image = pygame.transform.rotate(self.image, self.rotate_index)
        else:
            # If user loses the game
            if not self.lost_rotation:
                # Rotates the bird such that the bird's head is
                # directed towards down the ground
                self.image = pygame.transform.rotate(
                    self.image, -90 - self.rotate_index)
                self.lost_rotation = True

    def bird_touches_ground(self):
        """
        If the bird touches the ground
        or the bird's y position is lower than 590
        """

        if self.rect.bottom >= 590:
            hit_sound = pygame.mixer.Sound('./sound/hit.mp3')
            die_sound = pygame.mixer.Sound('./sound/die.mp3')
            if not variables.hit_played:
                hit_sound.play()
                die_sound.play()
                variables.hit_played = True
            variables.bird_collision = True

    def gravity_and_rotate(self):
        """
        Always makes the bird fall down because of gravity
        Rotates the bird as it falls
        """

        if self.rect.bottom <= 590 and variables.user_started:
            # Always move the bird down
            self.rect.y += self.gravity_count
            # Increase the gravity
            self.gravity_count += 0.5

            # Rotates the bird
            # self.image = pygame.transform.rotate(self.image, self.rotate_index)
            self.rotate_index -= 2 if self.rotate_index > -90 else 0

    def update(self):
        self.animation()
        self.change_state()
        self.gravity_and_rotate()
        self.bird_touches_ground()
