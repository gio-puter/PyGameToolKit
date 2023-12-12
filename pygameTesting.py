from os import environ
import pygame
import UI
import Color

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

pygame.init()

# screen = pygame.display.set_mode((1280, 720))
screen = pygame.display.set_mode((1280, 720), flags=0)
pygame.display.set_caption('PyGame Tester')

UI.screenColor = Color.BLACK

clock = pygame.time.Clock()
pygame.key.set_repeat(750, 50)

def test_screen():
    run = True
    screen_center = screen.get_rect().center
    textList = ['Testing String', 'I', 'HOPE', 'this', 'WoRkS']

    label = UI.Label([screen_center[0], screen_center[1]-75], 'Testing String', Color.WHITE, 16,
                 bold=True, italic=True, textBackgroundColor=Color.BLUE, textBackgroundRounded=5, margin=[25,10]),
    input = UI.InputField([screen_center[0], screen_center[1]-225], 'Coach Name', Color.WHITE, 24, Color.WHITE, 16,
                      bold=True, italic=True, placeHolderText='Name Here', inputBackgroundColor=Color.DIMGRAY, 
                      inputBackgroundRounded=5, inputMargin=[25,10], inputWidth=[250,30], inputBackgroundWidth=2, labelAlign='left'),
    # label2 = UI.Label(screen_center, '-10000', Color.WHITE, 16)
    group = pygame.sprite.Group(
        # input,
        # UI.Table([screen_center[0], screen_center[1]+75], textList, Color.WHITE, 32, 'Arial', bold=True),
        UI.Slider(screen_center, [300, 5], 7.5, [-100, 100]),
        UI.Slider([screen_center[0]-175, screen_center[1]+75], [300, 5], 7.5, ['ooga booga', 'tiny tim']),
        UI.Slider([screen_center[0]+175, screen_center[1]+75], [300, 5], 7.5, ['10', 20]),
        # label2,
        # UI.Switch(screen_center, 100, 50)
    )

    while run:
        clock.tick(60)
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit(0)
        
        group.update(event_list)

        screen.fill(UI.screenColor)
        group.draw(screen)
        pygame.display.flip()

    return 

test_screen()


pygame.quit()