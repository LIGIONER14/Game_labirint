from pygame import *
#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
  
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    #метод, в котором реализовано управление спрайтом по кнопкам стрелочкам клавиатуры
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Вызываем конструктор класса (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
  
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        ''' перемещает персонажа, применяя текущую горизонтальную и вертикальную скорость'''
        # сначала движение по горизонтали
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platform_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platform_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        platform_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0:
            for p in platform_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platform_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)
    
    def fire(self):
        bullet = Bullet('weapon.png', self.rect.right, self.rect.centery, 25, 30, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    side = 'left'
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10:
            self.kill()

#Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Лабиринт")
window = display.set_mode((win_width, win_height))
back = (119, 210, 223)#задаем цвет согласно цветовой схеме RGB

#Создание яруппы стен
barriers = sprite.Group()

#Группа пули
bullets = sprite.Group()

#Группа монстров
villains = sprite.Group()

#создаем стены картинки
w1 = GameSprite('platform_h.png',win_width / 2 - win_width / 3, win_height / 2, 300, 50)
w2 = GameSprite('platform_v.png', 370, 100, 50, 400)

#Добавление стены в яруппу
barriers.add(w1)
barriers.add(w2)

#создаем спрайты
packman = Player('hero.png', 5, win_height - 80, 80, 80, 0, 0)
villain1 = Enemy('enemy.png', win_width - 80, 150, 80, 80, 5)
villain2 = Enemy('enemy.png', win_width - 80, 260, 80, 80, 5)
final_sprite = GameSprite('enemy2.png', win_width - 85, win_height - 100, 80, 80)

villains.add(villain1)
villains.add(villain2)

#оконцание игры
finish = False

#игровой цикл
run = True

while run:
    #цикл срабатывает каждую 0.05 секунд
    time.delay(50)
  
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()

        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    if not finish:
        window.fill(back)
        #рисуем объекты
        packman.update()
        bullets.update()

        packman.reset()
        w1.reset()
        w2.reset()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()
        
        sprite.groupcollide(villains, bullets, True, True)
        villains.update()
        villains.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.spritecollide(packman, villains, False):
            finish = True
            img = image.load('game-over_1.png')
            d = img.get_width() // img.get_height()
            window.fill((255,255,255))
            window.blit(transform.scale(img, (win_height * d, win_height)),(90,0))
    
        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thumb.jpg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img,(win_width, win_height)), (0,0))

    display.update()

