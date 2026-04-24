from flask import g
import pygame
import sys
import time

pygame.init()

WIDTH, HEIGHT = 1400, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Word-Dash')

font = pygame.font.SysFont(None, 42)
sentence_font = pygame.font.SysFont(None, 60)
start = 0.0
end = 0.0
wpm = 0
completed_words = 0
user_text = ''
game_state = 'menu'
difficulty = 'medium'
selected_option = 0
menu_options = ['Start', 'Change Difficulty', 'Exit']
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (4, 49, 97)
GREEN = (0, 200, 0)
RED = (220, 0, 0)
PURPLE = (41, 4, 61)
GREY = (24, 24, 24)

clock = pygame.time.Clock()

#load words
with open('./wordlists/medium_words.txt', 'r') as f:
    words = [line.strip() for line in f]

sentence_start = 0
sentence_end = 10
current_sentence = ''

def draw_colored_sentence(text, target, x, y):
    total_width = 0

    #loop through the current sentence, render each char black
    for char in target:
        char_surface = sentence_font.render(char, True, BLACK)
        total_width += char_surface.get_width()

    #find center
    start_x = x - total_width // 2

    #iterate through each letter in sentence, compare against user input, change color
    for i, char in enumerate(target):
        if i < len(text): 
            if text[i] == char:
                color = GREEN
            else:
                color = RED
        else:
            color = BLACK

        char_surface = sentence_font.render(char, True, color)
        screen.blit(char_surface, (start_x, y))
        start_x += char_surface.get_width()


def draw_menu():
    #def surfaces/ print title
    title_font = pygame.font.Font('./fonts/majormono.ttf', 80)
    title_surface = title_font.render('WORd-DAsh', True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
    screen.blit(title_surface, title_rect)

    #for each menu option, define surface/print
    for i, option in enumerate(menu_options):
        if i == selected_option:
            color = WHITE
        else:
            color = BLACK

        option_surface = font.render(option, True, color)
        option_rect = option_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 60))
        screen.blit(option_surface, option_rect)

    difficulty_surface = font.render(f'Difficulty: {difficulty}', True, GREY)
    difficulty_rect = difficulty_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 250))
    screen.blit(difficulty_surface, difficulty_rect)
    wpm_surface = font.render(f'WPM: {wpm}', True, GREY)
    wpm_rect = wpm_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 290))
    screen.blit(wpm_surface, wpm_rect)

for word in words[:10]:
    if word != words[9]:
        current_sentence = current_sentence + word + ' '
    else:
        current_sentence = current_sentence + word

current_word_index = 0
current_word = words[current_word_index]

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_state == 'menu': #game mode is menu, handle these arrow key cases
                if event.key == pygame.K_UP:
                    selected_option -= 1
                    if selected_option < 0:
                        selected_option = len(menu_options) - 1

                elif event.key == pygame.K_DOWN:
                    selected_option += 1
                    if selected_option >= len(menu_options):
                        selected_option = 0

                elif event.key == pygame.K_RETURN:
                    if menu_options[selected_option] == 'Start':
                        game_state = 'game'
                        start = time.time()
                    elif menu_options[selected_option] == 'Exit':
                        pygame.quit()
                        sys.exit()
                    elif menu_options[selected_option] == 'Change Difficulty': #change gamemode global and corresponding wordlist
                        if difficulty == 'easy':
                            difficulty = 'medium'
                            filename = './wordlists/medium_words.txt'
                            sentence_font = pygame.font.SysFont(None, 60) #change font size to fit on game window per difficulity
                        elif difficulty == 'medium':
                            difficulty = 'hard'
                            filename = './wordlists/hard_words.txt'
                            sentence_font = pygame.font.SysFont(None, 35)
                        else:
                            difficulty = 'easy'
                            filename = './wordlists/easy_words.txt'
                            sentence_font = pygame.font.SysFont(None, 60)

                        with open(filename, 'r') as f:
                            words = [line.strip() for line in f]

                        sentence_start = 0
                        sentence_end = 10
                        current_sentence = ''

                        #create sentence/ append spaces between words
                        for word in words[sentence_start:sentence_end]:
                            if word != words[sentence_end - 1]:
                                current_sentence += word + ' '
                            else:
                                current_sentence += word

                        user_text = ''
                        completed_words = 0

            elif game_state == 'game':
                if event.key == pygame.K_RETURN:
                    #if text is correct, shift words down in wordlist by x, creating new sentence
                    if user_text == current_sentence:
                        completed_words += 10
                        sentence_start += 10
                        sentence_end += 10
                        current_sentence = ''

                        for word in words[sentence_start:sentence_end]:
                            if word != words[sentence_end - 1]:
                                current_sentence += word + ' '
                            else:
                                current_sentence += word

                        user_text = ''

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

                elif event.key == pygame.K_ESCAPE:
                    game_state = 'menu'
                    end = time.time()
                    wpm = int(completed_words / ((end - start) / 60))
                    #print('WPM:',wpm)

                else:
                    user_text += event.unicode
    #fill bg color
    screen.fill(BLUE)
    #start with game state menu by default
    
    if game_state == 'menu':
        draw_menu()
        
    #when gamestate changes, start game
    elif game_state == 'game':
        draw_colored_sentence(user_text, current_sentence, WIDTH // 2, HEIGHT // 2)

    pygame.display.flip()
    clock.tick(60)