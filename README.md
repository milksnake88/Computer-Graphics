# 🎨 Computer Graphics Projects

This repository contains two OpenGL-based projects developed for the Computer Graphics course.  
Both projects focus on **real-time 3D rendering**, **animation**, and **interactive visualization**.

---

## 🧱 OBJ Rendering Viewer

**Description**  
Implemented a real-time 3D viewer using **OpenGL**, supporting both *single mesh rendering* and *hierarchical model animation* modes.  
Features include **multiple light sources**, **wireframe/solid toggle**, and **smooth shading control** using normal data.

**Key Features**
- Load and render `.obj` meshes via drag & drop  
- Hierarchical model animation with 3-level joint structure  
- Multiple light sources (directional + point lights)  
- Toggle between wireframe/solid mode (`Z` key) and shading modes (`S` key)

🎥 **Demo Video**  
[![OBJ Rendering Demo](https://img.youtube.com/vi/AJb_own4frw/hqdefault.jpg)](https://youtu.be/AJb_own4frw)

---

## 🕺 BVH Motion Viewer

**Description**  
Developed a **BVH motion viewer** using OpenGL that parses and visualizes skeletal motion data in real time.  
Supports both *line rendering* and *box rendering* modes, and allows switching between them during execution.

**Key Features**
- Load `.bvh` motion data via drag & drop  
- Render static skeleton (T-pose) or animated motion (`Spacebar` key)  
- Switch rendering modes (line ↔ box) with `1` / `2` keys  
- Optional OBJ body parts rendering (`O` key)

🎥 **Demo Video**  
[![BVH Motion Demo](https://img.youtube.com/vi/ZMB0ilohrlE/hqdefault.jpg)](https://youtu.be/ZMB0ilohrlE)

---

🧩 *Built with Python (OpenGL), GLFW, and NumPy for matrix & vector operations.*  
📚 *Projects completed as part of the Computer Graphics course.*
