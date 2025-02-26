import numpy as np, sys, psutil, time
from numba import njit
@njit
def eval_f_numba(terms,x,n): 
    val_out: np.int8 = 0 
    for term in terms:
        weight = term[0]
        indices = term[1]
        v = bool(1) 
        for j in indices:
            v &= x[j-n] 
        val_out = np.int8(val_out + weight*int(v))%8 
    return val_out

def get_new_terms_numba(terms,n):
    new_terms = []
    for term in terms:
        indices = term[1]
        remove_term = False
        for q in indices:
            if q < n: 
                remove_term = True
                break
        if not remove_term :
            new_terms.append(term)
    return new_terms

# ============== This is the most time consuming step ==============
@njit
def get_truthtable_no_ivs_numba(terms, n, t, initial_state):
    new_terms = get_new_terms_numba(terms,n)
    new_terms = np.array(terms, dtype=[('weight', np.int32), ('indices', np.int32, (3,))])

    x_range = 2**(t-n) 

    ttb = np.empty(x_range, dtype=np.uint8) 
    x_no_ivs = np.empty(t-n, dtype='bool')
    for i in range(x_range):
        y_bin = np.zeros(t - n, dtype=bool)
        for bit_pos in range(t - n):
            y_bin[bit_pos] = (i >> (t - n - 1 - bit_pos)) & 1
        for ind, val in enumerate(y_bin):
            x_no_ivs[ind] = val
        ttb[i] = eval_f_numba(new_terms,x_no_ivs,n) 
    return ttb
