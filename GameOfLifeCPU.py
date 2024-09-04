﻿import pygame
import tkinter as tk
from tkinter import messagebox
import time

title_bar_height = 40
margin_L = 150
margin_R = 150
margin_T = 50
margin_B = 50
min_cell_size = 10
max_cell_size = 50
bg_color = (192, 192, 192)
cell_color = (204, 255, 153)
grid_color = (0, 0, 0)
button_color = (128, 0, 128)  
button_text_color = (255, 255, 255) 
initial_screen_width, initial_screen_height = 800, 600
button_width = 120  
button_height = 40 
button_gap = 20 
screen = pygame.display.set_mode((initial_screen_width, initial_screen_height), pygame.RESIZABLE)

class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=(0, 0, 0)):
        if outline:
            pygame.draw.ellipse(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 1)
        
        pygame.draw.ellipse(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, button_text_color)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False

def draw_title_bar(screen, width):
    title_bar_color = (192, 0, 180)
    pygame.draw.rect(screen, title_bar_color, (0, 0, width, title_bar_height))
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('GAME OF LIFE', True, (255, 255, 255))  
    text_rect = text.get_rect(center=(width / 2, title_bar_height / 2))
    screen.blit(text, text_rect)
    return title_bar_height

def show_rules():
    rules_text = ("1. Any live cell with fewer than two live neighbors dies (underpopulation).\n"
                  "2. Any live cell with two or three live neighbors lives on to the next generation.\n"
                  "3. Any live cell with more than three live neighbors dies (overpopulation).\n"
                  "4. Any dead cell with exactly three live neighbors becomes a live cell (reproduction).")
    
   
    root = tk.Tk()
    root.withdraw() 
    messagebox.showinfo("Game of Life Rules", rules_text)
    root.destroy() 

def reset_game():
    global cell_states
    cell_states = {}
    update_display(screen.get_width(), screen.get_height())

def restore_initial_configuration():
    global cell_states, initial_cell_states
    cell_states = initial_cell_states.copy()
    update_display(screen.get_width(), screen.get_height())

def update_display(window_width, window_height):
    global start_button, stop_button, rules_button, reset_button, restore_button, game_surface
    screen.fill(bg_color)
    
    draw_title_bar(screen, window_width)
    
    grid_start_y = margin_T + title_bar_height 
    grid_start_x = margin_L  # Start of the grid on the X axis
    button_x = (grid_start_x // 2) - (button_width // 2) 

    start_button.x = button_x
    start_button.y = grid_start_y
    start_button.width = button_width
    start_button.height = button_height

    stop_button.x = button_x
    stop_button.y = start_button.y + button_height + button_gap
    stop_button.width = button_width
    stop_button.height = button_height

    rules_button.x = button_x
    rules_button.y = stop_button.y + button_height + button_gap
    rules_button.width = button_width
    rules_button.height = button_height

    reset_button.x = button_x
    reset_button.y = rules_button.y + button_height + button_gap
    reset_button.width = button_width
    reset_button.height = button_height

    restore_button.x = button_x
    restore_button.y = reset_button.y + button_gap + button_height
    restore_button.width = button_width
    restore_button.height = button_height

    start_button.draw(screen)
    stop_button.draw(screen)
    rules_button.draw(screen)
    reset_button.draw(screen)
    restore_button.draw(screen)

    game_surface.fill(bg_color)
    draw_cells(game_surface)
    draw_grid(game_surface)
    
    screen.blit(game_surface, (margin_L, grid_start_y))

    pygame.display.flip()

def resize_grid(new_width, new_height):
    global game_surface
    game_surface = pygame.Surface((new_width, new_height))
    game_surface.fill(bg_color)
    draw_cells(game_surface)
    draw_grid(game_surface)

def draw_grid(surface):
    surface_width, surface_height = surface.get_size()
    for y in range(0, surface_height, cell_size):
        for x in range(0, surface_width, cell_size):
            rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(surface, grid_color, rect, 1)

cell_states = {}
initial_cell_states = {}

def color_cell(position, window_size):
    x, y = position
    cell_x = (x - margin_L) // cell_size
    cell_y = (y - (title_bar_height + margin_T)) // cell_size
    key = (cell_x, cell_y)
    if key in cell_states:
        cell_states[key] = not cell_states[key]
    else:
        cell_states[key] = True

def draw_cells(surface):
    for (x, y), alive in cell_states.items():
        if alive:
            pygame.draw.rect(surface, cell_color, (x * cell_size, y * cell_size, cell_size, cell_size))

def adjust_grid_and_cells_for_zoom():
    global cell_size, old_cell_size, game_surface, game_surface_width, game_surface_height, screen

    new_game_surface_width = screen.get_width() - margin_L - margin_R
    new_game_surface_height = screen.get_height() - margin_T - margin_B - title_bar_height
    new_game_surface = pygame.Surface((new_game_surface_width, new_game_surface_height))
    new_game_surface.fill(bg_color)

    game_surface = new_game_surface
    game_surface_width = new_game_surface_width
    game_surface_height = new_game_surface_height

    update_display(screen.get_width(), screen.get_height())

def update_game_of_life():
    global cell_states, is_running
    new_states = {}
    neighbors_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    to_check = set()
    for (x, y) in cell_states.keys():
        to_check.add((x, y))
        for dx, dy in neighbors_offsets:
            to_check.add((x + dx, y + dy))

    for (x, y) in to_check:
        live_neighbors = sum(cell_states.get((x + dx, y + dy), False) for dx, dy in neighbors_offsets)
        if cell_states.get((x, y), False):
            if live_neighbors in [2, 3]:
                new_states[(x, y)] = True
            else:
                new_states[(x, y)] = False
        else:
            if live_neighbors == 3:
                new_states[(x, y)] = True

    if new_states == cell_states:
        is_running = False
        elapsed_time = time.time() - start_time
        print(f"Game reached a stable configuration and has stopped. Elapsed time: {elapsed_time:.2f} seconds.")
    
    cell_states = new_states

def main():
    pygame.init()
    global screen, cell_size, old_cell_size, game_surface, grid, cell_states, initial_cell_states, initial_screen_height, initial_screen_width
    global start_button, stop_button, rules_button, reset_button, restore_button
    global game_surface_width, game_surface_height, start_time  
    
    window_width, window_height = initial_screen_width, initial_screen_height
    clock = pygame.time.Clock()
    running = True
    is_running = False
    cell_size = 20
   
    title_bar_height = draw_title_bar(screen, window_width)
    print(title_bar_height)
    game_surface = pygame.Surface((window_width - margin_L - margin_R, window_height - margin_T - margin_B - title_bar_height))
    game_surface.fill(bg_color)

    start_button = Button(button_color, 0, 0, button_width, button_height, 'Start')
    stop_button = Button(button_color, 0, 0, button_width, button_height, 'Stop')
    rules_button = Button(button_color, 0, 0, button_width, button_height, 'Rules')
    reset_button = Button(button_color, 0, 0, button_width, button_height, 'Reset')
    restore_button = Button(button_color, 0, 0, button_width, button_height, '<--')

    grid_height = (window_height - margin_T - margin_B - title_bar_height) // cell_size
    grid_width = (window_width - margin_L - margin_R) // cell_size
    grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
    cell_states = {}
    initial_cell_states = {}

    game_surface_width = window_width - margin_L - margin_R
    game_surface_height = window_height - margin_T - margin_B - title_bar_height
    old_cell_size = cell_size

    previous_states = []  # To store previous states for detecting stable configurations

    while running:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False    
                elif event.key == pygame.K_SPACE:
                    is_running = not is_running
                    if is_running:
                        start_time = time.time()
                        initial_cell_states = cell_states.copy()
                    print(f"is_running set to {is_running} via space bar") 

            elif event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_over(pos):
                    is_running = True
                    start_time = time.time()
                    initial_cell_states = cell_states.copy()
                    print(f"is_running set to {is_running} via start button")

                elif stop_button.is_over(pos):
                    is_running = False
                    print(f"is_running set to {is_running} via stop button")

                elif rules_button.is_over(pos):
                    show_rules()

                elif reset_button.is_over(pos):
                    reset_game()
                    print("Game reset to initial configuration")
                
                elif restore_button.is_over(pos):
                    restore_initial_configuration()
                    print("Game restored to initial configuration")
                    
                else:
                    if event.button == 1 and not is_running:
                        mouse_pos = event.pos
                        color_cell(mouse_pos, screen.get_size())
                        draw_cells(game_surface)
                        pygame.display.flip()
                    elif event.button == 4:
                        old_cell_size = cell_size
                        cell_size += 5
                        if cell_size > max_cell_size:
                            cell_size = max_cell_size
                        adjust_grid_and_cells_for_zoom()
                        
                    elif event.button == 5:
                        old_cell_size = cell_size
                        cell_size -= 5
                        if cell_size < min_cell_size:
                            cell_size = min_cell_size
                        adjust_grid_and_cells_for_zoom()
           
            elif event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.w, event.h
                screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
                
                game_surface_width = window_width - margin_L - margin_R
                game_surface_height = window_height - margin_T - margin_B - title_bar_height
                new_grid_width = game_surface_width // cell_size
                new_grid_height = game_surface_height // cell_size

                game_surface = pygame.Surface((new_grid_width * cell_size, new_grid_height * cell_size))
                game_surface.fill(bg_color)

                adjust_grid_and_cells_for_zoom()
                update_display(window_width, window_height)
                pygame.display.flip()
                        
        if is_running:
            print("Game of Life is updating")
            previous_state = cell_states.copy()
            update_game_of_life()
            if cell_states == previous_state:
                is_running = False
                elapsed_time = time.time() - start_time
                print(f"Game reached a stable configuration and has stopped. Elapsed time: {elapsed_time:.2f} seconds.")
            previous_states.append(previous_state)
            if len(previous_states) > 2:
                previous_states.pop(0)
            print("Game of Life updated")
        
        update_display(window_width, window_height)
        clock.tick(60)

if __name__ == "__main__":
    main()
