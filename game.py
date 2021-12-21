import pygame
import random
from sprites import *
import random
import variables

pygame.init()


class Game:
    """
    A class for most things of the entire game
    """

    def __init__(self):
        self.WIDTH, self.HEIGHT = 500, 700
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Flappy Bird')

        self.clock = pygame.time.Clock()

        icon_surface = pygame.image.load('./images/icon.ico')
        pygame.display.set_icon(icon_surface)

        # Background surfaces (day, night)
        self.day_background = pygame.transform.scale(
            pygame.image.load('./images/graphics/day.png').convert(), (500, 800))
        self.night_background = pygame.transform.scale(
            pygame.image.load('./images/graphics/night.png').convert(), (500, 800))
        self.backgrounds = [self.day_background, self.night_background]

        # When the game starts, choose a random background, day or night
        self.selected_background = random.choice(self.backgrounds)

        # Sprite groups
        self.grounds_group = pygame.sprite.Group()
        self.bird_group = pygame.sprite.GroupSingle(
            Bird([self.grounds_group]))

        self.grounds_group.add(
            Base(0, 710, self.grounds_group))

        self.pipes_group = pygame.sprite.Group()

        self.all_groups = [self.pipes_group, self.bird_group,
                           self.grounds_group]

        # Event for pipes to spawn
        self.pipe_event = pygame.USEREVENT + 1
        # Set timer for pipe event
        pygame.time.set_timer(self.pipe_event, 2000)

        # Sound effects
        self.wing_sound = pygame.mixer.Sound('./sound/wing.mp3')

        self.wing_sound.set_volume(0.5)

    def show_background(self):
        """
        Draws background, ground
        """

        self.background_rect = self.selected_background.get_rect(
            topleft=(0, 0))
        self.screen.blit(self.selected_background, self.background_rect)

    def update_group(self):
        """
        Update all sprite groups in 'self.all_groups'
        """

        for group in self.all_groups:
            group.draw(self.screen)
            group.update()

    def refresh(self):
        """
        Clears and resets the game
        """

        self.bird_group.empty()
        self.pipes_group.empty()
        self.bird_group.add(Bird([self.grounds_group]))
        variables.bird_collision, variables.user_started, variables.hit_played, variables.update_score = False, False, False, False
        variables.score = 0

    def lose_screen(self):
        """
        If player loses the game, then show the retry button
        and the result panel
        """

        if variables.bird_collision:
            current_score = variables.score

            # Access user's highest score data
            with open('./score.txt', 'r') as f:
                content = f.read()
                # If the data syntax in the file is not correct
                if any(['score:' not in content.lower(), content.strip().split(' ')[0].lower() != 'score:']):
                    with open('./score.txt', 'w') as f:
                        # Set the high score as the current score
                        f.write(f'Score: {variables.score}')

            # The line after the try keyword might have an error
            # this is due to the wrong value of the score in the 'score.txt'
            # e.g: "score: 12abc", "Score: abcxyz",....
            try:
                highest_score = int(content.strip().split(' ')[1])

            except ValueError:
                # Set the highest score as the current score
                highest_score = current_score
                with open('./score.txt', 'w') as f:
                    # Overwrite the file
                    f.write(f'Score: {variables.score}')

            # Retry button (this button allows you to play the game again)
            retry_button = pygame.image.load(
                './images/buttons/retry.png').convert()
            retry_button_rect = retry_button.get_rect(
                center=(150, 490))

            # Reset button (this button resets your highest score)
            reset_button = pygame.image.load(
                './images/buttons/reset.png').convert()
            reset_button_rect = reset_button.get_rect(center=(350, 490))

            # Result Image
            result_image = pygame.transform.scale(pygame.image.load(
                './images/result.png').convert(), (400, 200))
            result_image_rect = result_image.get_rect(
                center=(self.WIDTH / 2, self.HEIGHT / 2))
            # Draw the retry button and the result panel
            self.screen.blit(retry_button, retry_button_rect)
            self.screen.blit(reset_button, reset_button_rect)
            self.screen.blit(result_image, result_image_rect)

            # Show current score and highgest score when the game is over
            self.show_score(variables.score, 390, 323, True)
            self.show_score(highest_score, 390, 413, True)

            # Shows a star to indicate that you just made a new high score
            if current_score > highest_score:
                star_image = pygame.transform.scale(
                    pygame.image.load('./images/star.png').convert_alpha(), (35, 35))
                star_rect = star_image.get_rect(center=(350, 320))
                self.screen.blit(star_image, star_rect)

            # If user clicks on the reset button
            if all([reset_button_rect.collidepoint(pygame.mouse.get_pos()), pygame.mouse.get_pressed()[0]]):
                with open('./score.txt', 'w') as f:
                    f.write('Score: 0')

            # If user presses SPACE, KEY UP or clicks on the retry button
            if any([retry_button_rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0], pygame.key.get_pressed()[pygame.K_SPACE] or pygame.key.get_pressed()[pygame.K_UP]]):
                if current_score > highest_score:
                    # Update the highest score if the current score user got
                    # is higher than it
                    with open('./score.txt', 'w') as f:
                        f.write(f'Score: {current_score}')
                # Refresh the game
                self.refresh()

    def events(self) -> bool:
        """
        Tracks all game events

        Returns:
            bool: True if the game is running, False otherwise
        """

        for event in pygame.event.get():
            # User quits the game
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                # If user presses SPACE or KEY_UP
                if any([event.key == pygame.K_SPACE, event.key == pygame.K_UP, pygame.mouse.get_pressed()[0]]):
                    if not variables.bird_collision:
                        # Play the wing sound effect
                        self.wing_sound.play()

                        # Make the bird jump
                        self.bird_group.sprite.gravity_count = -9

                        # Rotate the bird a bit up to the sky
                        self.bird_group.sprite.rotate_index = 35

                        # Make the bird not to fly lower than y = -50
                        # the bird is too high
                        if self.bird_group.sprite.rect.y <= -50:
                            self.bird_group.sprite.rect.y = -50

                    # If the game is not manually started by the user
                    if not variables.user_started:
                        variables.user_started = True

            # If the game's started and the pipe timer is triggered
            if event.type == self.pipe_event and variables.user_started:
                pipe_y_pos = random.randint(50, 400)
                self.pipes_group.add(
                    Pipe('down', 550, pipe_y_pos, self.bird_group))
                self.pipes_group.add(
                    Pipe('up', 550, pipe_y_pos + 175, self.bird_group))

        # True if the game is not closed by the user
        return True

    def show_score(self, score: int, default_x_position: int, default_y_position: int, lose_game: bool = False):
        """
        Shows score onto the screen with specific x and y values

        Args:
            score (int): The score that needs to be displayed (e.g: 1, 2, 3, ...)
            default_x_position (int): The default x position for each digit in the score
            default_y_position (int): ___________ y position for each digit in the score
            lose_game (bool, optional): The score can be shown depending on the game state (True or false). Defaults to False.
        """

        if variables.user_started and lose_game == variables.bird_collision:
            x_center_pos = default_x_position
            digit_images = []
            digit_image_rects = []

            for digit in str(score):
                digit_images.append(pygame.image.load(
                    f'./images/numbers/{digit}.png').convert_alpha())

            if len(digit_images) == 1:
                digit_image_rects.append(
                    digit_images[0].get_rect(center=(x_center_pos, default_y_position)))

            if len(digit_images) == 2:
                digit_image_rects.append(digit_images[0].get_rect(
                    center=(x_center_pos - 10, default_y_position)))
                digit_image_rects.append(digit_images[1].get_rect(
                    center=(x_center_pos + 10, default_y_position)))

            if len(digit_images) == 3:
                digit_image_rects.append(digit_images[0].get_rect(
                    center=(x_center_pos - 20, default_y_position)))
                digit_image_rects.append(digit_images[1].get_rect(
                    center=(x_center_pos, default_y_position)))
                digit_image_rects.append(digit_images[2].get_rect(
                    center=(x_center_pos + 20, default_y_position)))

            for i in range(0, len(digit_images) + 1):
                try:
                    self.screen.blit(digit_images[i], digit_image_rects[i])
                except IndexError:
                    pass

    def fps(self):
        """
        Controls the FPS and updates the game
        """

        self.clock.tick(60)
        pygame.display.update()
