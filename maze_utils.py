def is_circle_maze(maze):
    return isinstance(maze, dict) and bool(maze) and "inner" in next(iter(maze.values()))
def is_hex_maze(maze):
    return isinstance(maze, dict) and bool(maze) and "top_left" in next(iter(maze.values()))
def is_triangle_maze(maze):
    return isinstance(maze, dict) and not is_hex_maze(maze) and not is_circle_maze(maze)
def maze_size(maze):
    if isinstance(maze, dict): return max(r for r,_ in maze)+1, (None if is_triangle_maze(maze) else max(c for _,c in maze)+1)
    return len(maze), len(maze[0])
def start_goal(maze):
    rows, cols=maze_size(maze)
    return ((0,0),(rows-1,2*(rows-1))) if is_triangle_maze(maze) else ((0,0),(rows-1,cols-1))
def get_neighbors(maze,row,col):
    if is_triangle_maze(maze):
        cell=maze[(row,col)]; out=[]
        for wall,other in (("left",(row,col-1)),("right",(row,col+1)),("vert",(row+1,col+1) if col%2==0 else (row-1,col-1))):
            if not cell[wall] and other in maze: out.append(other)
        return out
    if is_circle_maze(maze):
        cell=maze[(row,col)]; sectors=max(c for _,c in maze)+1
        return [other for wall,other in (("inner",(row-1,col)),("outer",(row+1,col)),("ccw",(row,(col-1)%sectors)),("cw",(row,(col+1)%sectors))) if not cell[wall] and other in maze]
    if is_hex_maze(maze):
        cell=maze[(row,col)]; dirs=(("top_left",-1,0),("top_right",-1,1),("right",0,1),("bottom_right",1,0),("bottom_left",1,-1),("left",0,-1))
        return [(row+dr,col+dc) for wall,dr,dc in dirs if not cell[wall] and (row+dr,col+dc) in maze]
    cell=maze[row][col]; rows,cols=maze_size(maze); out=[]
    for wall,other in (("top",(row-1,col)),("bottom",(row+1,col)),("left",(row,col-1)),("right",(row,col+1))):
        if not cell[wall] and 0<=other[0]<rows and 0<=other[1]<cols: out.append(other)
    return out
def heuristic(node,goal): return abs(node[0]-goal[0])+abs(node[1]-goal[1])
def wall_keys(maze):
    if is_triangle_maze(maze): return ["left","right","vert"]
    if is_circle_maze(maze): return ["inner","outer","cw","ccw"]
    if is_hex_maze(maze): return ["top_left","top_right","right","bottom_right","bottom_left","left"]
    return ["top","bottom","left","right"]
def iter_cells(maze): return maze.values() if isinstance(maze,dict) else (c for row in maze for c in row)
def cell_count(maze): return len(maze) if isinstance(maze,dict) else len(maze)*len(maze[0])
