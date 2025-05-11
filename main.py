import pygame
count = 0
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

pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            last_position = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            last_position = None
        elif event.type == pygame.KEYDOWN:
            box = sketch_surface.get_bounding_rect()
            if event.key == pygame.K_RETURN:
                if box.width and box.height:
                    sketch = sketch_surface.subsurface(box).copy()

                    inverted = pygame.Surface(sketch.get_size())
                    inverted.fill(BLACK)

                    for w in range(inverted.get_width()):
                        for h in range(inverted.get_height()):
                            r, g, b, a = sketch.get_at((w, h))
                            if a and (r, g, b) == BLACK:
                                inverted.set_at((w, h), WHITE)
                    pygame.image.save(inverted, f"data/train/four-circled/sketch_{count}.png")
                    count += 1
            if event.key == pygame.K_BACKSPACE:
                sketch_surface.fill((0, 0, 0, 0), rect=box)
    
    if drawing: 
        mouse_position = pygame.mouse.get_pos()
        if draw_area.collidepoint(mouse_position):
            if last_position and draw_area.collidepoint(last_position):
                pygame.draw.line(sketch_surface, BLACK, last_position, mouse_position, 2)
            last_position = mouse_position
        else: 
            last_position = None
    
    screen.blit(resized_court, (0, 0))
    screen.blit(sketch_surface, (0, 0))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()