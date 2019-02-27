class Config:
    GRID_SIZE = 30
    # 主界面
    SCREEN_X = 300
    SCREEN_Y = 600
    # 显示信息 （下一个方块，得分）
    INFO_X = 180

    SCREEN_SIZE = (SCREEN_X+INFO_X, SCREEN_Y)

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)

    FPS = 60
    # 最大下落速度，值越小，速度越快
    MAX_SPEED = 15
    # 下落速度加快的变化率
    FALL_SPEED_RATE = 0.6
    # 加快下落速度的得分，每获得多少分后，下落速度加快
    FALL_SPEED_SCORE = 40