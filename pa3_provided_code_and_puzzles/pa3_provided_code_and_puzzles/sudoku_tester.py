execfile("kea218.py")
sb = init_board("input_puzzles/easy/4_4.sudoku")
sb.print_board()

fb = solve(sb, True, True, False, False)

fb.print_board()
