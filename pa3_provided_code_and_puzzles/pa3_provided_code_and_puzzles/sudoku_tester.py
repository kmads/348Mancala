import time
execfile("kea218.py")

sb = init_board("input_puzzles/easy/16_16.sudoku")
# sb.print_board()

start = time.time()

fb = solve(sb, True, False, False, False)

finish = time.time() - start

fb.print_board()

print "Board is complete:", is_complete(fb)

# finish = time.time() - start
print "Solved in", finish, "seconds"
