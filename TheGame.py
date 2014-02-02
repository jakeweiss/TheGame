import pygame
import random
import time
class game(object):
    def __init__(self):
        self.makeScreen()
        self.makePlayer()
        self.gameLevels = levels(self.screen)
        self.levelNumber = 1 
        self.currentLevel = self.gameLevels.levelsList[self.levelNumber-1]
        self.gameOver = False
        self.confetti = False
        self.startTime = time.time()
        self.endTime = 0 
        self.run()
    
    def makePlayer(self):
        self.player = Player()
        self.player.rect.centerx = 100
        self.player.rect.bottom = 495
        self.player.xspeed = 0
        self.player.yspeed = 0
        self.sprites_list = pygame.sprite.Group()
        self.sprites_list.add(self.player)
    
    def makeScreen(self):
        pygame.mixer.pre_init(48000)
        pygame.init()
        screen_width = 1000
        screen_height = 600
        self.screen = pygame.display.set_mode([screen_width, screen_height])
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("The Game")

    def trophyEnding(self):
        if self.player.rect.bottom == 495:
            if self.gameOver == False:
                pygame.mixer.music.load('assets/takeonme2.wav')
                pygame.mixer.music.play(-1)  
                self.endTime = time.time()
                self.fullTime = (self.endTime-self.startTime)/60
                self.gameOver = True
        if self.gameOver:
            self.player.rect.centerx = 850
            #creates mask for spotlight
            mask = pygame.surface.Surface((1000,600)).convert_alpha()
            #fills the screen with black except for an alpha value
            mask.fill((0,0,0,150))
            #draws the spotlight shape in white
            pygame.draw.polygon(mask, (255,255,255),
                                ((750,495),(850,-200),(950,495)))
            pygame.draw.rect(
                mask,(255,255,255),pygame.Rect((280,150),(350,100)))
            font = pygame.font.SysFont("Helvetica", 20)
            text = font.render("Congratulations!", 1, (0,0,0))
            mask.blit(text, (375, 150))
            font = pygame.font.SysFont("Helvetica", 20)
            text = font.render(
                "You beat The Game in %d minutes!" %self.fullTime, 1, (0,0,0))
            mask.blit(text, (300, 185))
            text = font.render("Click anywhere to replay.", 1, (0,0,0))
            mask.blit(text, (340, 220))
            self.screen.blit(mask,(0,0))
            self.sprites_list.draw(self.screen) 
            group = pygame.sprite.Group()
            group.add(self.currentLevel.trophy)
            group.draw(self.screen)
            self.player.yspeed = -2
            #creates random confetti
            for i in xrange(200):
                pygame.draw.circle(self.screen,
                    (random.randrange(0,255),random.randrange(0,255),
                        random.randrange(0,255)),
                    [random.randrange(830,875),random.randrange(0,495)],1)

    def drawAll(self):
        #slight flicker in background
        self.screen.fill((random.randint(250,255),random.randint(250,255),
                        random.randint(250,255)))
        self.currentLevel.drawLevel(self.levelNumber,self.screen)
        self.sprites_list.draw(self.screen)
        #checks if player is in range of the trophy
        if (self.levelNumber == 14 and self.player.rect.centerx>=840 and 
            self.player.rect.centerx<=860):
            self.trophyEnding()

    def bounds(self):
        checkBounds = [self.player]
        for ball in self.currentLevel.balls_list:
            checkBounds+= [ball]
        if self.player.rect.top>=600 or self.player.rect.bottom<=0:
            self.reset()
            #level scrolls right
        if self.player.rect.right >= 700:
            if (self.currentLevel.enterDoor.endX < 
                self.currentLevel.enterDoor.rect.centerx):
                for sprite in self.currentLevel.sprites_list:
                    #continuous moving
                    sprite.rect.x -= self.player.rect.right - 700
                self.player.rect.right=700
            #level scrolls left
        if self.player.rect.left <= 300:
            if (self.currentLevel.enterDoor.startX > 
                self.currentLevel.enterDoor.rect.centerx):
                for sprite in self.currentLevel.sprites_list:
                    #continuous moving
                    sprite.rect.x += 300 - self.player.rect.left
                self.player.rect.left=300
            
    def reset(self):
        self.currentLevel.retry = False
        entered = self.currentLevel.entered
        self.gameLevels.levelsList[self.levelNumber-1] = level(
            self.levelNumber-1,self.screen)
        if self.levelNumber == 3:
            self.gameLevels.makeLevelOne()
        if self.levelNumber == 4:
            self.gameLevels.makeLevelTwo()
        if self.levelNumber == 11:
            self.gameLevels.makeLevelSeven()
        #resets window
        self.currentLevel.enters[entered].rect.centerx = (
            self.currentLevel.enterDoor.startX)
        #resets player location
        self.player.rect.bottom = self.currentLevel.enters[
            entered].rect.bottom
        self.player.rect.centerx = self.currentLevel.enters[
            entered].rect.centerx
        self.player.yspeed = 0
        self.player.onsurface = True
        self.player.gravShifted = "down"
        self.player.spritesheet.set_clip(pygame.Rect(self.player.steady))
        self.player.image = self.player.spritesheet.subsurface(
            self.player.spritesheet.get_clip())

    def welcomeRun(self):
        welcomeRunning = True
        picture = pygame.image.load('assets/welcome.png')
        rect = picture.get_rect()
        self.screen.blit(picture,rect)
        #pygame.mixer.music.load('assets/menu.wav')
        #pygame.mixer.music.play(-1)
        onButton = False  
        while welcomeRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    welcomeRunning = False
                elif event.type == pygame.MOUSEMOTION:
                    (x,y) = pygame.mouse.get_pos()
                    #these coords are the position of the "button"
                    if x>= 342 and x<= 587 and y>= 250 and y<=340:
                        if onButton == False:
                            click = pygame.mixer.Sound('assets/click.wav')
                            click.play(0)
                        onButton = True
                    else:
                        onButton = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    (x,y) = pygame.mouse.get_pos()
                    #these coords are the position of the "button"
                    if x>= 342 and x<= 587 and y>= 250 and y<=340:
                        pygame.mixer.music.stop()
                        gun = pygame.mixer.Sound('assets/gun.wav')
                        gun.play(0)
                        return
            pygame.display.flip()
        pygame.quit()

    def pause(self):
        welcomeRunning = True
        picture = pygame.image.load('assets/pause.png')
        rect = picture.get_rect()
        self.screen.blit(picture,rect)
        #pygame.mixer.music.load('assets/menu.wav')
        #pygame.mixer.music.play(-1)
        while welcomeRunning:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    welcomeRunning = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = False
                        return           
            pygame.display.flip()
        pygame.quit()
    
    def updateAfterExit(self):
        #after you leave a level, other doors are unlocked
        self.player.gravShifted = "down"
        if self.levelNumber == 3:
            self.gameLevels.levelsList[1].exits[1].greens = 3
            self.gameLevels.levelsList[0].exits[1].greens = 1
        if self.levelNumber == 4:
            self.gameLevels.levelsList[1].exits[2].greens = 3
            self.gameLevels.levelsList[0].exits[1].greens = 2 
        if self.levelNumber == 7:
            self.gameLevels.levelsList[5].exits[1].greens = 3
            self.gameLevels.levelsList[0].exits[2].greens = 1
        if self.levelNumber == 8:
            self.gameLevels.levelsList[5].exits[2].greens = 3
            self.gameLevels.levelsList[0].exits[2].greens = 2
        if self.levelNumber == 11:
            self.gameLevels.levelsList[9].exits[1].greens = 3
        if self.levelNumber == 12:
            self.gameLevels.levelsList[9].exits[2].greens = 3

    def keyDownA(self):
        if (self.player.gravShifted == "down" or
            self.player.gravShifted == "up"):
            self.player.xspeed = -10
        elif self.player.gravShifted == "right":
            self.player.jump()

    def keyDownD(self):
        if (self.player.gravShifted == "down" or
            self.player.gravShifted == "up"):
            self.player.xspeed = 10
        elif self.player.gravShifted == "left":
            self.player.jump()

    def keyDownW(self):
        level = self.currentLevel
        #if there are no collisions, the player jumps or moves
        #depending on gravity
        if (pygame.sprite.spritecollideany(self.player,
                         level.doors_list) == None and
                        pygame.sprite.spritecollideany(self.player,
                         level.posts_list) == None):
            if self.player.gravShifted == "down":
                self.player.jump()
            elif (self.player.gravShifted == "left" or
             self.player.gravShifted == "right"):
                self.player.yspeed = -10
        #if the player collides with a post
        elif (pygame.sprite.spritecollideany(
            self.player,level.posts_list) != None):
            for post in level.posts_list.sprites():
                if self.player.rect.colliderect(post):
                    click = pygame.mixer.Sound(
                        'assets/click.wav')
                    click.play(0)
                    if post.mode == 0:
                        post.mode = 1
                        self.gameLevels.levelsList[
                        post.doorLevel-1].exits[
                        post.doorNumber].greens+=1
                    elif post.mode == 1:
                        post.mode = 0
                        self.gameLevels.levelsList[
                        post.doorLevel-1].exits[
                        post.doorNumber].greens-=1
        #if the player collides with an enter door
        elif (pygame.sprite.spritecollideany(
            self.player, level.enters) != None):
            for enter in level.enters:
                if (self.player.rect.colliderect(enter) and
                 self.levelNumber != 1):
                    door = pygame.mixer.Sound(
                            'assets/door.wav')
                    door.play(0)
                    self.levelNumber = enter.fromRoom
                    self.player.rect.centerx = (self.gameLevels
                        .levelsList[self.levelNumber-1].
                        exits[enter.whichExit].rect.centerx)
                    self.player.rect.bottom = (self.gameLevels.
                        levelsList[self.levelNumber-1].
                        exits[enter.whichExit].rect.bottom-1)
                    self.player.gravShifted == "down"
        #if the player collides with an exit door
        else:
            for exit in level.exits:
                if self.player.rect.colliderect(exit):
                    if exit.greens == 3:
                        self.updateAfterExit()
                        door = pygame.mixer.Sound(
                            'assets/door.wav')
                        door.play(0)
                        self.levelNumber = exit.toRoom
                        (self.gameLevels.levelsList
                            [self.levelNumber-1]
                            .entered) = exit.whichEnter
                        self.player.rect.centerx = (self.
                            gameLevels.levelsList
                            [self.levelNumber-1].
                            enters[exit.whichEnter].
                            rect.centerx)
                        self.player.rect.bottom = (self.
                            gameLevels.levelsList
                            [self.levelNumber-1].
                            enters[exit.whichEnter].
                            rect.bottom-1)
                        self.player.gravShifted == "down"

    def pressed(self):
        pressed = pygame.key.get_pressed()
        if (self.player.gravShifted == "up" or
            self.player.gravShifted == "down"):
            if pressed[pygame.K_a]:
                self.keyDownA()
            if pressed[pygame.K_d]:
                self.keyDownD()
        else:
            if pressed[pygame.K_w]:
                self.keyDownW()
            if pressed[pygame.K_s]:
                self.keyDownS()


    def keyDown(self,event):
        if event.key == pygame.K_p:
            self.paused = True
        if event.key == pygame.K_a:
            self.keyDownA()
        elif event.key == pygame.K_d:
            self.keyDownD()
        elif event.key == pygame.K_w:      
            self.keyDownW()
        elif event.key == pygame.K_s:
            self.keyDownS()
        elif event.key == pygame.K_r:
            self.keyDownR()
        elif event.key == pygame.K_1:
            self.levelNumber = 5
        elif event.key == pygame.K_2:
            self.levelNumber = 9
        elif event.key == pygame.K_3:
            self.levelNumber = 13
        elif event.key == pygame.K_4:
            self.levelNumber = 14
        elif event.key == pygame.K_RIGHT:
            self.levelNumber +=1
        elif event.key == pygame.K_q:
            self.currentLevel.boss.ended = 1


    def keyUp(self,event):
        if event.key == pygame.K_a:
            self.keyUpA()
        elif event.key == pygame.K_d:
            self.keyUpD()
        elif event.key == pygame.K_w:
            self.keyUpW()
        elif event.key == pygame.K_s:
            self.keyUpS()

    def keyDownS(self):
        if self.player.gravShifted == "up":
            self.player.jump()
        elif (self.player.gravShifted == "left" or
              self.player.gravShifted == "right"):
            self.player.yspeed = 10

    def keyDownR(self):
        if self.currentLevel.retry == True:
            self.currentLevel.reset = True

    def keyUpA(self):
        if (self.player.gravShifted == "down" or
            self.player.gravShifted == "up"):
            self.player.xspeed = 0

    def keyUpD(self):
        if (self.player.gravShifted == "down" or 
            self.player.gravShifted == "up"):
            self.player.xspeed = 0

    def keyUpW(self):
        if (self.player.gravShifted == "left" or
            self.player.gravShifted == "right"):
            self.player.yspeed = 0

    def keyUpS(self):
        if (self.player.gravShifted == "left" or
            self.player.gravShifted == "right"):
            self.player.yspeed = 0

    def mouseButtonDown(self):
        #for resetting a level if the player dies during a boss fight
        if (self.currentLevel.retry == True and 
            self.currentLevel.retryButton.rect.collidepoint(
            pygame.mouse.get_pos())):
            self.currentLevel.reset = True
        #for replaying the game
        if self.gameOver:
            pygame.mixer.music.stop()
            self.__init__()


    def run(self):
        gameRunning = True
        self.welcomeRun()
        self.paused = False
        while gameRunning:
            while self.paused:
                self.pause()
            self.pressed()
            if self.gameOver == False:
                self.pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameRunning = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseButtonDown()
                if self.gameOver == False:
                    level = self.currentLevel
                    if event.type == pygame.KEYDOWN:
                        self.keyDown(event)
                    elif event.type == pygame.KEYUP:
                        self.keyUp(event)
                    
            self.update()
            self.drawAll()
            self.clock.tick(20)
            pygame.display.flip()
        pygame.quit()

    def update(self):
        self.player.addgrav()
        self.player.updateGrav(self.currentLevel)
        for block in self.currentLevel.blocks_list:
            block.update(self.player)
        self.player.update(self.currentLevel.collision_list)
        for exit in self.currentLevel.exits:
            exit.update()
        for post in self.currentLevel.posts_list:
            post.update()
        for button in self.currentLevel.buttons_list:
            button.update(self.player,self.currentLevel.balls_list)
        for ball in self.currentLevel.balls_list:
            ball.addGrav(self.player)
            ball.update(self.player,self.currentLevel.blocks_list)
        self.currentLevel = self.gameLevels.levelsList[self.levelNumber-1]
        self.bounds()
        if self.currentLevel.retry:
            self.currentLevel.retry_group.add(self.currentLevel.retryButton)
        if (self.levelNumber == 5 or 
            self.levelNumber == 9 or 
            self.levelNumber == 13):
            self.updateBosses()
        else:
            self.updateOtherLevels()

    def updateOtherLevels(self):
        if self.levelNumber == 7:
            for button in self.currentLevel.buttons_list:
                if button.mode == 1:
                    #beams player up in the light
                    if self.player.rect.x>=100 and self.player.rect.x<=200:
                        self.player.yspeed = -5
                    if button.pressed == False:
                        button.pressed = True
                    #button also prevents door from opening
                        self.gameLevels.levelsList[6].exits[0].greens -= 1
                elif button.pressed:
                    self.gameLevels.levelsList[6].exits[0].greens += 1
                    button.pressed = False
        if self.levelNumber == 8:
            for button in self.currentLevel.buttons_list:
                if button.mode == 1:
                    #beams playing up in the light
                    if (button.rect.y>100 and 
                        self.player.rect.x>=button.rect.x+400 and 
                        self.player.rect.x<=button.rect.x+500):
                        self.player.yspeed = -5
                    #beams player down in the light
                    elif (self.player.rect.x>=button.rect.x-350 and
                        self.player.rect.x<=button.rect.x-250):
                        self.player.yspeed = 5
        if self.levelNumber == 12:
            for button in self.currentLevel.buttons_list:
                if button.mode == 1:
                    #sends player through a "window"
                    if (button.rect.y>100 and self.player.rect.left<= 5 and 
                        self.player.rect.top>=395):
                        self.player.rect.right=995
                        self.player.rect.centery=100
                    #another "window"
                    elif (self.player.rect.left<=5 and 
                        self.player.rect.top<=5):
                        self.player.rect.right = 995
                        self.player.rect.centery = 300
                        
    def updateBosses(self):
        if self.currentLevel.health.health>0:
            self.currentLevel.boss.update(self.currentLevel.collision_list,
            self.player,self.currentLevel)
        self.currentLevel.boss.addgrav()
        self.player.updateGrav(self.currentLevel)
        for bullet in self.currentLevel.bullets_list:
            bullet.update(self.player)
        if self.levelNumber == 5:
            self.updateBossOne()
        elif self.levelNumber == 9:
            self.updateBossTwo()
        else:
            self.updateBossThree()
        if self.currentLevel.boss.ended == 1:
            #every time you beat a boss a trophy door is more unlocked
            self.gameLevels.levelsList[0].exits[3].greens+=1
            self.currentLevel.boss.kill()
            self.currentLevel.boss.remove()
            self.currentLevel.health.kill()
            self.currentLevel.health.remove()
            self.currentLevel.heli = Heli(600,495)
            self.currentLevel.sprites_list.add(self.currentLevel.heli)
            for bullet in self.currentLevel.bullets_list:
                bullet.kill()
                bullet.remove()
            self.currentLevel.boss.ended = 3
        if self.currentLevel.reset:
            self.currentLevel.reset = False
            self.currentLevel.retry = False
            self.makePlayer()
            self.player.gravShifted = "down" 
        if (self.currentLevel.boss.ended != 0 and 
            self.player.rect.colliderect(self.currentLevel.heli)):
        #starts helicopter animation
            self.player.kill()
            self.player.remove()
            self.heli = pygame.mixer.Sound('assets/heli.wav')
            self.heli.play(-1,4500)
            self.currentLevel.flyAway = True
        if self.currentLevel.flyAway:
            self.currentLevel.heli.update()
            self.currentLevel.heli.rect.y-=5
            if self.currentLevel.heli.rect.bottom<=0:
                self.levelNumber = 1
                self.makePlayer()
                self.player.rect.bottom = 495
                level = self.gameLevels.levelsList[0]
                if level.exits[3].greens == 1:
                    self.player.rect.centerx = level.exits[0].rect.centerx
                elif level.exits[3].greens == 2:
                    self.player.rect.centerx = level.exits[1].rect.centerx
                else:
                    self.player.rect.centerx = level.exits[2].rect.centerx

    def updateBossOne(self):
        self.currentLevel.health.updateOne(self.player, self.currentLevel)
        self.currentLevel.spikes.update(self.currentLevel.boss)
        if self.currentLevel.boss.ended == 1:
            self.currentLevel.spikes.kill()
            self.currentLevel.spikes.remove()
            self.gameLevels.levelsList[0].exits[1].greens+=1
        if self.currentLevel.reset:
            self.gameLevels.levelsList[4] = level(4,self.screen)
            self.gameLevels.makeLevelThree()

    def updateBossTwo(self):
        self.currentLevel.health.updateTwo(self.player, self.currentLevel)
        if self.currentLevel.boss.ended == 1:
            self.currentLevel.timer.kill()
            self.currentLevel.timer.remove()
            self.gameLevels.levelsList[0].exits[2].greens+=1
        if self.currentLevel.reset:
            self.gameLevels.levelsList[8] = level(8,self.screen)
            self.gameLevels.makeLevelSix()
        #there can only be one ball on the screen at once
        for button in self.currentLevel.buttons_list:
            if (button.mode == 1 and len(self.currentLevel.balls_list) == 0 and 
                self.currentLevel.boss.vulnurable == False):
                ball = Ball(button.rect.centerx,275)
                drop = pygame.mixer.Sound('assets/balldrop.wav')
                drop.play(0)
                self.currentLevel.balls_list.add(ball)
                self.currentLevel.sprites_list.add(ball)
                machine = Item("ballmachine", button.rect.centerx,270)
                self.currentLevel.sprites_list.add(machine)
        for ball in self.currentLevel.balls_list:
            if ball.rect.colliderect(self.currentLevel.boss):
                self.currentLevel.boss.vulnurable = True
                self.currentLevel.boss.vulnurableTime = (pygame.time.
                    get_ticks())
                #countdown to hurt boss
                time = pygame.time.get_ticks()
                self.currentLevel.timer = Text(str(3-100*(
                                        time-self.currentLevel.
                                        boss.vulnurableTime)/100000)
                                        ,500,100,50)
                self.currentLevel.sprites_list.add(self.currentLevel.timer)
                ball.kill()
                ball.remove()
            if ball.rect.bottom >= 495:
                ball.kill()
                ball.remove()
        time = pygame.time.get_ticks()
        if self.currentLevel.boss.vulnurable:
            self.currentLevel.timer.kill()
            self.currentLevel.timer.remove()
            #countdown to hurt boss
            self.currentLevel.timer = Text(str(3-100*(
                                      time-self.currentLevel.boss.
                                      vulnurableTime)/100000),500,100,50)
            self.currentLevel.sprites_list.add(self.currentLevel.timer)
            self.currentLevel.boss.xspeed = 0
            if time-self.currentLevel.boss.vulnurableTime>3000:
                self.currentLevel.timer.kill()
                self.currentLevel.timer.remove()
                self.currentLevel.boss.vulnurable = False
                
    def updateBossThree(self):
        self.currentLevel.health.updateThree(self.player, self.currentLevel)
        if self.currentLevel.reset:
            self.gameLevels.levelsList[12] = level(12,self.screen)
            self.gameLevels.makeLevelNine()
        self.currentLevel.spikes.update(self.currentLevel.boss)
        for button in self.currentLevel.buttons_list:
            if button.mode == 1 and button.pressed == False:
                x = button.rect.x
                y = self.currentLevel.block.rect.y
                self.currentLevel.block.remove()
                self.currentLevel.block.kill()
                button.remove()
                button.kill()
                button = Button(x+100,5,40,3)
                self.currentLevel.buttons_list.add(button)
                self.currentLevel.sprites_list.add(button)
                self.currentLevel.block = Block(890,y+100,210,5)
                self.currentLevel.blocks_list.add(self.currentLevel.block)
                self.currentLevel.collision_list.add(self.currentLevel.block)
                self.currentLevel.sprites_list.add(self.currentLevel.block)
                button.pressed = True   
            elif button.pressed:
                 button.pressed = False     

            
class levels(object):
    def __init__(self,screen):
        self.levelsList = []
        self.screen = screen
        for i in xrange(14):
            self.levelsList.append(level(i,self.screen))
            self.levelsList[i].entered = 0
            self.levelsList[i].exits = []
            self.levelsList[i].enters = []
        self.makeRoomOne()
        self.makeRoomTwo()
        self.makeLevelOne()
        self.makeLevelTwo()
        self.makeLevelThree()
        self.makeRoomThree()
        self.makeLevelFour()
        self.makeLevelFive()
        self.makeLevelSix()
        self.makeRoomFour()
        self.makeLevelSeven()
        self.makeLevelEight()
        self.makeLevelNine()
        self.makeTrophyRoom()
    #these functions are very long because
    #it creates all the levels and adds each
    #element to their respective lists, needed
    #for collision detection and drawing
    def makeRoomOne(self):
        level = self.levelsList[0]
        level.enterDoor = EnterDoor(100,495,1,0)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters+= [level.enterDoor]
        name = Text("Outside",level.enterDoor.rect.centerx,360)
        level.sprites_list.add(name)
        level.enterDoor.endX = level.enterDoor.startX-500
        exit = ExitDoor(300, 495,0,2,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Levels 1-3",exit.rect.centerx,360)
        level.sprites_list.add(name)
        exit = ExitDoor(500, 495,0,6,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Levels 4-6",exit.rect.centerx,360)
        level.sprites_list.add(name)
        exit = ExitDoor(700, 495,0,10,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Levels 7-9",exit.rect.centerx,360)
        level.sprites_list.add(name)
        exit = ExitDoor(900, 495,0,14,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("???",exit.rect.centerx,360)
        level.sprites_list.add(name)
        block = Block(0,0,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(65,122,1200,5)
        level.collision_list.add(block)
        level.blocks_list.add(block)
        level.sprites_list.add(block)
        block = Block(1100,375,160,5)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        level.blocks_list.add(block)
        block = Block(1400,250,100,5)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        level.blocks_list.add(block)
        block = Block(-10,495,1515,5)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        level.blocks_list.add(block)
        post = Post(200,122,1,0)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        post = Post(600,122,1,0)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        post = Post(1000,122,1,0)
        level.posts_list.add(post)
        level.sprites_list.add(post)

    def makeRoomTwo(self):
        level = self.levelsList[1]
        level.enterDoor = EnterDoor(100,495,1,0)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX
        exit = ExitDoor(350, 495,3,3,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Level 1",exit.rect.centerx,360)
        level.sprites_list.add(name)
        exit = ExitDoor(600, 495,2,4,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Level 2",exit.rect.centerx,360)
        level.sprites_list.add(name)
        exit = ExitDoor(850, 495,2,5,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Boss 1",exit.rect.centerx,360)
        level.sprites_list.add(name)
        block = Block(0,0,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(-5,495,1510,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)

    def makeLevelOne(self):
        level = self.levelsList[2]
        level.enterDoor = EnterDoor(300,495,2,0)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX-200
        exit = ExitDoor(400,125,0,2,0,True)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        grav = Item("gravup",650,495, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        block = Block(0,0,600,5)
        level.collision_list.add(block)
        level.blocks_list.add(block)
        level.sprites_list.add(block)
        block = Block(700,0,800,5)
        level.collision_list.add(block)
        level.blocks_list.add(block)
        level.sprites_list.add(block)
        block = Block(-5,495,1510,5)
        level.collision_list.add(block)
        level.blocks_list.add(block)
        level.sprites_list.add(block)
        post = Post(100,80,3,0,True)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        post = Post(800,80,3,0,True)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        post = Post(1100,495,3,0)
        level.posts_list.add(post)
        level.sprites_list.add(post)

    def makeLevelTwo(self):
        level = self.levelsList[3]
        level.enterDoor = EnterDoor(60,495,2,1)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX-300
        exit = ExitDoor(60, 125,2,2,0,True)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        grav = Item("gravup",175,495, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        block = Block(0,0,205,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,250,205,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(300,0,5,180)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(300,320,5,180)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(400,0,205,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        grav = Item("gravdown",500,55, "down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        block = Block(700,0,5,180)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(700,320,5,180)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(800,495,205,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(400,250,205,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        grav = Item("gravup",900,495, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        block = Block(1100,0,5,180)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(1100,320,5,180)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(1150,495,255,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(1200,0,205,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        grav = Item("gravdown", 1250,55, "down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravup", 1210,495, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        block = Block(-5,495,210,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        post = Post(1280,495,4,0)
        level.posts_list.add(post)
        level.sprites_list.add(post)

    def makeLevelThree(self):
        level = self.levelsList[4]
        level.enterDoor = EnterDoor(300,495,2,2)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX
        block = Block(0,0,1000,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,495,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,0,5,495)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(995,0,5,500)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        level.boss = BossOne()
        level.sprites_list.add(level.boss)
        level.spikes = Spikes(700,495)
        level.sprites_list.add(level.spikes)
        grav = Item("gravup",200,75, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravleft",50,200, "left")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravright",950,200, "right")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravup",850,75,"up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravleft",30,430, "left")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravdown",200,400, "down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravright",950,450, "right")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravdown",800,400, "down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        level.health = HealthBar()
        level.sprites_list.add(level.health)
        level.flyAway = False

    def makeRoomThree(self):
        level = self.levelsList[5]
        level.enterDoor = EnterDoor(100,495,1,1)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX
        exit = ExitDoor(350, 495,3,7,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Level 4",exit.rect.centerx,360)
        level.sprites_list.add(name)
        exit = ExitDoor(600, 495,2,8,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Level 5",exit.rect.centerx,360)
        level.sprites_list.add(name)
        exit = ExitDoor(850, 495,2,9,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Boss 2",exit.rect.centerx,360)
        level.sprites_list.add(name)
        block = Block(0,0,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,495,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        
    def makeLevelFour(self):
        level = self.levelsList[6]
        level.enterDoor = EnterDoor(50,495,6,0)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters += [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX
        exit = ExitDoor(700,495,1,6,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        block = Block(0,0,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,495,1500,5)
        level.collision_list.add(block)
        level.blocks_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,150,100,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(200,150,100,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        post = Post(50,150,7,0)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        post = Post(250,150,7,0)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        block = Block(1495,0,5,600)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        ball = Ball(500,495)
        level.balls_list.add(ball)
        level.sprites_list.add(ball)
        button = Button(350,492,40,3)
        level.buttons_list.add(button)
        level.sprites_list.add(button)

    def makeLevelFive(self):
        level = self.levelsList[7]
        level.enterDoor = EnterDoor(300,495,6,1)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX-200
        block = Block(0,0,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,495,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        post = Post(150,80,8,0,True)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        button = Button(100,492,40,3)
        level.buttons_list.add(button)
        level.sprites_list.add(button)
        button = Button(1150,5,40,3)
        level.buttons_list.add(button)
        level.sprites_list.add(button)
        exit = ExitDoor(1000,495,2,6,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        grav = Item("gravup",550,55,"up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravdown",850,495,"down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        ball = Ball(500,495)
        level.balls_list.add(ball)
        level.sprites_list.add(ball)

    def makeLevelSix(self):
        level = self.levelsList[8]
        level.enterDoor = EnterDoor(300,495,6,2)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX
        block = Block(0,0,1000,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(75,200,100,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(300,200,140,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(560,200,140,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(825,200,100,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,495,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,0,5,495)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(995,0,5,600)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        level.boss = BossTwo()
        level.sprites_list.add(level.boss)
        level.health = HealthBar()
        level.sprites_list.add(level.health)
        grav = Item("gravdown",30,55, "down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravup",30,495, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravdown",970,55, "down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravup",970,495, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        button = Button(350,197,40,3)
        level.buttons_list.add(button)
        level.sprites_list.add(button)
        machine = Item("ballmachine",button.rect.centerx,270)
        level.sprites_list.add(machine)
        button = Button(610,197,40,3)
        level.buttons_list.add(button)
        level.sprites_list.add(button)
        machine = Item("ballmachine",button.rect.centerx,270)
        level.sprites_list.add(machine)
        level.flyAway = False


    def makeRoomFour(self):
        level = self.levelsList[9]
        level.enterDoor = EnterDoor(100,495,1,2)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX
        exit = ExitDoor(350, 495,3,11,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Level 7",exit.rect.centerx,360)
        level.sprites_list.add(name)
        exit = ExitDoor(600, 495,2,12,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Level 8",exit.rect.centerx,360)
        level.sprites_list.add(name)
        exit = ExitDoor(850, 495,2,13,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        name = Text("Boss 3",exit.rect.centerx,360)
        level.sprites_list.add(name)
        block = Block(0,0,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,495,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        
    def makeLevelSeven(self):
        level = self.levelsList[10]
        level.enterDoor = EnterDoor(100,495,10,0)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX
        exit = ExitDoor(60, 125,1,10,0,True)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        block = Block(-5,0,205,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(-5,495,205,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(350,400,100,5,1,300,550)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(700,400,100,5,-1,650,900)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        post = Post(600,495,11,0,True)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        post = Post(950,495,11,0,True)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        grav = Item("gravdown",950,200, "down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravup",950,300, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravdown",600,200, "down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravup",600,300, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravdown",350,120, "down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        grav = Item("gravup",75,200, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)

    def makeLevelEight(self):
        level = self.levelsList[11]
        level.enterDoor = EnterDoor(300,495,10,1)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX
        enterDoor = EnterDoor(340,300,12,0)
        level.doors_list.add(enterDoor)
        level.sprites_list.add(enterDoor)
        level.enters+= [enterDoor]
        block = Block(300,300,150,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(300,180,150,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(300,180,5,120)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(450,180,5,125)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        exit = ExitDoor(800, 495,1,12,1)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        exit = ExitDoor(700, 495,2,10,0)
        level.doors_list.add(exit)
        level.sprites_list.add(exit)
        level.exits += [exit]
        block = Block(0,0,1000,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,495,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        post = Post(800,200,12,0)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        post = Post(410,300,12,1)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        grav = Item("gravup",750,200, "up")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        ball = Ball(500,495)
        post = Post(800,280,12,0,True)
        level.posts_list.add(post)
        level.sprites_list.add(post)
        grav = Item("gravdown",750,255, "down")
        level.sprites_list.add(grav)
        level.grav_list.add(grav)
        ball = Ball(500,495)
        level.balls_list.add(ball)
        level.sprites_list.add(ball)
        button = Button(600,492,40,3)
        level.buttons_list.add(button)
        level.sprites_list.add(button)
        block = Block(720,200,100,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        button = Button(170,5,40,3)
        level.buttons_list.add(button)
        level.sprites_list.add(button)
        
    def makeLevelNine(self):
        level = self.levelsList[12]
        level.enterDoor = EnterDoor(300,495,10,2)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX
        block = Block(0,0,1000,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,495,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,0,5,495)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(995,0,5,600)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        level.block = Block(890,220,210,5)
        level.blocks_list.add(level.block)
        level.collision_list.add(level.block)
        level.sprites_list.add(level.block)
        block = Block(890,0,5,500)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(400,370,100,5,1,70,500)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(580,370,100,5,-1,550,800)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(80,240,100,5,-1,70,400)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(700,240,100,5,1,400,800)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(200,120,100,5,-4,190,800)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        level.spikes = Spikes(940,495)
        level.sprites_list.add(level.spikes)
        level.boss = BossThree()
        level.sprites_list.add(level.boss)
        level.health = HealthBar()
        level.sprites_list.add(level.health)
        level.flyAway = False
        button = Button(350,5,40,3)
        level.buttons_list.add(button)
        level.sprites_list.add(button)

    def makeTrophyRoom(self):
        level = self.levelsList[13]
        level.enterDoor = EnterDoor(100,495,1,3)
        level.doors_list.add(level.enterDoor)
        level.sprites_list.add(level.enterDoor)
        level.enters+= [level.enterDoor]
        level.enterDoor.endX = level.enterDoor.startX
        block = Block(0,0,1000,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        block = Block(0,495,1500,5)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
        level.trophy = Item("trophy",850,495)
        level.sprites_list.add(level.trophy)
        block = Block(1495,0,5,600)
        level.blocks_list.add(block)
        level.collision_list.add(block)
        level.sprites_list.add(block)
    

class level(object):
    def __init__(self, i,screen):
        self.screen = screen
        self.levelNumber = 1
        #creates different sprite groups
        self.doors_list = pygame.sprite.Group()
        self.retry_group = pygame.sprite.Group()
        self.posts_list = pygame.sprite.Group()
        self.collision_list = pygame.sprite.Group()
        self.buttons_list = pygame.sprite.Group()
        self.balls_list = pygame.sprite.Group()
        self.sprites_list = pygame.sprite.Group()
        self.blocks_list = pygame.sprite.Group()
        self.grav_list = pygame.sprite.Group()
        self.bullets_list = pygame.sprite.Group()
        self.entered = 0
        self.exits = []
        self.enters = []
        self.retry = False
        self.reset = False
    def drawLevelSeven(self,screen):
        for button in self.buttons_list:
            #draws light beams
            if button.mode == 1:
                y = random.randint(5,495)
                pygame.draw.lines(screen,
                ((random.randint(0,255),random.randint(0,255),
                random.randint(0,255))),True,((100,y),(200,y)), 10)
                pygame.draw.lines(screen,
                ((random.randint(0,255),random.randint(0,255),
                random.randint(0,255))),True,((100,5),(100,495)), 10)
                pygame.draw.lines(screen,
                ((random.randint(0,255),random.randint(0,255),
                random.randint(0,255))),True,((200,495),(200,5)), 10)

    def drawLevelEight(self,screen):
        #draws light beams
        for button in self.buttons_list:
            if button.mode == 1:
                y = random.randint(5,495)
                if button.rect.y>100:
                    (x1, x2) = (button.rect.x+400,button.rect.x+500)
                    pygame.draw.lines(screen,
                    ((random.randint(0,255),random.randint(0,255),
                    random.randint(0,255))),True,((x1,y),(x2,y)), 10)
                    pygame.draw.lines(screen,
                    ((random.randint(0,255),random.randint(0,255),
                    random.randint(0,255))),True,((x1,5),(x1,495)), 10)
                    pygame.draw.lines(screen,
                    ((random.randint(0,255),random.randint(0,255),
                    random.randint(0,255))),True,((x2,495),(x2,5)), 10)
                else:
                    (x1, x2) = (button.rect.x-350,button.rect.x-250)
                    pygame.draw.lines(screen,
                    ((random.randint(0,255),random.randint(0,255),
                    random.randint(0,255))),True,((x1,y),(x2,y)), 10)
                    pygame.draw.lines(screen,
                    ((random.randint(0,255),random.randint(0,255),
                    random.randint(0,255))),True,((x1,5),(x1,495)), 10)
                    pygame.draw.lines(screen,
                    ((random.randint(0,255),random.randint(0,255),
                    random.randint(0,255))),True,((x2,495),(x2,5)), 10)

    def drawLevelTwelve(self,screen):
        #draws "windows"
        for button in self.buttons_list:
            if button.mode == 1:
                if button.rect.y>100:
                    pygame.draw.lines(screen,
                    ((random.randint(0,255),random.randint(0,255),
                    random.randint(0,255))),True,((0,395),(0,494)), 8)
                    pygame.draw.lines(screen,
                    ((random.randint(0,255),random.randint(0,255),
                    random.randint(0,255))),True,((999,50),(999,150)), 10)
                else:
                    pygame.draw.lines(screen,
                    ((random.randint(0,255),random.randint(0,255),
                    random.randint(0,255))),True,((0,5),(0,100)), 8)
                    pygame.draw.lines(screen,
                    ((random.randint(0,255),random.randint(0,255),
                    random.randint(0,255))),True,((999,255),(999,350)), 10)

    def drawLevel(self,levelNumber,screen):
        self.doors_list.draw(screen)
        self.sprites_list.draw(screen)
        #draws left and right walls if at beginning/end of level
        if (self.enterDoor.startX <= self.enterDoor.rect.centerx):
            pygame.draw.lines(
                screen, ((0,0,0)),True,((2,0),(2,498)), 5)

        if (self.enterDoor.endX >= self.enterDoor.rect.centerx):
            pygame.draw.lines(
                screen,((0,0,0)),True,((997,0),(997,498)), 5)
        if self.retry:
            screen.fill((255,255,255))
            self.retry_group.draw(screen)
        if levelNumber == 7:
            self.drawLevelSeven(screen)
        if levelNumber == 8:
            self.drawLevelEight(screen)
        if levelNumber == 12:
            self.drawLevelTwelve(screen)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load("assets/spritesheet.png")
        self.steady = (0,0,50,100)
        self.jumping = (50,0,50,100)
        self.movingright = [(0,100,50,100),(50,100,50,100),(100,100,50,100)]
        self.movingleft = [(0,200,50,100),(50,200,50,100),(100,200,50,100)]
        self.spritesheet.set_clip(pygame.Rect(self.steady))
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.xspeed = 0
        self.yspeed = 0
        self.onsurface = True
        self.gravShifted = "down"
        self.moveframe = 0
    def update(self,other):
        #collision detection doesn't work if width/height aren't correct
        if self.gravShifted == "left" or self.gravShifted == "right":
            self.rect.width = 100
            self.rect.height = 50
        else:
            self.rect.width = 50
            self.rect.height = 100
        self.updatePlayerClip()
        self.updateXCollisions(other)
        self.updateYCollisions(other)
        #bounds
        if self.rect.x<=5:
            self.rect.x = 5
        if self.rect.right>=995:
            self.rect.right = 995

    def updatePlayerClip(self):
        #animation of player
        if self.onsurface == False:
            self.moveframe = 0
            self.spritesheet.set_clip(pygame.Rect(self.jumping))
            self.image=self.spritesheet.subsurface(self.spritesheet.get_clip())
        else:
            if (self.xspeed == 0 and (self.gravShifted == "up" or 
                self.gravShifted == "down") or self.yspeed == 0 and 
            (self.gravShifted == "left" or self.gravShifted == "right")):
                self.moveframe = 0
                self.spritesheet.set_clip(pygame.Rect(self.steady))
            elif (self.xspeed<0 and (self.gravShifted == "up" or
             self.gravShifted == "down") or (self.yspeed<0 and 
             self.gravShifted == "left")
                or (self.yspeed>0 and self.gravShifted == "right")):
                self.spritesheet.set_clip(
                    pygame.Rect(self.movingleft[self.moveframe]))
            elif (self.xspeed>0 and (self.gravShifted == "up" 
                or self.gravShifted == "down") or 
            (self.yspeed>0 and self.gravShifted == "left") or 
            (self.yspeed<0 and self.gravShifted == "right")):
                self.spritesheet.set_clip(
                    pygame.Rect(self.movingright[self.moveframe]))
            #cycles through 3 images
            self.moveframe = (self.moveframe+1)%3
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        self.updateOrientation()

    def updateOrientation(self):
        if self.gravShifted == "up":
            flipped = pygame.transform.flip(self.image, 0, 1)
            self.image = flipped
        if  self.gravShifted == "left":
            rotate = pygame.transform.rotate(self.image, 270)
            self.image = rotate
        if self.gravShifted == "right":
            rotate = pygame.transform.rotate(self.image,90)
            self.image = rotate

    def updateXCollisions(self,other):
        #sort of self explanatory
        self.rect.x+=self.xspeed
        collisions = pygame.sprite.spritecollide(self, other, False)
        if (collisions == [] and (self.yspeed>.5 and self.gravShifted == "up") 
            or (self.yspeed<-.5 and self.gravShifted == "down") or
            (self.xspeed>.5 and self.gravShifted == "left") or
            (self.xspeed<-.5 and self.gravShifted == "right")):
            self.onsurface = False
        for collision in collisions:
            if self.xspeed <= 0 and self.rect.centerx>collision.rect.centerx:
                self.rect.left = collision.rect.right
                if self.gravShifted == "left":
                    self.onsurface = True
            else:
                self.rect.right = collision.rect.left
                if self.gravShifted == "right":
                    self.onsurface = True
            self.xspeed = 0

    def updateYCollisions(self,other):
        #sort of self explanatory
        self.rect.y+=self.yspeed
        collisions = pygame.sprite.spritecollide(self, other, False)
        for collision in collisions:
            if self.yspeed >= .5 and self.rect.centery<collision.rect.centery:
                self.rect.bottom = collision.rect.top
                if self.gravShifted == "down":
                    self.onsurface = True
            else:
                self.rect.top = collision.rect.bottom
                if self.gravShifted == "up":
                    self.onsurface = True
            self.yspeed = .5

    def updateGrav(self,currentLevel):
        #if player collides with gravity shifter... gravity shifts
        for grav in currentLevel.grav_list:
            if self.rect.colliderect(grav):
                if grav.special == "right":
                    self.gravShifted = "right"
                elif grav.special == "left":
                    self.gravShifted = "left"
                elif grav.special == "up":
                    self.gravShifted = "up"
                else:
                    self.gravShifted = "down"

    def jump(self):
        if self.onsurface:
            jump = pygame.mixer.Sound('assets/jump.wav')
            jump.play(0)
            if self.gravShifted == "up":
                self.yspeed = 12
            elif self.gravShifted == "down":
                self.yspeed = -12
            elif self.gravShifted == "left":
                self.xspeed = 12
            else:
                self.xspeed = -12
            self.onsurface = False

    def addgrav(self):
        if self.gravShifted == "up":
            self.yspeed-=.5
        elif self.gravShifted == "down":
            self.yspeed+=.5
        elif self.gravShifted == "left":
            self.xspeed-=.5
        else:
            self.xspeed+=.5


class BossOne(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load("assets/bossOneSpritesheet.png")
        self.steady = (0,0,100,170)
        self.jumping = (100,0,100,170)
        self.spritesheet.set_clip(pygame.Rect(self.jumping))
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.xspeed = 0
        self.yspeed = 18
        self.onsurface = False
        self.gravShifted = "down"
        self.rect.centerx = 600
        self.rect.bottom = 250
        self.mode = 0
        self.health = 3
        self.ended = 0
    def update(self,other,player,currentLevel):
        if self.health <= 0:
            if self.ended == 0:
                self.ended = 1
        else:
            if self.gravShifted == "left" or self.gravShifted == "right":
                self.rect.width = 170
                self.rect.height = 100
            else:
                self.rect.width = 100
                self.rect.height = 170
            self.gravShifted = player.gravShifted
            self.updateXCollisions(other)
            self.updateYCollisions(other)
            self.updateBossClip()
            self.move(player,currentLevel)
            #bounds
            if self.rect.x<=5:
                self.rect.x = 5
            if self.rect.x>=995:
                self.rect.x = 995
            if self.rect.y<=5:
                self.rect.y = 5
            if self.rect.y>=495:
                self.rect.y = 495

    def move(self,player,currentLevel):
        if self.onsurface == True:
            if self.gravShifted == "up" or self.gravShifted == "down":
                if player.rect.x<self.rect.x:
                    self.xspeed = -8
                else:
                    self.xspeed = 8
            else:
                if player.rect.y<self.rect.y:
                    self.yspeed = -8
                else:
                    self.yspeed = 8
            if self.mode == 0:
                self.jump()
                self.mode = 1
            else:
                self.fire(player,currentLevel)
                self.mode = 0

    def updateBossClip(self):
        if self.onsurface == False:
            self.spritesheet.set_clip(pygame.Rect(self.jumping))
            self.image = self.spritesheet.subsurface(
                self.spritesheet.get_clip())
        elif self.onsurface == True:
            self.spritesheet.set_clip(pygame.Rect(self.steady))
            self.image = self.spritesheet.subsurface(
                self.spritesheet.get_clip())
        if self.gravShifted == "up":
            flipped = pygame.transform.flip(self.image, 0, 1)
            self.image = flipped
        elif self.gravShifted == "left":
            turned = pygame.transform.rotate(self.image,270)
            self.image = turned
        elif self.gravShifted == "right":
            turned = pygame.transform.rotate(self.image, 90)
            self.image = turned

    def updateXCollisions(self,other):
        #same as player collisions
        self.rect.x+=self.xspeed
        collisions = pygame.sprite.spritecollide(self, other, False)
        if (collisions == [] and 
            (self.yspeed>.5 and self.gravShifted == "up") or 
            (self.yspeed<-.5 and self.gravShifted == "down") or
            (self.xspeed>.5 and self.gravShifted == "left") or
            (self.xspeed<-.5 and self.gravShifted == "right")):
            self.onsurface = False
        for collision in collisions:
            if self.xspeed < 0:
                self.rect.left = collision.rect.right
                if self.gravShifted == "left":
                    self.onsurface = True
            else:
                self.rect.right = collision.rect.left
                if self.gravShifted == "right":
                    self.onsurface = True
            self.xspeed = 0

    def updateYCollisions(self,other):
        #same as player collisions
        self.rect.y+=self.yspeed
        collisions = pygame.sprite.spritecollide(self, other, False)
        for collision in collisions:
            if self.yspeed > 0:
                self.rect.bottom = collision.rect.top
                if self.gravShifted == "down":
                    self.onsurface = True    
            else:
                self.rect.top = collision.rect.bottom
                if self.gravShifted == "up":
                    self.onsurface = True
            self.yspeed = 0

    def jump(self):
        if self.onsurface:
            jump = pygame.mixer.Sound('assets/jump.wav')
            jump.play(0)
            if self.gravShifted == "up":
                self.yspeed = 12
            elif self.gravShifted == "down":
                self.yspeed = -12
            elif self.gravShifted == "left":
                self.xspeed = 12
            else:
                self.xspeed = -12
            self.onsurface = False

    def fire(self,player,currentLevel):
        fire = pygame.mixer.Sound('assets/gun.wav')
        fire.play(0)
        #shoots in direction of player
        if self.gravShifted == "up" or self.gravShifted == "down":
            if player.rect.x <self.rect.x:
                bullet = Bullet(self.rect.left,self.rect.centery,-10,0)
            else:
                bullet = Bullet(self.rect.right,self.rect.centery,10,0)
        else:
            if player.rect.y<self.rect.y:
                bullet = Bullet(self.rect.centerx,self.rect.top,0,-10)
            else:
                bullet = Bullet(self.rect.centerx,self.rect.bottom,0,10)
        currentLevel.bullets_list.add(bullet)
        currentLevel.sprites_list.add(bullet)


    def addgrav(self):
        if self.gravShifted == "up":
            self.yspeed-=.5
        elif self.gravShifted == "down":
            self.yspeed+=.5
        elif self.gravShifted == "left":
            self.xspeed-=.5
        else:
            self.xspeed+=.5

class BossTwo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load("assets/bossTwoSpritesheet.png")
        self.steady = (0,0,100,150)
        self.left = (200,0,100,150)
        self.right = (300,0,100,150)
        self.spritesheet.set_clip(pygame.Rect(self.left))
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.xspeed = 0
        self.yspeed = 12
        self.onsurface = False
        self.gravShifted = "down"
        self.rect.centerx = 900
        self.rect.bottom = 400
        self.health = 3
        self.ended = 0
        #for moving and shooting delays
        self.moveTime = pygame.time.get_ticks()
        self.bulletTime = pygame.time.get_ticks()
        self.vulnurableTime = 0
        self.vulnurable = False
    def update(self,other,player,currentLevel):
        if self.health <= 0:
            if self.ended == 0:
                self.ended = 1
        else:
            self.updateXCollisions(other)
            self.updateYCollisions(other)
            self.gravShifted = player.gravShifted
            self.updateBossClip(player)
            self.moveAndShoot(player,currentLevel)
            #bounds
            if self.rect.x<=5:
                self.rect.x = 5
            if self.rect.x>=995:
                self.rect.x = 995
            if self.rect.y<=5:
                self.rect.y = 5
            if self.rect.y>=495:
                self.rect.y = 495

    def updateXCollisions(self,other):
        #same as player collisions
        self.rect.x+=self.xspeed
        collisions = pygame.sprite.spritecollide(self, other, False)
        if (collisions == [] and 
            (self.yspeed>.5 and self.gravShifted == "up") or 
            (self.yspeed<-.5 and self.gravShifted == "down")):
            self.onsurface = False
        for collision in collisions:
            if self.xspeed < 0:
                self.rect.left = collision.rect.right
            else:
                self.rect.right = collision.rect.left
            self.xspeed = 0

    def updateYCollisions(self,other):
        #same as player collisions
        self.rect.y+=self.yspeed
        collisions = pygame.sprite.spritecollide(self, other, False)
        for collision in collisions:
            if self.yspeed > 0:
                self.rect.bottom = collision.rect.top
                if self.gravShifted == "down":
                    self.onsurface = True    
            else:
                self.rect.top = collision.rect.bottom
                if self.gravShifted == "up":
                    self.onsurface = True
            self.yspeed = 0

    def updateBossClip(self,player):
        if self.vulnurable:
            self.spritesheet.set_clip(pygame.Rect(self.steady))
            self.image = self.spritesheet.subsurface(
                self.spritesheet.get_clip())
        elif player.rect.x<self.rect.x:
            self.spritesheet.set_clip(pygame.Rect(self.left))
            self.image = self.spritesheet.subsurface(
                self.spritesheet.get_clip())
        else:
            self.spritesheet.set_clip(pygame.Rect(self.right))
            self.image = self.spritesheet.subsurface(
                self.spritesheet.get_clip())
        if self.gravShifted == "up":
                flipped = pygame.transform.flip(self.image, 0, 1)
                self.image = flipped

    def moveAndShoot(self,player,currentLevel):
        #checks if delay has happened
        newTime = pygame.time.get_ticks()
        if self.onsurface == True and newTime-self.moveTime>2000:
            #if it has, move
            self.moveTime = newTime
            if self.health == 3:
                speed = 10
            elif self.health == 2:
                speed = 12
            else:
                speed = 14
            #moves in direction of player
            if player.rect.x<self.rect.x:
                self.xspeed = -1*speed
            else:
                self.xspeed = speed
            #like moving, shoot on delay
            newTime = pygame.time.get_ticks()
            if newTime-self.bulletTime>=1000 and self.vulnurable == False:
                self.bulletTime = newTime
                self.fire(player,currentLevel)

    def fire(self,player,currentLevel):
        #fire in direction of player
        fire = pygame.mixer.Sound('assets/gun.wav')
        fire.play(0)
        if self.gravShifted == "up" or self.gravShifted == "down":
            if player.rect.x <self.rect.x:
                bullet = Bullet(self.rect.left,self.rect.centery,-10,0)
            else:
                bullet = Bullet(self.rect.right,self.rect.centery,10,0)
        else:
            if player.rect.y<self.rect.y:
                bullet = Bullet(self.rect.centerx,self.rect.top,0,-10)
            else:
                bullet = Bullet(self.rect.centerx,self.rect.bottom,0,10)
        currentLevel.bullets_list.add(bullet)
        currentLevel.sprites_list.add(bullet)

    def addgrav(self):
        if self.gravShifted == "up":
            self.yspeed-=.5
        elif self.gravShifted == "down":
            self.yspeed+=.5
        elif self.gravShifted == "left":
            self.xspeed-=.5
        else:
            self.xspeed+=.5

class BossThree(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load("assets/bossThreeSpritesheet.png")
        self.left = (200,0,100,150)
        self.right = (300,0,100,150)
        self.spritesheet.set_clip(pygame.Rect(self.left))
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.xspeed = 0
        self.yspeed = 12
        self.onsurface = False
        self.gravShifted = "down"
        self.rect.centerx = 975
        self.rect.bottom = 220
        self.health = 3
        self.ended = 0
        #bullet delay
        self.bulletTime = pygame.time.get_ticks()
    def update(self,other,player,currentLevel):
        if self.health <= 0:
            if self.ended == 0:
                self.ended = 1
        else:
            self.updateXCollisions(other)
            self.updateYCollisions(other)
            self.gravShifted = player.gravShifted
            self.updateBossClip(player)
            self.updateShooting(player,currentLevel)
            #bounds
            if self.rect.x<=5:
                self.rect.x = 5
            if self.rect.x>=995:
                self.rect.x = 995
            if self.rect.y<=5:
                self.rect.y = 5
            if self.rect.y>=495:
                self.rect.y = 495

    def updateXCollisions(self,other):
        #same as player collisions
        self.rect.x+=self.xspeed
        collisions = pygame.sprite.spritecollide(self, other, False)
        if (collisions == [] and
            (self.yspeed>.5 and self.gravShifted == "up") or 
            (self.yspeed<-.5 and self.gravShifted == "down")):
            self.onsurface = False
        for collision in collisions:
            if self.xspeed < 0:
                self.rect.left = collision.rect.right
            else:
                self.rect.right = collision.rect.left
            self.xspeed = 0

    def updateYCollisions(self,other):
        #same as player collisions
        self.rect.y+=self.yspeed
        collisions = pygame.sprite.spritecollide(self, other, False)
        for collision in collisions:
            if self.yspeed > 0:
                self.rect.bottom = collision.rect.top
                if self.gravShifted == "down":
                    self.onsurface = True    
            else:
                self.rect.top = collision.rect.bottom
                if self.gravShifted == "up":
                    self.onsurface = True
            self.yspeed = 0

    def updateBossClip(self,player):
        if player.rect.x<self.rect.x:
            self.spritesheet.set_clip(pygame.Rect(self.left))
            self.image = self.spritesheet.subsurface(
                self.spritesheet.get_clip())
        else:
            self.spritesheet.set_clip(pygame.Rect(self.right))
            self.image = self.spritesheet.subsurface(
                self.spritesheet.get_clip())

        if self.gravShifted == "up":
            flipped = pygame.transform.flip(self.image, 0, 1)
            self.image = flipped

    def updateShooting(self,player,currentLevel):
        #delay
        if self.onsurface:
            newTime = pygame.time.get_ticks()
            if newTime-self.bulletTime>=2000:
                self.bulletTime = newTime
                self.fire(player,currentLevel)

    def fire(self,player,currentLevel):
        #shoot towards player
        #he's always facing left but I wanted to keep a standard format
        fire = pygame.mixer.Sound('assets/gun.wav')
        fire.play(0)
        bullet = Bullet(self.rect.left,self.rect.centery,-12,0)
        if self.gravShifted == "up" or self.gravShifted == "down":
            if player.rect.x <self.rect.x:
                bullet = Bullet(self.rect.left,self.rect.centery,-12,0)
            else:
                bullet = Bullet(self.rect.right,self.rect.centery,12,0)
        else:
            if player.rect.y<self.rect.y:
                bullet = Bullet(self.rect.centerx,self.rect.top,0,-12)
            else:
                bullet = Bullet(self.rect.centerx,self.rect.bottom,0,12)
        currentLevel.bullets_list.add(bullet)
        currentLevel.sprites_list.add(bullet)

    def addgrav(self):
        #standard gravity adder
        if self.gravShifted == "up":
            self.yspeed-=.5
        elif self.gravShifted == "down":
            self.yspeed+=.5
        elif self.gravShifted == "left":
            self.xspeed-=.5
        else:
            self.xspeed+=.5


class EnterDoor(pygame.sprite.Sprite):
    def __init__(self,x,y,fromRoom,whichExit):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/enterdoor.png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.startX = x
        self.fromRoom = fromRoom
        self.whichExit = whichExit


class ExitDoor(pygame.sprite.Sprite):
    def __init__(self,x,y,greens,toRoom,whichEnter,flipped = False):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load("assets/exitdoor.png")
        self.zero = (0,0,81,120)
        self.one = (81,0,81,120)
        self.two = (162,0,81,120)
        self.three = (243,0,81,120)
        self.toRoom = toRoom
        self.whichEnter = whichEnter
        self.greens = greens
        self.flipped = flipped
        if self.greens == 0:
            self.spritesheet.set_clip(pygame.Rect(self.zero))
        elif self.greens == 1:
            self.spritesheet.set_clip(pygame.Rect(self.one))
        elif self.greens == 2:
            self.spritesheet.set_clip(pygame.Rect(self.two))
        else:
            self.spritesheet.set_clip(pygame.Rect(self.three))
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        self.image.set_colorkey((255,255,255))
        if self.flipped:
            flipped = pygame.transform.flip(self.image, 0, 1)
            self.image = flipped
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
    def update(self):
        if self.greens<0:
            self.greens = 0
        if self.greens == 0:
            self.spritesheet.set_clip(pygame.Rect(self.zero))
        elif self.greens == 1:
            self.spritesheet.set_clip(pygame.Rect(self.one))
        elif self.greens == 2:
            self.spritesheet.set_clip(pygame.Rect(self.two))
        else:
            self.spritesheet.set_clip(pygame.Rect(self.three))
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        if self.flipped:
            flipped = pygame.transform.flip(self.image, 0, 1)
            self.image = flipped

class Post(pygame.sprite.Sprite):
    def __init__(self,x,y,doorLevel,doorNumber,flipped=False):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load("assets/post.png")
        self.off = (0,0,20,75)
        self.on = (20,0,20,75)
        self.flipped = flipped
        self.spritesheet.set_clip(pygame.Rect(self.off))
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        self.image.set_colorkey((255,255,255))
        if self.flipped:
            flipped = pygame.transform.flip(self.image, 0, 1)
            self.image = flipped
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.mode = 0
        self.doorLevel = doorLevel
        self.doorNumber = doorNumber
        
    def update(self):
        if self.mode == 0:
            self.spritesheet.set_clip(pygame.Rect(self.off))
        else:
            self.spritesheet.set_clip(pygame.Rect(self.on))
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        if self.flipped:
            flipped = pygame.transform.flip(self.image, 0, 1)
            self.image = flipped

class Button(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pygame.sprite.Sprite.__init__(self)
        self.mode = 0
        self.image = pygame.Surface((width,height))
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pressed = False

    def update(self,player,balls):
        if self.rect.colliderect(player):
            self.mode = 1
        else:
            self.mode = 0
        for ball in balls.sprites():
            if self.rect.colliderect(ball) or self.rect.colliderect(player):
                self.mode = 1
            else:
                self.mode = 0
        if self.mode == 0:
            self.image.fill((255,0,0))
        else:
            self.image.fill((0,255,0))

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((60, 60))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255,255,255))
        pygame.draw.circle(self.image, (255, 0, 0), (30, 30), 30, 0)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.xspeed = 0
        self.yspeed = 0

    def update(self,player,other):
        self.rect.x+=self.xspeed
        self.rect.y+=self.yspeed
        collisions = pygame.sprite.spritecollide(self, other, False)
        for collision in collisions:
            if self.yspeed > 0:
                self.rect.bottom = collision.rect.top
                self.onsurface = True
                self.yspeed = 0
            else:
                self.rect.top = collision.rect.bottom
                self.yspeed = 0
        if self.rect.colliderect(player):
            if player.xspeed < 0:
                self.rect.right = player.rect.left
            else:
                self.rect.left = player.rect.right
            if self.rect.left <= 5:
                self.rect.left = 5
            if self.rect.right >= 995:
                self.rect.right = 995

    def addGrav(self,player):
        if player.gravShifted == "down":
            self.yspeed+=.5
        else:
            self.yspeed-=.5

class Block(pygame.sprite.Sprite):
    def __init__(self,x,y,width,height, direction = 0, left = 0, right = 1000):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width,height))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        #direction is for if its a moving platform
        self.direction = direction
        self.left = left
        self.right = right

    def update(self, player):
        if self.direction !=0:
            #changes direction if it hits the limits
            if self.rect.left<=self.left or self.rect.right>=self.right:
                self.direction*=-1
            if (self.rect.top == player.rect.bottom and
                player.rect.left>self.rect.left and
                player.rect.right<self.rect.right):
                player.rect.x+=self.direction*10
            self.rect.x+=self.direction*10


class Item(pygame.sprite.Sprite):
    #only used this for grav and ball machine
    #but if game were to be expanded
    #it would be more useful
    def __init__(self,name,x,y,special=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/"+name + ".png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.special = special


class Text(pygame.sprite.Sprite):
    def __init__(self,name,x,y,size = 20,color = (0,0,0)):
        pygame.sprite.Sprite.__init__(self)
        self.text = "%s" %name
        self.font = pygame.font.SysFont("Helvetica", size)
        self.image = self.font.render(self.text, True, color)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y


class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 100
        self.image = pygame.Surface((self.health,10))
        self.image.fill((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.x = 75
        self.rect.y = 10

    def updateOne(self,player,level):
        #health update for first boss, incorporating spikes
        if self.health<=0:
            level.boss.kill()
            level.boss.remove()
            level.spikes.kill()
            level.spikes.remove()
            self.kill()
            self.remove()
            player.kill()
            player.remove()
            for bullet in level.bullets_list:
                bullet.kill()
            level.retryButton = Retry()
            level.retry = True
        elif level.boss.ended == False:
            if player.rect.colliderect(level.boss):
                self.health-=5
                self.image = pygame.Surface((self.health,10))
                if player.rect.x <= level.boss.rect.x:
                    player.rect.x-=20
                elif player.rect.x > level.boss.rect.x:
                    player.rect.x+=20
                elif player.rect.y <= level.boss.rect.y:
                    player.rect.y-=20
                else:
                    player.rect.y+=20
            if player.rect.colliderect(level.spikes):
                self.health-=5
                self.image = pygame.Surface((self.health,10))
                if player.rect.y<=level.spikes.rect.y:
                    player.jump()
                elif player.rect.y>=level.spikes.rect.y:
                    player.rect.y+=20
                elif player.rect.x <= level.spikes.rect.x:
                    player.rect.x-=20
                else:
                    player.rect.x+=20
            for bullet in level.bullets_list:
                if player.rect.colliderect(bullet):
                    self.health-=5
                    self.image = pygame.Surface((self.health,10))
                    bullet.kill()
                    bullet.remove()
            if self.health >=75:
                self.image.fill((0,255,0))
            else:
                self.image.fill((255,0,0))
    def updateTwo(self,player,level):
        #health update for second boss, incorporating vulnurablity mode
        if self.health<=0:
            level.boss.kill()
            level.boss.remove()
            self.kill()
            self.remove()
            player.kill()
            player.remove()
            for bullet in level.bullets_list:
                bullet.kill()
            level.retryButton = Retry()
            level.retry = True
        elif level.boss.ended == False:
            if level.boss.vulnurable and player.rect.colliderect(level.boss):
                level.boss.health-=1
                grunt = pygame.mixer.Sound('assets/grunt.wav')
                grunt.play(0)
                level.boss.xspeed = 50
                level.boss.yspeed = -120
                level.boss.vulnurable = False
                level.timer.kill()
                level.timer.remove()

            elif player.rect.colliderect(level.boss):
                self.health-=5
                self.image = pygame.Surface((self.health,10))
                if player.rect.x <= level.boss.rect.x:
                    player.rect.x-=20
                elif player.rect.x > level.boss.rect.x:
                    player.rect.x+=20
                elif player.rect.y <= level.boss.rect.y:
                    player.rect.y-=20
                else:
                    player.rect.y+=20

            for bullet in level.bullets_list:
                if player.rect.colliderect(bullet):
                    self.health-=5
                    self.image = pygame.Surface((self.health,10))
                    bullet.kill()
                    bullet.remove()
            if self.health >=75:
                self.image.fill((0,255,0))
            else:
                self.image.fill((255,0,0))

    def updateThree(self,player,level):
        #health update for third boss, can only be hurt by bullets
        if self.health<=0:
            level.boss.kill()
            level.boss.remove()
            self.kill()
            self.remove()
            player.kill()
            player.remove()
            for bullet in level.bullets_list:
                bullet.kill()
            level.retryButton = Retry()
            level.retry = True
        else:
            for bullet in level.bullets_list:
                if player.rect.colliderect(bullet):
                    self.health-=5
                    self.image = pygame.Surface((self.health,10))
                    bullet.kill()
                    bullet.remove()
            if self.health >=75:
                self.image.fill((0,255,0))
            else:
                self.image.fill((255,0,0))


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,xspeed,yspeed):
        pygame.sprite.Sprite.__init__(self)
        if yspeed == 0:
            self.image = pygame.Surface((20,5))
        else:
            self.image = pygame.Surface((5,20))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xspeed = xspeed
        self.yspeed = yspeed
    def update(self,player):
        #sort of follows player
        if player.rect.x <= self.rect.x:
            self.rect.x -=4
        if player.rect.x >= self.rect.x:
            self.rect.x+=4 
        if player.rect.y <= self.rect.y:
            self.rect.y -=4
        if player.rect.y >= self.rect.y:
            self.rect.y +=4
        self.rect.x+=self.xspeed
        self.rect.y+=self.yspeed


class Retry(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/retry.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = 500
        self.rect.centery = 250
   

class Spikes(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/spikes.png")
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self,boss):
        #hurts boss
        if self.rect.colliderect(boss) and boss.health>0:
            grunt = pygame.mixer.Sound('assets/grunt.wav')
            grunt.play(0)
            boss.health-=1
            boss.xspeed=-100
            boss.yspeed=-30


class Heli(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = pygame.image.load("assets/heli.png")
        self.spritesheet.set_clip(pygame.Rect((0,0,239,160)))
        self.image = self.spritesheet.subsurface(self.spritesheet.get_clip())
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.frame = 0

    def update(self):
        #animated fly-away
        self.frame = self.frame%2
        if self.frame == 0:
            self.spritesheet.set_clip(pygame.Rect((478,0,239,160)))
        else:
            self.spritesheet.set_clip(pygame.Rect((239,0,239,160)))
        self.image = (self.spritesheet.subsurface(self.spritesheet.get_clip()))
        self.frame+=1

game()