from env import Env
import pygame
from MapLoader import ChallengeDesigner
from gui import GUI
from gui import InputBox
from gui import InputBoxSaveLoad
from gui import Paint
# YOU CAN CHOOSE AGENT TYPE FROM THE AGENT/AGENT_INSPIRATION CLASS
from ai import Agent
from other_agents import AgentInspiration


def main():
    # GUI initial config
    cubeSize = 50
    delay = 300

    # Getting preferred parameters from user
    InpGui = InputBox()
    userParams = InpGui.run_inputGUI()
    if max( int(userParams[0]), int(userParams[1]) ) >= 14:
        cubeSize -= max(int(userParams[0]), int(userParams[1]))

    cd = ChallengeDesigner(int(userParams[0]), int(userParams[1]))

    # Preparing the Paint Gui
    PaintGui = Paint(cubeSize, *userParams)
    PaintGui.draw_pallete()



    while True:

        request = PaintGui.request
        print(request)

        if request[0] == 'get array':
            PaintGui.map_array = cd.get_array()
            PaintGui.feedback = True

        elif request[0] == 'set array':
            
            x, y, val = request[1]
            cd.set_array(x, y, val)
            PaintGui.feedback = True

        elif request[0] == 'save':
            pygame.display.set_mode( (1000, 250) )
            InputText = InputBoxSaveLoad()
            saveFileName = InputText.inputPopup()
            pygame.display.set_mode( (PaintGui.screenX, PaintGui.screenY) )
            info = [PaintGui.w, PaintGui.h, PaintGui.R, PaintGui.B, PaintGui.EH, PaintGui.R_B_EH_usedList ]
            cd.save_array(saveFileName, info)
            PaintGui.feedback = True

        elif request[0] == 'load':
            pygame.display.set_mode( (1000, 250) )
            InputText = InputBoxSaveLoad()
            loadFileName = InputText.inputPopup()
            pygame.display.set_mode( (PaintGui.screenX, PaintGui.screenY) )
            loaded_map_info = cd.load_array(loadFileName)
            loaded_map = cd.get_array()
            
            PaintGui = Paint(cubeSize, loaded_map_info[0], loaded_map_info[1], loaded_map_info[2],
                            loaded_map_info[3], loaded_map_info[4],)###
            PaintGui.R_B_EH_usedList = loaded_map_info[5]
            PaintGui.map_array = loaded_map
            PaintGui.feedback = True
            PaintGui.draw_pallete()###



        elif request[0] == 'reset':
            cd.reset_array()
            PaintGui.map_array = cd.get_array()
            PaintGui.feedback = True

        elif request[0] == 'generate':
            cd.generate_array(userParams)
            PaintGui.map_array = cd.get_array()
            PaintGui.feedback = True

        elif request[0] == 'simulate':
            break

        PaintGui.draw_pallete()

    initial_Map = [list(x) for x in zip(*cd.get_array())]

    sim = Env(initial_Map)
    # agent = AgentInspiration(sim.send_map)
    agent = Agent(sim.send_map)
    gui = GUI(cubeSize=cubeSize, delay=delay, state=sim.state)

    
    while not (sim.goal_test()) :
        if gui.user_done :
            break
        action = agent.act()
        while sim.state.validate_action(action.return_action()) is False:
            action = agent.act()

        gui.redrawPage(sim.state, action.return_action())

        sim.take_action(action.return_action())

    if not gui.user_done :
            gui.redrawPage(sim.state)

    print("End Of Simulation !!!")



main()
