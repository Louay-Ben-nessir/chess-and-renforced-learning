from Board import Board
from stockfish import Stockfish
import time
STARTER_ARRANGMENT='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'




def fen_to_list(fen_string):
        #https://www.chess.com/terms/fen-chess  
        fen_string=fen_string.split(' ')
        positions=[ list( ''.join( [' '*int(char) if ord(char) in range(48,58) else char for char in line] )) for line in fen_string[0].split('/')] 
        settings=[int(fen_string[1].lower()=='b'),fen_string[2],fen_string[3]]
        return positions,settings

    





def ChessGame(l,state=STARTER_ARRANGMENT):
    postions,setting=fen_to_list(state)
    BOARD=Board(postions,setting)
    BOARD.update()
    BOARD.MAKE_DRAWABLE()
    BOARD.Draw_Current_placment() 
    stockfish = Stockfish("stockfish",parameters={"Skill Level": 5})
    conv_move=['7','6','5','4','3','2','1','0']

    for i in range(l):
        time.sleep(.05)
        stockfish.set_fen_position(BOARD.to_fen())
        move=stockfish.get_best_move()
        print(conv_move[(int(move[1])-1)]+str(int(move[0],18)-10),conv_move[(int(move[3])-1)]+str(int(move[2],18)-10),BOARD.to_fen())
        BOARD.move_pice(conv_move[(int(move[1])-1)]+str(int(move[0],18)-10),conv_move[(int(move[3])-1)]+str(int(move[2],18)-10))
        
        BOARD.Draw_Current_placment() 
    print(BOARD.end_game_check())
    print(BOARD.to_fen())
    return BOARD
if __name__ == '__main__':
    #l1=ChessGame(8,'rn1q1k1r/1bp2pp1/p3p2p/1p1nP3/2pPN1Q1/2P5/P2BBPPP/R3K2R w Kk - 0 1')
    #print('======================')
    #l1=ChessGame(8,'rn1q1k1r/1bp2pp1/p3p2p/1p1nP3/2pPN1Q1/2P5/P2BBPPP/R4RK1 w - - 0 1')
    l2=ChessGame(200)#,'8/1R6/3p2k1/3B1p1p/1B1P1K1P/8/P5P1/8 w - - 0 1')
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