class State:
    def __init__(self, map):
        self.map_array = map
        self.cost = 0
        self.ex_move = None
        self.ex_dir = None
        self.prev_num_box=0

        self.animate = None

    # def __deepcopy__(self, memo):
    #     from copy import deepcopy
    #     id_self = id(self)  # memoization avoids unnecessary recursion
    #     _copy = memo.get(id_self)
    #     if _copy is None:
    #         _copy = type(self)( deepcopy(self.state.map_array, memo) )
    #         _copy.cost = deepcopy(self.cost, memo)
    #         _copy.ex_dir = deepcopy(self.ex_dir, memo)
    #         _copy.ex_move = deepcopy(self.ex_move, memo)
    #         _copy.prev_num_box = deepcopy(self.prev_num_box, memo)
    #         memo[id_self] = _copy
    #     return _copy

    def update(self, i, j, direction):

        self.update_score(i, j, direction)
        self.update_map(i, j, direction)

    def tuple_add(self, x, y):
        return (x[0] + y[0], x[1] + y[1])

    def update_score(self, i, j, direction):

        ################################################################### READ ME ########################################################################
        #                                                                                                                                                  #
        # What the code below does is as follow :                                                                                                          #
        # I have defined 2 variables called ex_move and ex_dir which holds the last crate we tried to push and its direction                               #
        # we increament the cost by the amount of stacked_crates which we wish to push (whether we can or not !) plus 1 (the initial cost)                 #
        # we decreament the cost by 1 if the ex_move and ex_dir matches the current move and current dir                                                   #
        # -- Its also notable that i had to change the order of called funtions in the funtion "update" for the algorithm to work properly                 #
        #                                                                                                                                                  #
        ####################################################################################################################################################

        p_cost_conf = 4
        if (i, j) == self.ex_move and direction == self.ex_dir:
            self.prev_num_box *= 2
            penalty_cost = 0
        else: penalty_cost = p_cost_conf

        dir_dic = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        number_of_box = 0
        pos = (i, j)
        while True:
            if self.map_array[pos[0]][pos[1]] != 1: break
            number_of_box += 1
            pos = self.tuple_add(pos, dir_dic[direction])

        if number_of_box > self.prev_num_box: penalty_cost = p_cost_conf

        if self.map_array[pos[0]][pos[1]] != -2:
            self.ex_move = self.tuple_add((i, j), dir_dic[direction])
            self.ex_dir = direction
        else:
            self.ex_move = (i, j)
            self.ex_dir = direction

        self.cost += number_of_box + penalty_cost
        self.prev_num_box = number_of_box

    def update_map(self, i, j, direction):

        ################################################################### READ ME ########################################################################
        #                                                                                                                                                  #
        # What the code below does is as follow :                                                                                                          #
        # a dir_dic is made so we won't have to use multiple if statements                                                                                 #
        # an assumed cursor is made, which follows the direction until it reaches a non crate cell                                                         #
        # if its a rock we'll do nothing, if its lava we remove the box in x,y and if its a empty cell we'll remove the box in x,y and we add a box in     #
        #   (x, y) + direction, and if its a crate we follow the direction by cursor untill we reach a non crate cell                                      #
        # the rest doesn't need anymore comments as it is clear in the code  (sorry if it's messy !!!)                                                     #
        #                                                                                                                                                  #
        ####################################################################################################################################################

        dir_dic = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        cursor_pos = (i, j)

        cursor_pos = self.tuple_add(cursor_pos, dir_dic[direction])
        self.animate = []
        if self.map_array[i][j] == 1:
            self.animate = [dir_dic[direction], cursor_pos]
            while True:
                if self.map_array[cursor_pos[0]][cursor_pos[1]] == 1:
                    cursor_pos = self.tuple_add(cursor_pos, dir_dic[direction])
                    self.animate.append(cursor_pos)

                elif self.map_array[cursor_pos[0]][cursor_pos[1]] == -2:
                    self.animate = None
                    break

                elif self.map_array[cursor_pos[0]][cursor_pos[1]] == -1:
                    self.map_array[i][j] = 0
                    break

                elif self.map_array[cursor_pos[0]][cursor_pos[1]] == 0:
                    self.map_array[i][j] = 0
                    self.map_array[cursor_pos[0]][cursor_pos[1]] = 1
                    break

    def validate_action(self, action):
        i, j, direction = action[0], action[1], action[2]
        # Checks if the direction is valid
        if direction not in ["up", "down", "right", "left"]:
            print("invalid, action name is wrong")
            return False

        # Makes sure if the coordinates are within range
        if 1 > i or i > len(self.map_array) - 2 or \
                1 > j or j > len(self.map_array[0]) - 2:
            print("invalid, chosen coordinate out of border")
            return False

        # Makes sure if it's chosen a box
        # if self.map_array[x][y] != 1:
        #     print("invalid, no box in this slot")
        #     return False

        return True


class Env:
    def __init__(self, map):
        self.state = State(map)

    def __eq__(self, obj):
        return isinstance(obj, Env) and \
               obj.state.ex_dir == self.state.ex_dir and \
               obj.state.ex_move == self.state.ex_move and \
               obj.state.map_array == self.state.map_array

    def take_action(self, action):
        self.state.update(*action)

    def send_map(self):
        from copy import deepcopy
        return deepcopy(self.state.map_array)

    def send_cost(self):
        return self.state.cost

    def copy_env(self):
        from copy import deepcopy
        a=Env(deepcopy(self.state.map_array))
        a.state = deepcopy(self.state)
        return a

    def goal_test(self):
        if any(1 in sublist for sublist in self.state.map_array):
            return False
        print("Total cost = " + str(self.state.cost))
        return True
