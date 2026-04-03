import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Word-Dash')

font = pygame.font.SysFont(None, 64)

user_text = ''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (4, 49, 97)

clock = pygame.time.Clock()

#load words
with open('./words.txt', 'r') as f:
    words = [line.strip() for line in f]

current_word_index = 0
current_word = words[current_word_index]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_text == current_word:
                    current_word_index += 1
                    current_word = words[current_word_index]
                    user_text = ''
                    
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            else:
                user_text += event.unicode  #increment word with typed char

    #color background
    screen.fill(BLUE)

    #display text to game
    word_surface = font.render(current_word, True, BLACK)
    input_surface = font.render(user_text, True, WHITE)
    word_rect = word_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    input_rect = input_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(word_surface, word_rect)
    screen.blit(input_surface, input_rect)

    pygame.display.flip()
    clock.tick(60)