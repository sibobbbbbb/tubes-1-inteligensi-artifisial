# Tugas Besar 1 IF3170 Inteligensi Artifisial 2024/2025
Diagonal Magic Cube Solver with Local Search

## **General Information**
This project is an implementation of local search algorithms to solve the Diagonal Magic Cube problem as part of assignments IF3070 (Dasar Inteligensi Buatan) and IF3170 (Inteligensi Buatan). The objective is to find a solution for a 5x5x5 Diagonal Magic Cube using three local search algorithms: Hill Climbing, Simulated Annealing, and Genetic Algorithm.

Problem Description
A Diagonal Magic Cube is a 3-dimensional cube filled with unique integers from 1 to n^3, where n is the cube's side length. The cube satisfies specific properties:
- Each row, column, pillar, diagonal, and cross-section sums up to a predetermined "magic number."
- The task is to rearrange numbers such that all constraints are met using local search techniques.

Algorithms Implemented
The project covers three primary local search algorithms:
1. Hill Climbing: Implemented with variations such as Steepest Ascent, Stochastic Hill Climbing, Hill Climbing with Sideways Moves, and Random Restart Hill Climbing.
2. Simulated Annealing: Applies a probabilistic approach to escape local optima.
3. Genetic Algorithm: Includes experimentation with population size and iteration count to assess convergence.

Experimental Approach
Each algorithm is executed three times, with results recorded as follows:
1. Initial and final cube states
2. Objective function values and convergence plots
3. Iterations, restarts, sideways moves, and duration per run
4. Specific metrics such as population size and iteration count for Genetic Algorithm

## **Requirements**

To use this program, you will need to install **Node.js and Pyhton(flask)** on the device you are using.

## **How to Run and Compile**

### **Setup**

1. Clone repository

```sh
$ git clone https://github.com/sibobbbbbb/tubes-1-inteligensi-artifisial.git
$ cd tubes-1-inteligensi-artifisial
```

### **Compile**

1. split terminal for frontend and backend setup
2. Frontend
   - cd frontend
     ```sh
     $ cd src/frontend
     ```
   - install dependecies
     ```sh
     $ npm i
     ```
   - build
     ```sh
     $ npm run dev
     ```
3. Backend
   - cd backend
     ```sh
     $ cd src/backend
     ```
   - install dependecies
     ```sh
     $ python app.py
     ```
 4. open the program at http://localhost:3000/

## Author

| **NIM**  |         **Name**          | **Class** | **Pembagian Tugas**  | 
| :------: | :-----------------------: | :-------: | :--------------: | 
| 13522142 |   Farhan Raditya Aji    |    K03    | Genetic Algorithm |
| 13522146 |   Muhammad Zaidan S. R.    |    K03    | Frontend Web |
| 13522159 |   Rafif Ardhinto Ichwantoro    |    K03    | Simulated Annealing |
| 13522160 |   Rayhan Ridhar Rahman    |    K03    | Hill Climbing Algorithm |
