# Autonomous Multi-Agent Drone Navigation System

## Overview
This project simulates an autonomous multi-drone system capable of:

- Global path planning using A* algorithm
- Local obstacle avoidance using ORCA-inspired control
- Dynamic replanning in changing environments
- Multi-agent task allocation
- ROS-inspired modular architecture

---

## System Architecture

The system is divided into modular robotics nodes:

### 1. Planner Node
Computes optimal grid paths using A*.

### 2. Controller Node
Executes motion using ORCA-style velocity avoidance.

### 3. Safety Node
Monitors collision risk in real-time.

### 4. Task Allocation Node
Assigns goals dynamically to multiple drones.

### 5. Message Bus (ROS-style simulation)
Handles communication between modules.

---

## Features

- Multi-drone swarm simulation
- Real-time obstacle avoidance
- Dynamic replanning system
- Distributed ROS-like architecture
- Grid-based environment simulation

---

## Technologies Used

- Python
- Pygame
- Graph search algorithms (A*)
- Robotics motion planning concepts

---

## How to Run

pip install -r requirements.txt

python main.py
