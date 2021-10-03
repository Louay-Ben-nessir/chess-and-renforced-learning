import pygame
from Pices import Pice
pygame.init()
#colour 
light = (112,102,119)#(112,102,119)
dark  = (200,183,174)#(204,183,174)

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
        self.update()
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
                    self.pice_placement[yDest][xDest].postion,self.pice_placement[ypos][xpos-1*KoQs].postion=(ypos,xpos),(yDest,xDest+(1+int(xDest==2))*KoQs)
                    
                    self.pice_placement[ypos][xpos],self.Board_state[ypos][xpos]=None,' ' #clearing old king and rook places
                    self.pice_placement[ypos][xpos-(3+int(xDest==2))*KoQs],self.Board_state[ypos][xpos-(3+int(xDest==2))*KoQs]=None,' ' #clearing old king and rook places

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
            is_black=int(self.pice_placement[yDest][xDest].colour=='b')
            if self.pice_placement[yDest][xDest].type_and_clour.lower()=='p' and (yDest,xDest)==self.special_enpassent: # take pice during an enpassent
                    self.Board_state[yDest+1-2*is_black][xDest]= ' '
                    self.pice_placement[yDest+1-2*is_black][xDest]=None
                    
            self.special_enpassent=(9,9) #reset the enpassent after a single move
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
            
            
    def check_for_check(self,yDest,xDest,ypos,xpos):
        #-------if a player plays and their king is still at check after then that's a false move ----------------------- temp do the move

        saved_Board = self.backup()
        self.pice_placement[yDest][xDest]=self.pice_placement[ypos][xpos]
        self.pice_placement[yDest][xDest].postion=(yDest,xDest)
        self.pice_placement[ypos][xpos]=None
        #enpassent
        is_black=int(self.pice_placement[yDest][xDest].colour=='b')
        if self.pice_placement[yDest][xDest].type_and_clour.lower()=='p' and (yDest,xDest)==self.special_enpassent:self.pice_placement[yDest+1-2*is_black][xDest]=None # take pice during an enpassent           
        self.update()
        check_check_passed = ((self.playing_colour == 0) and (self.white_king.postion not in self.black_controlled_squares)) or ((self.playing_colour == 1) and (self.black_king.postion not in self.white_controlled_squares))
        self.restaur(saved_Board)
        return check_check_passed
    
    
    def backup(self):
        return ([i.copy() for i in self.pice_placement] ,self.white_controlled_squares.copy(),self.black_controlled_squares.copy())
    
    def restaur(self,backup):
        self.pice_placement=backup[0]
        self.white_controlled_squares=backup[1]
        self.black_controlled_squares=backup[2]
        
    def end_game_check(self):
        back_up=self.backup()
        if self.white_king.postion in self.black_controlled_squares:
            for y,x in self.white_controlled_squares:
                self.pice_placement[y][x]=Pice([y,x],'p')
            self.update()
            if self.white_king.postion in self.black_controlled_squares:return 'b'
            
        if self.black_king.postion in self.white_controlled_squares:
            for y,x in self.black_controlled_squares:
                self.pice_placement[y][x]=Pice([y,x],'P')
            self.update()
            if self.black_king.postion in self.white_controlled_squares:return 'w'
        self.restaur(back_up)
    
    def to_fen(self):
        fen_string=''
        for row in self.Board_state:
            row_fen_string=''
            coloum=0
            while coloum<=7:  
                if row[coloum]==' ':
                    space_count=1
                    while coloum <=6 and row[coloum+1]==' ':
                        space_count+=1
                        coloum+=1
                    coloum+=1
                    row_fen_string+=str(space_count)
                else:
                    row_fen_string+=row[coloum]
                    coloum+=1
                        
                
            fen_string+=row_fen_string+'/'

            
        fen_string=fen_string[:-1]+' '
        fen_string+='w' if self.playing_colour==0 else 'b'
        fen_string+=' '+'K'*self.special_casteling_rights[0]+'Q'*self.special_casteling_rights[1]+ 'k'*self.special_casteling_rights[2]+'q'*self.special_casteling_rights[3]+' ' if any(self.special_casteling_rights) else ' - ' 
        fen_string+= chr(ord('a')+self.special_enpassent[1])+str(self.special_enpassent[0]) if self.special_enpassent!=(9,9) else '-'
        fen_string+=' 0 1'
        
        return fen_string
                
        
