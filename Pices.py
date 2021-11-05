from itertools import product

def in_bound(move):
    return 0<=move[0]<8 and 0<=move[1]<8

class Pice:
    def __init__(self,postion,Pice_info):
        self.postion=(postion[0],postion[1])
        self.type_and_clour=Pice_info
        self.colour='w' if Pice_info.isupper() else 'b'
        
    def check_possible_move(self,board,not_update_call=True):

        if self==None: return [] # cant move an empty space
    
        if self.type_and_clour.lower()=='p':#pawn move set
            is_black=(self.colour=='b')
            move_lenght= 1 + (int(self.postion[0]==1) if is_black else int(self.postion[0]==6)  )#2 or 1 if on the starting line or not 
            possible_moves=[ (self.postion[0]-1+2*is_black,self.postion[1]+ind)  #check for side selfs
                            for ind in range(-1,2,2) 
                            if in_bound((self.postion[0]-1+2*is_black,self.postion[1]+ind) )
                            and( (board.pice_placement[self.postion[0]-1+2*is_black][self.postion[1]+ind]!=None #not empty 
                            and board.pice_placement[self.postion[0]-1+2*is_black][self.postion[1]+ind].colour!=self.colour )#has an enemy self ;-;
                            or (self.postion[0]-1+2*is_black,self.postion[1]+ind)==board.special_enpassent)
                           ]# IF IT'S IN BOUND and (has an eney self or is an enpassent location)
            
            if not_update_call: possible_moves+=[ (self.postion[0]-ind+2*ind*is_black,self.postion[1])  # check for 2 or 1 blocks to the front  # pawn can eat it's fron squares 
                            for ind in range(1,move_lenght+1) 
                            if in_bound((self.postion[0]-ind+2*ind*is_black,self.postion[1]) )
                            and board.pice_placement[self.postion[0]-ind+2*ind*is_black][self.postion[1]]==None ]# empty
                
                
        elif self.type_and_clour.lower()=='n':   
            horse_moves_offset=[(-2,1),(-2,-1),(-1,2),(-1,-2),(2,1),(2,-1),(1,2),(1,-2)]
            possible_moves=self.non_linear_move(horse_moves_offset,board)
            
        elif self.type_and_clour.lower()=='r':
            rook_moves_offset=[(-1,0),(1,0),(0,1),(0,-1)]
            possible_moves=self.line_move(rook_moves_offset,board)
                    
        elif self.type_and_clour.lower()=='b':
            bishop_moves_offset=[(1,1),(-1,1),(1,-1),(-1,-1)]
            possible_moves=self.line_move(bishop_moves_offset,board)
            
        elif self.type_and_clour.lower()=='q':
            queen_moves_offest=[(1,1),(-1,1),(1,-1),(-1,-1),(-1,0),(1,0),(0,1),(0,-1)]
            possible_moves=self.line_move(queen_moves_offest,board)
        
        elif self.type_and_clour.lower()=='k':
            King_moves_offset=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            possible_moves=set(self.non_linear_move(King_moves_offset,board))
            if self.colour=='w':possible_moves=list(possible_moves-set(board.black_controlled_squares))
            else:possible_moves=list(possible_moves-set(board.white_controlled_squares))
    
        return possible_moves
    #THEY CAN BE COMBIND DAWGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGG
    def line_move(self,move_set_offest,board):
            possible_moves=[]
            for move in move_set_offest:
                for i in range(1,8):
                    offset=(move[0]*i,move[1]*i)
                    if in_bound((self.postion[0]+offset[0],self.postion[1]+offset[1]) ): 
                        if board.pice_placement[self.postion[0]+offset[0]][self.postion[1]+offset[1]]==None:
                            possible_moves.append((self.postion[0]+offset[0],self.postion[1]+offset[1]))
                        elif board.pice_placement[self.postion[0]+offset[0]][self.postion[1]+offset[1]].colour != self.colour:
                            possible_moves.append((self.postion[0]+offset[0],self.postion[1]+offset[1]))
                            break
                        else:break
                    else:break
            return(possible_moves)
        
    def non_linear_move(self,move_set_offest,board):
        return [ (self.postion[0]+offset[0],self.postion[1]+offset[1])
                            for offset in move_set_offest
                            if in_bound((self.postion[0]+offset[0],self.postion[1]+offset[1]))
                            and (board.pice_placement[self.postion[0]+offset[0]][self.postion[1]+offset[1]]==None # empty
                            or board.pice_placement[self.postion[0]+offset[0]][self.postion[1]+offset[1]].colour!=self.colour #not the same colour
                                ) 
                            ]



                
            

    