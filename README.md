# ⚙️ Computer Graphics Course Projects (2022_CSE4020_2016026608)

This repository contains two OpenGL-based projects developed for the Computer Graphics course.  
Both projects focus on **real-time 3D rendering**, **animation**, and **interactive visualization**.

---

## OBJ Rendering Viewer

**Description**  
Implemented a **real-time 3D viewer** using OpenGL, supporting both *single mesh rendering* and *hierarchical model animation* modes.  
Features include **multiple light sources**, **wireframe/solid toggle**, and **smooth shading control** using normal data.

**Key Features**
- Load and render `.obj` meshes via drag & drop  
- Hierarchical model animation with 3-level joint structure  
- Multiple light sources (directional + point lights)  
- Toggle between wireframe/solid mode (`Z` key) and shading modes (`S` key)

**Demo** 

![ezgif-6777544f541e10](https://github.com/user-attachments/assets/54f167cb-edcd-44c4-86a5-0a003be7133d)

---

## BVH Motion Viewer

**Description**  
Implemented a **BVH motion viewer** using OpenGL that parses and visualizes skeletal motion data in real time.  
Supports both *line rendering* and *box rendering* modes, and allows switching between them during execution.

**Key Features**
- Load `.bvh` motion data via drag & drop  
- Render static skeleton (T-pose) or animated motion (`Spacebar` key)  
- Switch rendering modes (line ↔ box) with `1` / `2` keys  
- Optional OBJ body parts rendering (`O` key)

**Demo**  

![내-동영상](https://github.com/user-attachments/assets/7b6124e2-b54b-418c-a8f5-ea0f6ef5d698)

---
---
    

# 🌐 Computer Graphics Lab Projects (particle_dynamics)

This repository contains two implementations of **physics-based particle simulations** built with **OpenGL**.  
The goal was to practice **forward dynamics simulation**, force modeling, and numerical integration methods.

---

## Mass-Spring Model

**Description**  
Implemented a 2D mass-spring system that simulates physical motion under **Gravity**, **Spring force**, and **Ground contact force** (with friction).

Particles exist in 3D space but move on a 2D plane by fixing one coordinate to a constant value.  
The system is integrated using **Euler Integration**, updating position and velocity at each timestep.

**Demo Video**  

<p>
  <img src="https://github.com/user-attachments/assets/d8032b51-4032-46e6-b63e-150fbb25bfd4" alt="mass-spring-model" width="78%">
</p>

---

## Particle Collision Simulation

**Description**  
Simulated multiple elastic particles that bounce and settle under **gravity**.  
Each particle exhibits **elastic collision response** upon ground contact.

This version uses **Runge–Kutta 4th order integration (RK4)** for higher accuracy and numerical stability.

**Demo Video**  

<p>
  <img src="https://github.com/user-attachments/assets/1d1b28aa-057d-42e6-922c-791b982cc4d8" alt="elastic-particle-simulation" width="78%">
</p>


