# DRL-Pong

It is a pong game not using GYM environment. 

## Code Structure

The DRL server is in the "dqn-server" folder
    - DqnServer.py:     the DRL computing engine
    - nernet.py:        the neural network class, implemeted with pytorch (MLP)
    - optim.py:         the optimisation (Huber Loss)
    - server.py:        the main running script
    - utils.py:         the replay memory (FIFO)

The Pong Game is in the "pong-game" folder
    - simple-pong-learner-only.py:          the game file without teacher
    - simple-pong.py:          the game file with teacher
    - sprite.py:        the game sprit objects (ball, Cpu Greedy Player, RL Player)

## IO

The Pong Game contains one CPU player and one RL player, the CPU player uses a naive (greedy) method always following the ball's x position. 
The RL player takes features from the game as its state including: 1) the position of the ball, 2) the position of the player bar (bottom) and the position of the ball in the previous frame. 

The RL player sends the **state** to the server to get the **action**, then push the 4-item tuple (s, a, s', r) to the server for training. THe server has a MLP of size 6x10x10x2 (state -> action<left, right>). 

## Algorithm

The exploitation and exploration is **Simulated Annealing** 0.99 -> 0.05
The replay buffer is of size 10000 with an FIFO replacement policy, batch size is 800. 


# HOWTO

$ cd dqn-server 
$ python3 server # Start the server earlier than the game
