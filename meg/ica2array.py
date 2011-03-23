'''rpy2 ica to array'''



def convertica2array(inputvector):
    
    I = {}; x = 0
    for j in (input.names):
         m = r.matrix(input)
         I[j] = asarray(m[x]); x = x+1
    i = I
