import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 850))
pygame.display.set_caption("Playbook")

court = pygame.image.load("images/halfcourt.jpeg")
width, height = court.get_size()
resized_court = pygame.transform.smoothscale(court, (width * 0.5, height * 0.5))
screen.blit(resized_court, (0, 0))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()