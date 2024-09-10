# GameOfLife

  This project contains an implementation of Conway's Game of Life, invented by British mathematician John Horton Conway in 1970. This game is a cellular automaton with zero players and it is played on a two-dimensional grid of square cells, each cell having two possible states: alive or dead. 
  The evolution is determined solely by the initial state of the cells and the rules of interaction between without further intervention from the players. Although the rules are simple, the complexity and diversity of emerging behaviors are surprising and fascinating.
![image](https://github.com/user-attachments/assets/7e967cf9-3764-42e9-905a-2842d34c32ea)\
  I implemented the game on both CPU and GPU in order to compare the different methods and see the differences. For the version running on GPU I used the following versions: 2.0.1. for Pytorch and 11.7 for CUDA Toolkit
  The video below contains an example of how the application works: 
  ![GameOfLifeExampleVideo](https://github.com/user-attachments/assets/78d82a06-8329-4e70-86b7-b19de4ea2dd4)


● **Data structure**\
**CPU** - Cell states are stored in a Python dictionary (cell_states), where each key
represents the coordinates of a cell and the value represents its state (alive or dead).
Updating the state is done by iterating over the dictionary and applying the game rules on
each cell.\
**GPU** - Cell states are stored in a PyTorch tensor (cell_states), which is processed in
in parallel on the GPU. The tensor enables efficient data management on the GPU, ensuring parallelization
operations.

● **Processing mode**\
**CPU** - Processing is done sequentially, i.e. each cell is processed one by one by the
CPU. The update_game_of_life function calculates the number of live neighbors for each cell and
updates its state based on the game rules.\
**GPU**: Processing is done in parallel using multiple cores on the GPU. Function
update_game_of_life uses PyTorch tensor operations to compute the number of live neighbors
and applies game rules to all cells simultaneously, significantly reducing execution time.

● **Memory management**\
**CPU** - Memory is managed by Python and there are no specific optimizations for
memory utilization. Data is stored in standard Python data structures (dictionaries, lists).\
**GPU** - The use of PyTorch tensors enables efficient memory management on the GPU.
Global memory, shared memory and GPU caches are used to maximize
performance.

● **Grid resize and zoom**\
**CPU** - Resizing and zooming the grid is done by adjusting the size of the window and cells,
and recalculating cell positions based on the new dimensions.
The functions resize_grid and adjust_grid_and_cells_for_zoom handle these adjustments.\
**GPU** -Similar to the CPU implementation, but the tensors are recalculated to match the new
grid sizes and positions. Synchronization between CPU and GPU is required to ensure correct display update.

● **User interface and control functions**\
**CPU** - The user interface is managed through Pygame and Tkinter.
Control functions (start, stop, reset, restore) are implemented to allow the user to
to interact with the simulation.\
**GPU** - User interface and control functions are similar to the CPU implementation, but with
adjustments to work with PyTorch tensors.The control functions must synchronize the actions of the user's actions with parallel operations on the GPU.\


  To illustrate the performance, I took 2 simple cases, whose configurations were set for both CPU and GPU, and then obtained the execution times until the final, stable conformation.\
  
  ![GameOfLifeEx1](https://github.com/user-attachments/assets/249da60d-6348-4df8-be34-78c7f31182b8)

  - CPU running time: 0.15 seconds
  - GPU running time: 0.13 seconds

![GameOfLifeEx2](https://github.com/user-attachments/assets/66c0fd22-f4a1-47fe-8543-e5b95492c23d)

  - CPU running time: 0.05 seconds
  - GPU running time: 0.03 seconds
