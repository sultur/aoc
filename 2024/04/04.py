import sys

matrix = [line.strip() for line in sys.stdin.readlines()]
ROWS = len(matrix)
COLS = len(matrix[0])

# Part 1
WORD = "XMAS"
WLEN = len(WORD)
TO_MATCH = frozenset((WORD,WORD[::-1]))

n = 0
for row in range(ROWS):
    for col in range(COLS):
        # Horizontal matches
        if matrix[row][col:col+WLEN] in TO_MATCH:
            n+=1
        # Vertical/Diagonal matches
        if row+WLEN > ROWS:
            continue
        # Down to the left
        if col+1 >= WLEN:
            x = ''.join(matrix[row+i][col-i] for i in range(WLEN))
            n += x in TO_MATCH
        # Directly down
        x = ''.join(matrix[row+i][col] for i in range(WLEN))
        n += x in TO_MATCH
        # Down to the right
        if col+WLEN <= COLS:
            x = ''.join(matrix[row+i][col+i] for i in range(WLEN))
            n += x in TO_MATCH
print(n)

# Part 2
WORD = "MAS"
WLEN = len(WORD)
TO_MATCH = frozenset((WORD,WORD[::-1]))

n = 0
for row in range(ROWS-WLEN+1):
    for col in range(COLS-WLEN+1):
        # Matches down to the right?
        x = ''.join(matrix[row+i][col+i] for i in range(WLEN))
        if x in TO_MATCH:
            # Matches up to the right?
            y = ''.join(matrix[row+WLEN-1-i][col+i] for i in range(WLEN))
            n += y in TO_MATCH
print(n)

