# TODO: Your name, Cornell NetID

import dynamic_programming


# DO NOT CHANGE THIS CLASS
class DiffingCell:
    def __init__(self, s_char, t_char, cost):
        self.cost = cost
        self.s_char = s_char
        self.t_char = t_char
        self.validate()

    # Helper function so Python can print out objects of this type.
    def __repr__(self):
        return "(%d,%s,%s)" % (self.cost, self.s_char, self.t_char)

    # Ensure everything stored is the right type and size
    def validate(self):
        assert (type(self.cost) == int), "cost should be an integer"
        assert (type(self.s_char) == str), "s_char should be a string"
        assert (type(self.t_char) == str), "t_char should be a string"
        assert (len(self.s_char) == 1), "s_char should be length 1"
        assert (len(self.t_char) == 1), "t_char should be length 1"


# Input: a dynamic programming table,  cell index i and j, the input strings s and t, and a cost function cost.
# Should return a DiffingCell which we will place at (i--,j) for you.
def fill_cell(table, i, j, s, t, cost):
    t += '-'
    s += '-'
    assert i < len(s), print(i, s)
    assert j < len(t), print(j, t)
    c = cost(s[i], t[j])
    return DiffingCell(s[i], t[j], c)


# Input: n and m, represents the sizes of s and t respectively.
# Should return a list of (i,j) tuples, in the order you would like fill_cell to be called
def cell_ordering(n, m):
    # print(n, m)
    n += 1
    m += 1
    dim = [n, m]
    indices = []
    for p in range(n * m):  # generalized to n-d!
        _index = [0, 0]
        for i in [1, 0]:
            _index[i] = p % dim[i]
            p = p // dim[i]
        indices.append(tuple(_index))
    return indices


# Returns a size-3 tuple (cost, align_s, align_t).
# cost is an integer cost.
# align_s and align_t are strings of the same length demonstrating the alignment.
# See instructions.pdf for more information on align_s and align_t.
def diff_from_table(s, t, table):
    t += '-'
    s += '-'
    n, m = len(s), len(t)
    cost = 0
    align_s, align_t = "", ""
    row = [i for i in range(n - 1, -5, -1)]
    col = [i for i in range(m - 1, -5, -1)]
    _c, _r = iter(col), iter(row)
    left_step = lambda: next(_c)
    up_step = lambda: next(_r)
    i, j = up_step(), left_step()

    def traverse(i, j, align_s, align_t, cost):
        if not (i == 0 and j == 0):
            c1 = table.get(i - 1, j - 1)
            c1_cost = c1.cost
        else:
            c1_cost = 1e10
        if not (i == 0):
            c3 = table.get(i - 1, -1)
            c3_cost = c3.cost
        else:
            c3_cost = 1e10
        if not (j == 0):
            c2 = table.get(-1, j - 1)
            c2_cost = c2.cost
        else:
            c2_cost = 1e10
        c_min = min(c1_cost, c2_cost, c3_cost)
        if c_min == c1_cost:
            cost += c1.cost
            i = up_step()
            j = left_step()
            print(c1.s_char + c1.t_char, 'diag->', i, j)
            align_s = c1.s_char + align_s
            align_t = c1.t_char + align_t
            return i, j, align_s, align_t, cost
        elif c_min == c2_cost:
            cost += c2.cost
            j = left_step()
            print(c2.s_char + c2.t_char, 'left->', i, j, )
            align_s = c2.s_char + align_s
            align_t = c2.t_char + align_t
            return i, j, align_s, align_t, cost
        elif c_min == c3_cost:
            cost += c_min
            i = up_step()
            print(c3.s_char + c3.t_char, 'up->', i, j, )
            align_s = c3.s_char + align_s
            align_t = c3.t_char + align_t
            return i, j, align_s, align_t, cost
        else:
            Exception(msg="Check for tie conditions.")

    for c in range(n + m - 2):
        # print("\n",align_s,"\n", align_t)
        i, j, align_s, align_t, cost = traverse(i, j, align_s, align_t, cost)
        if i == -1 or i == n - 1 and j == m - 1 or j == -1:
            print((cost, align_s, align_t))
            return (cost, align_s, align_t)


# Example usage
if __name__ == "__main__":
    # Example cost function from instructions.pdf
    def costfunc(s_char, t_char):
        if s_char == t_char: return 0
        if s_char == 'a':
            if t_char == 'b': return 5
            if t_char == 'c': return 3
            if t_char == '-': return 2
        if s_char == 'b':
            if t_char == 'a': return 1
            if t_char == 'c': return 4
            if t_char == '-': return 2
        if s_char == 'c':
            if t_char == 'a': return 5
            if t_char == 'b': return 5
            if t_char == '-': return 1
        if s_char == '-':
            if t_char == 'a': return 3
            if t_char == 'b': return 3
            if t_char == 'c': return 3


    import dynamic_programming

    s = "acb"
    t = "baa"
    D = dynamic_programming.DynamicProgramTable(len(s) + 1, len(t) + 1,
                                                cell_ordering(len(s), len(t)), fill_cell)

    D.fill(s=s, t=t, cost=costfunc)
    # (x) = diff_from_table(s,t, D)
    (cost, align_s, align_t) = diff_from_table(s, t, D)
    # print(align_s)
    # print(align_t)
    # print("cost was %d"%cost)
