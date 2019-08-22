from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    width = len(b) + 1
    height = len(a) + 1

    # initialise the matrix
    x = [[0 for i in range(width)] for j in range(height)]

    # populate the first column and row
    for i in range(height):
        x[i][0] = (i, Operation(1))
    for i in range(width):
        x[0][i] = (i, Operation(2))

    # populate the rest of the matrix
    # calculate the values for each cell
    for i in range(1, height):
        for j in range(1, width):
            insertion = x[i][j-1][0] + 1
            deletion = x[i-1][j][0] + 1
            if a[i-1] == b[j-1]:
                substitution = x[i-1][j-1][0]
            else:
                substitution = x[i-1][j-1][0] + 1

            # figure out what type of operation is used
            possible_ops = (deletion, insertion, substitution)
            op = Operation(possible_ops.index(min(possible_ops)) + 1)
            cost = min(possible_ops)

            # store result
            x[i][j] = (cost, op)

    return x