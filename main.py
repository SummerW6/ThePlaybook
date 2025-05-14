import pygame
import speech_recognition as sr
import threading
from classifier import classify

for i, name in enumerate(sr.Microphone.list_microphone_names()):
    print(f"Device {i}: {name}")

device_index = 2 # Choose correct microphone

recognizing = False

symbols = {
    'asterisk' : "images/basketball.svg",
    'one-circled' : "images/number-1.svg",
    'two-circled' : "images/number-2.svg",
    'three-circled' : "images/number-3.svg",
    'four-circled' : "images/number-4.svg",
    'five-circled' : "images/number-5.svg"
}

current_symbols = []
dragged_symbol = None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (170, 170, 170)
DARK_GRAY = (100, 100, 100)

pygame.init()

screen = pygame.display.set_mode((1000, 850))
pygame.display.set_caption("Playbook")

screen.fill(WHITE)

court = pygame.image.load("images/halfcourt.jpeg")
width, height = court.get_size()
resized_court = pygame.transform.smoothscale(court, (width * 0.5, height * 0.5))
screen.blit(resized_court, (0, 0))

draw_area = pygame.Rect(0, 0, width * 0.5, height * 0.5)
drawing = False
last_position = None
clock = pygame.time.Clock()
sketch_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
scratch_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

button_rect = pygame.Rect(screen.get_width() - 200, 20, 200, 50)
font = pygame.font.SysFont(None, 28)
record_text = "Start Record"


def draw_button():
    button_text = font.render(record_text, True, BLACK)
    mouse_position = pygame.mouse.get_pos()
    color = LIGHT_GRAY if button_rect.collidepoint(mouse_position) else DARK_GRAY
    pygame.draw.rect(screen, color, button_rect)
    screen.blit(button_text, (button_rect.x + 40, button_rect.y + 15))

def draw_message_box(text):
    message = font.render(text, True, BLACK)
    padding = 10
    box_width = message.get_width() + 2 * padding
    box_height = message.get_height() + 2 * padding

    x = screen.get_width() - box_width - 20
    y = screen.get_height() - box_height - 20
    message_rect = pygame.Rect(x, y, box_width, box_height)

    pygame.draw.rect(screen, LIGHT_GRAY, message_rect)
    pygame.draw.rect(screen, DARK_GRAY, message_rect, 2)
    screen.blit(message, (x + padding, y + padding))

def parse_command(command):
    command = command.lower()
    symbol = None
    if "draw" in command:
        if "basketball" in command:
            symbol = pygame.image.load(symbols["asterisk"]).convert_alpha()
        if "point" in command:
            symbol = pygame.image.load(symbols["one-circled"]).convert_alpha()
        if "shooting" in command:
            symbol = pygame.image.load(symbols["two-circled"]).convert_alpha()
        if "small" in command:
            symbol = pygame.image.load(symbols["three-circled"]).convert_alpha()
        if "power" in command:
            symbol = pygame.image.load(symbols["four-circled"]).convert_alpha()
        if "center" in command:
            symbol = pygame.image.load(symbols["five-circled"]).convert_alpha()
    if symbol is not None: 
        symbol = pygame.transform.smoothscale(symbol, (50, 50))
        current_symbols.append((symbol, symbol.get_rect(topleft=(500, 400))))
        
recognizer = sr.Recognizer()

def listen():
    global recognizing, record_text

    with sr.Microphone(device_index=device_index) as source:
        # recognizer.adjust_for_ambient_noise(source)
        try:
            print("Lisitening")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            text = recognizer.recognize_google(audio)
            parse_command(text)
            print("You said: ", text)
        except Exception as e:
            print("there was an error", repr(e))
    recognizing = False
    record_text = "Start Record"

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(event.pos):
                recognizing = True
                record_text = "Stop Record" if record_text == "Start Record" else "Start Record"
                threading.Thread(target=listen, daemon=True).start()
            for idx, (symbol, rect) in enumerate(current_symbols):
                if rect.collidepoint(event.pos):
                    dragged_symbol = idx
                    break
            if dragged_symbol is None:
                drawing = True
                last_position = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_position = None
            if dragged_symbol is not None:
                dragged_symbol = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                box = scratch_surface.get_bounding_rect()
                if box.width and box.height:
                    sketch = scratch_surface.subsurface(box).copy()
                    scratch_surface.fill((0, 0, 0, 0), rect=box)

                    inverted = pygame.Surface(sketch.get_size())
                    inverted.fill(BLACK)

                    for w in range(inverted.get_width()):
                        for h in range(inverted.get_height()):
                            r, g, b, a = sketch.get_at((w, h))
                            if a and (r, g, b) == BLACK:
                                inverted.set_at((w, h), WHITE)
                    label = classify(inverted)
                    symbol = pygame.image.load(symbols[label]).convert_alpha()
                    symbol = pygame.transform.smoothscale(symbol, (50, 50))
                    current_symbols.append((symbol, symbol.get_rect(topleft=box.topleft)))
                    sketch_surface.blit(symbol, box.topleft)

                    print(label)
                    # resized = pygame.transform.smoothscale(inverted, (28, 28))
                    # pygame.image.save(inverted, f"sketch_{count}.png")
                    # count += 1
        elif event.type == pygame.MOUSEMOTION:
            if dragged_symbol is not None:
                    symbol, rect = current_symbols[dragged_symbol]
                    rect.move_ip(event.rel)
                    rect.clamp_ip(draw_area)
                    current_symbols[dragged_symbol] = (symbol, rect)
    
    if drawing: 
        mouse_position = pygame.mouse.get_pos()
        if draw_area.collidepoint(mouse_position):
            if last_position and draw_area.collidepoint(last_position):
                pygame.draw.line(scratch_surface, BLACK, last_position, mouse_position, 2)
            last_position = mouse_position
        else: 
            last_position = None
    

    screen.blit(resized_court, (0, 0))
    draw_button()

    for symbol, rect in current_symbols:
        screen.blit(symbol, rect)
    screen.blit(scratch_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()