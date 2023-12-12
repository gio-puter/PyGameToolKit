import pygame
import Color

from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

size = tuple[int, int]
span = tuple[int or str, int or str]
Coordinate = tuple[float, float]
ColorValue = tuple[float, float, float]

screenColor = Color.BLACK

class Label(pygame.sprite.Sprite):
    """ Create text object centered at dest """
    def __init__(self, dest: Coordinate, textString: str, textColor: ColorValue, textSize: int, **kwargs) -> None:
        super().__init__()
        self.__dict__.update(locals())
        defaults = {
            'fontName' : 'Arial',
            'drawBorders' : False,
            'bold' : False,
            'italic' : False,
            'textBackgroundColor': None,
            'textBackgroundRounded' : -1,
            'textBackgroundWidth' : 0,
            'backgroundColor' : screenColor,
            'margin' : [0,0],
            'transparent' : True,
            'destOrientation' : 'center',
        }

        for attr, default in defaults.items():
            setattr(self, attr, kwargs.get(attr, default))
        
        font = pygame.font.SysFont(self.fontName, textSize, self.bold, self.italic)
        text = font.render(str(textString), True, textColor)
        textRect = text.get_rect()

        self.original_image = pygame.Surface(textRect.inflate(self.margin).size, pygame.SRCALPHA).convert_alpha()
        if not self.transparent: self.original_image.fill(self.backgroundColor)
        
        if self.textBackgroundColor:
            pygame.draw.rect(self.original_image, self.textBackgroundColor, self.original_image.get_rect(), self.textBackgroundWidth, self.textBackgroundRounded)

        textRect.center = self.original_image.get_rect().center
        self.original_image.blit(text, textRect)

        if self.drawBorders:
            pygame.draw.rect(self.original_image, Color.RED, textRect, 2)
            pygame.draw.rect(self.original_image, Color.CYAN, self.original_image.get_rect(), 2)

        self.image = self.original_image.copy()
        if self.destOrientation == 'topleft':
            self.rect = self.image.get_rect(topleft = dest)
        if self.destOrientation == 'midtop':
            self.rect = self.image.get_rect(midtop = dest)
        if self.destOrientation == 'topright':
            self.rect = self.image.get_rect(topright = dest)
        if self.destOrientation == 'midleft':
            self.rect = self.image.get_rect(midleft = dest)
        if self.destOrientation == 'center':
            self.rect = self.image.get_rect(center = dest)
        if self.destOrientation == 'midright':
            self.rect = self.image.get_rect(midright = dest)
        if self.destOrientation == 'bottomleft':
            self.rect = self.image.get_rect(bottomleft = dest)
        if self.destOrientation == 'midbottom':
            self.rect = self.image.get_rect(midbottom = dest)
        if self.destOrientation == 'bottomright':
            self.rect = self.image.get_rect(bottomright = dest)

class InputField(pygame.sprite.Sprite):
    """ Create input field centered at dest with label """
    def __init__(self, dest: Coordinate, label: str, labelColor: ColorValue, labelSize: int, 
                 inputTextColor: ColorValue, inputTextSize: str, inputWidth: size = [0,0], **kwargs) -> None:
        super().__init__()
        self.__dict__.update(locals())
        defaults = {
            'fontName' : 'Arial',
            'drawBorders' : False,
            'bold' : False,
            'italic' : False,
            'labelBold' : False,
            'labelItalic' : False,
            'inputBold' : False,
            'inputItalic' : False,
            'labelAlign' : 'center',
            'placeHolderText' : '',
            'placeHolderColor' : Color.GRAY,
            'inputMinLength' : 0,
            'inputMaxLength' : 100,
            'inputBackgroundColor' : None,
            'inputBackgroundRounded' : False,
            'inputBackgroundWidth' : 1,
            'inputMargin' : [0,0],
            'backgroundColor' : screenColor
        }

        for attr, default in defaults.items():
            setattr(self, attr, kwargs.get(attr, default))

        self.inputString = ''
        self.clicked = False

        font = pygame.font.SysFont(self.fontName, labelSize, self.bold or self.labelBold, self.italic or self.labelItalic)
        self.title = font.render(label, True, labelColor)
        self.titleRect = self.title.get_rect()

        self.inputFont = pygame.font.SysFont(self.fontName, inputTextSize, self.bold or self.inputBold, self.italic or self.inputItalic)
        self.inputPlaceholder = self.inputFont.render(self.placeHolderText, True, self.placeHolderColor)
        self.inputPlaceholderRect = self.inputPlaceholder.get_rect()

        inputRectMargin = self.inputPlaceholderRect.inflate(self.inputMargin[0]*2, self.inputMargin[1]*2)
        inputRectMargin.topleft = [0,0]
        inputRectWidth = pygame.Rect(0,0,*self.inputWidth)
        self.inputBar = inputRectMargin.union(inputRectWidth)

        surfaceRect = pygame.Rect(0,0, max(self.inputBar.width, self.titleRect.width), self.inputBar.height + self.titleRect.height)
        self.original_image = pygame.Surface(surfaceRect.size, pygame.SRCALPHA).convert_alpha()
        self.original_image.fill(self.backgroundColor)

        self.titleRect.centery = 0 + self.titleRect.height//2
        if self.labelAlign == 'center':
            self.titleRect.centerx = self.original_image.get_rect().centerx
        elif self.labelAlign == 'left':
            self.titleRect.left = self.original_image.get_rect().left
        elif self.labelAlign == 'right':
            self.titleRect.right = self.original_image.get_rect().right
        self.inputBar.center = (self.original_image.get_rect().centerx, self.titleRect.bottom + self.inputBar.h//2)
        self.inputPlaceholderRect.center = self.inputBar.center

        if self.inputBackgroundColor:
            pygame.draw.rect(self.original_image, self.inputBackgroundColor, self.inputBar, self.inputBackgroundWidth, self.inputBackgroundRounded)

        self.original_image.blits([(self.title, self.titleRect), (self.inputPlaceholder, self.inputPlaceholderRect)])

        if self.drawBorders: self.drawOutlines(self.original_image)

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center = dest)

    def update(self, event_list: list[pygame.event.Event], **kwargs) -> None:
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.clicked = self.checkSelect()

            if self.clicked and event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_RETURN, pygame.K_TAB, pygame.K_ESCAPE]:
                    continue
                if event.key == pygame.K_BACKSPACE:
                    self.inputString = '' if len(self.inputString) <= 1 else self.inputString[:-1]
                elif len(self.inputString) < self.inputMaxLength:
                    self.inputString += event.unicode

        if self.inputString == '':
            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(center = self.dest)
            return
        
        self.inputFont = pygame.font.SysFont(self.fontName, self.inputTextSize, self.bold or self.inputBold, self.italic or self.inputItalic)
        self.inputText = self.inputFont.render(self.inputString, True, self.inputTextColor)
        self.inputRect = self.inputText.get_rect()

        if self.inputBar.width - self.inputRect.width < self.inputMargin[0]*2:
            self.inputString = self.inputString[:-1]
            self.inputFont = pygame.font.SysFont(self.fontName, self.inputTextSize, self.bold, self.italic)
            self.inputText = self.inputFont.render(self.inputString, True, self.inputTextColor)
            self.inputRect = self.inputText.get_rect()
            return

        surfaceRect = pygame.Rect(0,0, max(self.inputBar.width, self.titleRect.width), self.inputBar.height + self.titleRect.height)
        self.image = pygame.Surface(surfaceRect.size, pygame.SRCALPHA).convert()
        self.image.fill(self.backgroundColor)

        self.inputBar.center = (self.image.get_rect().centerx, self.titleRect.bottom + self.inputBar.h//2)
        self.inputRect.center = self.inputBar.center

        if self.inputBackgroundColor:
            pygame.draw.rect(self.image, self.inputBackgroundColor, self.inputBar, self.inputBackgroundWidth, self.inputBackgroundRounded)

        self.image.blits([(self.title, self.titleRect), (self.inputText, self.inputRect)])

        if self.drawBorders: self.drawOutlines(self.image)

        self.rect = self.image.get_rect(center = self.dest)
    
    def checkSelect(self) -> bool:
        """
        Return true if mouse position is in input field 
        """
        tempInputBar = self.inputBar.copy()
        tempInputBar.center = (self.rect.centerx, self.rect.centery + self.inputMargin[1] + self.inputBar.height/2)
        return tempInputBar.collidepoint(pygame.mouse.get_pos())

    def drawOutlines(self, surface: pygame.Surface) -> None:
        """
        Draw bounding rectangles around image objects
        """
        pygame.draw.rect(surface, Color.LIME, surface.get_rect(), 2)
        pygame.draw.rect(surface, Color.RED, self.titleRect, 2)
        if len(self.inputString) == 0:
            pygame.draw.rect(surface, Color.YELLOW, self.inputPlaceholderRect, 2)
        else:
            pygame.draw.rect(surface, Color.YELLOW, self.inputRect, 2)
        pygame.draw.rect(surface, Color.CYAN, self.inputBar, 2)

    def getInput(self) -> str:
        """
        Return string in input field
        """
        return self.inputString


# ALMOST DONE
# COULD FIGURE OUT DECIMAL STEP
# NEED TO FIGURE OUT HOVER LOCATION (ABOVE OR BELOW)
# NEED TO FIGURE OUT LABEL LOCATION (SIDES OR BELOW)
class Slider(pygame.sprite.Sprite):
    """ Create slider centered at dest with range"""
    def __init__(self, dest: Coordinate, sliderSize: size, circleRadius: float, bounds: span = ['',''], **kwargs) -> None:
        super().__init__()
        self.__dict__.update(locals())
        defaults = {
            'sliderColor' : Color.DARKGRAY,
            'circleColor' : Color.BLUE,
            'circleOutlineColor' : None, 
            'circleOutlineWidth' : 1,
            'labelSize' : int(4*circleRadius/3),
            'labelPos' : 'sides',
            'sliderLabelGap' : 2,
            'bold' : False,
            'italic' : False,
            'scale' : bounds,
            'step' : 1,
            'backgroundColor' : screenColor,
            'transparent' : True,
            'hover' : True,
            'hoverPos' : 'bottom',
            'hoverColor' : Color.WHITE,
            'hoverBackground' : screenColor,
        }

        for attr, default in defaults.items():
            setattr(self, attr, kwargs.get(attr, default))

        self.clicked = False
        self.sliderWidth, self.sliderHeight = self.sliderSize

        sliderArea = pygame.Rect(0,0, self.sliderWidth + self.circleRadius*2, max(int(self.circleRadius)*2, self.sliderHeight))
        sliderBarRect = pygame.Rect(0,0,*self.sliderSize)
        minVal = Label([0, 0], bounds[0], Color.WHITE, self.labelSize)
        maxVal = Label([0, 0], bounds[1], Color.WHITE, self.labelSize)

        surfaceRect = pygame.Rect(0,0,sliderArea.w + minVal.rect.w/2 + maxVal.rect.w/2, sliderArea.h + minVal.rect.h + self.sliderLabelGap)
        self.original_image = pygame.Surface(surfaceRect.size, pygame.SRCALPHA).convert_alpha()
        if not self.transparent: self.original_image.fill(self.backgroundColor)

        sliderBarRect.center = [self.original_image.get_rect().centerx, sliderArea.centery]
        minVal.rect.midtop = [sliderBarRect.left, sliderArea.h + self.sliderLabelGap]
        maxVal.rect.midtop = [sliderBarRect.right, sliderArea.h + self.sliderLabelGap] 

        self.sliderBar = pygame.draw.rect(self.original_image, self.sliderColor, sliderBarRect, 0, 30)
        self.original_image.blits([(minVal.image, minVal.rect), (maxVal.image, maxVal.rect)])

        self.image = self.original_image.copy()
        
        self.sliderCircle = pygame.draw.circle(self.image, self.circleColor, self.sliderBar.midleft, self.circleRadius)
        if self.circleOutlineColor:
            self.sliderCircleOutline = pygame.draw.circle(self.image, self.circleOutlineColor, self.sliderBar.midleft, self.circleRadius, self.circleOutlineWidth)

        self.non_hover_image = self.image.copy()
        self.rect = self.image.get_rect(center=dest)

        if (isinstance(self.scale[0], (int, float)) or self.scale[0].isdigit()) and (isinstance(self.scale[1], (int, float)) or self.scale[1].isdigit()):
            self.scale[0] = float(self.scale[0])
            self.scale[1] = float(self.scale[1])
            self.minValue = self.scale[0]
            self.maxValue = self.scale[1]
            self.currentValue = self.minValue
        else:
            self.hover = False

    def update(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and self.checkSelect():
                self.clicked = True
            if self.clicked and event.type == pygame.MOUSEBUTTONUP:
                self.clicked = False
                if self.hover:
                    self.image = self.non_hover_image
            if self.clicked and event.type == pygame.MOUSEMOTION:
                self.image = self.original_image.copy()

                mousePos = self.getRelativeMousePos()
                self.currentValue = self.getCurrentValue(mousePos[0])

                # snap to step 
                self.sliderCircle = pygame.draw.circle(self.image, self.circleColor, self.calcCircleCenter(mousePos), self.circleRadius)

                if self.circleOutlineColor:
                    self.sliderCircleOutline = pygame.draw.circle(self.image, self.circleOutlineColor, mousePos, self.circleRadius, self.circleOutlineWidth)

                if self.hover:
                    self.non_hover_image = self.image.copy()
                    hoverMidTop = [self.sliderCircle.centerx, self.sliderCircle.bottom + self.sliderLabelGap]
                    hoverTag = Label(hoverMidTop, int(self.currentValue), self.hoverColor, 10, destOrientation='midtop', 
                                     textBackgroundColor=Color.RED, textBackgroundRounded=2, margin=[10,0])
                    self.image.blit(hoverTag.image, hoverTag.rect)

    def checkSelect(self) -> bool:
        """
        Return true if mouse position is on slider circle
        """
        tempCircle = self.sliderCircle.copy()
        centerDif = [self.image.get_rect().centerx - tempCircle.centerx, self.image.get_rect().centery - tempCircle.centery]
        tempCircle.center = [self.rect.centerx - centerDif[0], self.rect.centery - centerDif[1]]
        return tempCircle.collidepoint(pygame.mouse.get_pos())
    
    def getRelativeMousePos(self) -> Coordinate:
        """ Return coordinate translation of mouse to slider circle """
        mousePos = pygame.mouse.get_pos()
        mouseX = min(max(self.sliderBar.left, self.sliderBar.centerx + (mousePos[0] - self.dest[0])), self.sliderBar.right)
        mouseY = self.sliderBar.centery
        return [mouseX, mouseY] 

    def getCurrentValue(self, centerx: float) -> int:
        """ Return value slider circle is on"""
        if not isinstance(self.scale[0], float):
            return None
        
        value = self.minValue + (centerx - self.sliderBar.left) * ((self.scale[1]-self.scale[0]) / self.sliderWidth)
        if self.step == 1 or value <= self.scale[0] or value >= self.scale[1]:
            return value
        
        step_value = self.scale[0] + self.step*((value // self.step) - (self.scale[0] // self.step)) # unit/pixel

        sign = (value-step_value)/abs(value-step_value) if value-step_value else 0
        step_value += self.step * sign if abs(value-step_value) % self.step > self.step/2 else 0
        step_value = max(self.scale[0], min(step_value, self.scale[1]))
        return step_value

    def calcCircleCenter(self, mousePos: Coordinate) -> Coordinate:
        """ Return new slider circle center snapped to span and step"""
        if not isinstance(self.scale[0], float) or self.step == 1:
            return mousePos
        
        newCircleCenterX = self.sliderBar.left + (self.currentValue - self.scale[0]) * (self.sliderWidth/(self.scale[1]-self.scale[0])) # pixels/unit
        newCircleCenterX = min(self.sliderBar.right, max(self.sliderBar.left, newCircleCenterX))
        return(newCircleCenterX, mousePos[1])


class Table(pygame.sprite.Sprite):
    def __init__(self, dest: Coordinate, textList: list, textColor: ColorValue, textSize: int, fontName: str, **kwargs) -> None:
        super().__init__()
        self.__dict__.update(locals())
        defaults = {
            'bold' : False,
            'italic' : False,
            'backgroundColor' : [0,0,0],
        }

        for attr, default in defaults.items():
            setattr(self, attr, kwargs.get(attr, default))

        font = pygame.font.SysFont(fontName, textSize, self.bold)
        self.listElements = []
        maxWidth = 0
        for order, item in enumerate(textList):
            text = font.render(item, True, textColor)
            textRect = text.get_rect().move(0, order*textSize)
            self.listElements.append([text, textRect])
            maxWidth = max(maxWidth, textRect.width)

        surfaceRect = pygame.Rect(0,0, maxWidth, len(textList) * textSize)
        self.original_image = pygame.Surface(surfaceRect.size, pygame.SRCALPHA).convert()
        self.original_image.fill(self.backgroundColor)

        for text, textRect in self.listElements:
            textRect.centerx = self.original_image.get_rect().centerx
        
        self.original_image.blits(self.listElements)

        self.image = self.original_image
        self.rect = self.image.get_rect(centerx = dest[0], top = dest[1] - self.listElements[0][1].height/2)


class Switch(pygame.sprite.Sprite):
    def __init__(self, dest: Coordinate, width: int, height: int, **kwargs) -> None:
        super().__init__()
        self.__dict__.update(locals())
        defaults = {

        }        

        for attr, default in defaults.items():
            setattr(self, attr, kwargs.get(attr, default))

        surfaceRect = pygame.Rect(0, 0, width+10, height+10)
        self.original_image = pygame.Surface(surfaceRect.size, pygame.SRCALPHA).convert()
        self.original_image.fill(Color.DIMGRAY)

        switchBarRect = pygame.Rect(0, 0, width, height)
        switchBarRect.center = self.original_image.get_rect().center
        switchBar = pygame.draw.rect(self.original_image, Color.DARKGRAY, switchBarRect, 0, 25)

        self.image = self.original_image.copy()

        switchCircle = pygame.draw.circle(self.image, (0,0,255), [switchBarRect.left + switchBar.height/2, switchBarRect.centery], switchBar.height/2)

        self.rect = self.image.get_rect(center = dest)

        self.clicked = False
        self.switchBar = switchBar
        self.switchCircle = switchCircle

    def update(self, event_list: list[pygame.event.Event]) -> None:
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and self.checkSelect():
                self.clicked = not self.clicked

        self.image = self.original_image.copy()

        if self.clicked and self.switchCircle.right < self.switchBar.right:
            self.switchCircle.move_ip(10, 0)
        elif not self.clicked and self.switchCircle.left > self.switchBar.left:
            self.switchCircle.move_ip(-10, 0)

        pygame.draw.circle(self.image, (0,0,255), self.switchCircle.center, self.switchBar.height/2)

        self.rect = self.image.get_rect(center = self.dest)

    def checkSelect(self) -> bool:
        """
        Return true if mouse position is on switch circle
        """
        tempBar = self.switchBar.copy()
        tempBar.center = self.rect.center

        return tempBar.collidepoint(pygame.mouse.get_pos())


class Button(pygame.sprite.Sprite): 
    def __init__(self, centerX, centerY, textString, textSize, action):
        super().__init__()

        self.centerX = centerX
        self.centerY = centerY

        font = pygame.font.SysFont('Arial', textSize, bold=True)

        text = font.render(textString, True, Color.WHITE)
        # pygame.draw.circle(text, WHITE, text.get_rect().center, 10) <-- is in front of text
        textRect = text.get_rect()
        self.original_image = pygame.Surface(textRect.size, pygame.SRCALPHA)
        self.original_image.fill(Color.BLACK)
        self.original_image.blit(text, textRect)

        text = font.render(textString, True, Color.DARKGRAY)
        textRect = text.get_rect()
        self.hovered_image = pygame.Surface(textRect.size, pygame.SRCALPHA)
        self.hovered_image.fill(Color.BLACK)
        self.hovered_image.blit(text, textRect)

        text = font.render(textString, True, Color.DIMGRAY)
        textRect = text.get_rect()
        self.clicked_image = pygame.Surface(textRect.size, pygame.SRCALPHA)
        self.clicked_image.fill(Color.BLACK)
        self.clicked_image.blit(text, textRect)

        self.image = self.original_image
        self.rect = self.image.get_rect(center = (centerX, centerY))

        self.clicked = False
        self.dragged = False
        self.hovered = False

        self.action = action
        self.textString = textString
    
    def update(self, event_list):
        self.hovered = self.rect.collidepoint(pygame.mouse.get_pos())

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
                self.clicked = True
                self.dragged = True
            if event.type == pygame.MOUSEBUTTONUP:
                if self.clicked:
                    self.onClick()

                self.clicked = False
                self.dragged = False

        if self.clicked or self.dragged:
            self.image = self.clicked_image
        elif self.hovered:
            self.image = self.hovered_image
        else:
            self.image = self.original_image
        
        self.rect = self.image.get_rect(center = (self.centerX, self.centerY))
        
    def onClick(self):
        self.action()
        # print('clicked button')












