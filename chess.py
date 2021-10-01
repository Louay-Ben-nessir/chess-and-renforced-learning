import pygame
pygame.init()
#colour 
light = (112,102,119)#(112,102,119)
dark  = (200,183,174)#(204,183,174)
STARTER_ARRANGMENT='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'




def fen_to_list(fen_string):
        #https://www.chess.com/terms/fen-chess  
        fen_string=fen_string.split(' ')
        positions=[ list( ''.join( [' '*int(char) if ord(char) in range(48,58) else char for char in line] )) for line in fen_string[0].split('/')] 
        settings=[int(fen_string[1].lower()=='b'),fen_string[2],fen_string[3]]
        return positions,settings
    
def in_bound(move):
    return 0<=move[0]<8 and 0<=move[1]<8


    

class Pice:
    def __init__(self,postion,Pice_info):
        self.postion=(postion[0],postion[1])
        self.type_and_clour=Pice_info
        self.colour='w' if Pice_info.isupper() else 'b'
        
    def check_possible_move(self,board):

        if self==None: return [] # cant move an empty space
    
        if self.type_and_clour.lower()=='p':#pawn move set
            is_black=int(self.type_and_clour.islower())
            move_lenght= 1 + (int(self.postion[0]==1) if is_black else int(self.postion[0]==6)  )#2 or 1 if on the starting line or not 
            possible_moves=[ (self.postion[0]-1+2*is_black,self.postion[1]+ind)  #check for side selfs
                            for ind in range(-1,2,2) 
                            if in_bound((self.postion[0]-1+2*is_black,self.postion[1]+ind) )
                            and( (board.pice_placement[self.postion[0]-1+2*is_black][self.postion[1]+ind]!=None #not empty 
                            and board.pice_placement[self.postion[0]-1+2*is_black][self.postion[1]+ind].type_and_clour.isupper()!=self.type_and_clour.isupper() )#has an enemy self ;-;
                            or (self.postion[0]-1+2*is_black,self.postion[1]+ind)==board.special_enpassent)
                           ]# IF IT'S IN BOUND and (has an eney self or is an enpassent location)
            pawn_moves_offest=[(1,0)] if is_black else [(-1,0)]
            possible_moves+=self.line_move(pawn_moves_offest,board,move_lenght+1)
                
                
        if self.type_and_clour.lower()=='n':   #THE KNIGHT MOVE SET 
            horse_moves_offset=[(-2,1),(-2,-1),(-1,2),(-1,-2),(2,1),(2,-1),(1,2),(1,-2)]
            possible_moves=self.non_linear_move(horse_moves_offset,board)
            
        if self.type_and_clour.lower()=='r':
            rook_moves_offset=[(-1,0),(1,0),(0,1),(0,-1)]
            possible_moves=self.line_move(rook_moves_offset,board)
            
                    
        if self.type_and_clour.lower()=='b':
            bishop_moves_offset=[(1,1),(-1,1),(1,-1),(-1,-1)]
            possible_moves=self.line_move(bishop_moves_offset,board)
            
        if self.type_and_clour.lower()=='q':
            queen_moves_offest=[(1,1),(-1,1),(1,-1),(-1,-1),(-1,0),(1,0),(0,1),(0,-1)]
            possible_moves=self.line_move(queen_moves_offest,board)
        
        if self.type_and_clour.lower()=='k':
            King_moves_offset=[(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
            possible_moves=set(self.non_linear_move(King_moves_offset,board))
            if self.colour=='w':possible_moves=list(possible_moves-set(board.black_controlled_squares))
            else:possible_moves=list(possible_moves-set(board.white_controlled_squares))
    
        return possible_moves
    
    def line_move(self,move_set_offest,board,max_len=8):
            possible_moves=[]
            for move in move_set_offest:
                for i in range(1,max_len):
                    offset=(move[0]*i,move[1]*i)
                    if in_bound((self.postion[0]+offset[0],self.postion[1]+offset[1]) ): 
                        if board.pice_placement[self.postion[0]+offset[0]][self.postion[1]+offset[1]]==None:
                            possible_moves.append((self.postion[0]+offset[0],self.postion[1]+offset[1]))
                        elif board.pice_placement[self.postion[0]+offset[0]][self.postion[1]+offset[1]].type_and_clour.isupper() != self.type_and_clour.isupper():
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
                            or board.pice_placement[self.postion[0]+offset[0]][self.postion[1]+offset[1]].type_and_clour.isupper()!=self.type_and_clour.isupper() #not the same colour
                                ) 
                            ]
            
        
        
        
        
class Board:
    def __init__(self,Board_state,settings):
        self.Board_state = Board_state # keeping it to print the board on demand
        self.pice_placement= [[Pice([row,coloum],Board_state[row][coloum]) if Board_state[row][coloum]!=' ' else None for coloum in range(8)] for row in range(8) ]#placement of pices on the board Aa empty to make it nutral to isupper and islower
        self.playing_colour = settings[0]
        self.special_casteling_rights = [int(i in settings[1]) for i in ['K','Q','k','q'] ] # casteling rights in oreder 
        self.special_enpassent = (9,9) if settings[2]=='-' else (int(settings[2][1])-1,int(settings[2][0],18)-10) # math tp convet base18 ( a to h) to base10 and in range 0-7
        for pice in sum(self.pice_placement,[]):
            if pice!=None and pice.type_and_clour=='k':self.black_king=pice
            elif pice!=None and pice.type_and_clour=='K':self.white_king=pice
  


    def update(self):
        self.white_controlled_squares=[]
        self.black_controlled_squares=[]
        for row in  self.pice_placement:
            for pice in row:
                if pice!=None and pice.type_and_clour.lower()!='k':
                    if pice.colour=='w':self.white_controlled_squares+=pice.check_possible_move(self)
                    else:self.black_controlled_squares+=pice.check_possible_move(self)

        self.white_controlled_squares+=self.white_king.check_possible_move(self)
        self.black_controlled_squares+=self.black_king.check_possible_move(self)

        
                
        
    def MAKE_DRAWABLE(self,BOARD_SIZE=600):
        self.display=pygame.display.set_mode((BOARD_SIZE,BOARD_SIZE))
        self.pices_sptie=pygame.image.load('ChessPiecesArray.png').convert_alpha()

    def Draw_Current_placment(self,BOARD_SIZE=600):
        BOARD_SIZE=BOARD_SIZE
        pices_ord_in_sptie={'q':0,'k':1,'r':2,'n':3,'b':4,'p':5}
        pice_szie=60
        scale=BOARD_SIZE//8
        OFFSET_TO_CENTER=(scale-pice_szie)//2
        for rows in range(8):#--------------------- draw the board
            for coloum in range(8):
                squar_colour=dark if (rows%2==coloum%2) else light
                squar_colour=(squar_colour[0]+int( (coloum,rows) in self.black_controlled_squares)*50,squar_colour[1]+int( (coloum,rows) in self.white_controlled_squares)*50,squar_colour[2])
                pygame.draw.rect(self.display,squar_colour , pygame.Rect(rows*scale, coloum*scale, scale,scale )  )
                pice_or_space=self.Board_state[rows][coloum].lower()#+int( (coloum,rows) in self.white_controlled_squares)*50

        for rows in range(8):#--------------------- draw the pices 
            for coloum in range(8):
                pice_or_space=self.Board_state[rows][coloum].lower()
                if pice_or_space!=' ':
                    self.display.blit(self.pices_sptie, (coloum*scale+OFFSET_TO_CENTER,  rows*scale+OFFSET_TO_CENTER), (pices_ord_in_sptie[pice_or_space]*pice_szie,(pice_or_space!=self.Board_state[rows][coloum])*pice_szie,pice_szie,pice_szie))
        
        pygame.display.update() 
        
        
    def move_pice(self,position,destination):
        ypos,xpos=[int(i) for i in list(position)]
        yDest,xDest=[int(i) for i in list(destination)]
        leagl_move=False      

        if self.pice_placement[ypos][xpos]!=None:leagl_move=(yDest,xDest) in self.pice_placement[ypos][xpos].check_possible_move(self) 
        #casteling----------------------------------------------------------------------------------
        if self.pice_placement[ypos][xpos]!=None and self.pice_placement[ypos][xpos].type_and_clour.lower()=='k' and (yDest,xDest) in [(7,6),(7,2),(0,6),(0,2)]: #casteling move
            KoQs=-1 if xDest==6 else 1#king or queen side -1 if king 
            if self.pice_placement[ypos][xpos-1*KoQs]==self.pice_placement[ypos][xpos-2*KoQs]==None and ((self.special_casteling_rights[1*xDest==2] and self.pice_placement[ypos][xpos].colour=='w') or (self.special_casteling_rights[3-1*xDest==2] and self.pice_placement[ypos][xpos].colour=='b')):
                
                    self.Board_state[yDest][xDest],self.Board_state[ypos][xpos-1*KoQs]=self.Board_state[ypos][xpos],self.Board_state[yDest][xDest-(1+int(xDest==2))*KoQs]#drawing board rook king swithc
                    self.pice_placement[yDest][xDest],self.pice_placement[ypos][xpos-1*KoQs]=self.pice_placement[ypos][xpos],self.pice_placement[yDest][xDest-(1+int(xDest==2))*KoQs]#switch king and rook
                    self.pice_placement[yDest][xDest].postion,self.pice_placement[ypos][xpos-1*KoQs].postion=(ypos,xpos),(yDest,xDest-(1+int(xDest==2))*KoQs)
                    
                    self.pice_placement[ypos][xpos],self.Board_state[ypos][xpos]=None,' ' #clearing old king and rook places
                    self.pice_placement[ypos][xpos-(3+int(xDest==2))*KoQs],self.Board_state[ypos][xpos-(3+int(xDest==2))*KoQs]=None,' ' #clearing old king and rook places
                    print(ypos,3+int(xDest==2))
                    #xpos-3*KoQs IS THE ROOKS POSTION from king xDest==6 and xpos-4*KoQs if for queen so we add int(xDest==2)
                                      
            if self.pice_placement[yDest][xDest].colour=='w': # reset the flags since a move has been done
                self.special_casteling_rights[0],self.special_casteling_rights[2]=0,0
            else:
                self.special_casteling_rights[1],self.special_casteling_rights[3]=0,0
        #-------------------------------------------------------------------------------------------------------------------------------
        
        elif leagl_move and self.check_for_check(yDest,xDest,ypos,xpos):#do the taking and or the moving and updating of Board_state and pice_placement   
            self.Board_state[yDest][xDest],self.Board_state[ypos][xpos]=self.Board_state[ypos][xpos],' '
            self.pice_placement[yDest][xDest]=self.pice_placement[ypos][xpos]
            self.pice_placement[yDest][xDest].postion=(yDest,xDest)
            self.pice_placement[ypos][xpos]=None
            
            #enpassent
            is_black=int(self.pice_placement[yDest][xDest].type_and_clour.islower())
            if self.pice_placement[yDest][xDest].type_and_clour.lower()=='p' and (yDest,xDest)==self.special_enpassent: # take pice during an enpassent
                    self.Board_state[yDest+1-2*is_black][xDest]= ' '
                    self.pice_placement[yDest+1-2*is_black][xDest]=None
                    
            self.special_enpassent=(9,9) #reset the enpassent after a signle move 
            #set 
            if self.pice_placement[yDest][xDest].type_and_clour.lower()=='p' and abs(yDest-ypos)==2:# set the enpassent falg
                    self.special_enpassent=(yDest+1-2*is_black,xDest)
            
            
            #check for casteling flags
            self.special_casteling_rights=[ int( (ypos,xpos)!=roock_postions and old_flags ) for roock_postions,old_flags in zip([(7,7),(7,0),(0,7),(0,0)],self.special_casteling_rights)]# if rook moves 
            if self.pice_placement[yDest][xDest].type_and_clour=='K':
                self.special_casteling_rights[0],self.special_casteling_rights[2]=0,0
            if self.pice_placement[yDest][xDest].type_and_clour=='k':
                self.special_casteling_rights[1],self.special_casteling_rights[3]=0,0
                
            self.playing_colour=int(not self.playing_colour)
            self.end_game()
            
    def check_for_check(self,yDest,xDest,ypos,xpos):
        #-------if a player plays and their king is still at check after then that's a false move ----------------------- temp do the move
        saved_Board = self.backup()
        self.pice_placement[yDest][xDest]=self.pice_placement[ypos][xpos]
        self.pice_placement[ypos][xpos]=None
        self.update()
        check_check_passed = ( (self.playing_colour == 0) and (self.white_king.postion not in self.black_controlled_squares)) or ((self.playing_colour == 1) and (self.black_king.postion not in self.white_controlled_squares))
        self.restaur(saved_Board)
        return check_check_passed
    
    
    def backup(self):
        return ([i.copy() for i in self.pice_placement] ,self.white_controlled_squares.copy(),self.black_controlled_squares.copy())
    def restaur(self,backup):
        self.pice_placement=backup[0]
        self.white_controlled_squares=backup[1]
        self.black_controlled_squares=backup[2]
        
    def end_game(self):
        self.update()
        back_up=self.backup()
        if self.white_king.postion in self.black_controlled_squares:
            for y,x in self.white_controlled_squares:
                self.pice_placement[y][x]=Pice([y,x],'p')
            self.update()
            if self.white_king.postion in self.black_controlled_squares:print('BLACK WON')
            
        if self.black_king.postion in self.white_controlled_squares:
            for y,x in self.black_controlled_squares:
                self.pice_placement[y][x]=Pice([y,x],'P')
            self.update()
            if self.black_king.postion in self.white_controlled_squares:print('white WON')
        self.restaur(back_up)
        
    
                
            
            
            

def ChessGame(state=STARTER_ARRANGMENT):
    postions,setting=fen_to_list(state)
    BOARD=Board(postions,setting)
    BOARD.update()
    BOARD.MAKE_DRAWABLE()
    BOARD.Draw_Current_placment() 
    while True:
        move='56 76'.split(' ')#input().split(' ')
        if len(move)!=2:break
        BOARD.move_pice(move[0],move[1]) 
        BOARD.update()
        BOARD.Draw_Current_placment() 
        break
    pygame.quit() 
#DWON AND ACOSS
    

if __name__ == '__main__':
    ChessGame('K7/8/8/8/8/6R1/7R/k7 w - - 0 1')
    
#'K7/8/8/8/8/6R1/7R/k7 w - - 0 1'
#    for i in BOARD.pice_placement:
#        l=''
#        for j in i:
#            try :
#                l+=j.type_and_clour
#            except:
#                l+= ' '
#        print(l)
#1nbqkbn1/pppppppp/3r1r2/8/8/4K3/8/2BQ1BNR w - - 0 1