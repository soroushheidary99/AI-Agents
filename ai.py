class Agent:
    def __init__(self, env_perception):
        # YOU CAN CHOOSE AGENT TYPE HERE, LOOK AT AGENT_TYPE_DICT TO FIND OUT OTHER CHOICES
        self.agent_type = "random"

        # A DICTIONARY OF AVAILABLE AGENT ALGORITHMS. YOU CAN ADD UP MORE TO THIS LIST IF YOU WISH.
        self.agent_type_dict = {

            "A_Star": self.A_Star_agent,
            "IDS": self.IDS_agent,
            "random": self.random_agent,

        }

        self.perceive = env_perception
        self.sequence=[]

    # Algorithms which return an *action sequence* or a *single action*

    def A_Star_agent(self):
        map_array = self.perceive()
        action_sequence = []
        ######### EDITABLE SECTION #########



        ######### END OF EDITABLE SECTION #########
        return action_sequence

    def IDS_agent(self):
        map_array = self.perceive()
        action_sequence = []
        ######### EDITABLE SECTION #########



        ######### END OF EDITABLE SECTION #########
        return action_sequence

    def random_agent(self):
        import random

        map_array = self.perceive()
        w, h = len(map_array[0]), len(map_array)
        for _ in range(100):
            (i, j) = (random.randint(1, h - 2), random.randint(1, w - 2))
            if map_array[i][j] == 1: break
        h_edge_dist = min(i, h - 1 - i)
        v_edge_dist = min(j, w - 1 - j)
        if h_edge_dist < v_edge_dist:
            if 2 * i < h:
                dir = 'up'
            else:
                dir = 'down'
        else:
            if 2 * j < w:
                dir = 'left'
            else:
                dir = 'right'

        return Action(i, j, dir)


    def act(self):
        # If sequence not empty, pops another action
        if len(self.sequence)!=0: return self.sequence.pop(0)

        # Result is whether a sequence or a single action object
        result = self.agent_type_dict[self.agent_type]()

        # check if the result was a sequence
        if isinstance(result, list) and not(False in [isinstance(ar, Action) for ar in result]):
            self.sequence = result
            return self.sequence.pop(0)

        # As it was not a sequence, this line assures the result was a valid single action
        if not isinstance(result, Action):
            raise TypeError("Agent did not return an instance of the class Action")

        return result

class State:
    pass

class Node:
    pass

class Action:
    def __init__(self,i,j,direction):
        self.update(i,j,direction)

    def update(self, i, j, direction):
        # Validates the action format as (int, int, string)
        if not (isinstance(i, int) and isinstance(j, int) and isinstance(direction, str)):
            raise TypeError("x, y or direction has wrong type")

        self.x = i
        self.y = j
        self.direction = direction

    def return_action(self): return (self.x, self.y, self.direction)
