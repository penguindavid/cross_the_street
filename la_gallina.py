import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("The Chicken Cross The Street")

# Colores
VERDE_PASTO = (34, 139, 34)
AMARILLO_GALLINA = (255, 255, 0)
AZUL_METALICO = (70, 130, 180)
GRIS_CARRETERA = (105, 105, 105)
BLANCO = (255, 255, 255)
MARRON = (139, 69, 19)
rojo = (178, 34, 34)

# Clase Gallina
class Gallina(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(AMARILLO_GALLINA)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO - 50)

    def mover(self, keys):
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= 10
        if keys[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += 10
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 10
        if keys[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += 10

    def reiniciar(self):
        self.rect.center = (ANCHO // 2, ALTO - 50)

# Clase Vehículo
class Vehiculo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad):
        super().__init__()
        self.image = pygame.Surface((80, 40))
        self.image.fill(AZUL_METALICO)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocidad = velocidad

    def update(self):
        self.rect.x += self.velocidad
        if self.rect.right < 0:  # Sale por la izquierda
            self.rect.left = ANCHO
        elif self.rect.left > ANCHO:  # Sale por la derecha
            self.rect.right = 0

# Función para dibujar casas decorativas
def dibujar_casas(pantalla):
    for i in range(1):
        x = ANCHO - 130
        y = 50 + i * 180
        pygame.draw.rect(pantalla, AMARILLO_GALLINA, (x, y, 80, 100))
        pygame.draw.polygon(pantalla, GRIS_CARRETERA, [(x, y), (x + 80, y), (x + 40, y - 50)])

# Configuración inicial del juego
gallina = Gallina()
vehiculos = pygame.sprite.Group()

for i in range(5):
    y = 200 + i * 60
    x = random.randint(0, ANCHO)
    velocidad = random.choice([-5, 5])
    vehiculo = Vehiculo(x, y, velocidad)
    vehiculos.add(vehiculo)

todos_sprites = pygame.sprite.Group()
todos_sprites.add(gallina)
todos_sprites.add(vehiculos)

# Variables del juego
reloj = pygame.time.Clock()
puntuacion = 0
vidas = 3
ejecutando = True
colision_detectada = False

# Bucle principal del juego
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Capturar teclas presionadas
    teclas = pygame.key.get_pressed()
    gallina.mover(teclas)

    # Actualizar posiciones de los vehículos
    vehiculos.update()

    # Verificar colisión de la gallina con los vehículos
    if pygame.sprite.spritecollideany(gallina, vehiculos) and not colision_detectada:
        colision_detectada = True
        print("¡La gallina fue golpeada!")
        vidas -= 1
        if vidas == 0:
            print("¡Juego terminado! La gallina se quedó sin vidas.")
            ejecutando = False  # Finalizar el juego
        gallina.reiniciar()
        puntuacion = 0  # Reiniciar la puntuación
    elif not pygame.sprite.spritecollideany(gallina, vehiculos):
        colision_detectada = False

    # Verificar si la gallina llegó al otro lado
    if gallina.rect.top <= 0:
        puntuacion += 1
        print(f"¡Puntuación: {puntuacion}!")
        gallina.reiniciar()

    # Dibujar en pantalla
    pantalla.fill(VERDE_PASTO)
    pygame.draw.rect(pantalla, GRIS_CARRETERA, (0, 200, ANCHO, 300))
    dibujar_casas(pantalla)
    todos_sprites.draw(pantalla)

    # Dibujar texto de puntuación y vidas
    fuente = pygame.font.SysFont(None, 36)
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
    texto_vidas = fuente.render(f"Vidas: {vidas}", True, BLANCO)
    pantalla.blit(texto_puntuacion, (10, 10))
    pantalla.blit(texto_vidas, (10, 50))

    # Actualizar pantalla
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()








