import sys
import math
import heapq
import copy
import time
import os

__author__ = 'Dakota'

if len(sys.argv) != 2:
    print "Usage: python MazeSolver.py file_name"
    quit()

fileName = sys.argv[1]
textFile = open(fileName)

def read_maze(f) :
    """
    Reads from a text file and outputs a 2d list of chars from f
    :param f: The given text file
    :return: A 2d list of chars from f
    """
    maze = []
    for line in f :
        row = []
        for char in line :
            if char != '\n' :
                row.append(char)
        maze.append(row)
    return maze

def print_maze(m) :
    """
    Prints a maze to the terminal
    :param m: The given maze
    :return: void
    """
    for row in m:
        line = ""
        for character in row:
            line += character
        print line

def find_char(ch, m) :
    """
    Finds the first occurance of character in the maze and returns its postition
    :param ch: The given character
    :param m: The given maze
    :return: Its position in the form (row, column)
    """
    row_pos = 0
    for row in m:
        col_pos = 0
        for character in row:
            if character == ch:
                return row_pos, col_pos
            col_pos += 1
        row_pos += 1

def is_open(row, col, maze):
    """
    Returns true if maze[row][col] is passable
    :param row: The row given
    :param col:  The column given
    :param maze: The maze given
    :return: True if the maze at the position is passable
    """
    if 0 <= row < len(maze) and 0 <= col < len(maze[row]):
        return maze[row][col] != '#'
    else: return False

#Maze, Player location, and goal location are set.
m = read_maze(textFile)
playerLoc = find_char('@', m)
goalLoc = find_char('%', m)

#Check if player or goal do not exist
if not (playerLoc and goalLoc):
    print "No solution to the maze"
    quit()

def euclidian(player, goal):
    """
    Returns the euclidian distance between the player and the goal
    :param player: The player position
    :param goal: The goal position
    :return: The distance between the two positions
    """
    dx = player[0] - goal[0]
    dy = player[1] - goal[1]
    return math.sqrt(dx*dx + dy*dy)

def preprocessMaze(goal, maze):
    r = goal[0]
    c = goal[1]
    global rowMin, rowMax, colMin, colMax
    while r > 0 and is_open(r, c, maze):
        r-= 1
    rowMin = r
    r = goal[0]
    while r < len(maze) and is_open(r, c, maze):
        r += 1
    rowMax = r
    r = goal[0]

    while c > 0 and is_open(r, c, maze):
        c-= 1
    colMin = c
    c = goal[1]
    while c < len(maze[r]) and is_open(r, c, maze):
        c += 1
    colMax = c

def a_star(start, dest, maze):
    """
    A* algorithm for finding a path through a maze
    :param start: The starting position
    :param dest: The destination position
    :param maze: The given maze
    :return: A path from the destination to the position
    """
    visited = {start}
    current = start
    frontier = []
    paths = {start : []}
    traveled = {start : 0}
    while current != dest:
        r = current[0]
        c = current[1]
        newFrontier = set()
        if is_open(r-1, c, maze) and not (r-1, c) in visited:
            newFrontier |= {((r-1, c))}
        if is_open(r+1, c, maze) and not (r+1, c) in visited:
            newFrontier |= {(r+1, c)}
        if is_open(r, c-1, maze) and not (r, c-1) in visited:
            newFrontier |= {(r, c-1)}
        if is_open(r, c+1, maze) and not (r, c+1) in visited:
            newFrontier |= {(r, c+1)}

        newPath = copy.copy(paths[current]);
        newPath.append(current);
        for node in newFrontier:
            if (not node in traveled) or traveled[node] > traveled[current] + 1:
                paths[node] = newPath;
                traveled[node] = traveled[current]+1
            heapq.heappush(frontier, (traveled[node] +
                euclidian(node, dest), node))

        if frontier == []:
            return None
        visited |= {current}
        while current in visited:
            current = heapq.heappop(frontier)[1]

    ret = paths[current]
    ret.append(current)
    return ret

def print_path_without_history(path, maze):
    """
    Prints the given path through the maze
    :param path: The given path
    :param maze: The given maze
    :return: void
    """
    if not path:
        print "No solution To the Maze"
        return
    step = 0
    for node in path:
        #Delete this comment if on windows
        os.system('cls')
        #Delete this comment if on linux or os x!
        # os.system('clear')
        if step == 0:
            print "Initial:"
        else:
            print "Step " + str(step) + ":"
        maze[node[0]][node[1]] = '@'
        print_maze(m)
        maze[node[0]][node[1]] = '.'
        step += 1
        print
    print "Problem Solved!"

def print_path(path, maze):
    if not path:
        print "No solution To the Maze"
        return
    step = 0
    for node in path:
        if step == 0:
            print "Initial:"
        else:
            print "Step " + str(step) + ":"
        maze[node[0]][node[1]] = '@'
        print_maze(m)
        maze[node[0]][node[1]] = '.'
        step += 1
        print
    print "Problem Solved!"

path = a_star(playerLoc, goalLoc, m)
print_path(path, m)
#print_path_without_history(path, m)