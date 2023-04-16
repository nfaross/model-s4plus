# implementation of the arithmetics in A^{\otimes 3}, where A 
# is the algebra generated by universal two projections p and q.

# an alternating product of p's and q's is stored as pair of its
# starting value and length, e.g. pqpqp = (START_P, 5)
START_ONE, START_P, START_Q = 0, 1, 2
I = (START_ONE, 0)  # the unit '1'
P = (START_P,   1)  # a single 'p'
Q = (START_Q,   1)  # a single 'q'

# the matrix M_3 := R^{\operp 3}
M = [
    [
        {(P, P, P): 1,
         (I, Q, I): 1, (I, Q, P): -1, (P, Q, I): -1, (P, Q, P): 1},
        {(P, I, Q): 2, (P, P, Q): -1,
         (I, I, I): 1, (I, I, Q): -1, (I, Q, I): -1, (I, Q, Q): 1,
         (P, I, I): -1, (P, Q, I): 1, (P, Q, Q): -1},
        {(P, P, I): 1, (P, P, P): -1, (I, Q, P): 1, (P, Q, P): -1},
        {(P, I, I): 1, (P, I, Q): -2, (P, P, I): -1, (P, P, Q): 1,
         (I, I, Q): 1, (I, Q, Q): -1, (P, Q, Q): 1}
    ],
    [
        {(I, P, P): 1, (P, P, P): -1, (P, Q, I): 1, (P, Q, P): -1},
        {(I, I, Q): 1, (I, P, Q): -1, (P, I, Q): -2, (P, P, Q): 1,
         (P, I, I): 1, (P, Q, I): -1, (P, Q, Q): 1},
        {(I, P, I): 1, (I, P, P): -1, (P, P, I): -1, (P, P, P): 1,
         (P, Q, P): 1},
        {(I, I, I): 1, (I, I, Q): -1, (I, P, I): -1, (I, P, Q): 1,
         (P, I, I): -1, (P, I, Q): 2, (P, P, I): 1, (P, P, Q): -1,
         (P, Q, Q): -1}
    ],
    [
        {(Q, P, P): -1,
         (I, I, I): 1, (I, I, P): -1, (I, Q, I): -1, (I, Q, P): 1,
         (Q, I, I): -1, (Q, I, P): 2, (Q, Q, I): 1, (Q, Q, P): -1},
        {(Q, P, Q): 1,
         (I, Q, I): 1, (I, Q, Q): -1, (Q, Q, I): -1, (Q, Q, Q): 1},
        {(Q, I, I): 1, (Q, I, P): -2, (Q, P, I): -1, (Q, P, P): 1,
         (I, I, P): 1, (I, Q, P): -1, (Q, Q, P): 1},
        {(Q, P, I): 1, (Q, P, Q): -1,
         (I, Q, Q): 1, (Q, Q, Q): -1}
    ],
    [
        {(I, I, P): 1, (I, P, P): -1, (Q, I, P): -2, (Q, P, P): 1,
         (Q, I, I): 1, (Q, Q, I): -1, (Q, Q, P): 1,},
        {(I, P, Q): 1, (Q, P, Q): -1, (Q, Q, I): 1, (Q, Q, Q): -1},
        {(I, I, I): 1, (I, I, P): -1, (I, P, I): -1, (I, P, P): 1,
         (Q, I, I): -1, (Q, I, P): 2, (Q, P, I): 1, (Q, P, P): -1,
         (Q, Q, P): -1},
        {(I, P, I): 1, (I, P, Q): -1, (Q, P, I): -1, (Q, P, Q): 1,
         (Q, Q, Q): 1}
    ]
]

def proj_mult(x, y):
    """
    Multiplies 'x' and 'y' as alternating products of p's and q's.
    Such products are represented as pairs (start, length).
    """
    start1, length1 = x
    start2, length2 = y

    # nothing to check if a factor is '1'
    if start1 == START_ONE:
        return y
    if start2 == START_ONE:
        return x

    # combine the products and possibly remove a factor
    if start1 == START_P:
        if ((start2 == START_P and length1 % 2 == 0) or
            (start2 == START_Q and length1 % 2 == 1)):
            return (START_P, length1 + length2)
        else:
            return (START_P, length1 + length2 - 1)

    if start1 == START_Q:
        if ((start2 == START_Q and length1 % 2 == 0) or
            (start2 == START_P and length1 % 2 == 1)):
            return (START_Q, length1 + length2)
        else:
            return (START_Q, length1 + length2 - 1)


def tensor_mult(x, y):
    """
    Multiplies 'x' and 'y' as tensor product of alternating p's and q's.
    Such a tensor products are represented as triple (alt1, alt2, alt3).
    """
    return (
        proj_mult(x[0], y[0]), proj_mult(x[1], y[1]), proj_mult(x[2], y[2]),
    )

def mult(x, y):
    """
    Multiplies 'x' and 'y' as linear combinations of tensor products.
    Such linear combinations are represented as dictionary
    {tensor1: coeff1, tensor2: coeff2, ...} storing only non-zero coefficients.
    """
    result = {}
    for tensor1, coeff1 in x.items():
        for tensor2, coeff2 in y.items():
            new_tensor = tensor_mult(tensor1, tensor2)
            new_coeff  = result.get(new_tensor, 0) + coeff1 * coeff2
            if new_coeff != 0:
                result[new_tensor] = new_coeff
            elif new_tensor in result:
                del result[new_tensor]
    return result

