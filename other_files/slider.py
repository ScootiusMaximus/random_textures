import pygame

class Slider:
    def __init__(self,screen,xpos,ypos,length=100,width=30):
        self.screen = screen
        self.xpos = xpos
        self.ypos = ypos
        self.length = length
        self.width = width
        self.sliderPos = self.xpos + self.length

    def move_to(self,xpos,ypos):
        xdiff = self.xpos - xpos
        self.xpos = xpos
        self.sliderPos -= xdiff
        self.ypos = ypos

    def draw(self):
        pygame.draw.rect(self.screen,(50,50,50),(self.xpos,self.ypos,self.length,self.width))
        pygame.draw.rect(self.screen,(150,150,150),(self.sliderPos,self.ypos-10,15,self.width+20))

    def update(self):
        left, right, up, down = False, False, False, False
        if pygame.mouse.get_pos()[0] > self.xpos:
            left = True
        if pygame.mouse.get_pos()[0] < self.xpos+self.length:
            right = True
        if pygame.mouse.get_pos()[1] > self.ypos:
            up = True
        if pygame.mouse.get_pos()[1] < self.ypos+self.width:
            down = True

        if left and right and up and down and pygame.mouse.get_pressed()[0]:
            self.sliderPos = pygame.mouse.get_pos()[0]

    def get(self) -> float:
        '''Returns a value between 0 and 1 of the slider's position '''
        relativePos = self.sliderPos-self.xpos
        return relativePos / self.length

    def set(self,val):
        relative_pos = val * self.length
        self.sliderPos = relative_pos + self.xpos
