import pygame
# from classifier import classify


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

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
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
                    symbol = pygame.image.load(symbols["asterisk"]).convert_alpha()
                    symbol = pygame.transform.smoothscale(symbol, (50, 50))
                    current_symbols.append((symbol, symbol.get_rect(topleft=box.topleft)))
                    sketch_surface.blit(symbol, box.topleft)
                    # label = classify(inverted)
                    # print(label)
                    # resized = pygame.transform.smoothscale(inverted, (28, 28))
                    # pygame.image.save(inverted, f"sketch_{count}.png")
                    # count += 1
        elif event.type == pygame.MOUSEMOTION:
            if dragged_symbol is not None:
                current_symbols[dragged_symbol][1].move_ip(event.rel)
    
    if drawing: 
        mouse_position = pygame.mouse.get_pos()
        if draw_area.collidepoint(mouse_position):
            if last_position and draw_area.collidepoint(last_position):
                pygame.draw.line(scratch_surface, BLACK, last_position, mouse_position, 2)
            last_position = mouse_position
        else: 
            last_position = None
    
    screen.blit(resized_court, (0, 0))
    for symbol, rect in current_symbols:
        screen.blit(symbol, rect)
    screen.blit(scratch_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()