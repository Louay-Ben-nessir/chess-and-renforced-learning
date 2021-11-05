from Board import Board
from stockfish import Stockfish
import time
STARTER_ARRANGMENT='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'




def fen_to_list(fen_string): 
        fen_string=fen_string.split(' ')
        positions=[ list( ''.join( [' '*int(char) if ord(char) in range(48,58) else char for char in line] )) for line in fen_string[0].split('/')] 
        settings=[int(fen_string[1].lower()=='b'),fen_string[2],fen_string[3]]
        return positions,settings

    

def ChessGame(l,state=STARTER_ARRANGMENT,loyl=True):
    postions,setting=fen_to_list(state)
    BOARD=Board(postions,setting)
    BOARD.update()
    stockfish = Stockfish("stockfish",parameters={"Skill Level": 15})
    conv_move=['7','6','5','4','3','2','1','0']
    old_fen=BOARD.to_fen()
    for i in range(l):
        stockfish.set_fen_position(BOARD.to_fen())
        move=stockfish.get_best_move()
        if move==None:break
        BOARD.update()
        BOARD.move_pice(conv_move[(int(move[1])-1)]+str(int(move[0],18)-10),conv_move[(int(move[3])-1)]+str(int(move[2],18)-10))
    return BOARD



if __name__ == '__main__':
    l=ChessGame(100)
