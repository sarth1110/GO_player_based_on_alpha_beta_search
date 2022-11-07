# GO playing agent based on alpha beta search
- Created a GO playing agent for a 5*5 board based on alpha beta pruning for minimax algorithm.
- The agent reads previous board and current board states from input.txt file and writes the best move in output.txt file.
- For one step the player will search till a depth of 4 moves and find the best possible move based on a custom heuristic using liberty of stones and the number of stones of the opponent a move will kill.
- The game continues until both the players make a total of 24 moves or either of the player makes a wrong move.
