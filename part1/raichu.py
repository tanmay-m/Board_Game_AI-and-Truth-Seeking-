#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
# Name - Mansi Kishore Ranka, Tanmay Girish Mahindrakar, Sohan Narayan Kakatkar
# UID: mranka, tmahind, skakatka
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def to_matirx(board,N):
    return [[*board[i:i+N]] for i in range(0, N*N, N)]

def matrix_to_string(board,n):
    s = ""
    for i in range(n):
        for j in range(n):
            s = s + board[i][j]
    return s


def evaluation_function(board,N):
    weight_dict = {'w':1, 'W': 5, '@': 10, 'b':-2, 'B': -5, '$': -10}
    
    score = 0

    for i in range(N):
        for j in range(N):
            ## Piece advantage
            score = score + weight_dict.get(board[i][j],0)

            ## Mobility

            # if(board[i][j]=='W'):
            #     if(N-(j+2)>0):
            #         score = score + 2
            #     else:
            #         score = score + 

            ## If I am going to get a white raichu
            if(board[i][j]=='w' and i>N/2):
                #score = score + N*(1**(N-1-i))
                 score = score + 1*(1**(N-1-i))
            if(board[i][j]=='W' and i>N/2):
                #score = score + N*(1**(N-1-i))
                 score = score + 1*(1**(N-1-i))
            ## If my white pikachu is at the center of the board
            # if(board[i][j]=='W' and i>=(N/2)-1 and i<=(N/2)+1 and j>=(N/2)-1 and j<=(N/2)+1):
            #     score = score + 5
            # ## If my white raichu is at the center of the board
            # if(board[i][j]=='@' and i>=(N/2)-1 and i<=(N/2)+1 and j>=(N/2)-1 and j<=(N/2)+1):
            #     score = score + 8

            ## If I am going to get a black raichu
            if(board[i][j]=='b' and i<N/2):
                #score = score - N*(1**(i))
                score = score - 1*(1**(i))
            if(board[i][j]=='B' and i<N/2):
                #score = score - N*(1**(i))
                score = score - 1*(1**(i))
            ## If my black pikachu is at the center of the board
            # if(board[i][j]=='B' and i>=(N/2)-1 and i<=(N/2)+1 and j>=(N/2)-1 and j<=(N/2)+1):
            #     score = score - 5
            # ## If my black raichu is at the center of the board
            # if(board[i][j]=='$' and i>=(N/2)-1 and i<=(N/2)+1 and j>=(N/2)-1 and j<=(N/2)+1):
            #     score = score - 8

    # if(player=="White"):
    #     return score
    # return -1*score
    return score

def is_goal(board,N):

    white_state = ['w','W','@']

    black_state = ['b','B','$']

    white_pieces,black_pieces = 0,0

    for i in range(N):
        for j in range(N):
            if(board[i][j] in white_state):   
                white_pieces = white_pieces+1
            elif(board[i][j] in black_state):         
                black_pieces = black_pieces+1

    if(white_pieces!=0 and black_pieces==0):
        return sys.maxsize
    elif(black_pieces!=0 and white_pieces==0):
        return -sys.maxsize
    
    return 0

## Reference for alpha beta pruning is taken from  -> https://www.naftaliharris.com/blog/chess/
def minimax(board,N,max_depth,curr_depth,turn,alpha,beta,timelimit,curr_time,best_board):
    #print("in minimax")
    ## base case -> if goal has reached
    #print(matrix_to_string(best_board,N))
    
    #print("hi1")
    start_time = time.perf_counter()

    is_goal_state = is_goal(board,N)
    if(is_goal_state!=0):
        #print("hello")
        # print(board)
        return board,is_goal_state

    #print("hi2")
    ## base case -> max depth of exploration is reached
    if(curr_depth>max_depth):
        #print("Max depth is reached")
        print(matrix_to_string(best_board,N))
        score = evaluation_function(board,N)
        return board,score

    if(turn):
        #print("It is white's move")
        max_score = -sys.maxsize
        max_score_board = None
        best_move = None
        for state in get_successors(board,N,"White",timelimit):
            # if(curr_depth==0):
            #     print(matrix_to_string(state,N))
            curr_board,score = minimax(state,N,max_depth,curr_depth+1,False,alpha,beta,timelimit,curr_time,best_board)
            if(score>alpha and curr_board!=None):
                alpha = score
                best_move = state
                best_board = state
            if(score>max_score and curr_board!=None):
                max_score = score
                max_score_board = state
            if(curr_depth==0):
                print(matrix_to_string(best_board,N))
            if(alpha>=beta):
                break
        #return max_score_board,max_score
        return best_move,alpha
    else:
        #print("It is black's move")
        min_score = sys.maxsize
        min_score_board = None
        best_move = None
        for state in get_successors(board,N,"Black",timelimit):
            # if(curr_depth==0):
            #     print(matrix_to_string(state,N))
            curr_board,score = minimax(state,N,max_depth,curr_depth+1,True,alpha,beta,timelimit,curr_time,best_board)
            if(score<beta and curr_board!=None):
                beta = score
                best_move = state
                best_board = state
            if(score<min_score and curr_board!=None):
                min_score = score
                min_score_board = state
            if(curr_depth==0):
                print(matrix_to_string(best_board,N))
            if(alpha>=beta):
                break
        #return min_score_board,min_score
        return best_move,beta


def test_fucntion(board,N):

    temp = to_matirx(board,N)

    # print("Printing initial board")
    # print(temp)
    next_board,next_score = temp,-1000000000
    next_board,next_score = minimax(temp,N,5,0,True,-sys.maxsize,sys.maxsize)
    # print("Printing final move")
    # print(next_score)
    # print(next_board)
    print(matrix_to_string(next_board,N))

def isallowed(N,x,y):
    if(x<0 or x>=N or y<0 or y>=N):
        return False
    return True

def move_pichu(board,N,row,col,player="White"):

    #print("In move_pichu printing origional board")
    #print(board)

    moved_pichus = []
    if(player=="White"):
        direction = [(1,1),(1,-1)]
        can_kill = ['b']
        c = 'w'
        raichu_c = '@'
    else:
        direction = [(-1,-1),(-1,+1)]
        can_kill = ['w']
        c = 'b'
        raichu_c = '$'
    
    for dir in direction:
        dirx,diry = dir
        total_kills = 0
        x,y = row+dirx,col+diry
        steps = 1
        while(isallowed(N,x,y) and steps>0):
            # print(x,end=" ")
            # print(y)
            if(board[x][y]=='.'):
                new_board = board[0:row] + [board[row][0:col] + ['.',] + board[row][col+1:]] + board[row+1:]
                if(player=="White" and x==N-1):
                    new_board = new_board[0:x] + [new_board[x][0:y] + [raichu_c,] + new_board[x][y+1:]] + new_board[x+1:]
                elif(player=="Black" and x==0):
                    new_board = new_board[0:x] + [new_board[x][0:y] + [raichu_c,] + new_board[x][y+1:]] + new_board[x+1:]
                else:
                    new_board = new_board[0:x] + [new_board[x][0:y] + [c,] + new_board[x][y+1:]] + new_board[x+1:]
                #new_board = board[0:row] + [board[row][0:col] + ['.',] + board[row][col+1:]] + [board[x][0:y] + [c,] + board[x][y+1:]] + board[x+1:]
                moved_pichus.append(new_board)
                x,y = x+dirx,y+diry
                steps = steps-1
            elif(board[x][y] in can_kill and isallowed(N,x+dirx,y+diry) and board[x+dirx][y+diry]=='.'):
                x_prime = x+dirx
                y_prime = y+diry
                new_board = board[0:x] + [board[x][0:y] + ['.',] + board[x][y+1:]] + board[x+1:]
                new_board = new_board[0:row] + [new_board[row][0:col] + ['.',] + new_board[row][col+1:]] + new_board[row+1:]

                if(player=="White" and x_prime==N-1):
                    new_board = new_board[0:x_prime] + [new_board[x_prime][0:y_prime] + [raichu_c,] + new_board[x_prime][y_prime+1:]] + new_board[x_prime+1:]
                elif(player=="Black" and x_prime==0):
                    new_board = new_board[0:x_prime] + [new_board[x_prime][0:y_prime] + [raichu_c,] + new_board[x_prime][y_prime+1:]] + new_board[x_prime+1:]
                else:
                    new_board = new_board[0:x_prime] + [new_board[x_prime][0:y_prime] + [c,] + new_board[x_prime][y_prime+1:]] + new_board[x_prime+1:]
                moved_pichus.append(new_board)
                total_kills = total_kills+1
                x,y = x_prime,y_prime
                steps = steps-1
            else:
                break
    ## diagonal right
    # x,y = row+1,col+1
    # if(isallowed(N,x,y)):
    #     #print("hi1")
    #     if(board[x][y]=='.'):
    #         new_board = board[0:row] + [board[row][0:col] + ['.',] + board[row][col+1:]] + [board[x][0:y] + ['w',] + board[x][y+1:]] + board[x+1:]
    #         moved_pichus.append(new_board)
    #     elif(board[x][y] in can_kill and isallowed(N,x+1,y+1) and board[x+1][y+1]=='.'):
    #         x_prime = x+1
    #         y_prime = y+1
    #         new_board = board[0:row] + [board[row][0:col] + ['.',] + board[row][col+1:]] + [board[x][0:y] + ['.',] + board[x][y+1:]] + [board[x_prime][0:y_prime] + ['w',] + board[x_prime][y_prime+1:]] + board[x_prime+1:]
    #         moved_pichus.append(new_board)

    # ## diagonal left
    # x,y = row+1,col-1
    # if(isallowed(N,x,y)):
    #     if(board[x][y]=='.'):
    #         new_board = board[0:row] + [board[row][0:col] + ['.',] + board[row][col+1:]] + [board[x][0:y] + ['w',] + board[x][y+1:]] + board[x+1:]
    #         moved_pichus.append(new_board)
    #     elif(board[x][y] in can_kill and isallowed(N,x+1,y-1) and board[x+1][y-1]=='.'):
    #         x_prime = x+1
    #         y_prime = y-1
    #         new_board = board[0:row] + [board[row][0:col] + ['.',] + board[row][col+1:]] + [board[x][0:y] + ['.',] + board[x][y+1:]] + [board[x_prime][0:y_prime] + ['w',] + board[x_prime][y_prime+1:]] + board[x_prime+1:]
    #         moved_pichus.append(new_board)

    return moved_pichus

### Confirm that if in the first move i kill a black pikachu or pichu can i move forward
def move_pikachu(board,N,row,col,player="White"):
    #print(board)

    # print("In move_pikachu printing origional board")
    # print(board)

    moved_pikachu = []

    if(player=="White"):
        c = 'W'
        can_kill = ['b','B']
        direction = [(1,0),(0,1),(0,-1)]
        raichu_c = '@'
    else:
        c = 'B'
        can_kill = ['w','W']
        direction = [(-1,0),(0,1),(0,-1)]
        raichu_c = '$'

    for dir in direction:
        x,y = row,col
        x_prev,y_prev = x,y
        opponent_x,opponent_y = -1,-1
        steps = 2
        total_kills = 0
        dirx,diry = dir[0],dir[1]
        #x,y = x+dirx,y+diry
        while(isallowed(N,x,y) and steps>0):
            #print(dirx)
            #print(diry)
            x_prev,y_prev = x,y
            x,y = x+dirx,y+diry
            if(isallowed(N,x,y)):
                if(board[x][y]=='.'):
                    new_board = board[0:row] + [board[row][0:col] + ['.',] + board[row][col+1:]] + board[row+1:]
                    if(opponent_x!=-1 and opponent_y!=-1):
                        new_board = new_board[0:opponent_x] + [new_board[opponent_x][0:opponent_y] + ['.',] + new_board[opponent_x][opponent_y+1:]] + new_board[opponent_x+1:]
                    if(player=="White" and x==N-1):
                        new_board = new_board[0:x] + [new_board[x][0:y] + [raichu_c,] + new_board[x][y+1:]] + new_board[x+1:]
                    elif(player=="Black" and x==0):
                        new_board = new_board[0:x] + [new_board[x][0:y] + [raichu_c,] + new_board[x][y+1:]] + new_board[x+1:]
                    else:
                        new_board = new_board[0:x] + [new_board[x][0:y] + [c,] + new_board[x][y+1:]] + new_board[x+1:]
                        #new_board = new_board[0:x] + [new_board[x][0:y] + [c,] + new_board[x][y+1:]] + new_board[x+1:]
                    moved_pikachu.append(new_board)
                    steps = steps-1
                elif(board[x][y] in can_kill and isallowed(N,x+dirx,y+diry) and board[x+dirx][y+diry]=='.' and total_kills==0):
                    opponent_x,opponent_y = x,y
                    total_kills = total_kills+1
                    x_prime = x+dirx
                    y_prime = y+diry
                    new_board = board[0:x] + [board[x][0:y] + ['.',] + board[x][y+1:]] + board[x+1:]
                    new_board = new_board[0:row] + [new_board[row][0:col] + ['.',] + new_board[row][col+1:]] + new_board[row+1:]

                    if(player=="White" and x_prime==N-1):
                        new_board = new_board[0:x_prime] + [new_board[x_prime][0:y_prime] + [raichu_c,] + new_board[x_prime][y_prime+1:]] + new_board[x_prime+1:]
                    elif(player=="Black" and x_prime==0):
                        new_board = new_board[0:x_prime] + [new_board[x_prime][0:y_prime] + [raichu_c,] + new_board[x_prime][y_prime+1:]] + new_board[x_prime+1:]
                    else:
                        new_board = new_board[0:x_prime] + [new_board[x_prime][0:y_prime] + [c,] + new_board[x_prime][y_prime+1:]] + new_board[x_prime+1:]
                        #new_board = new_board[0:x_prime] + [new_board[x_prime][0:y_prime] + [c,] + new_board[x_prime][y_prime+1:]] + new_board[x_prime+1:]
                        moved_pikachu.append(new_board)
                    steps = steps-1
                    x,y = x_prime,y_prime
                else:
                    steps = 0
                    break

    return moved_pikachu

def move_raichu(board,N,row,col,player="White"):
    #print(board)

    # print("In move_pikachu printing origional board")
    # print(board)

    moved_raichu = []

    if(player == "White"):
        c = '@'
        direction = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
        can_kill = ['b','B','$']
    else:
        c = '$'
        direction = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]
        can_kill = ['w','W','@']

    for dir in direction:
        x,y = row,col
        x_prev,y_prev = x,y
        dirx,diry = dir[0],dir[1]
        opponent_x,opponent_y = -1,-1
        total_kills = 0
        while(isallowed(N,x,y)):
            x_prev,y_prev = x,y
            x,y = x+dirx,y+diry
            if(isallowed(N,x,y)):
                if(board[x][y]=='.'):
                    new_board = board[0:row] + [board[row][0:col] + ['.',] + board[row][col+1:]] + board[row+1:]
                    if(opponent_x!=-1 and opponent_y!=-1):
                        new_board = new_board[0:opponent_x] + [new_board[opponent_x][0:opponent_y] + ['.',] + new_board[opponent_x][opponent_y+1:]] + new_board[opponent_x+1:]
                    new_board = new_board[0:x] + [new_board[x][0:y] + [c,] + new_board[x][y+1:]] + new_board[x+1:]
                    moved_raichu.append(new_board)
                elif(board[x][y] in can_kill and isallowed(N,x+dirx,y+diry) and board[x+dirx][y+diry]=='.' and total_kills==0):
                    opponent_x,opponent_y = x,y
                    total_kills = total_kills+1
                    x_prime = x+dirx
                    y_prime = y+diry
                    new_board = board[0:x] + [board[x][0:y] + ['.',] + board[x][y+1:]] + board[x+1:]
                    new_board = new_board[0:row] + [new_board[row][0:col] + ['.',] + new_board[row][col+1:]] + new_board[row+1:]
                    new_board = new_board[0:x_prime] + [new_board[x_prime][0:y_prime] + [c,] + new_board[x_prime][y_prime+1:]] + new_board[x_prime+1:]
                    moved_raichu.append(new_board)
                    x,y = x_prime,y_prime
                else:
                    break

    return moved_raichu

def get_successors(board,N,player,timelimit):
    #print("in succesors")
    successors = []

    if(player == "White"):
        for i in range(N):
            for j in range(N):
                if(board[i][j]=='@'):
                    for state in move_raichu(board,N,i,j):
                        successors += [state]
                if(board[i][j]=='W'):
                    for state in move_pikachu(board,N,i,j):
                        successors.append(state)
                if(board[i][j]=='w'):
                    for state in move_pichu(board,N,i,j):
                        successors.append(state)
    else:
        for i in range(N):
            for j in range(N):
                if(board[i][j]=='$'):
                    for state in move_raichu(board,N,i,j,"Black"):
                        successors.append(state)
                if(board[i][j]=='B'):
                    for state in move_pikachu(board,N,i,j,"Black"):
                        successors.append(state)
                if(board[i][j]=='b'):
                    for state in move_pichu(board,N,i,j,"Black"):
                        successors +=[state]
            
    return successors

def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #
    #print("In find best move")
    #print(player.lower())
    temp = to_matirx(board,N)

    best_board = temp

    while True:
        if(player.lower()=='w'):
            #print("1")
            next_board,next_score = minimax(temp,N,3,0,True,-sys.maxsize,sys.maxsize,timelimit,time.perf_counter(),best_board)
        else:
            #print("2")
            next_board,next_score = minimax(temp,N,3,0,False,-sys.maxsize,sys.maxsize,timelimit,time.perf_counter(),best_board)
        print(matrix_to_string(next_board,N))
        break
    yield matrix_to_string(next_board,N)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    
    # test_fucntion(board,N)

    for new_board in find_best_move(board, N, player, timelimit):
        #print(matrix_to_string(new_board,N))
        print(new_board)
