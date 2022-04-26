from enum import Enum

class NoteSnap(Enum):
    _4THS = 4
    _8THS = 8
    _12THS = 12
    _16THS = 16
    _20THS = 20
    _24THS = 24
    _32NDS = 32
    _48THS = 48
    _64THS = 64
    _96THS = 96
    _192THS = 192
    

class NoteColor(Enum): # based on subtract colors
    RED = [1.0/4 * i for i in range(4)]
    BLUE = [1.0/8 * (2*i)+1 for i in range(4)]
    GREEN = [1.0/12 * (i+1+i//3) for i in range(8)]
    YELLOW = [1.0/16 * (2*i)+1 for i in range(8)]
    PINK = [1.0/12 * (i+1+(2*((i+1)//2))) for i in range(8)]
    ORANGE = [1.0/32 * (2*i)+1 for i in range(16)]
    CYAN = [1.0/48 * (i+1+(2*((i+1)//2))) for i in range(16)]
    GREY = 0
