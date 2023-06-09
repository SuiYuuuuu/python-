import pygame
import datetime
import sys
import random
from pygame.locals import *

# 简单设置一些必要的常量

BGC = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
FPS = 30     #设置游戏帧率

GNUMS = 3     #有几行几列
ALLNUMS = GNUMS ** 2    #一共几个格子
RANDOMTIME = 100  #随机打乱次数

# 结束程序
def End():
    pygame.quit()
    sys.exit()

# 随机生成游戏盘面
def NewGameScreen():
    pieces = []      #储存每一片拼图位置信息
    for i in range(ALLNUMS):
        pieces.append(i)    #保存初始设置
    WhitePiece = ALLNUMS - 1  #把最后一块设置为白块
    pieces[WhitePiece] = -1   #用-1代表白块

    for i in range(RANDOMTIME):
        strategy = random.randint(0, 3)  #随机产生0，1、2、3，然后将白块与对应的拼图换位置，以白块的随即移动打乱整个拼图，即是新建拼图
        if strategy == 0:
            WhitePiece = ShiftLeft(pieces, WhitePiece)
        elif strategy == 1:
            WhitePiece = ShiftRight(pieces, WhitePiece)
        elif strategy == 2:
            WhitePiece = ShiftUp(pieces, WhitePiece)
        elif strategy == 3:
            WhitePiece = ShiftBeneath(pieces, WhitePiece)
    return pieces, WhitePiece

# 若白块不在最左边，则将白块左边的块移动到白块位置，先边缘检测，再做交换
def ShiftRight(pieces, WhitePiece):
    if WhitePiece % GNUMS == 0:
        return WhitePiece
    pieces[WhitePiece - 1], pieces[WhitePiece] = pieces[WhitePiece], pieces[WhitePiece - 1]  #必须这样写，不然两个都变成白块，后面同理
    return WhitePiece - 1

# 若白块不在最右边，则将白块右边的块移动到白块位置
def ShiftLeft(pieces, WhitePiece):
    if WhitePiece % GNUMS == GNUMS - 1:
        return WhitePiece
    pieces[WhitePiece + 1], pieces[WhitePiece] = pieces[WhitePiece], pieces[WhitePiece + 1]
    return WhitePiece + 1

# 若白块不在最上边，则将白块上边的块移动到白块位置
def ShiftBeneath(pieces, WhitePiece):
    if WhitePiece < GNUMS:
        return WhitePiece
    pieces[WhitePiece - GNUMS], pieces[WhitePiece] = pieces[WhitePiece], pieces[WhitePiece - GNUMS]
    return WhitePiece - GNUMS

# 若白块不在最下边，则将白块下边的块移动到白块位置
def ShiftUp(pieces, WhitePiece):
    if WhitePiece >= ALLNUMS - GNUMS:
        return WhitePiece
    pieces[WhitePiece + GNUMS], pieces[WhitePiece] = pieces[WhitePiece], pieces[WhitePiece + GNUMS]
    return WhitePiece + GNUMS

# 检测拼图是否正确完成
def isEnded(pieces, WhitePiece):
    for i in range(ALLNUMS - 1):
        if pieces[i] != i:
            return False
    return True


#搭建开始界面
def ShowStartScreen(windowViews, gamesImages):
    windowViews.fill(BGC)
    # 显示原图
    windowViews.blit(gamesImages, (0, 0))
    # 显示欢迎文本
    font = pygame.font.Font(None, 100)
    text = font.render("Welcome! Press any key to start!", True, BLUE)
    text_rect = text.get_rect(center=(gamesRects.width // 2, gamesRects.height - text.get_height() // 2 - 50))
    windowViews.blit(text, text_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                End()
            if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                return

def calculateHint(pieces, WhitePiece):
    targetState = list(range(ALLNUMS))  # 目标状态
    targetState[-1] = -1  # 白块用-1表示,且白块的初始位置是最后一个

    visited = set()  # 记录访问过的状态
    queue = [(pieces, WhitePiece, [])]  # 广度优先搜索队列，元素为当前状态、白块位置、路径

    while queue:
        currentState, currentWhite, path = queue.pop(0)  # 弹出队列的第一个状态

        if currentState == targetState:  # 找到目标状态
            return len(path), path

        if tuple(currentState) in visited:  # 当前状态已访问过，跳过
            continue

        visited.add(tuple(currentState))   #元组

        # 判断上下左右移动的合法性，执行移动操作并将新状态加入队列，之后再根据队头状态再做扩展，形成广度优先
        if currentWhite % GNUMS != 0:  # 可以向左移动
            newState = currentState[:]
            newState[currentWhite], newState[currentWhite - 1] = newState[currentWhite - 1], newState[currentWhite]
            queue.append((newState, currentWhite - 1, path + ['Left']))

        if currentWhite % GNUMS != GNUMS - 1:  # 可以向右移动
            newState = currentState[:]
            newState[currentWhite], newState[currentWhite + 1] = newState[currentWhite + 1], newState[currentWhite]
            queue.append((newState, currentWhite + 1, path + ['Right']))

        if currentWhite >= GNUMS:  # 可以向上移动
            newState = currentState[:]
            newState[currentWhite], newState[currentWhite - GNUMS] = newState[currentWhite - GNUMS], newState[currentWhite]
            queue.append((newState, currentWhite - GNUMS, path + ['Up']))

        if currentWhite < ALLNUMS - GNUMS:  # 可以向下移动
            newState = currentState[:]
            newState[currentWhite], newState[currentWhite + GNUMS] = newState[currentWhite + GNUMS], newState[currentWhite]
            queue.append((newState, currentWhite + GNUMS, path + ['Down']))
    return 0 , ['end']  #当做到最后一步时，由于下面的第193行代码，使得gamepieces最后一个不是-1，即没有了白块，使得此函数所有if语句均无法执行且queue空，函数结束，因此写这个return语句，返回最后的end指示

# 初始化
pygame.init()
myClock = pygame.time.Clock()

# 加载图片，图片导入
gamesImages = pygame.image.load('D:\桌面\QQ图片20230523223553.jpg')
gamesRects = gamesImages.get_rect()

# 设置窗口，窗口的宽度和高度取决于图片的宽高，因此可以规定任意图片作为拼图游戏
windowViews = pygame.display.set_mode((gamesRects.width, gamesRects.height))
pygame.display.set_caption('Mikasa & Eren')

GWidth = gamesRects.width // GNUMS
GHeight = gamesRects.height // GNUMS

end = False
moveCount = 0

gamepieces, WhitePiece = NewGameScreen()

ShowStartScreen(windowViews, gamesImages)#显示开始界面，等待用户按下任意键
showHelp = False
# 游戏主循环
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            End()
        if end:
            continue
        if event.type == KEYDOWN:    #运用鼠标和键盘事件，移动方块
            if event.key == ord('a') or event.key == K_LEFT:
                WhitePiece = ShiftLeft(gamepieces, WhitePiece)
                moveCount += 1
            if event.key == ord('d') or event.key == K_RIGHT:
                WhitePiece = ShiftRight(gamepieces, WhitePiece)
                moveCount += 1
            if event.key == ord('w') or event.key == K_UP:
                WhitePiece = ShiftUp(gamepieces, WhitePiece)
                moveCount += 1
            if event.key == ord('s') or event.key == K_DOWN:
                WhitePiece = ShiftBeneath(gamepieces, WhitePiece)
                moveCount += 1
            if event.key == K_h:   # 按下 'h' 键，呼出小助手
                showHelp = True
        if event.type == MOUSEBUTTONDOWN and event.button == 1:   #规定必须用左键
            x, y = pygame.mouse.get_pos()
            column = x // GWidth  #强制转换为整形，可得到当前位置
            row = y // GHeight
            position = column + row * GNUMS
            if (position == WhitePiece - 1 or position == WhitePiece + 1 or position == WhitePiece - GNUMS or position == WhitePiece + GNUMS):
                gamepieces[WhitePiece], gamepieces[position] = gamepieces[position], gamepieces[WhitePiece]
                WhitePiece = position
                moveCount += 1

    if isEnded(gamepieces, WhitePiece):    #判断是否完成拼图
        gamepieces[WhitePiece] = ALLNUMS - 1  #不加这一句最终拼图不完善
        end = True

    windowViews.fill(BGC)
    
    #绘制游戏界面
    for i in range(ALLNUMS):
        if gamepieces[i] == -1:
            continue
        xpos = i % GNUMS
        ypos = int(i / GNUMS)
        pygame.draw.rect(windowViews, BLUE, (xpos * GWidth, ypos * GHeight, GWidth, GHeight))
        # 在每个格子里显示对应的图片
        windowViews.blit(gamesImages, (xpos * GWidth, ypos * GHeight), (gamepieces[i] % GNUMS * GWidth, gamepieces[i] // GNUMS * GHeight, GWidth, GHeight))

     # 绘制网格线
    for i in range(GNUMS + 1):
        pygame.draw.line(windowViews, BLACK, (i * GWidth, 0), (i * GWidth, gamesRects.height))
    for i in range(GNUMS + 1):
        pygame.draw.line(windowViews, BLACK, (0, i * GHeight), (gamesRects.width, i * GHeight))

    if showHelp:
        min_moves, best_path = calculateHint(gamepieces, WhitePiece)
        font = pygame.font.Font(None, 36)    #设置字体大小
        text = font.render(f"Next Move: {best_path[0]}", True, BLACK)
        windowViews.blit(text, (10, 30))   #调整文本位置
        text = font.render(f"Minimum Moves: {min_moves}", True, BLACK)
        windowViews.blit(text, (10, 50))    #设置字体大小


    if end:    #显示完成拼图后的文本信息
        font = pygame.font.Font(None, 36)  # 设置字体大小
        text = font.render("Congratulations!", True, BLACK)
        windowViews.blit(text, (gamesRects.width // 2 - text.get_width() // 2, gamesRects.height // 2 - text.get_height() // 2))

    # 显示移动次数
    font = pygame.font.Font(None, 36)  # 设置字体大小
    text = font.render(f"Moves: {moveCount}", True, BLACK)
    windowViews.blit(text, (10, 10))  # 调整文本的位置

    pygame.display.update()
    myClock.tick(FPS)
