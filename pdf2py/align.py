from numpy import mod

def check(fid):
    current_position = fid.tell();
    if mod(current_position, 8) != 0:
        offset = 8 - mod(current_position,8);
        fid.seek(offset, 1);#go to next 8*N position
        
    