#application data
TITLE = 'Lotus'
DEFAULT_WINDOW_WIDTH = 3200
DEFAULT_WINDOW_HEIGHT = 1800
window_width = DEFAULT_WINDOW_WIDTH
window_height = DEFAULT_WINDOW_HEIGHT
DEFAULT_WINDOW_SIZE = (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

#time constants
H_MS = 1000*60*60
M_MS = 1000*60
S_MS = 1000


#style settings
title_font = 'logo.ttf'
text_font = 'arial.ttf'
SCRAMBLE_SIZE = 100
text_color = (183, 183, 183)
background_color = (51, 51, 51)
border_color = text_color
box_fill_color = (38, 38, 38) #(45, 45, 50)
logo = 'lotus.png'
button_img_gap = 5

#scramble settings
R_MOVES = ("R","R'","R2")
U_MOVES = ("U","U'","U2")
F_MOVES = ("F","F'","F2")
L_MOVES = ("L","L'","L2")
D_MOVES = ("D","D'","D2")
B_MOVES = ("B","B'","B2")
Rw_MOVES = ("Rw","Rw'","Rw2")
Uw_MOVES = ("Uw","Uw'","Uw2")
Fw_MOVES = ("Fw","Fw'","Fw2")
Lw_MOVES = ("Lw","Lw'","Lw2")
Dw_MOVES = ("Dw","Dw'","Dw2")
Bw_MOVES = ("Bw","Bw'","Bw2")
TRw_MOVES = ("3Rw","3Rw'","3Rw2")
TUw_MOVES = ("3Uw","3Uw'","3Uw2")
TFw_MOVES = ("3Fw","3Fw'","3Fw2")
TLw_MOVES = ("3Lw","3Lw'","3Lw2")
TDw_MOVES = ("3Dw","3Dw'","3Dw2")
TBw_MOVES = ("3Bw","3Bw'","3Bw2")

ALL_NxN_MOVES = (R_MOVES, U_MOVES, F_MOVES, L_MOVES, D_MOVES, B_MOVES,
             Rw_MOVES, Uw_MOVES, Fw_MOVES, Lw_MOVES, Dw_MOVES, Bw_MOVES,
             TRw_MOVES, TUw_MOVES, TFw_MOVES, TLw_MOVES, TDw_MOVES, TBw_MOVES)

REG_SETS = {
"2x2": (R_MOVES, U_MOVES, F_MOVES),
"3x3": (R_MOVES, U_MOVES, F_MOVES, L_MOVES, D_MOVES, B_MOVES),
"4x4": (R_MOVES, U_MOVES, F_MOVES, L_MOVES, D_MOVES, B_MOVES, 
        Rw_MOVES, Uw_MOVES,Fw_MOVES, Lw_MOVES, Dw_MOVES, Bw_MOVES),
"5x5": (R_MOVES, U_MOVES, F_MOVES, L_MOVES, D_MOVES, B_MOVES,
        Rw_MOVES, Uw_MOVES,Fw_MOVES, Lw_MOVES, Dw_MOVES, Bw_MOVES),
"6x6": (R_MOVES, U_MOVES, F_MOVES, L_MOVES, D_MOVES, B_MOVES,
        Rw_MOVES, Uw_MOVES, Fw_MOVES, Lw_MOVES, Dw_MOVES, Bw_MOVES, 
        TRw_MOVES, TUw_MOVES, TFw_MOVES, TLw_MOVES, TDw_MOVES, TBw_MOVES),
"7x7": (R_MOVES, U_MOVES, F_MOVES, L_MOVES, D_MOVES, B_MOVES,
        Rw_MOVES, Uw_MOVES, Fw_MOVES, Lw_MOVES, Dw_MOVES, Bw_MOVES, 
        TRw_MOVES, TUw_MOVES, TFw_MOVES, TLw_MOVES, TDw_MOVES, TBw_MOVES),
"Skewb": (R_MOVES, U_MOVES, L_MOVES, B_MOVES),
"Mega": (("R++", "R--"), ("D++", "D--"), ("U", "U'")),
"Pyra": (("R","R'"), ("U","U'"), ("L","L'"), ("B","B'"), ("r", "r'"), ("l", "l'"), ("u", "u'"), ("b", "b'"))}

SQ1_MOVES = ("6", "5", "4", "3", "2", "1", "0", "-1", "-2", "-3", "-4", "-5", "-6")

NxN_MOVES = (R_MOVES, U_MOVES, F_MOVES, L_MOVES, D_MOVES, B_MOVES,
             Rw_MOVES, Uw_MOVES, Fw_MOVES, Lw_MOVES, Dw_MOVES, Bw_MOVES,
             TRw_MOVES, TUw_MOVES, TFw_MOVES, TLw_MOVES, TDw_MOVES, TBw_MOVES)

SCRAMBLE_LENGTHS = {"2x2":(9,10),
                    "3x3":(19,21),
                    "4x4":(44,45),
                    "5x5":(60,60),
                    "6x6":(80,80),
                    "7x7":(100,100),
                    "Skewb":(8,9),
                    "Pyra":(19,12),
                    "Mega":(77,77),
                    "Sq1":(10,14)}

#text validation
TIME_CHARS = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ':', '+', 'd', 'n', 'f')
CUBE_PREFIXES = {'222':'2x2', '444':'4x4', '555':'5x5', '666':'6x6', '777':'7x7', 'sqr':'Sq1', 'skb':'Skewb', 'mgm':'Mega', 'pyr':'Pyra'}
VALID_TIME_FORMATS = ('00:00:00.00', '0:00:00.00', '00:00.00', '0:00.00', '00.00', '0.00', '.00',
                 '0:00', '00:00', '0:00:00', '00:00:00', '0.0', '00.0', '0:00.0', '00:00.0', '0:00:00.0', '00:00:00.0',
                 '0.', '00.', '0:00.', '00:00.', '0:00:00.', '00:00:00.',
                 '0', '00', '000', '0000', '00000', '000000', '0000000', '00000000', '')