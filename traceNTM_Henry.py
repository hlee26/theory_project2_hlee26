#!/usr/bin/env python3

# import libraries
from collections import deque
import csv

class NTM:
    def __init__(self, name, states, a_in, t_in, start, acc, rej, transitions):
        self.name = name
        self.states = states
        self.a_in = a_in
        self.t_in = t_in
        self.start = start
        self.acc = acc
        self.rej = rej
        self.transitions = transitions
    
    def read_files(data):
        name = data[0][0]
        states = data[1]
        a_in = data[2]
        t_in = data[3]
        start = data[4][0]
        acc = data[5][0]
        rej = data[6][0]
        transitions = [tuple(row) for row in data[7:]]
        
        return NTM(name, states, a_in, t_in, start, acc, rej, transitions)
        
class sim:
    def __init__(self, ntm):
        self.ntm = ntm
        # store bfs tree
        self.tree = []
    
    def go(self, input, max_d=50):
        #begining of tape
        tape = list(input) + ['_']
        starting = ('', self.ntm.start, tape)
        q = deque([starting]) #BFS
        d = 0 # depth of tree
        visited = set() # keep track of visited configs
        total = 0 # count of total transitions

        # display machine details
        print(f"Machine Name: {self.ntm.name}")
        print(f"Initial String: {input}")
        print(f"Max Depth Allowed: {max_d}")

        # do bfs until queue is empty or max depth reached
        while q and d <= max_d:
            curr_lvl = []
            next = deque()
            # process configs in curr queue
            while q:
                left, state, right = q.popleft()
                
                left_str = left.replace('_', '')
                right_str = ''.join(right).replace('_', '')
                curr_config = (left_str, state, right_str)

                # skip if already visited
                if curr_config in visited:
                    continue
                visited.add(curr_config)
                
                curr_lvl.append((left_str, state, right_str))

                # check if machine is accepting
                if state == self.ntm.acc:
                    self.tree.append(curr_lvl)
                    self.print_tree()
                    # this is for visualing the tree
                    print(f'string accepted at depth of {d}')
                    print(f'Total transitions simulated: {total}')
                    print(f'Average determinism: {total/d}')
                    return
                elif state == self.ntm.rej:
                    next.append((left, self.ntm.rej, right))
                    #curr_lvl.append([left_str, state, right_str])
                    continue
                
                curr = right[0] if right else '_'

                # process transitions
                for trans_state, read, n_state, write, dir in self.ntm.transitions:
                    if trans_state == state and read == curr:
                        #print(f"Transition: ({state}, {curr}) -> ({n_state}, {write}, {dir})") #debug line
                        n_left, n_right = self.move_head(left, right, write, dir)
                        next.append((n_left, n_state, n_right))
                        total+=1

                # check if no valid transitions found
                found_transition = any(trans_state == state and read == curr for trans_state, read, _, _, _ in self.ntm.transitions)
                if not found_transition:
                    next.append((left, self.ntm.rej, right))
                    total+=1
            if curr_lvl:
                self.tree.append(curr_lvl)
            
            if not next:
                break

            # increment bfs
            q = next
            d += 1
        if d>max_d:
            print(f'execution stopped after reaching step limit')
        else:
            print(f'string rejected in {d} steps')
            print(f'total transitions simulated: {total}')
        self.print_tree()
        # this is for seeing the tree
        
    def move_head(self, left, right, write, dir):
        #print(left,right,write)
        left = left[:]
        right = right[:]
        if right:
            right[0] = write
        else:
            right = [write]
        
        if dir == 'R': # move head right
            left = left + right.pop(0)
            if not right:
                right = ['_']
        elif dir == 'L': # move head left
            right.insert(0, left[-1] if left else '_')
            left = left[:-1] if left else ''
        else:
            raise ValueError("invalid direction")
        
        return left, right
    
    def print_tree(self):
        for d, lvl in enumerate(self.tree):
            print(f"depth {d}: {lvl}")
        
def load_data(path):
    with open(path, 'r') as file:
        reading = csv.reader(file)
        return [line for line in reading]
    
def main():
    # here is where you have to type in the desired csv file 
    file_content = load_data('a_plus.csv')
    ntm = NTM.read_files(file_content)
    
    simulation = sim(ntm)
    # here is where you have to type in desired input string
    simulation.go('aaa', max_d=50)
    
    
if __name__ == "__main__":
    main()
