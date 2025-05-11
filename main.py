import pygame

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
    
    if drawing: 
        mouse_position = pygame.mouse.get_pos()
        if draw_area.collidepoint(mouse_position):
            if last_position and draw_area.collidepoint(last_position):
                pygame.draw.line(screen, BLACK, last_position, mouse_position, 2)
            last_position = mouse_position
        else: 
            last_position = mouse_position
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()