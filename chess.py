#/bin/tcsh
# -*- coding: utf-8 -*-
import time,os,sys
import random,copy

dict={
	1:"将",
	2:"士",
	3:"相",
	4:"马",
	5:"车",
	6:"包",
	7:"兵",
        8:"暗",
	-1:"帅",
	-2:"仕",
	-3:"象",
	-4:"馬",
	-5:"車",
	-6:"炮",
	-7:"卒",
        -8:"暗",
        0:"  ",
}

value_dict={
        1:10000,
	2:150,
	3:100,
	4:300,
	5:500,
	6:300,
	7:200,
        8:247,# (150*2+100*2+300*2+500*2++300*2+200*5)/15
        -1:-10000,
	-2:-150,
	-3:-100,
	-4:-300,
	-5:-500,
	-6:-300,
	-7:-200,
        -8:-247,
        0:0,
}

def evaluation(current):
    #update 8 and -8 value
    sum = 0
    cnt = 0
    for p in pos_pieces:
        sum += value_dict[p]
        cnt += 1
    value_dict[8] = sum/cnt
    sum = 0
    cnt = 0
    for p in neg_pieces:
        sum += value_dict[p]
        cnt += 1
    value_dict[-8] = sum/cnt
    # calculate state score
    cur_ret=0
    for i in range(10):
        for j in range(9):
            cur_ret+=value_dict[current[i][j]]
            if(current[i][j]==7): # pass river soilder + 50
	        if i-4.5>0:
                    cur_ret+=50
            if(current[i][j]==-7): # pass river soilder + 50
	        if i-4.5<0:
                    cur_ret-=50
    return cur_ret;

# find max self value
def choose_a_move_lv0(current, ismemove):
    mypawn=[]
    for i in range(10): 
        for j in range(9):
            if (ismemove*current[i][j]>0):
                mypawn.append((i,j)) 
    random.shuffle(mypawn);
    # move commander to the last, if not benifit, commander won't move
    for p in mypawn:
        if(abs(current[p[0]][p[1]]) == 1):
            mypawn.remove(p)
            mypawn.append(p)
            break
    max_value = -200000
    for piece in mypawn:
        (i,j)=piece
        next=moverule(current, piece)
        for (k, l) in next:
            cur_tmp = copy.deepcopy(current)
            cur_tmp[k][l]=cur_tmp[i][j]
            cur_tmp[i][j]=0
            cur_ret = evaluation(cur_tmp) * ismemove
            if cur_ret > max_value:
                next_step=(k,l)
                max_value = cur_ret
                from_i = i
                from_j = j
    return next_step, from_i, from_j, max_value

# find min opp value
def choose_a_move_lv1(current, ismemove):
    mypawn=[]
    for i in range(10): 
        for j in range(9):
            if (ismemove*current[i][j]>0):
                mypawn.append((i,j)) 
    random.shuffle(mypawn);
    # move commander to the last, if not benifit, commander won't move
    for p in mypawn:
        if(abs(current[p[0]][p[1]]) == 1):
            mypawn.remove(p)
            mypawn.append(p)
            break
    min_value = 200000
    for piece in mypawn:
        (i,j)=piece
        next=moverule(current, piece)
        for (k, l) in next:
            cur_tmp = copy.deepcopy(current)
            cur_tmp[k][l]=cur_tmp[i][j]
            cur_tmp[i][j]=0
            _, _, _, cur_ret = choose_a_move_lv0(cur_tmp, -1*ismemove)
            if cur_ret < min_value:
                next_step=(k,l)
                min_value = cur_ret
                from_i = i
                from_j = j
    return next_step, from_i, from_j , min_value

# find max self value of min opp value 
def choose_a_move_lv2(current, ismemove):
    mypawn=[]
    for i in range(10): 
        for j in range(9):
            if (ismemove*current[i][j]>0):
                mypawn.append((i,j)) 
    random.shuffle(mypawn);
    # move commander to the last, if not benifit, commander won't move
    for p in mypawn:
        if(abs(current[p[0]][p[1]]) == 1):
            mypawn.remove(p)
            mypawn.append(p)
            break
    # 1st move, no need cal
    for p in mypawn:
        if(abs(current[p[0]][p[1]]) not in [1, 8]):
            break
    else:
        return choose_a_move_lv0(current, ismemove)
    max_value = -200000
    for piece in mypawn:
        (i,j)=piece
        next=moverule(current, piece)
        for (k, l) in next:
            # kill commander
            if(abs(current[k][l])==1):
                next_step=(k,l)
                from_i = i
                from_j = j
                return next_step, from_i, from_j, max_value
            cur_tmp = copy.deepcopy(current)
            cur_tmp[k][l]=cur_tmp[i][j]
            cur_tmp[i][j]=0
            _, _, _, cur_ret = choose_a_move_lv1(cur_tmp, -1*ismemove)
            if cur_ret > max_value:
                next_step=(k,l)
                max_value = cur_ret
                from_i = i
                from_j = j
    return next_step, from_i, from_j, max_value


def human_input_a_move(current, ismemove):
    print "it is black ture, input 4 nums of a black piece\
 row from_col to_row to_col:"
    while(1):
        from_i = input("from_row: ")
        from_j = input("from_col: ")
        to_i = input("to_row: ")
        to_j = input("to_col: ")
        next_step = (to_i, to_j)
        next = moverule(current, (from_i, from_j))
        if next_step in next and ismemove * current[from_i][from_j] > 0:
            break
        else:
            print "invalid input, try again...\n"
    return next_step, from_i, from_j

current=[[0]*9 for j in range(10)]

pos_pieces = [2, 3, 4, 5, 6]*2 + [7] * 5
neg_pieces = [-2, -3, -4, -5, -6]*2 + [-7] * 5
random.shuffle(pos_pieces)
random.shuffle(neg_pieces)

def init(current, jieqi):
    if jieqi:
        total_chesspieces_positive = [8] * 15
        total_chesspieces_negtive =  [-8] * 15 
    else:
        # random all pieces except 1
        total_chesspieces_positive = [2, 3, 4, 5, 6]*2 + [7] * 5;
        total_chesspieces_negtive = [-2, -3, -4, -5, -6]*2 + [-7] * 5;
        random.shuffle(total_chesspieces_positive);
        random.shuffle(total_chesspieces_negtive);
    # add 1 and -1 in 5 of the list
    total_chesspieces_positive.insert(4, 1);
    total_chesspieces_negtive.insert(4, -1);
    # place all pieces
    for i in range(9):    
        current[0][i]=total_chesspieces_positive[i]
        current[9][i]=total_chesspieces_negtive[i]
        
    current[2][1]=total_chesspieces_positive[9]
    current[2][7]=total_chesspieces_positive[10]
    
    current[7][1]=total_chesspieces_negtive[9]
    current[7][7]=total_chesspieces_negtive[10]

    for i in range(0,9,2):
        current[3][i]=total_chesspieces_positive[11+i/2]
        current[6][i]=total_chesspieces_negtive[11+i/2]

def print_chess(current,now=(0,0),blink=False):
    #os.system("clear")
    for i in range(10):
        if i==5:
            print "\n"+"-"*35
        for j in range(9):
            index_i=9-i     
            character=dict[current[index_i][j]]
            if blink and (index_i,j)==now:
                bb=5
            else:
                bb=1
            if current[index_i][j]>0:
                color="31"
            else:
                color="30"
            #print "\033[%d;%sm;47 %s\033[0m|" % (bb,color,character),
            print "\033[%d;%sm%s\033[0m|" % (bb,color,character), 
        print str(9-i),
        print "\n"+"-"*35
    str_num = ""
    for j in range(9):
        str_num += str(j)
        str_num += " | "
    print str_num
    print "~"*35
#now=(0,0)
#next=[(),(),(),()]

def moverule(current,now):
    i,j=now
    index=abs(current[i][j])

    next=[]
    if index==8: # 暗
        if((i, j) == (0, 3) or
	    (i, j) == (0, 5) or
	    (i, j) == (9, 3) or
	    (i, j) == (9, 5)): # 士
	    index = 2;
        if((i, j) == (0, 2) or
	    (i, j) == (0, 6) or
	    (i, j) == (9, 2) or
	    (i, j) == (9, 6)): # 象
	    index = 3;
        if((i, j) == (0, 1) or
	    (i, j) == (0, 7) or
	    (i, j) == (9, 1) or
	    (i, j) == (9, 7)): # 马
	    index = 4;
	if((i, j) == (0, 0) or
	    (i, j) == (0, 8) or
	    (i, j) == (9, 0) or
	    (i, j) == (9, 8)): # 车
	    index = 5;
	if((i, j) == (2, 1) or
	    (i, j) == (2, 7) or
	    (i, j) == (7, 1) or
	    (i, j) == (7, 7)): # 炮
	    index = 6;
	if((i == 3 or i == 6) and j%2 == 0): # 兵
	    index = 7;
    if index==1: # 将
        next=[(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
        for k,l in copy.deepcopy(next):
            if k not in(0,1,2,7,8,9) or l not in (3,4,5):
                next.remove((k,l))
        start={1:[0,1,2],-1:[7,8,9]}
        mystart=start[current[i][j]]
        enemystart=start[-current[i][j]]

        enemy_i=-10
        for k in enemystart:
              if current[k][j]==-current[i][j]:
                  enemy_i=k
        nums=0
        for k in range(min(i,enemy_i)+1,max(i,enemy_i)): 
            if (enemy_i!=-10 and current[k][j]!=0):    
                nums+=1
        if nums==0 and enemy_i!=-10:
            next.append((enemy_i,j))
                

    if index==2: # 士
        next=[(i-1,j-1),(i+1,j-1),(i-1,j+1),(i+1,j+1)]
        for k,l in copy.deepcopy(next):
            #jieqi enlarge the moving scope
            if k<0 or k>9 or l<0 or l>8 or ((abs(current[i][j])==8) and (l<3 or l>5)):
                next.remove((k,l))
    if index==3: # 象
        next=[(i-2,j-2),(i+2,j-2),(i-2,j+2),(i+2,j+2)]
        for k,l in copy.deepcopy(next):
            #jieqi enlarge the moving scope
            if k<0 or k>9 or l<0 or l>8 :
                next.remove((k,l))      
        for k,l in copy.deepcopy(next):
            if current[(i+k)/2][(j+l)/2]!=0:
                next.remove((k,l))
    if index==4: # 马
        next=[(i-2,j+1),(i-2,j-1),(i-1,j+2),(i-1,j-2),(i+2,j-1),(i+2,j+1),(i+1,j+2),(i+1,j-2)] 
        for k,l in copy.deepcopy(next):
            if k<0 or k>9 or l<0 or l>8 :
                next.remove((k,l))
        for k,l in copy.deepcopy(next):
            biejiao_i=(i if abs(k-i)==1 else (i+k)/2 )
            biejiao_j=(j if abs(l-j)==1 else (j+l)/2)
            if current[biejiao_i][biejiao_j]!=0:
                next.remove((k,l))

    if index==5 or index==6:
        for k,l in [(k,j) for k in range(10)]+[(i,k) for k in range(9)]:
            if (k,l)==(i,j):
                continue
            nums=0
            for (k_try,l_try) in [(i,l_try) for l_try in range(min(j,l)+1,max(j,l))]+[(k_try,j) for k_try in range(min(i,k)+1,max(i,k))]: 
                if current[k_try][l_try]!=0:
                    nums+=1

            if index==5 and nums==0: # 车
                next.append((k,l))
            if index==6: # 炮
                if (current[k][l]==0  and nums==0) or ( current[k][l]!=0 and nums==1 ):
                    next.append((k,l))
               

    if index==7: # 兵
        value=current[i][j]/abs(current[i][j])
	if value*(i-4.5)<0:
            next=[(i+value,j)]
        else:
            next=[(i+value,j),(i,j-1),(i,j+1)]
            for k,l in copy.deepcopy(next):
                if k<0 or k>9 or l<0 or l>8 :
                    next.remove((k,l))
    for k,l in copy.deepcopy(next):    
        if(current[i][j]*current[k][l]>0):
            next.remove((k,l))
    # add 2 commanders face to face judgement
    for k,l in copy.deepcopy(next):
        cur_tmp = copy.deepcopy(current)
        cur_tmp[k][l]=cur_tmp[i][j]
        cur_tmp[i][j]=0
        neg_commander = (0,0)
        pos_commander = (0,0)
        for row in range(10):
            for col in range(9):
                if(cur_tmp[row][col] == 1):
                    pos_commander = (row, col)
                if(cur_tmp[row][col] == -1):
                    neg_commander = (row, col)

        if(neg_commander[1] == pos_commander[1]):
            for row in range(pos_commander[0], neg_commander[0]):
                if(abs(current[row][pos_commander[1]]) > 1):
                    break
            else:
                next.remove((k,l))
    random.shuffle(next)
    return next

# if ismemove=1 then me move,
# if ismemove=-1 then rival move
def do_move(current,ismemove):
    from_i = 0
    from_j = 0
    next_step = (0, 0)
    if(ismemove == -1):
        # next_step, from_i, from_j = human_input_a_move(current, ismemove)
        next_step, from_i, from_j, score = choose_a_move_lv2(current, ismemove)
    else:
        next_step, from_i, from_j, score = choose_a_move_lv1(current, ismemove)
    (k,l)=next_step

    os.system("clear")
    print_chess(current,(from_i,from_j),True)
    # give 8 piece a read number in jieqi
    if(abs(current[from_i][from_j]) == 8):
        if(ismemove == 1):
	    current[from_i][from_j] = pos_pieces.pop(0)
	else:
	    current[from_i][from_j] = neg_pieces.pop(0)

    current[k][l]=current[from_i][from_j]
    current[from_i][from_j]=0
    time.sleep(3)
    os.system("clear")
    print_chess(current)
    # time.sleep(3)
    return

def gameover(current):
    isover=0
    redwin=0
    blackwin=0
    for i in range(10): 
        for j in range(9):
            if current[i][j]==1:
                isover+=1 
                redwin=1
            if current[i][j]==-1:
                isover+=1
                blackwin=1 
    if isover!=2 and redwin:
        print "RED Wins!!!!"
    if isover!=2 and blackwin:
        print "BLACK Wins!!!"
    return isover!=2 

jieqi = 1
init(current, jieqi)
ismemove=1
while(not gameover(current)):
    #print_chess(current)
    #time.sleep(1)
    do_move(current,ismemove)
    ismemove=-1*ismemove
