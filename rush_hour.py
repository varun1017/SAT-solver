from z3 import *
import sys


info = []
with open(sys.argv[1]) as f:
	for line in f:
		info.append([int(v) for v in line.strip().split(',')])

n = info[0][0]
limit = info[0][1]

red = []
red.append(info[1][0])
red.append(info[1][1])

v = []
h = []
b = []
for i in range(1,len(info)):
    if(i == 1):
        h.append([info[1][0],info[1][1]])
    else:
        if(info[i][0] == 0):
            v.append([info[i][1],info[i][2]])
        elif(info[i][0] == 1):
            h.append([info[i][1],info[i][2]])
        else:
            b.append([info[i][1],info[i][2]])
vcount = len(v)
hcount = len(h)
bcount = len(b)

# print(v,h,b,sep="\n")
# Input 1 text output
# v = [[1, 11], [1, 12], [6, 10], [0, 0], [1, 1], [7, 8], [9, 8], [0, 9], [4, 0], [1, 3], [8, 5], [11, 0], [0, 8], [8, 7]]
# h = [[3, 3], [11, 11], [4, 11], [1, 4], [11, 4], [8, 10]]
# b = []
solver = Solver()

rcar = []
for i in range(limit+1):
     rcar.append([ Int('r_%i_0'%(i)) , Int('r_%i_1'%(i)) ])

vcar = []
hcar = []
bombs = []
for i in range(limit+1):
    vcar.append([])
    hcar.append([])
    for j in range(vcount):
        vcar[i].append( [ Int('v_%i_%i_0'%(i,j)) , Int('v_%i_%i_1'%(i,j)) ] )
    for j in range(hcount):
        hcar[i].append( [ Int('h_%i_%i_0'%(i,j)) , Int('h_%i_%i_1'%(i,j)) ] )

for i in range(bcount):
    bombs.append( [ Int('b_%i_%i'%(i,0)) , Int('b_%i_%i'%(i,1)) ] )
# solver.add(vcar[0][1][0]==5)
# solver.push()
# solver.pop()
# if(solver.check() == sat):
#     m = solver.model()
#     print(m[vcar[0][1][0]])

move_info = []
for i in range(limit):
    move_info.append([ Int('m_%i_0'%(i)) , Int('m_%i_1'%(i)) ])

# print(move_info) checked if the moves are correct

#Initializing the board -----------------------------------------------------------------------------------------------------

for i in range(vcount):
    solver.add(vcar[0][i][0] == v[i][0])
    solver.add(vcar[0][i][1] == v[i][1])
for i in range(hcount):
    solver.add(hcar[0][i][0] == h[i][0])
    solver.add(hcar[0][i][1] == h[i][1])
for i in range(bcount):
    solver.add(bombs[i][0] == b[i][0])
    solver.add(bombs[i][1] == b[i][1])
solver.add(rcar[0][0] == red[0])
solver.add(rcar[0][1] == red[1])


for i in range(limit):
    solver.add(move_info[i][0] >= 0)
    solver.add(move_info[i][0] < n)
    solver.add(move_info[i][1] >= 0)
    solver.add(move_info[i][1] < n)

#Adding clauses for moving the cars without any collisions with other cars and bombs --------------------------------------------------

def empty_square(row, col, step):
    car_I_present = BoolVal(False)
    if(col == 0):
        for i in range(hcount):
            car_I_present = Or(car_I_present, And(hcar[step][i][0]==row, hcar[step][i][1]==col))
    elif(col == n-1):
        for i in range(hcount):
            car_I_present = Or(car_I_present, And(hcar[step][i][0]==row, (hcar[step][i][1]+1)==col))
    else:
        for i in range(hcount):
            car_I_present = Or(car_I_present, And( hcar[step][i][0] == row, hcar[step][i][1] == col))
            car_I_present = Or(car_I_present, And(hcar[step][i][0] == row, (hcar[step][i][1]+1)==col))
    
    if(row == 0):
        for i in range(vcount):
            car_I_present = Or(car_I_present, And(vcar[step][i][0]==row, vcar[step][i][1]==col))
    elif(row == n-1):
        for i in range(vcount):
            car_I_present = Or(car_I_present, And((vcar[step][i][0]+1)==row, (vcar[step][i][1])==col))
    else:
        for i in range(vcount):
            car_I_present = Or(car_I_present, And(vcar[step][i][0]==row, vcar[step][i][1]==col))
            car_I_present = Or(car_I_present, And((vcar[step][i][0]+1)==row, vcar[step][i][1]==col))
    
    for i in range(bcount):
        car_I_present = Or(car_I_present, And(bombs[i][0]== row, bombs[i][1]== col))
    
    return Not(car_I_present)

# solver.add(empty_square(3,3,0))
# if(solver.check() == sat):
#     print("sat")

# print(h)
# print(v)
# i = 0
# j = 0
# left_move = And( hcar[i][j][0] == move_info[i][0] , hcar[i][j][1] == move_info[i][1] )
# right_move = And(hcar[i][j][0] == move_info[i][0] , (hcar[i][j][1]+1) == move_info[i][1])

# right_move_step = And(hcar[i+1][j][0] == hcar[i][j][0], hcar[i+1][j][1] == (hcar[i][j][1]+1))
# left_move_step = And(hcar[i+1][j][0] == hcar[i][j][0], hcar[i+1][j][1] == (hcar[i][j][1]-1))
# No_move = And(hcar[i+1][j][0] == hcar[i][j][0], hcar[i+1][j][1] == hcar[i][j][1])

# left_or_right = Or(left_move, right_move)
# # moved = Or(moved , left_or_right)

# cond_left_mov = And(empty_square(hcar[i][j][0], (hcar[i][j][1]-1), i), hcar[i][j][1]-1 >= 0)
# cond_right_mov = And(empty_square(hcar[i][j][0], hcar[i][j][1]+2, i), (hcar[i][j][1]+2 < n))

# cond_left_mov = And(cond_left_mov, left_move_step)
# cond_right_mov = And(cond_right_mov, right_move_step)
# is_moved = Or(Not(left_move), cond_left_mov)
# is_moved = And(is_moved, Or(Not(right_move, cond_right_mov)))
# is_moved =  And(is_moved, Or(left_or_right, No_move))

# solver.add(is_moved)

# up_move = And( vcar[i][j][0] == move_info[i][0] , vcar[i][j][1] == move_info[i][1] )
# down_move = And((vcar[i][j][0]+1) == move_info[i][0] , vcar[i][j][1] == move_info[i][1])

# down_move_step = And(vcar[i+1][j][0] == (vcar[i][j][0]+1), vcar[i+1][j][1] == vcar[i][j][1])
# up_move_step = And(vcar[i+1][j][0] == (vcar[i][j][0]-1), vcar[i+1][j][1] == vcar[i][j][1])
# No_move = And(vcar[i+1][j][0] == vcar[i][j][0], vcar[i+1][j][1] == vcar[i][j][1])
# up_or_down = Or(up_move, down_move)
# # moved = Or(moved , up_or_down)
# cond_up_mov = And(empty_square((vcar[i][j][0]-1), vcar[i][j][1], i), (vcar[i][j][0]-1) >= 0)
# cond_down_mov = And(empty_square((vcar[i][j][0]+2), vcar[i][j][1], i), (vcar[i][j][0]+2 < n))
# cond_up_mov = And(cond_up_mov, up_move_step)
# cond_down_mov = And(cond_down_mov, down_move_step)
# is_moved = Or(Not(up_move), cond_up_mov)
# is_moved = And(is_moved, Or(Not(down_move), cond_down_mov))
# is_moved =  And(is_moved, Or(up_or_down, No_move))
# solver.add(is_moved)



# if solver.check() == sat :
#     m = solver.model()
#     print(m)
#     print(m.eval(move_info[j][0]),",",m.eval(move_info[j][1]),sep="")

for i in range(limit):
    moved = BoolVal(False)
    
    for j in range(hcount):

        left_move = And( hcar[i][j][0] == move_info[i][0] , hcar[i][j][1] == move_info[i][1] )
        right_move = And(hcar[i][j][0] == move_info[i][0] , (hcar[i][j][1]+1) == move_info[i][1])

        right_move_step = And(hcar[i+1][j][0] == hcar[i][j][0], hcar[i+1][j][1] == (hcar[i][j][1]+1))
        left_move_step = And(hcar[i+1][j][0] == hcar[i][j][0], hcar[i+1][j][1] == (hcar[i][j][1]-1))
        No_move = And(hcar[i+1][j][0] == hcar[i][j][0], hcar[i+1][j][1] == hcar[i][j][1])

        left_or_right = Or(left_move, right_move)
        moved = Or(moved , left_or_right)

        cond_left_mov = And(empty_square(hcar[i][j][0], (hcar[i][j][1]-1), i), hcar[i][j][1]-1 >= 0)
        cond_right_mov = And(empty_square(hcar[i][j][0], hcar[i][j][1]+2, i), (hcar[i][j][1]+2 < n))

        cond_left_mov = And(cond_left_mov, left_move_step)
        cond_right_mov = And(cond_right_mov, right_move_step)
        is_moved = Or(Not(left_move), cond_left_mov)
        is_moved = And(is_moved, Or(Not(right_move), cond_right_mov))
        is_moved =  And(is_moved, Or(left_or_right, No_move))

        solver.add(is_moved)

    for j in range(vcount):

        up_move = And( vcar[i][j][0] == move_info[i][0] , vcar[i][j][1] == move_info[i][1] )
        down_move = And((vcar[i][j][0]+1) == move_info[i][0] , vcar[i][j][1] == move_info[i][1])
        
        down_move_step = And(vcar[i+1][j][0] == (vcar[i][j][0]+1), vcar[i+1][j][1] == vcar[i][j][1])
        up_move_step = And(vcar[i+1][j][0] == (vcar[i][j][0]-1), vcar[i+1][j][1] == vcar[i][j][1])
        No_move = And(vcar[i+1][j][0] == vcar[i][j][0], vcar[i+1][j][1] == vcar[i][j][1])

        up_or_down = Or(up_move, down_move)
        moved = Or(moved , up_or_down)

        cond_up_mov = And(empty_square((vcar[i][j][0]-1), vcar[i][j][1], i), (vcar[i][j][0]-1) >= 0)
        cond_down_mov = And(empty_square((vcar[i][j][0]+2), vcar[i][j][1], i), (vcar[i][j][0]+2 < n))

        cond_up_mov = And(cond_up_mov, up_move_step)
        cond_down_mov = And(cond_down_mov, down_move_step)
        is_moved = Or(Not(up_move), cond_up_mov)
        is_moved = And(is_moved, Or(Not(down_move), cond_down_mov))
        is_moved =  And(is_moved, Or(up_or_down, No_move))

        solver.add(is_moved)
    
    left_move = And( rcar[i][0] == move_info[i][0] , rcar[i][1] == move_info[i][1] )
    right_move = And(rcar[i][0] == move_info[i][0] , (rcar[i][1]+1) == move_info[i][1])

    right_move_step = And(rcar[i+1][0] == rcar[i][0], rcar[i+1][1] == (rcar[i][1]+1))
    left_move_step = And(rcar[i+1][0] == rcar[i][0], rcar[i+1][1] == (rcar[i][1]-1))
    No_move = And(rcar[i+1][0] == rcar[i][0], rcar[i+1][1] == rcar[i][1])

    left_or_right = Or(left_move, right_move)
    moved = Or(moved , left_or_right)

    cond_left_mov = And(empty_square(rcar[i][0], (rcar[i][1]-1), i), rcar[i][1]-1 >= 0)
    cond_right_mov = And(empty_square(rcar[i][0], rcar[i][1]+2, i), (rcar[i][1]+2 < n))

    cond_left_mov = And(cond_left_mov, left_move_step)
    cond_right_mov = And(cond_right_mov, right_move_step)
    is_moved = Or(Not(left_move), cond_left_mov)
    is_moved = And(is_moved, Or(Not(right_move), cond_right_mov))
    is_moved =  And(is_moved, Or(left_or_right, No_move))

    solver.add(is_moved)
    solver.add(moved)
    solver.push()
    solver.add(rcar[i+1][1] == n-2)

    if(solver.check() == sat):
        m = solver.model()
        for j in range(i+1):
            print(m.eval(move_info[j][0]),",",m.eval(move_info[j][1]),sep="")
        sys.exit(0)
    else: 
        solver.pop()
print("Unsat")