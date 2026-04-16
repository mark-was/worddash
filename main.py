import pygame
import sys
import time

pygame.init()

WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Word-Dash')

font = pygame.font.SysFont(None, 42)
start = 0.0
end = 0.0
wpm = 0
completed_words = 0
user_text = ''
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (4, 49, 97)

clock = pygame.time.Clock()

#load words
with open('./medium_words.txt', 'r') as f:
    words = [line.strip() for line in f]

sentence_start = 0
sentence_end = 10
current_sentence = ''
for word in words[:10]:
    if word != words[9]:
        current_sentence = current_sentence + word + ' '
    else:
        current_sentence = current_sentence + word


current_word_index = 0
current_word = words[current_word_index]
start = time.time()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if user_text == current_sentence:
                    completed_words += 10
                    #current_word_index += 1
                    #current_word = words[current_word_index]
                    sentence_start += 10
                    sentence_end += 10
                    current_sentence = ''
                    for word in words[sentence_start:sentence_end]:
                        if word != words[sentence_end - 1]:
                            current_sentence = current_sentence + word + ' '
                        else:
                            current_sentence = current_sentence + word
                    user_text = ''
                    
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_ESCAPE:
                end = time.time()
                wpm = completed_words / ((end - start) / 60)
                print('WPM:',wpm)
                pygame.quit()
                sys.exit()
            else:
                user_text += event.unicode  #increment word with typed char

    #color background
    screen.fill(BLUE)

    #display text to game
    word_surface = font.render(current_sentence, True, BLACK)
    input_surface = font.render(user_text, True, WHITE)
    word_rect = word_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    input_rect = input_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(word_surface, word_rect)
    screen.blit(input_surface, input_rect)

    pygame.display.flip()
    clock.tick(60)