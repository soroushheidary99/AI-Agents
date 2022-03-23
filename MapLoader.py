class ChallengeDesigner:

    ##################################################################  READ ME !!! ###################################################################
    ###################################################################################################################################################
    ################################################## what has been added here is explained as follows ###############################################
    # as already being said in the main file, GUI cannot access the env and its attributes directly so it needs to request for the needed properties  #
    # the main file acts as a mediator, which takes the requests from GUI and calls the needed function on challange designers, for example when the  #
    # user is painting a map, the gui needs the constant updates of map_array so it requests it from main, and main will call the                     #
    # ChallangeDesigner.get_array() and applies that to the GUI                                                                                       #
    ###################################################################################################################################################
    # other functions added here are 2 basic (with a not so great algorithm for generating solvable maps)  ((validation_array_maker and create_map))  #
    # the algorithm for that purpose is simply, to check if a tile has "solvable neighbours" if a neighbour is located next to a abyss tile           #
    # then its neighbours are solvable too, after a list of valid (solvable) cells is created then it as many as boxes as we want can be taken out    #
    # from the list (which are valid cells for boxes as the whole algorithms focuses on that ! )                                                      #
    ###################################################################################################################################################
    ###################################################################################################################################################

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.map_array = [[-1 if u == self.h + 1 or u == 0 or k == 0 or k == self.w + 1
                           else 1 for u in range(self.h + 2)] for k in range(self.w + 2)]
        self.load_info = None

    def validation_array_maker(self):
        h, w = len(self.map_array), len(self.map_array[0])
        temp_h = h - 2
        temp_w = w - 2
        step = 0

        validation_array = [[True if self.map_array[j][i] == -1 else False for i in range(w)] for j in range(h)]

        for i in range(1, h - 1):
            for j in range(1, w - 1):
                if validation_array[i + 1][j] or validation_array[i - 1][j] or validation_array[i][j + 1] or \
                        validation_array[i][j - 1]:
                    validation_array[i][j] = True

        # We un-validate all the cells of the most outer layer we want the crates to be intially only on the deck not on the lava
        for i in range(h):
            for j in range(w):
                if self.map_array[i][j] == -2 or self.map_array[i][j] == -1:
                    validation_array[i][j] = False

        valid_list = []
        for i in range(h):
            for j in range(w):
                if validation_array[i][j] == True:
                    valid_list.append((i, j))

        return valid_list

    def create_map(self, h, w, rock_number, crate_number, extra_holes):
        w, h, rock_number, crate_number, extra_holes = int(w), int(h), int(rock_number), int(crate_number), int(
            extra_holes)

        ######### EDITABLE SECTION #########

        import random
        self.map_array = [[-1 if u == w + 1 or u == 0 or k == 0 or k == h + 1
                           else 0 for u in range(w + 2)] for k in range(h + 2)]

        
        for i in range(rock_number):
            i_rand = random.randint(0, w + 1)
            j_rand = random.randint(0, h + 1)

            # this while makes sure not to put rock on a cell which is already filled with rick
            while self.map_array[j_rand][i_rand] == -2:
                i_rand = random.randint(0, w + 1)
                j_rand = random.randint(0, h + 1)

            self.map_array[j_rand][i_rand] = -2

        for i in range(extra_holes):
            j_rand = random.randint(1, w)
            i_rand = random.randint(1, h)

            # this while makes sure not to put rock on a cell which is already filled with extra holes
            while self.map_array[i_rand][j_rand] == -2 or self.map_array[i_rand][j_rand] == -1:
                j_rand = random.randint(1, w)
                i_rand = random.randint(1, h)

            self.map_array[i_rand][j_rand] = -1

        valid_cells = self.validation_array_maker()

        random.shuffle(valid_cells)

        for i in range(min(crate_number, len(valid_cells))):
            self.map_array[valid_cells[i][0]][valid_cells[i][1]] = 1

        return self.map_array

    def set_array(self, x, y, val):
        self.map_array[x][y] = val

    def get_array(self, ):
        return self.map_array

    def generate_array(self, ans):
        self.map_array = self.create_map(*ans)

    def save_array(self, name, info):
        import pickle
        pickle.dump(self.map_array, open(name + ".pickle", "wb"))
        pickle.dump(info, open(name + "_info.pickle", "wb"))

    def load_array(self, name):
        import pickle
        self.map_array = pickle.load(open(name + ".pickle", "rb"))
        load_info = pickle.load(open(name + "_info.pickle", "rb"))
        return load_info

    def reset_array(self, ):
        self.map_array = [[-1 if u == self.h + 1 or u == 0 or k == 0 or k == self.w + 1
                           else 0 for u in range(self.h + 2)] for k in range(self.w + 2)]
