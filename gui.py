import pygame
import time

class GUI:
    ##################################################################  READ ME !!! ###################################################################
    ###################################################################################################################################################
    ################################################## what has been added here is explained as follows ###############################################
    # this file is consisted of 3 classes, one for getting w,h,R,B,EH from user, one for providing a paint palette for hand made maps, generation and #
    # it's other provided buttons, and one for simulating the the ready-to-use map                                                                    #
    ###################################################################################################################################################
    # this class does the visualizing of the simulation, the above classes could get merged but this variation has a better modularity property #######
    ###################################################################################################################################################
    ###################################################################################################################################################

    pixelWidth, pixelHeight, page, cubeSize, colors = 0, 0, 0, 0, []

    def __init__(self, cubeSize, delay, state):

        self.pause = False
        self.user_done = False
        ############## Start of Loading Images#############
        self.img_rock = pygame.image.load('pics/rock.png')
        self.img_tile = pygame.image.load('pics/tile.png')
        self.img_crate = pygame.image.load('pics/crate.png')
        self.img_lava = pygame.image.load('pics/lava.png')
        self.img_arrow = pygame.image.load('pics/arrow.png')
        self.img_bg = pygame.image.load('pics/background.png')
        self.img_againButton1 = pygame.image.load('pics/rainbowBox.png')
        self.img_againButton2 = pygame.image.load('pics/rainbowBox2.png')

        ############## initializing and scaling the images and some other needed variables #############
        self.pre_cost = 0
        self.delay = delay
        w = len(state.map_array[0])
        h = len(state.map_array)

        # colors for rocks, hole, empty, box
        self.colors = [-2, -1, 0, 1]
        self.cubeSize = cubeSize
        self.pixelWidth, self.pixelHeight = (w) * self.cubeSize, h * self.cubeSize
        ########
        self.img_lava = pygame.transform.scale(self.img_lava, (int(self.pixelWidth / w), int(self.pixelWidth / w)))
        self.img_rock = pygame.transform.scale(self.img_rock, (int(self.pixelWidth / w), int(self.pixelWidth / w)))
        self.img_tile = pygame.transform.scale(self.img_tile, (int(self.pixelWidth / w), int(self.pixelWidth / w)))
        self.img_crate = pygame.transform.scale(self.img_crate, (int(self.pixelWidth / w), int(self.pixelWidth / w)))
        self.img_arrow = pygame.transform.scale(self.img_arrow, (int(self.pixelWidth / w), int(self.pixelWidth / w)))
        self.img_bg = pygame.transform.scale(self.img_bg, (self.pixelWidth, self.pixelHeight + 2 * self.cubeSize))
        self.img_againButton1 = pygame.transform.scale(self.img_againButton1, (3 * self.cubeSize, self.cubeSize))
        self.img_againButton2 = pygame.transform.scale(self.img_againButton2, (3 * self.cubeSize, self.cubeSize))
        ########
        self.img_againButton = self.img_againButton1
        self.page = pygame.display.set_mode((self.pixelWidth, self.pixelHeight + 2 * self.cubeSize))
        self.redrawPage(state)

    #####################################################################################################################################

    ################################################# refreshing the gui with every action ###############################################
    ################ this functions does almost all the job, it re draws the page and every element of it from scrach, with the action 
    ################ taken from main and map_array it will draw everting tile by tile ####################################################
    def redrawPage(self, game, action=(100, 100, 0)):

        mapArr = game.map_array

        ####################### creating background and a button for re starting the program ##############################################
        self.page.blit(self.img_bg, (0, 0))
        self.page.blit(self.img_againButton,
                       (self.pixelWidth - 3 * self.cubeSize, int(self.pixelHeight + 0.5 * self.cubeSize)))

        ######################## drawing the tiles and the score and the direction of the agents decision ###############################
        self.animate(mapArr, game.animate)
        self.drawTile(mapArr)
        self.drawScores(game)
        self.drawArrow(action[0], action[1], action[2])

        ################# simply a black line border for the sake fo better visuals ##################################################
        pygame.draw.rect(self.page, (0, 0, 0), (0, 0, self.pixelWidth, self.pixelHeight), 3)

        ###################### updates the display by a pre-assigned delay on every step ##############################################
        pygame.display.update()
        pygame.time.delay(self.delay)

        self.handleEvents()

    ########################################################################################################################################

    def handleEvents(self):
        ######################### this for loop keeps track of the events happening on the gui  ########################################
        ######################### so that the buttons and x button could work properly by the event of a click #########################
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            x, y = pygame.mouse.get_pos()
            if ((self.pixelWidth - 3 * self.cubeSize < x < self.pixelWidth) and
                    int(self.pixelHeight + 0.5 * self.cubeSize) < y < int(
                        self.pixelHeight + 0.5 * self.cubeSize) + self.cubeSize):
                self.img_againButton = self.img_againButton2
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.user_done = True
                    import Main as main
                    main.main()
            else:
                ############################# animating a buttons visuals by using 2 versions of its pictures #############################
                ############################# one where the mouse is located on it and the other when its not ############################
                ############################# rest of the button animations are the same way so x'll not be commenting them after one #####
                self.img_againButton = self.img_againButton1

    ############################### draws animation #########################################
    def animate(self, mapArray, animationArray, frames=30):
        if animationArray is None or len(animationArray)==0: return None
        di, dj = animationArray.pop(0)

        t = 0
        while t < self.delay:
            for i, a in enumerate(mapArray):
                for j, tile in enumerate(a):
                    self.colorCube(j, i, self.colors[tile])
                    if (i, j) in animationArray:
                        self.colorCube(j, i, self.colors[0 if tile == 1 else tile])

            pygame.time.delay(self.delay // frames)
            t += self.delay / frames
            for (i, j) in animationArray:
                i += -di + di * t / self.delay;
                j += -dj + dj * t / self.delay
                self.page.blit(self.img_crate, (int(j * self.cubeSize), int(i * self.cubeSize)))
            pygame.display.update()

            self.handleEvents()

    ############################### draws the map array tile by tile #########################################
    def drawTile(self, array):
        for i, a in enumerate(array):
            for j, tile in enumerate(a):
                self.colorCube(j, i, self.colors[tile])

    ############################################ drawing the score ##################################################
    def drawScores(self, state):

        #
        pygame.font.init()
        font = pygame.font.SysFont('Arial Rounded MT', 28)

        color = (41, 0, 0)
        text = "Path Cost : " + str(state.cost)
        text_surface = font.render(text, True, color)

        pre_cost = state.cost - self.pre_cost

        text2 = "Step Cost : " + str(pre_cost)
        text2_surface = font.render(text2, True, color)
        self.pre_cost = state.cost
        self.page.blit(text_surface, (10, self.pixelHeight + self.cubeSize * 1.2))
        self.page.blit(text2_surface, (10, self.pixelHeight + self.cubeSize * 0.8))

        temp = state.cost
        pygame.display.update()

    ####################################################################################################################

    ############################################### draw tiles ###########################################################
    def colorCube(self, i, j, color):
        if color == 0:
            self.page.blit(self.img_rock, (self.pixelPos(i), self.pixelPos(j)))
        if color == 1:
            self.page.blit(self.img_lava, (self.pixelPos(i), self.pixelPos(j)))
        if color == -2:
            self.page.blit(self.img_tile, (self.pixelPos(i), self.pixelPos(j)))
        if color == -1:
            self.page.blit(self.img_crate, (self.pixelPos(i), self.pixelPos(j)))

    ########################################################################################################################

    ######################################### draws the direction and position of ai's decision ############################################
    def drawArrow(self, i, j, dir):
        angle = 0
        if dir == 'right':
            angle = 270
        elif dir == 'down':
            angle = 180
        elif dir == 'left':
            angle = 90
        rotated_image = pygame.transform.rotate(self.img_arrow, angle)
        self.page.blit(rotated_image, (self.pixelPos(j), self.pixelPos(i)))
        ######################################################################################################################

    ################################### converts pixel coordination to grid coordination ###################################
    def pixelPos(self, i):
        return i * self.cubeSize
        #######################################################################################################################


#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
####################################################       NEXT CLASS : INPUT GUI       #####################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################


class InputBox:

    ##################################################################  READ ME !!! ###################################################################
    ###################################################################################################################################################
    ################################################## what has been added here is explained as follows ###############################################
    # the following class takes the numerical inputs from the user and gives them to the main function so it can be used for later classes            #
    #
    ###################################################################################################################################################
    # consists of 3 main functions, draw (which simply drawsa textbox and a rectangle for its visuals), draw_base, which draws and updates the gui    #
    # window, and the handle_events for handeling changes to texts and selecting textboxes ############################################################
    ###################################################################################################################################################
    ###################################################################################################################################################

    def __init__(self, x=0, y=0, w=0, h=0, text=''):
        ##################################### messy it is, sorry, just nitializing the needed variables and the images and so on .. ########
        pygame.init()
        self.page1 = pygame.display.set_mode((1000, 700))
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('black')
        self.FONT = pygame.font.Font(None, 32)
        self.N = 10
        self.valid_args = True
        ###################### loading the background and button images########################
        self.img_bg1 = pygame.image.load('pics/background.png')
        self.img_bg1 = pygame.transform.scale(self.img_bg1, (1000, 700))
        self.img_doneButton1 = pygame.image.load('pics/doneButton.png')
        self.img_doneButton1 = pygame.transform.scale(self.img_doneButton1, (240, 80))
        self.img_doneButton2 = pygame.image.load('pics/doneButton2.png')
        self.img_doneButton2 = pygame.transform.scale(self.img_doneButton2, (240, 80))
        self.img_doneButton3 = pygame.image.load('pics/doneButton3.png')
        self.img_doneButton3 = pygame.transform.scale(self.img_doneButton3, (240, 80))
        self.img_txtBox = pygame.image.load('pics/textBoxLong.png')
        self.img_txtBox = pygame.transform.scale(self.img_txtBox, (500, 50))
        self.img_txtBoxShort = pygame.image.load('pics/textBox.png')
        self.img_txtBoxShort = pygame.transform.scale(self.img_txtBoxShort, (250, 50))
        self.img_doneButton = self.img_doneButton1
        ###################### making a list of our texts####################################

        self.textList = ["Input you're disired width : ", "Input you're disired height : ",
                         "Input you're disired amount of rocks : ", "Input you're disired amount boxes : ",
                         "Input you're disired amount of extra holes : "]
        #####################################################################################

        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_ACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    ########################### this one mainly controls the texts that are shown in the text boxes #####################################################
    ########################## we keep track of mouse clicks and if it collides with any textbox it will be activated, as simple as that ! #############
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                # toggeling the active var if it is clicked on
                self.active = not self.active
            else:
                self.active = False
                # we change the color so it is visualized which one are we editing
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                ####################### taking keyboard inputs ################################
                if event.key == pygame.K_RETURN:

                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <= 10:
                        self.text += event.unicode
                # rendeting the text (more exactly re rendering)
                self.txt_surface = self.FONT.render(self.text, True, (0, 0, 0))

    def update(self):
        # it can update the lengh of the textbox if its needed (we woudlnt really ..)
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, page1):
        self.page1.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 14))
        pygame.draw.rect(self.page1, self.color, self.rect, 1)

    ##################### this one draws the gui window from scrach we'll call this one over and over again untill user hits done buttons ##################
    def draw_base(self, img_bg, img_doneButton1, img_txtBoxShort, img_txtBox, page1, FONT, textList):
        self.page1.blit(self.img_bg1, (0, 0))
        self.page1.blit(self.img_doneButton, (700, 550))

        ################# we'll create 5 txtbox pictures for the sake fo visuals 
        for i in range(5):
            self.page1.blit(self.img_txtBox, (50, 50 + 100 * i))
            self.page1.blit(self.img_txtBoxShort, (700, 50 + 100 * i))

            text = self.textList[i]
            txt_surface = self.FONT.render(text, True, (0, 0, 0))
            self.page1.blit(txt_surface, (50 + 25, 50 + 100 * i + 15))

        self.img_txtBoxLarge = pygame.transform.scale(self.img_txtBox, (620, 75))

        ################## some un-interactable texts for informing the user ###############################
        self.page1.blit(self.img_txtBoxLarge, (25, 55 + 500))
        text = ' R, B and EH are calculated by default if left empty !'
        txt_surface = self.FONT.render(text, True, (0, 0, 0))
        self.page1.blit(txt_surface, (35, 55 + 500 + 15))

        text2 = ' with the formula : R = m*n*0.02 and B = m*n*0.2 and 0'
        txt_surface2 = self.FONT.render(text2, True, (0, 0, 0))
        self.page1.blit(txt_surface2, (35, 80 + 500 + 15))

    ######################## this draws the first window of our program and instantiates the InputBox which creates boxes for text
    def firstPage(self):

        clock = pygame.time.Clock()
        self.draw_base(self.img_bg1, self.img_doneButton, self.img_txtBoxShort, self.img_txtBox, self.page1, self.FONT,
                       self.textList)

        input_box1 = InputBox(725, 50, 400, 50, '10')
        input_box2 = InputBox(725, 150, 400, 50, '10')
        input_box3 = InputBox(725, 250, 400, 50, '')
        input_box4 = InputBox(725, 350, 400, 50, '')
        input_box5 = InputBox(725, 450, 400, 50, '')

        input_boxes = [input_box1, input_box2, input_box3, input_box4, input_box5]

        done = False
        ############### the loop that takes the inputs, and refreshes the gui every moment, when user hits done button, the done var is set to True and the while vreaks
        while not done:
            # print()
            # if input_box1 == '' or input_box2.text == '' : 
            #     self.valid_args = False
            # else : 
            #     try : 
            #         tmp1, tmp2, tmp3 = input_box3.text, input_box4.text, input_box5.text
            #         if tmp1 == '' : 
            #             tmp1 = int(input_box1.text) * int(input_box2.text) * 0.05
            #         if tmp2 == '' : 
            #             tmp2 = int(input_box1.text) * int(input_box2.text) * 0.5
            #         if tmp3 == '' : 
            #             tmp3 = 0
            #         tmp1, tmp2, tmp3 = int(tmp1), int(tmp2), int(tmp3)
            #         if (2 + int(input_box1.text)) * (2 + int(input_box2.text)) < tmp1 + tmp2 + tmp3 : 
            #             self.valid_args = False
            #         else : 
            #             self.valid_args = True
            #     except :
            #         pass
            

            try : 
                
                a, b = int(input_box1.text), int(input_box2.text)
                
                try :
                    
                    tmp1, tmp2, tmp3 = input_box3.text, input_box4.text, input_box5.text
                    
                    if tmp1 == '' : 
                        tmp1 = int(input_box1.text) * int(input_box2.text) * 0.05
                    if tmp2 == '' : 
                        tmp2 = int(input_box1.text) * int(input_box2.text) * 0.5
                    if tmp3 == '' : 
                        tmp3 = 0
                    #print(tmp1, tmp2, tmp3, a, b)
                    if (2 + a) * (2 + b) < int(tmp1) + int(tmp2) + int(tmp3) : 
                        
                        self.valid_args = False
                    else : 
                        self.valid_args = True
                except : 
                    try : 
                        a, b = int(input_box1.text), int(input_box2).text
                        self.valid_args = True 
                    except : 
                        self.valid_args = False
            except : 
                self.valid_args = False



            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                x, y = pygame.mouse.get_pos()
                if 700 < int(x) < 940 and 550 < int(y) < 630:

                    self.img_doneButton = self.img_doneButton2
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.valid_args : 
                            done = True
                        else : 
                            pass
                            self.img_doneButton = self.img_doneButton3
                else:
                    self.img_doneButton = self.img_doneButton1

                ########### keeping track of each box's condition, so if the user clicks it we'll know
                for box in input_boxes:
                    box.handle_event(event)

            for box in input_boxes:
                box.update()

            self.draw_base(self.img_bg1, self.img_doneButton, self.img_txtBoxShort, self.img_txtBox, self.page1,
                           self.FONT, self.textList)

            for box in input_boxes:
                box.draw(self.page1)

            pygame.display.flip()
            clock.tick(60)

        return (input_boxes)

    ######################## this one doesnt do anything special, just outputing the user prefs to main file
    def run_inputGUI(self):
        inp_boxes = self.firstPage()  # 400, 550, 640, 630)
        cnt = 0
        c = []
        for i in inp_boxes:
            c.append(i.text)
            # print(textList[cnt], x.text)
            cnt += 1
        if c[2] == '' or c[2] == ' ':
            c[2] = str(int(c[0]) * int(c[1]) // 20)

        if c[3] == '' or c[3] == ' ':
            c[3] = str(int(c[0]) * int(c[1]) // 2)

        if c[4] == '' or c[4] == ' ':
            c[4] = '0'
        return c


#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
########################################################       NEXT CLASS : PAINT       #####################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################
#############################################################################################################################################





class InputBoxSaveLoad:

    ##################################################################  READ ME !!! ###################################################################
    ###################################################################################################################################################
    ################################################## what has been added here is explained as follows ###############################################
    # the following class takes the numerical inputs from the user and gives them to the main function so it can be used for later classes            #
    #
    ###################################################################################################################################################
    # consists of 3 main functions, draw (which simply drawsa textbox and a rectangle for its visuals), draw_base, which draws and updates the gui    #
    # window, and the handle_events for handeling changes to texts and selecting textboxes ############################################################
    ###################################################################################################################################################
    ###################################################################################################################################################

    def __init__(self, x=0, y=0, w=0, h=0, text=''):
        ##################################### messy it is, sorry, just nitializing the needed variables and the images and so on .. ########
        pygame.init()
        pygame.display.set_mode((1000, 250))
        self.page1 = pygame.display.set_mode((1000, 250))
        self.COLOR_INACTIVE = pygame.Color('lightskyblue3')
        self.COLOR_ACTIVE = pygame.Color('white')
        self.FONT = pygame.font.Font(None, 32)
        self.N = 10

        ###################### loading the background and button images########################
        self.img_bg1 = pygame.image.load('pics/background.png')
        self.img_bg1 = pygame.transform.scale(self.img_bg1, (1000, 300))
        self.img_doneButton1 = pygame.image.load('pics/doneButton.png')
        self.img_doneButton1 = pygame.transform.scale(self.img_doneButton1, (240, 80))
        self.img_doneButton2 = pygame.image.load('pics/doneButton2.png')
        self.img_doneButton2 = pygame.transform.scale(self.img_doneButton2, (240, 80))
        self.img_txtBox = pygame.image.load('pics/textBoxLong.png')
        self.img_txtBox = pygame.transform.scale(self.img_txtBox, (500, 50))
        self.img_txtBoxShort = pygame.image.load('pics/textBox.png')
        self.img_txtBoxShort = pygame.transform.scale(self.img_txtBoxShort, (250, 50))
        self.img_doneButton = self.img_doneButton1
        ###################### making a list of our texts####################################

        self.textList = ["Input The File Name : ", "", "", "", ""]
        #####################################################################################

        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_ACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        pygame.display.set_mode((1000, 300))

    ########################### this one mainly controls the texts that are shown in the text boxes #####################################################
    ########################## we keep track of mouse clicks and if it collides with any textbox it will be activated, as simple as that ! #############
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                # toggeling the active var if it is clicked on
                self.active = not self.active
            else:
                self.active = False
                # we change the color so it is visualized which one are we editing
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                ####################### taking keyboard inputs ################################
                if event.key == pygame.K_RETURN:

                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) <= 50:
                        self.text += event.unicode
                        
                # rendeting the text (more exactly re rendering)
                self.txt_surface = self.FONT.render(self.text, True, (0, 0, 0))

    def update(self):
        # it can update the lengh of the textbox if its needed (we woudlnt really ..)
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, page1):
        self.page1.blit(self.txt_surface, (self.rect.x + 15, self.rect.y + 14))
        pygame.draw.rect(self.page1, self.color, self.rect, 1)

    ##################### this one draws the gui window from scrach we'll call this one over and over again untill user hits done buttons ##################
    def draw_base(self, img_bg, img_doneButton1, img_txtBoxShort, img_txtBox, page1, FONT, textList):
        self.page1.blit(self.img_bg1, (0, 0))
        self.page1.blit(self.img_doneButton, (350, 150))

        ################# we'll create 5 txtbox pictures for the sake fo visuals 
        for i in range(1):
            self.page1.blit(self.img_txtBox, (50, 50 + 100 * i))
            self.page1.blit(self.img_txtBoxShort, (700, 50 + 100 * i))

            text = self.textList[i]
            txt_surface = self.FONT.render(text, True, (0, 0, 0))
            self.page1.blit(txt_surface, (50 + 25, 50 + 100 * i + 15))

        self.img_txtBoxLarge = pygame.transform.scale(self.img_txtBox, (620, 75))

    ######################## this draws the first window of our program and instantiates the InputBox which creates boxes for text
    def firstPage(self):

        clock = pygame.time.Clock()
        self.draw_base(self.img_bg1, self.img_doneButton, self.img_txtBoxShort, self.img_txtBox, self.page1, self.FONT,
                       self.textList)

        input_box1 = InputBox(725, 50, 400, 50, 'map')

        input_boxes = [input_box1]

        done = False
        ############### the loop that takes the inputs, and refreshes the gui every moment, when user hits done button, the done var is set to True and the while vreaks
        while not done:
            # print()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                x, y = pygame.mouse.get_pos()
                if 350 < int(x) < 590 and 150 < int(y) < 230:

                    self.img_doneButton = self.img_doneButton2
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        done = True
                else:
                    self.img_doneButton = self.img_doneButton1

                ########### keeping track of each box's condition, so if the user clicks it we'll know
                for box in input_boxes:
                    box.handle_event(event)

            for box in input_boxes:
                box.update()

            self.draw_base(self.img_bg1, self.img_doneButton, self.img_txtBoxShort, self.img_txtBox, self.page1,
                           self.FONT, self.textList)

            for box in input_boxes:
                box.draw(self.page1)

            pygame.display.update()
            clock.tick(60)

        return (input_boxes)

    ######################## this one doesnt do anything special, just outputing the user prefs to main file
    def inputPopup(self):
        inp_boxes = self.firstPage()  # 400, 550, 640, 630)
        cnt = 0
        c = []
        for i in inp_boxes:
            c.append(i.text)
        return c[0]






class Paint:
    pixelWidth, pixelHeight, page, cubeSize = 0, 0, 0, 0

    def __init__(self, cubeSize, w, h, R, B, EH):

        ##################################### this is the variable in which the Gui requests for data ##################################
        self.request = None
        ################################################################################################################################

        ############################################## Start of Loading Images #########################################################
        self.map_array = [[-1 if u == int(h) + 1 or u == 0 or k == 0 or k == int(w) + 1
                           else 0 for u in range(int(h) + 2)] for k in range(int(w) + 2)]

        self.request = 'reset'

        self.img_rock = pygame.image.load('pics/rock.png')
        self.img_tile = pygame.image.load('pics/tile.png')
        self.img_crate = pygame.image.load('pics/crate.png')
        self.img_lava = pygame.image.load('pics/lava.png')
        self.img_bg = pygame.image.load('pics/background.png')

        self.img_genButton1 = pygame.image.load('pics/generateButton.png')
        self.img_resetButton1 = pygame.image.load('pics/resetButton.png')
        self.img_simulButton1 = pygame.image.load('pics/simulateButton.png')
        self.img_saveButton1 = pygame.image.load('pics/saveButton.png')
        self.img_loadButton1 = pygame.image.load('pics/loadButton.png')
        self.img_valButton1 = pygame.image.load('pics/validateButton.png')
        self.img_selectButton1 = pygame.image.load('pics/pen.png')

        ###################### seconds ones are just for the animation of the buttons when mouse is located on them ###################

        self.img_genButton2 = pygame.image.load('pics/generateButton2.png')
        self.img_resetButton2 = pygame.image.load('pics/resetButton2.png')
        self.img_simulButton2 = pygame.image.load('pics/simulateButton2.png')
        self.img_saveButton2 = pygame.image.load('pics/saveButton2.png')
        self.img_loadButton2 = pygame.image.load('pics/loadButton2.png')
        self.img_valButton2 = pygame.image.load('pics/validateButton2.png')
        self.img_selectButton2 = pygame.image.load('pics/pen2.png')
        self.img_emptyBox = pygame.image.load('pics/emptyBox.png')

        ##############################################################################################################################

        ################################################ Start of Scaling Images##########################################
        self.w = int(w)
        
        
        self.h = int(h)
        self.R = int(R)
        self.B = int(B)
        self.EH = int(EH)
        self.real_h = int(h)
        self.real_w = int(w)
        self.R_B_EH_usedList = {-2: 0, -1: 0, 1: 0, 0: 0}
        self.R_B_EH_maxList = {-2: self.R, -1: self.EH, 1: self.B, 0: 99999}
        self.cubeSize = cubeSize
        self.FONT = pygame.font.Font(None, 32)
        self.base_w, self.base_h = self.w, self.h
        self.w, self.h = max(self.w, self.h), max(self.w, self.h)
        self.pixelWidth, self.pixelHeight = self.w * self.cubeSize + self.w - 1, self.h * self.cubeSize + self.h - 1
        self.pen = 3

        self.img_lava = pygame.transform.scale(self.img_lava,
                                               (int(self.pixelWidth / self.w), int(self.pixelWidth / self.w)))
        self.img_rock = pygame.transform.scale(self.img_rock,
                                               (int(self.pixelWidth / self.w), int(self.pixelWidth / self.w)))
        self.img_tile = pygame.transform.scale(self.img_tile,
                                               (int(self.pixelWidth / self.w), int(self.pixelWidth / self.w)))
        self.img_crate = pygame.transform.scale(self.img_crate,
                                                (int(self.pixelWidth / self.w), int(self.pixelWidth / self.w)))
        self.img_bg = pygame.transform.scale(self.img_bg, (
            self.pixelWidth + 8 * self.cubeSize, self.pixelHeight + 5 * self.cubeSize))
        self.img_genButton1 = pygame.transform.scale(self.img_genButton1, (cubeSize * 3, cubeSize))
        self.img_simulButton1 = pygame.transform.scale(self.img_simulButton1, (cubeSize * 3, cubeSize))
        self.img_resetButton1 = pygame.transform.scale(self.img_resetButton1, (cubeSize * 3, cubeSize))
        self.img_saveButton1 = pygame.transform.scale(self.img_saveButton1, (cubeSize * 3, cubeSize))
        self.img_loadButton1 = pygame.transform.scale(self.img_loadButton1, (cubeSize * 3, cubeSize))
        self.img_selectButton1 = pygame.transform.scale(self.img_selectButton1, (cubeSize * 3, cubeSize * 2))
        ###########################  same as above #####################################################
        self.img_genButton2 = pygame.transform.scale(self.img_genButton2, (cubeSize * 3, cubeSize))
        self.img_simulButton2 = pygame.transform.scale(self.img_simulButton2, (cubeSize * 3, cubeSize))
        self.img_resetButton2 = pygame.transform.scale(self.img_resetButton2, (cubeSize * 3, cubeSize))
        self.img_saveButton2 = pygame.transform.scale(self.img_saveButton2, (cubeSize * 3, cubeSize))
        self.img_loadButton2 = pygame.transform.scale(self.img_loadButton2, (cubeSize * 3, cubeSize))
        self.img_selectButton2 = pygame.transform.scale(self.img_selectButton2, (cubeSize * 3, cubeSize * 2))
        ###################################################################################################################
        self.img_genButton = self.img_genButton1
        self.img_simulButton = self.img_simulButton1
        self.img_resetButton = self.img_resetButton1
        self.img_saveButton = self.img_saveButton1
        self.img_loadButton = self.img_loadButton1
        self.img_selectButton = self.img_selectButton1

        ########################################## creating the base pallette #############################################
        self.exitButton = False
        self.feedback = True
        self.page = pygame.display.set_mode((self.pixelWidth + 8 * self.cubeSize, self.pixelHeight + 5 * self.cubeSize))
        self.draw_base_pallete()
        self.screenX, self.screenY = self.pixelWidth + 8 * self.cubeSize, self.pixelHeight + 5 * self.cubeSize
        ###################################################################################################################

        ###################################### we want to have a cleared map at the start of our drawing ###########################
        self.R_B_EH_usedList = {-2: 0, -1: 0, 1: 0, 0: 0}
        self.request = ['reset']
        self.draw_base_pallete()
        self.feedback = False

    ######################### this basically just draws the intial state of map pallette and the buttons in it###########################
    def draw_base_pallete(self):

        small_pics_scaler = 1 if min(self.w, self.h) <= 8 else 0
        self.page.blit(self.img_bg, (0, 0))
        pygame.draw.rect(self.page, (0, 0, 0),
                         pygame.Rect(0, 0, self.pixelWidth + 8 * self.cubeSize, self.pixelHeight + 5 * self.cubeSize),
                         20)
        pygame.draw.rect(self.page, (0, 0, 0),
                         pygame.Rect(self.cubeSize, self.cubeSize, (self.base_w + 2) * self.cubeSize,
                                     (self.base_h + 2) * self.cubeSize), 20)
        self.page.blit(self.img_genButton, ((self.w + 4) * self.cubeSize, self.cubeSize * (1)))
        self.page.blit(self.img_simulButton,
                       ((self.w + 4) * self.cubeSize, self.cubeSize * (3 - 1 * small_pics_scaler)))
        self.page.blit(self.img_resetButton,
                       ((self.w + 4) * self.cubeSize, self.cubeSize * (5 - 2 * small_pics_scaler)))
        self.page.blit(self.img_selectButton,
                       ((self.w + 4) * self.cubeSize, self.cubeSize * (7 - 3 * small_pics_scaler)))
        
        
        self.page.blit(self.img_loadButton, ((self.w + 4) * self.cubeSize, self.cubeSize * (self.h + 2 * small_pics_scaler)))
        self.page.blit(self.img_saveButton, ((self.w + 4) * self.cubeSize, self.cubeSize * (self.h + 2 + 1 * small_pics_scaler)))

        pygame.draw.rect(self.page, (0, 0, 0),
                         pygame.Rect(self.pixelPos(self.w + 6) - 2, self.pixelPos(8 - 3 * small_pics_scaler) - 2,
                                     self.cubeSize + 4, self.cubeSize), 8)
        self.colorCube(self.w + 6, 8 - 3 * small_pics_scaler, self.pen - 2)

        if 30 < self.cubeSize < 60:
            self.img_emptyBox = pygame.transform.scale(self.img_emptyBox, (self.cubeSize * 6, int(self.cubeSize * 1.5)))
            self.page.blit(self.img_emptyBox, ((1) * self.cubeSize - 10, self.cubeSize * (self.h + 4) - 30))

        text1 = ' Remaining Rocks : ' + str(abs(self.R_B_EH_maxList[-2] - self.R_B_EH_usedList[-2]))
        txt_surface1 = self.FONT.render(text1, True, (0, 0, 0))
        self.page.blit(txt_surface1, ((1) * self.cubeSize, self.cubeSize * (self.h + 4) - 20))

        text1 = ' Remaining Boxes : ' + str(abs(self.R_B_EH_maxList[1] - self.R_B_EH_usedList[1]))
        txt_surface1 = self.FONT.render(text1, True, (0, 0, 0))
        self.page.blit(txt_surface1, ((1) * self.cubeSize, self.cubeSize * (self.h + 4)))

        text1 = ' Remaining Extra Hs : ' + str(abs(self.R_B_EH_maxList[-1] - self.R_B_EH_usedList[-1]))
        txt_surface1 = self.FONT.render(text1, True, (0, 0, 0))
        self.page.blit(txt_surface1, ((1) * self.cubeSize, self.cubeSize * (self.h + 4) + 20))

        for i in range(len(self.map_array)):
            for j in range(len(self.map_array[i])):
                self.colorCube(i + 1, j + 1, self.map_array[i][j])

        pygame.display.flip()

    ####################################################################################################################################

    ######################### this one paints the pixel with the desired pen ################################################################
    def colorCube(self, i, j, color):
        if color == -2:
            self.page.blit(self.img_rock, (self.pixelPos(i), self.pixelPos(j)))
        if color == -1:
            self.page.blit(self.img_lava, (self.pixelPos(i), self.pixelPos(j)))
        if color == 0:
            self.page.blit(self.img_tile, (self.pixelPos(i), self.pixelPos(j)))
        if color == 1:
            self.page.blit(self.img_crate, (self.pixelPos(i), self.pixelPos(j)))

    #######################################################################################################################################

    ######################## just for converting pixels coordinations to grid coordinations ###########################
    def pixelPos(self, i):
        return i * self.cubeSize
        ###################################################################################################################

    ######################## in case we need to convert pygame.events to string keyboard input ########################
    def unicode_to_str(self, s):
        index = s.index(":")
        return (s[index + 3:index + 4])

    ###################################################################################################################

    ############################################# detects collisions of mouse and buttons ####################################
    def button_handler(self, buttonPos):
        x, y = pygame.mouse.get_pos()
        if buttonPos[0] < x < buttonPos[0] + self.cubeSize * 3 and buttonPos[1] < y < buttonPos[1] + self.cubeSize:
            return True

    ##########################################################################################################################

    ################################# the main part of code, this part draws the pallete with mouse movements #################################3
    def draw_pallete(self):
        small_pics_scaler = 1 if min(self.w, self.h) <= 8 else 0
        pen = 3
        last_time_pen_changed = 0
        while True:
            if (self.feedback):
                self.request = ''
            else:
                break

            if (self.exitButton):
                break

            event = pygame.event.poll()
            x, y = pygame.mouse.get_pos()

            quited = pygame.event.get(pygame.QUIT)
            if quited:
                exit()

                ########################################### Checking SaveButton ################################# DONE
            if self.button_handler(((self.w + 4) * self.cubeSize, self.cubeSize * (self.h  + 2 + 1 * small_pics_scaler))):
                self.img_saveButton = self.img_saveButton2

                if pygame.mouse.get_pressed()[0]:
                    self.request = ['save']
                    self.feedback = False

            else:
                self.img_saveButton = self.img_saveButton1
                pygame.display.flip

            ########################################### Checking LoadButton ################################# DONE
            if self.button_handler(((self.w + 4) * self.cubeSize, self.cubeSize * (self.h + 2 * small_pics_scaler))):
                self.img_loadButton = self.img_loadButton2

                if pygame.mouse.get_pressed()[0]:
                    self.R_B_EH_usedList = {-2: 0, -1: 0, 1: 0, 0: 0}
                    self.request = ['load']
                    self.draw_base_pallete()
                    self.feedback = False

            else:
                self.img_loadButton = self.img_loadButton1
                pygame.display.flip
                ########################################### Checking ResetButton ################################# DONE
            if self.button_handler(((self.w + 4) * self.cubeSize, self.cubeSize * (5 - 2 * small_pics_scaler))):
                self.img_resetButton = self.img_resetButton2

                if pygame.mouse.get_pressed()[0]:
                    self.R_B_EH_usedList = {-2: 0, -1: 0, 1: 0, 0: 0}
                    self.request = ['reset']
                    self.draw_base_pallete()
                    self.feedback = False
            else:
                self.img_resetButton = self.img_resetButton1
                pygame.display.flip
            ########################################### Checking SimulButton #################################   ?!
            if self.button_handler(((self.w + 4) * self.cubeSize, self.cubeSize * (3 - 1 * small_pics_scaler))):
                self.img_simulButton = self.img_simulButton2

                if pygame.mouse.get_pressed()[0]:
                    self.request = ['simulate']
                    self.feedback = False

            else:
                self.img_simulButton = self.img_simulButton1
                pygame.display.flip
            ########################################### Checking GenButton #################################    DONE
            if self.button_handler(((self.w + 4) * self.cubeSize, self.cubeSize * (1))):
                self.img_genButton = self.img_genButton2

                if pygame.mouse.get_pressed()[0]:
                    self.R_B_EH_usedList = self.R_B_EH_maxList
                    self.R_B_EH_usedList[0] = 0

                    self.request = ['generate']
                    self.draw_base_pallete()
                    self.feedback = False
            else:
                self.img_genButton = self.img_genButton1

            ########################################### Checking SelectlButton ####################################################3
            if (self.button_handler(((self.w + 4) * self.cubeSize, self.cubeSize * (7 - 3 * small_pics_scaler)))
                    or self.button_handler(((self.w + 4) * self.cubeSize, self.cubeSize * (8 - 3 * small_pics_scaler)))):
                self.img_selectButton = self.img_selectButton2

                if pygame.mouse.get_pressed()[0]:
                    self.pen = self.pen + 1 if self.pen <= 2 else 0
                    pygame.display.flip()
                    time.sleep(0.2)


            else:
                self.img_selectButton = self.img_selectButton1

            ######################################################################################################################

            ################################################ painting with mouse ##################################################
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                if (0 <= x // self.cubeSize - 1 <= self.real_w + 1) and (0 <= y // self.cubeSize - 1 <= self.real_h + 1):
                    try:

                        if ((self.pen - 2 == 1 or self.pen - 2 == 0) and
                                ((x // self.cubeSize == 1 or y // self.cubeSize == 1) or
                                 (x // self.cubeSize == self.w + 2 or y // self.cubeSize == self.h + 2))
                                or (self.pen - 2 == 1 and self.map_array[x // self.cubeSize - 1][
                                    y // self.cubeSize - 1] == -1)):
                            pass

                        else:

                            if self.R_B_EH_usedList[self.pen - 2] < self.R_B_EH_maxList[self.pen - 2]:
                                
                                

                                self.R_B_EH_usedList[
                                    int(self.map_array[x // self.cubeSize - 1][y // self.cubeSize - 1])] -= 1

                                self.R_B_EH_usedList[self.pen - 2] += 1

                                self.colorCube(x // self.cubeSize, y // self.cubeSize, self.pen - 2)
                                self.request = ['set array',
                                                (x // self.cubeSize - 1, y // self.cubeSize - 1, self.pen - 2)]
                                self.feedback = False

                                self.draw_base_pallete()


                    except AttributeError:
                        pass

            self.draw_base_pallete()
            pygame.display.update()
            pygame.time.Clock().tick(60)
            ###########################################################################################################################

