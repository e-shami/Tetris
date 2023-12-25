import pygame
from src.Tetris import Tetris

#Shapes of the blocks
shapes = [
        [[1, 5, 9, 13], [4, 5, 6, 7]], # right angle shape -> L
        [[4, 5, 9, 10], [2, 6, 5, 9]], # T shaped shape -> T
        [[6, 7, 9, 10], [1, 5, 6, 10]], # Z shaped shape -> Z
        [[2, 1, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], # I shaped shape -> I
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # S shaped shape -> S
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], # J shaped shape -> J
        [[1, 2, 5, 6]], # square shaped shape -> square
    ]
#Colors of the blocks
shapeColors = [(0, 255, 0), # green for I
                (255, 0, 0), # red for Z
                (0, 255, 255), # yellow for J
                (255, 255, 0), #  Orange for L
                (255, 165, 0), # cyan for S
                (0, 0, 255), # blue for T 
                (128, 0, 128)] # purple for square
# GLOBALS VARS
width = 700
height = 600
  # meaning 600 // 20 = 20 height per blo ck
blockSize = 30



gameWidth = 100  # meaning 300 // 10 = 30 width per block
gameHeight = 400
gameDimensions = {'width': gameWidth, 'height': gameHeight}
 
x = (width - gameWidth) // 2
y = height - gameHeight - 50

topLeft = {'x': x, 'y': y}


pygame.font.init()

def startGame():
    done = False
    clock = pygame.time.Clock()
    fps = 60
    game = Tetris(blockSize, blockSize-10, shapes, shapeColors, gameDimensions, topLeft)
    counter = 0

    pressing_down = False
    
    while not done: # game is running until escape button pressed 
        #Create a new block if there is no moving block
        if game.block is None:
            game.new_block()
        if game.nextBlock is None:
            game.next_block()
        counter += 1 #Keeping track if the time 
        if counter > 100000:
            counter = 0

        #Moving the block continuously with time or when down key is pressed
        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.moveDown()
        #Checking which key is pressed and running corresponding function
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                if event.key == pygame.K_DOWN:
                    game.moveDown()
                if event.key == pygame.K_LEFT:
                    game.moveHoriz(-1)
                if event.key == pygame.K_RIGHT:
                    game.moveHoriz(1)
                if event.key == pygame.K_SPACE:
                    game.moveBottom()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)

        screen.fill('#FFFFFF')

        #Updating the game board regularly
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, '#B2BEB5', [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, shapeColors[game.field[i][j]],
                                     [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        #Updating the board with the moving block
        if game.block is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.block.image():
                        pygame.draw.rect(screen, shapeColors[game.block.color],
                                         [game.x + game.zoom * (j + game.block.x) + 1,
                                          game.y + game.zoom * (i + game.block.y) + 1,
                                          game.zoom - 2, game.zoom - 2])

        #Showing the score
        font = pygame.font.SysFont('Calibri', 40, True, False)
        font1 = pygame.font.SysFont('Calibri', 25, True, False)
        text = font.render("Score: " + str(game.score), True, '#000000')
        text_game_over = font.render("Game Over", True, '#000000')
        text_game_over1 = font1.render("Press ESC", True, '#000000')

        #Ending the game if state is gameover
        screen.blit(text, [300, 0])
        if game.state == "gameover":
            screen.blit(text_game_over, [300, 200])
            screen.blit(text_game_over1, [300, 265])
       
        game.draw_next_block(screen)

        pygame.display.flip() #Updating the game window
        clock.tick(fps) #Setting the fps to 60


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris by Shehzad")
run = True
while run:
    screen.fill((70, 57, 64 ))
    font = pygame.font.SysFont("Calibri", 70, bold=True)
    label = font.render("Press any key to begin!", True, '#FFFFFF')

    screen.blit(label, (10, 300 ))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            startGame()
pygame.quit()