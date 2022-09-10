# Tetris
My own classic version of tetris. Implemented with Pygame.

I created this implementation of a single game to try to understand the basic logic which is required to make an engine working. However, the code structure is very simple, i created 2 classes: the first represent the tetris piece and the second the dynamic map. Every piece can rotate in both direction, clock-wise and anti clock-wise, thanks to the computation of relative coordinates and the presence of a centre. On the other hand, the Class map is needed to check the tetris pieces already blocked, to evaluate if a movement is possible and to check if a line is completed.

The main problem i found is that the velocity of the blocks is difficult to control properly. I used some counter varaibles, but maybe they are a naive way to interpret this kind of problem. It's possible that using a timer libray the dynamicity of movements will be more fluid and homogeneus. 

The implementation is created from scratch and for fun, but i accept suggestions to improve the engine.
