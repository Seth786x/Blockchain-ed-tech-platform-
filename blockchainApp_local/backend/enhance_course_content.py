#!/usr/bin/env python3

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import json
from typing import List, Dict

# Enhanced course module content
ENHANCED_CONTENT = {
    "graphics_evolution": {
        "modules": [
            {
                "title": "Introduction to Graphics Cards",
                "content": """# Introduction to Graphics Cards

## What is a Graphics Card?

A graphics card, also known as a **Graphics Processing Unit (GPU)**, is a specialized electronic circuit designed to accelerate the creation and rendering of images, videos, and animations. Unlike CPUs which are optimized for sequential processing, GPUs excel at parallel processing tasks.

### Key Components:
- **GPU Chip**: The main processor
- **VRAM**: Video Random Access Memory
- **Cooling System**: Fans, heat sinks, liquid cooling
- **Power Connectors**: PCIe connectors for power delivery
- **Display Outputs**: HDMI, DisplayPort, DVI, VGA

## History Overview

Graphics cards have evolved from simple display adapters to powerful parallel computing machines:

### 1980s - Early Graphics Adapters
- **CGA (Color Graphics Adapter)**: 4-color display at 320x200
- **EGA (Enhanced Graphics Adapter)**: 16 colors at 640x350
- **VGA (Video Graphics Array)**: 256 colors at 320x200

### 1990s - 2D Acceleration Era
- **SVGA**: Extended VGA with higher resolutions
- **2D Accelerators**: Specialized chips for faster 2D graphics
- **VESA Standards**: Standardized video interfaces

### 2000s - 3D Revolution
- **3Dfx Voodoo**: Dedicated 3D acceleration
- **DirectX/OpenGL**: Standardized 3D APIs
- **GPU Programming**: Shader languages introduced

## Modern Applications

Today's graphics cards are used for:
- **Gaming**: Real-time 3D rendering
- **Content Creation**: Video editing, 3D modeling
- **Machine Learning**: AI model training
- **Cryptocurrency**: Mining operations
- **Scientific Computing**: CUDA, OpenCL applications

## Exercise

Research and compare the specifications of three different graphics cards from different eras (1990s, 2000s, 2020s). Note the differences in:
- Memory capacity
- Processing power
- Power consumption
- Price points
"""
            },
            {
                "title": "The Voodoo Graphics Revolution",
                "content": """# The Voodoo Graphics Revolution

## 3Dfx Interactive - The Pioneer

Founded in 1994, **3Dfx Interactive** revolutionized PC gaming with the introduction of dedicated 3D graphics acceleration. Before Voodoo Graphics, PCs relied on software-based 3D rendering, which was slow and limited.

### The Voodoo Graphics (1996)

The original **Voodoo Graphics** was a groundbreaking graphics accelerator that changed everything:

#### Technical Specifications:
- **Memory**: 4MB EDO DRAM
- **Texture Memory**: 2MB for textures, 2MB for frame buffer
- **Architecture**: Single-chip design
- **Process**: 0.5-micron manufacturing
- **Fill Rate**: 45 million pixels per second
- **Texture Mapping**: Bilinear filtering

#### Revolutionary Features:
1. **Hardware 3D Acceleration**: First consumer card with dedicated 3D processing
2. **Texture Mapping**: Hardware-accelerated texture application
3. **Z-buffering**: Proper depth testing for 3D scenes
4. **Perspective Correction**: Eliminated texture warping
5. **Alpha Blending**: Transparency effects

## Impact on Gaming Industry

### Before Voodoo Graphics:
- **Software Rendering**: CPU handled all 3D calculations
- **Low Frame Rates**: Typically 5-15 FPS in 3D games
- **Limited Resolution**: Usually 320x240 or 640x480
- **Poor Visual Quality**: No texture filtering, aliasing issues

### After Voodoo Graphics:
- **Smooth Gameplay**: 30-60 FPS became achievable
- **Higher Resolutions**: 640x480 and 800x600 became standard
- **Better Visual Quality**: Filtered textures, anti-aliasing
- **New Game Genres**: Complex 3D games became viable

## Notable Games That Showcased Voodoo:

### Quake (1996)
- First major game to support Voodoo acceleration
- GLQuake renderer provided dramatic visual improvements
- Demonstrated the potential of hardware 3D acceleration

### Tomb Raider (1996)
- Enhanced lighting and texture detail
- Smoother character animations
- More detailed environments

### Unreal (1998)
- Showcased advanced lighting effects
- Demonstrated colored lighting capabilities
- Set new standards for 3D game visuals

## Glide API

3Dfx developed the **Glide API**, a proprietary graphics library that:
- Provided direct hardware access
- Offered superior performance compared to Direct3D/OpenGL
- Became the preferred API for many game developers
- Created vendor lock-in that later hurt 3Dfx's business

## Competition Response

The success of Voodoo Graphics sparked intense competition:
- **ATI**: Developed the Rage series
- **Matrox**: Created the Mystique and Millennium series
- **NVIDIA**: Entered the market with RIVA series
- **S3**: Enhanced their ViRGE series

## Technical Deep Dive

### Rendering Pipeline:
1. **Vertex Processing**: Transform 3D coordinates to screen space
2. **Triangle Setup**: Prepare polygons for rasterization
3. **Rasterization**: Convert triangles to pixels
4. **Texture Mapping**: Apply surface textures
5. **Pixel Operations**: Z-testing, alpha blending
6. **Frame Buffer**: Final image assembly

### Memory Architecture:
- **Dual Memory Banks**: Separate texture and frame buffer memory
- **Memory Bandwidth**: 1.3 GB/s peak throughput
- **Texture Compression**: Proprietary compression algorithms
- **Memory Management**: Efficient texture caching

## Legacy and Influence

The Voodoo Graphics card:
- **Established the GPU Market**: Created the dedicated 3D graphics industry
- **Influenced Design**: Modern GPUs still use similar principles
- **Changed Gaming**: Made complex 3D games commercially viable
- **Set Standards**: Established benchmarks for 3D performance

## Hands-On Activity

### Virtual Museum Visit:
1. Research original Voodoo Graphics advertisements from 1996-1997
2. Find video comparisons showing games before and after Voodoo acceleration
3. Locate technical reviews from computer magazines of that era
4. Create a timeline of 3Dfx's major product releases

### Discussion Questions:
1. Why was hardware 3D acceleration revolutionary for the gaming industry?
2. How did the Voodoo Graphics influence modern GPU architecture?
3. What were the advantages and disadvantages of the proprietary Glide API?
4. How did the Voodoo Graphics compare to its contemporary competitors?

## Assessment Quiz:
1. What was the memory configuration of the original Voodoo Graphics?
2. Name three games that significantly benefited from Voodoo acceleration.
3. What was the Glide API and why was it important?
4. How did hardware 3D acceleration change gaming frame rates?
"""
            },
            {
                "title": "GPU vs CPU Architecture",
                "content": """# GPU vs CPU Architecture: Understanding Parallel vs Sequential Processing

## Fundamental Design Philosophy

### CPU Architecture - Sequential Excellence
**Central Processing Units (CPUs)** are designed for **sequential processing** with emphasis on:
- **Single-threaded performance**
- **Complex instruction execution**
- **Large cache hierarchies**
- **Branch prediction**
- **Out-of-order execution**

### GPU Architecture - Parallel Powerhouse
**Graphics Processing Units (GPUs)** are designed for **parallel processing** with emphasis on:
- **Massively parallel execution**
- **Simple, repetitive operations**
- **High memory bandwidth**
- **Thousands of lightweight cores**
- **Stream processing**

## Core Count Comparison

### CPU Core Structure:
- **Modern CPUs**: 4-64 cores (high-end server CPUs)
- **Core Design**: Complex, large cores
- **Cache**: Large L1/L2/L3 cache per core
- **Power**: High power per core for complex operations

#### Intel Core i9-13900K Example:
- **Cores**: 8 Performance + 16 Efficiency cores
- **Cache**: 36MB L3 cache
- **Clock Speed**: Up to 5.8 GHz
- **Power**: 125W base, 253W max

### GPU Core Structure:
- **Modern GPUs**: 1,000-10,000+ cores
- **Core Design**: Simple, small cores (CUDA cores/Stream processors)
- **Memory**: Shared high-bandwidth memory
- **Specialization**: Optimized for floating-point operations

#### NVIDIA RTX 4090 Example:
- **CUDA Cores**: 16,384
- **RT Cores**: 128 (ray tracing)
- **Tensor Cores**: 512 (AI operations)
- **Memory**: 24GB GDDR6X
- **Memory Bandwidth**: 1008 GB/s

## Memory Architecture Differences

### CPU Memory Hierarchy:
```
CPU Core → L1 Cache (32KB) → L2 Cache (256KB-1MB) → L3 Cache (8-64MB) → System RAM (DDR4/DDR5)
```

**Characteristics:**
- **Low Latency**: Fast access to cached data
- **High Capacity**: Large system RAM (16GB-128GB+)
- **Complex Caching**: Multi-level cache with sophisticated algorithms

### GPU Memory Hierarchy:
```
GPU Core → Shared Memory → L1/L2 Cache → VRAM (GDDR6/HBM)
```

**Characteristics:**
- **High Bandwidth**: 500-1000+ GB/s memory bandwidth
- **Parallel Access**: Thousands of cores accessing memory simultaneously
- **Specialized Memory**: Optimized for graphics and compute workloads

## Processing Models

### CPU Processing Model:
```
Single Thread: Task1 → Task2 → Task3 → Task4
Multi-Thread:  Task1A → Task1B → Task1C
               Task2A → Task2B → Task2C
               Task3A → Task3B → Task3C
```

**Advantages:**
- **Complex Logic**: Excellent for branching, decision-making
- **Single-threaded Speed**: Fast execution of sequential algorithms
- **Versatility**: Can handle any type of computation

**Disadvantages:**
- **Limited Parallelism**: Fewer cores for parallel tasks
- **Expensive per Core**: High cost per processing unit

### GPU Processing Model:
```
Thousands of Threads in Parallel:
Thread 1: Simple Operation on Data[1]
Thread 2: Simple Operation on Data[2]
Thread 3: Simple Operation on Data[3]
...
Thread N: Simple Operation on Data[N]
```

**Advantages:**
- **Massive Parallelism**: Thousands of operations simultaneously
- **Cost Effective**: Many cores for parallel workloads
- **High Throughput**: Excellent for data-parallel tasks

**Disadvantages:**
- **Limited Branching**: Poor performance with complex logic
- **Memory Requirements**: Needs high-bandwidth memory
- **Programming Complexity**: Requires parallel programming skills

## Use Case Scenarios

### CPU-Optimized Tasks:
1. **Operating System Operations**
   - Process scheduling
   - File system operations
   - Device driver management

2. **Complex Algorithms**
   - Database queries with complex joins
   - Compiler optimization
   - Artificial intelligence decision trees

3. **Sequential Processing**
   - Single-threaded applications
   - Legacy software
   - Real-time system control

4. **Low-Latency Requirements**
   - Financial trading systems
   - Real-time communication
   - Interactive applications

### GPU-Optimized Tasks:
1. **Graphics Rendering**
   - 3D scene rasterization
   - Texture mapping
   - Pixel shading operations

2. **Scientific Computing**
   - Weather simulation
   - Molecular dynamics
   - Finite element analysis

3. **Machine Learning**
   - Neural network training
   - Matrix operations
   - Image recognition

4. **Cryptocurrency Mining**
   - Hash calculations
   - Cryptographic operations
   - Parallel proof-of-work

## Programming Models

### CPU Programming:
```c++
// Sequential processing
for(int i = 0; i < n; i++) {
    result[i] = complexFunction(data[i]);
}

// Multi-threading
#pragma omp parallel for
for(int i = 0; i < n; i++) {
    result[i] = simpleFunction(data[i]);
}
```

### GPU Programming (CUDA):
```c++
// GPU kernel
__global__ void processData(float* data, float* result, int n) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if(idx < n) {
        result[idx] = simpleFunction(data[idx]);
    }
}

// Launch kernel with thousands of threads
processData<<<blocks, threads>>>(data, result, n);
```

## Performance Comparison Examples

### Matrix Multiplication (1000x1000):
- **CPU (Single-threaded)**: ~2 seconds
- **CPU (Multi-threaded)**: ~0.3 seconds  
- **GPU (CUDA)**: ~0.02 seconds

### Image Processing (4K Image):
- **CPU**: 500ms for filter application
- **GPU**: 15ms for same filter

### Neural Network Training:
- **CPU**: Days to weeks for large models
- **GPU**: Hours to days for same models

## Future Trends

### CPU Evolution:
- **More Cores**: Increasing core counts
- **Heterogeneous Design**: Big.LITTLE architectures
- **AI Acceleration**: Built-in AI units
- **Improved Efficiency**: Better performance per watt

### GPU Evolution:
- **Ray Tracing**: Dedicated RT cores
- **AI Processing**: Tensor cores for machine learning
- **Memory Advances**: HBM, GDDR7 memory
- **Software Integration**: Better CPU-GPU cooperation

## Practical Exercise

### Benchmark Comparison:
1. **Setup**: Install GPU-Z and CPU-Z for hardware monitoring
2. **CPU Test**: Run Prime95 stress test, monitor single-core performance
3. **GPU Test**: Run FurMark or Unigine Heaven, monitor parallel performance
4. **Comparison**: Compare power consumption, temperature, and throughput

### Programming Challenge:
Write both CPU and GPU versions of a simple parallel algorithm (e.g., vector addition) and compare:
- **Development Time**: How long each took to implement
- **Performance**: Speed comparison on the same dataset
- **Scalability**: How performance changes with data size

## Assessment Questions:
1. Why do GPUs have thousands of simple cores instead of fewer complex cores?
2. What types of applications benefit most from GPU acceleration?
3. How does memory bandwidth affect GPU vs CPU performance?
4. What are the trade-offs between CPU and GPU architectures?
5. When would you choose CPU processing over GPU processing?
"""
            }
        ]
    },
    "quantum_computing": {
        "modules": [
            {
                "title": "Introduction to Quantum Computing",
                "content": """# Introduction to Quantum Computing

## What is Quantum Computing?

Quantum computing is a revolutionary computing paradigm that leverages the principles of **quantum mechanics** to process information in fundamentally different ways than classical computers. While classical computers use binary digits (bits) that exist in either 0 or 1 states, quantum computers use **quantum bits (qubits)** that can exist in multiple states simultaneously.

## Classical vs Quantum Information

### Classical Computing Principles:
- **Binary System**: Information stored as 0s and 1s
- **Deterministic**: Each operation produces a predictable result
- **Sequential Processing**: Operations performed one after another
- **Boolean Logic**: AND, OR, NOT gates

### Quantum Computing Principles:
- **Superposition**: Qubits can be 0, 1, or both simultaneously
- **Probabilistic**: Results are probabilistic, not deterministic
- **Parallel Processing**: Can process multiple possibilities at once
- **Quantum Logic**: Quantum gates manipulate qubit states

## Key Quantum Phenomena

### 1. Superposition
**Definition**: A quantum system can exist in multiple states simultaneously until measured.

**Classical Analogy**: Imagine a coin spinning in the air - it's neither heads nor tails until it lands. However, quantum superposition is more profound than this analogy suggests.

**Mathematical Representation**:
- A qubit state: |ψ⟩ = α|0⟩ + β|1⟩
- Where α and β are complex numbers (probability amplitudes)
- |α|² + |β|² = 1 (normalization condition)

**Example**: A qubit in superposition can be 50% |0⟩ and 50% |1⟩, written as:
|ψ⟩ = (1/√2)|0⟩ + (1/√2)|1⟩

### 2. Entanglement
**Definition**: Quantum particles become correlated such that the state of one particle instantly affects the state of another, regardless of distance.

**Einstein's "Spooky Action"**: Albert Einstein called this "spooky action at a distance" because it seemed to violate locality principles.

**Bell States**: The four maximally entangled two-qubit states:
- |Φ+⟩ = (1/√2)(|00⟩ + |11⟩)
- |Φ-⟩ = (1/√2)(|00⟩ - |11⟩)
- |Ψ+⟩ = (1/√2)(|01⟩ + |10⟩)
- |Ψ-⟩ = (1/√2)(|01⟩ - |10⟩)

**Applications**: Quantum cryptography, quantum teleportation, quantum error correction

### 3. Interference
**Definition**: Quantum states can interfere constructively or destructively, amplifying or canceling certain outcomes.

**Constructive Interference**: Probability amplitudes add up, increasing the likelihood of measuring a particular state
**Destructive Interference**: Probability amplitudes cancel out, reducing the likelihood of measuring a state

## Physical Implementations of Qubits

### 1. Superconducting Qubits
**Technology**: Used by IBM, Google, Rigetti
**Principle**: Josephson junctions in superconducting circuits
**Advantages**: Fast gate operations, scalable fabrication
**Disadvantages**: Requires extreme cooling (~0.01K)

**Example Systems**:
- IBM Quantum computers
- Google Sycamore processor
- Rigetti Aspen processors

### 2. Trapped Ion Qubits
**Technology**: Used by IonQ, Honeywell
**Principle**: Individual ions trapped in electromagnetic fields
**Advantages**: High fidelity, long coherence times
**Disadvantages**: Slower gate operations, complex control

**Example Systems**:
- IonQ quantum computers
- Honeywell System Model H1
- Alpine Quantum Technologies systems

### 3. Photonic Qubits
**Technology**: Used by Xanadu, PsiQuantum
**Principle**: Photons as qubits, manipulated with optical elements
**Advantages**: Room temperature operation, natural for communication
**Disadvantages**: Probabilistic gates, detection challenges

### 4. Topological Qubits
**Technology**: Under development by Microsoft
**Principle**: Anyons in topological materials
**Advantages**: Inherently error-resistant
**Disadvantages**: Still experimental, material challenges

## Quantum Gates and Circuits

### Single-Qubit Gates:

#### X Gate (Pauli-X / NOT Gate):
- **Matrix**: [[0,1],[1,0]]
- **Effect**: Flips |0⟩ ↔ |1⟩
- **Circuit Symbol**: ⊕

#### Y Gate (Pauli-Y):
- **Matrix**: [[0,-i],[i,0]]  
- **Effect**: |0⟩ → i|1⟩, |1⟩ → -i|0⟩

#### Z Gate (Pauli-Z):
- **Matrix**: [[1,0],[0,-1]]
- **Effect**: |0⟩ → |0⟩, |1⟩ → -|1⟩

#### Hadamard Gate (H):
- **Matrix**: (1/√2)[[1,1],[1,-1]]
- **Effect**: |0⟩ → (|0⟩+|1⟩)/√2, |1⟩ → (|0⟩-|1⟩)/√2
- **Purpose**: Creates superposition

### Two-Qubit Gates:

#### CNOT Gate (Controlled-X):
- **Control-Target**: Flips target if control is |1⟩
- **Matrix**: 4×4 matrix
- **Purpose**: Creates entanglement

#### CZ Gate (Controlled-Z):
- **Effect**: Applies Z gate to target if control is |1⟩
- **Purpose**: Phase operations

## Quantum Algorithms Overview

### 1. Grover's Algorithm
**Purpose**: Database search
**Speedup**: √N vs N for classical search
**Applications**: Optimization, cryptography

### 2. Shor's Algorithm  
**Purpose**: Integer factorization
**Speedup**: Exponential vs classical methods
**Impact**: Threatens current cryptography

### 3. Quantum Fourier Transform
**Purpose**: Frequency analysis
**Applications**: Period finding, phase estimation

### 4. Variational Quantum Eigensolver (VQE)
**Purpose**: Finding ground states of molecules
**Applications**: Drug discovery, materials science

## Current Limitations

### 1. Quantum Decoherence
**Problem**: Qubits lose quantum properties due to environmental noise
**Timeframes**: Microseconds to milliseconds
**Solutions**: Better isolation, error correction

### 2. Gate Fidelity
**Problem**: Quantum operations are imperfect
**Current State**: 99%+ for best single-qubit gates
**Target**: 99.9%+ needed for fault-tolerant computing

### 3. Limited Connectivity
**Problem**: Not all qubits can interact directly
**Impact**: Requires SWAP gates, increasing circuit depth
**Solutions**: Better architectures, routing algorithms

### 4. Classical Control
**Problem**: Need classical computers for control and measurement
**Bottleneck**: Classical-quantum interface

## Applications and Use Cases

### Near-Term Applications:
1. **Optimization Problems**
   - Portfolio optimization
   - Supply chain management
   - Traffic routing

2. **Machine Learning**
   - Quantum machine learning algorithms
   - Feature mapping
   - Classification problems

3. **Chemistry Simulation**
   - Molecular modeling
   - Drug discovery
   - Catalyst design

### Long-Term Applications:
1. **Cryptography Breaking**
   - RSA factorization
   - Elliptic curve cryptography
   - Impact on cybersecurity

2. **Weather Prediction**
   - Complex atmospheric modeling
   - Climate simulation
   - Improved accuracy

3. **Artificial Intelligence**
   - Quantum neural networks
   - Enhanced pattern recognition
   - Faster training algorithms

## Hands-On Exercise

### Quantum Circuit Simulator:
1. **Setup**: Use IBM Qiskit or Microsoft Q# simulator
2. **Create Circuit**: Build a simple Bell state preparation
3. **Run Simulation**: Execute multiple times to see probabilistic results
4. **Analyze**: Study the measurement statistics

### Bell State Creation:
```python
# Qiskit example
from qiskit import QuantumCircuit, execute, Aer

qc = QuantumCircuit(2, 2)
qc.h(0)        # Hadamard on qubit 0
qc.cx(0, 1)    # CNOT with control=0, target=1
qc.measure_all()

# Execute and analyze results
```

## Assessment Questions:
1. What makes quantum computing potentially more powerful than classical computing?
2. Explain superposition in your own words with an example.
3. How does quantum entanglement enable new computational capabilities?
4. What are the main challenges facing quantum computing today?
5. Name three potential applications of quantum computing and explain why quantum advantage might exist.

## Further Reading:
- "Quantum Computing: An Applied Approach" by Hidary
- IBM Qiskit Textbook (online)
- Microsoft Quantum Development Kit documentation
- "Programming Quantum Computers" by Johnston, Harrigan, and Gimeno-Segovia
"""
            },
            {
                "title": "Qubits and Quantum States",
                "content": """# Qubits and Quantum States

## Understanding the Qubit

A **qubit** (quantum bit) is the fundamental unit of quantum information, analogous to how a classical bit is the fundamental unit of classical information. However, qubits have properties that make them far more powerful and complex than classical bits.

### Classical Bit vs Quantum Bit

#### Classical Bit:
- **States**: 0 or 1 (mutually exclusive)
- **Representation**: Voltage levels, magnetic orientations
- **Operations**: Boolean logic (AND, OR, NOT)
- **Information**: 1 bit = 1 binary digit

#### Quantum Bit (Qubit):
- **States**: |0⟩, |1⟩, or superposition of both
- **Representation**: Quantum mechanical two-level systems
- **Operations**: Quantum gates (unitary transformations)
- **Information**: Can encode continuous parameters

## Mathematical Representation of Qubits

### Dirac Notation (Bra-Ket Notation)
Quantum states are written using **Dirac notation**:
- **Ket**: |ψ⟩ represents a quantum state
- **Bra**: ⟨ψ| represents the complex conjugate transpose
- **Bracket**: ⟨φ|ψ⟩ represents the inner product (probability amplitude)

### Basis States
The two basis states of a qubit are:
- **|0⟩**: Computational basis state "zero"
- **|1⟩**: Computational basis state "one"

In matrix representation:
- |0⟩ = [1, 0]ᵀ
- |1⟩ = [0, 1]ᵀ

### General Qubit State
Any qubit state can be written as:
**|ψ⟩ = α|0⟩ + β|1⟩**

Where:
- **α, β**: Complex numbers (probability amplitudes)
- **|α|² + |β|²= 1**: Normalization condition
- **|α|²**: Probability of measuring |0⟩
- **|β|²**: Probability of measuring |1⟩

### Examples of Qubit States:

#### 1. Computational Basis States:
- **|0⟩**: α = 1, β = 0
- **|1⟩**: α = 0, β = 1

#### 2. Equal Superposition:
- **|+⟩ = (1/√2)|0⟩ + (1/√2)|1⟩**
- Equal probability of measuring 0 or 1

#### 3. Equal Superposition with Phase:
- **|−⟩ = (1/√2)|0⟩ − (1/√2)|1⟩**
- Equal probability, but different phase relationship

#### 4. Unequal Superposition:
- **|ψ⟩ = (√3/2)|0⟩ + (1/2)|1⟩**
- 75% chance of measuring 0, 25% chance of measuring 1

## The Bloch Sphere

The **Bloch sphere** is a geometric representation of qubit states as points on a unit sphere.

### Bloch Sphere Parameterization:
**|ψ⟩ = cos(θ/2)|0⟩ + e^(iφ)sin(θ/2)|1⟩**

Where:
- **θ**: Polar angle (0 ≤ θ ≤ π)
- **φ**: Azimuthal angle (0 ≤ φ < 2π)
- **θ = 0**: North pole (|0⟩ state)
- **θ = π**: South pole (|1⟩ state)
- **θ = π/2**: Equatorial plane (superposition states)

### Key Points on Bloch Sphere:
- **North Pole**: |0⟩
- **South Pole**: |1⟩
- **+X axis**: |+⟩ = (|0⟩ + |1⟩)/√2
- **−X axis**: |−⟩ = (|0⟩ − |1⟩)/√2
- **+Y axis**: |i⟩ = (|0⟩ + i|1⟩)/√2
- **−Y axis**: |−i⟩ = (|0⟩ − i|1⟩)/√2

### Visualization Benefits:
- **Geometric Intuition**: Quantum operations as rotations
- **State Relationships**: Orthogonal states are antipodal points
- **Measurement**: Projection onto measurement axes
- **Evolution**: Smooth paths on the sphere surface

## Quantum Superposition

### Definition and Principle
**Superposition** is the ability of quantum systems to exist in multiple states simultaneously until measured.

### Mathematical Foundation:
If |ψ₁⟩ and |ψ₂⟩ are valid quantum states, then:
**|ψ⟩ = α|ψ₁⟩ + β|ψ₂⟩**
is also a valid quantum state (linearity of quantum mechanics).

### Key Properties:

#### 1. Coherent Superposition:
- Phase relationships between amplitudes matter
- Enables quantum interference effects
- Different from classical probability mixtures

#### 2. Measurement Collapse:
- Superposition exists only until measurement
- Measurement yields one definite outcome
- Post-measurement state is the measured eigenstate

#### 3. No-Cloning Theorem:
- Cannot create perfect copies of unknown quantum states
- Fundamental limitation of quantum information
- Basis for quantum cryptography security

### Examples in Nature:

#### 1. Electron Spin:
- Spin-up and spin-down superposition
- Measured by Stern-Gerlach experiments
- Foundation for many quantum technologies

#### 2. Photon Polarization:
- Horizontal and vertical polarization superposition
- Easily manipulated with optical elements
- Used in quantum communication

#### 3. Atomic Energy Levels:
- Superposition of energy eigenstates
- Creates atomic clocks precision
- Enables laser operation

## Multi-Qubit Systems

### Two-Qubit Systems:
A two-qubit system has four basis states:
- **|00⟩**: Both qubits in |0⟩
- **|01⟩**: First qubit |0⟩, second qubit |1⟩  
- **|10⟩**: First qubit |1⟩, second qubit |0⟩
- **|11⟩**: Both qubits in |1⟩

### General Two-Qubit State:
**|ψ⟩ = α₀₀|00⟩ + α₀₁|01⟩ + α₁₀|10⟩ + α₁₁|11⟩**

Where: |α₀₀|² + |α₀₁|² + |α₁₀|² + |α₁₁|² = 1

### Tensor Product Structure:
If two qubits are independent:
**|ψ⟩ = |ψ₁⟩ ⊗ |ψ₂⟩**

Example: (α|0⟩ + β|1⟩) ⊗ (γ|0⟩ + δ|1⟩) = αγ|00⟩ + αδ|01⟩ + βγ|10⟩ + βδ|11⟩

### Entangled States:
States that cannot be written as tensor products:
**Bell States**:
- |Φ⁺⟩ = (1/√2)(|00⟩ + |11⟩)
- |Φ⁻⟩ = (1/√2)(|00⟩ − |11⟩)
- |Ψ⁺⟩ = (1/√2)(|01⟩ + |10⟩)
- |Ψ⁻⟩ = (1/√2)(|01⟩ − |10⟩)

## Quantum Measurement

### Measurement Postulates:
1. **Observable**: Represented by Hermitian operators
2. **Outcomes**: Eigenvalues of the measurement operator
3. **Born Rule**: |⟨outcome|state⟩|² gives measurement probability
4. **State Update**: Post-measurement state is the corresponding eigenstate

### Computational Basis Measurement:
Measuring in the |0⟩, |1⟩ basis:
- **Measurement Operators**: M₀ = |0⟩⟨0|, M₁ = |1⟩⟨1|
- **Probabilities**: P(0) = |α|², P(1) = |β|²
- **Post-measurement States**: |0⟩ or |1⟩

### Other Measurement Bases:

#### X-Basis Measurement:
- **Basis**: |+⟩, |−⟩
- **Operators**: M₊ = |+⟩⟨+|, M₋ = |−⟩⟨−|

#### Y-Basis Measurement:  
- **Basis**: |i⟩, |−i⟩
- **Operators**: M₊ᵢ = |i⟩⟨i|, M₋ᵢ = |−i⟩⟨−i|

### Measurement Disturbance:
- Quantum measurement is fundamentally disturbing
- Cannot measure a quantum state without changing it
- Uncertainty principle: Cannot measure non-commuting observables simultaneously

## Physical Realizations of Qubits

### 1. Superconducting Transmon Qubits:

#### Structure:
- **Josephson Junctions**: Nonlinear inductors
- **Capacitive Coupling**: Energy storage
- **Microwave Control**: Gate operations via microwave pulses

#### Advantages:
- **Fast Gates**: Nanosecond operation times
- **Scalable Fabrication**: Semiconductor processing
- **Strong Coupling**: Easy to entangle

#### Challenges:
- **Short Coherence**: ~100 microseconds
- **Cooling Requirements**: mK temperatures
- **Crosstalk**: Unwanted interactions

### 2. Trapped Ion Qubits:

#### Structure:
- **Ion Species**: ⁴⁰Ca⁺, ¹⁷¹Yb⁺, ⁸⁸Sr⁺
- **Electromagnetic Traps**: Paul traps, Penning traps
- **Laser Control**: Precise frequency control

#### Advantages:
- **High Fidelity**: >99.9% gate fidelity
- **Long Coherence**: Seconds to minutes
- **Universal Gates**: Any two ions can interact

#### Challenges:
- **Slow Gates**: Microsecond timescales
- **Scalability**: Complex control systems
- **Heating**: Motional heating effects

### 3. Photonic Qubits:

#### Encoding:
- **Polarization**: Horizontal/vertical, diagonal/anti-diagonal
- **Path**: Different optical paths
- **Time-Bin**: Different arrival times

#### Advantages:
- **Room Temperature**: No cooling required
- **Low Decoherence**: Photons weakly interact
- **Network Ready**: Natural for communication

#### Challenges:
- **Probabilistic Gates**: Success probability < 1
- **Detection Efficiency**: Photon loss
- **Nonlinearity**: Weak photon-photon interactions

## Practical Exercise: Qubit State Analysis

### Exercise 1: State Probabilities
Given the state |ψ⟩ = (3/5)|0⟩ + (4/5)|1⟩:
1. Verify normalization
2. Calculate measurement probabilities
3. Find the Bloch sphere coordinates

### Exercise 2: Superposition Creation
Design a quantum circuit to create:
1. Equal superposition |+⟩
2. Unequal superposition with 80% probability of |0⟩
3. Complex superposition with phase π/4

### Exercise 3: Two-Qubit Analysis  
For the state |ψ⟩ = (1/2)|00⟩ + (1/2)|01⟩ + (1/√2)|10⟩:
1. Check if the state is properly normalized
2. Calculate single-qubit marginal probabilities  
3. Determine if the qubits are entangled

## Programming Example (Qiskit):

```python
from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
import numpy as np

# Create a qubit in superposition
qc = QuantumCircuit(1, 1)
qc.h(0)  # Hadamard gate creates |+⟩ state
qc.measure(0, 0)

# Execute and see probabilistic results
backend = Aer.get_backend('qasm_simulator')
result = execute(qc, backend, shots=1000).result()
counts = result.get_counts()
print(f"Measurement results: {counts}")

# Should show approximately 50% |0⟩ and 50% |1⟩
```

## Assessment Questions:

1. **Conceptual**: Explain why a qubit can store more information than a classical bit.

2. **Mathematical**: If |ψ⟩ = (1/√3)|0⟩ + (√2/√3)e^(iπ/4)|1⟩, what are the measurement probabilities?

3. **Geometric**: Where on the Bloch sphere would you find the state |ψ⟩ = (1/√2)|0⟩ - (i/√2)|1⟩?

4. **Practical**: How would you experimentally distinguish between the states |+⟩ and |0⟩?

5. **Critical Thinking**: Why can't we simply "read" the values of α and β in a qubit state |ψ⟩ = α|0⟩ + β|1⟩?

## Key Takeaways:
- Qubits are quantum mechanical two-level systems
- Superposition enables parallel computation possibilities  
- The Bloch sphere provides geometric intuition
- Measurement fundamentally disturbs quantum states
- Multiple physical platforms can implement qubits
- Mathematical formalism is essential for precise descriptions
"""
            }
        ]
    },
    # Add more course content for other courses...
    "ai_fundamentals": {
        "modules": [
            {
                "title": "Introduction to Artificial Intelligence",
                "content": """# Introduction to Artificial Intelligence

## What is Artificial Intelligence?

**Artificial Intelligence (AI)** is the field of computer science dedicated to creating systems that can perform tasks typically requiring human intelligence. These tasks include learning, reasoning, problem-solving, perception, language understanding, and decision-making.

### Historical Definition Evolution:

#### 1950s - The Turing Test:
Alan Turing proposed the **Turing Test** as a measure of machine intelligence:
- A machine is considered intelligent if a human evaluator cannot distinguish between human and machine responses in natural language conversations
- Still used today as a benchmark, though with recognized limitations

#### 1956 - Dartmouth Conference:
The term "Artificial Intelligence" was coined at the **Dartmouth Summer Research Project**:
- Organized by John McCarthy, Marvin Minsky, Nathaniel Rochester, and Claude Shannon
- Established AI as an academic discipline
- Optimistic predictions about achieving human-level AI within decades

#### Modern Definition:
AI encompasses systems that can:
- **Perceive** their environment
- **Process** information intelligently
- **Learn** from experience
- **Adapt** to new situations
- **Achieve** goals autonomously

## Types of Artificial Intelligence

### 1. Narrow AI (Weak AI)
**Current Reality**: All existing AI systems fall into this category.

**Characteristics**:
- Designed for specific tasks
- Cannot generalize beyond training domain
- Often surpass human performance in specialized areas
- No consciousness or self-awareness

**Examples**:
- **Chess Engines**: Deep Blue, Stockfish, AlphaZero
- **Image Recognition**: Google Photos, medical imaging systems
- **Language Translation**: Google Translate, DeepL
- **Recommendation Systems**: Netflix, Spotify, Amazon
- **Virtual Assistants**: Siri, Alexa, Google Assistant

### 2. General AI (Strong AI)
**Future Goal**: Human-level artificial general intelligence (AGI)

**Characteristics**:
- Human-level cognitive abilities across all domains
- Can understand, learn, and apply knowledge flexibly
- Transfer learning between different tasks
- Self-awareness and consciousness (potentially)

**Timeline Predictions**:
- **Optimistic**: 2030-2040
- **Moderate**: 2050-2070  
- **Conservative**: Beyond 2100
- **Skeptical**: May never be achieved

### 3. Superintelligence
**Speculative Future**: AI systems exceeding human intelligence in all areas

**Potential Characteristics**:
- Vastly superior to humans in creativity, problem-solving, and decision-making
- Could potentially improve itself recursively
- Raises significant philosophical and safety questions

## Core Approaches to AI

### 1. Symbolic AI (GOFAI - Good Old-Fashioned AI)

#### Principles:
- **Knowledge Representation**: Encode human knowledge in symbols and rules
- **Logical Reasoning**: Use formal logic to derive conclusions
- **Rule-Based Systems**: If-then rules guide decision making
- **Expert Systems**: Capture domain expert knowledge

#### Advantages:
- **Interpretable**: Clear reasoning chains
- **Precise**: Exact logical operations
- **Reliable**: Consistent behavior in defined domains
- **Debuggable**: Can trace decision processes

#### Limitations:
- **Brittle**: Fails outside programmed scenarios
- **Knowledge Acquisition Bottleneck**: Difficult to encode all relevant knowledge
- **Common Sense Problem**: Hard to represent everyday reasoning
- **Scalability Issues**: Exponential complexity growth

#### Historical Examples:
- **MYCIN** (1970s): Medical diagnosis expert system
- **DENDRAL** (1965): Chemical analysis system  
- **R1/XCON** (1980s): Computer configuration system

### 2. Machine Learning

#### Principles:
- **Data-Driven**: Learn patterns from examples rather than explicit programming
- **Statistical**: Use probabilistic and statistical methods
- **Adaptive**: Improve performance with more data
- **Generalization**: Apply learned patterns to new situations

#### Types of Machine Learning:

##### Supervised Learning:
- **Training Data**: Input-output pairs (labeled data)
- **Goal**: Learn mapping from inputs to outputs
- **Examples**: Classification, regression
- **Algorithms**: Linear regression, decision trees, neural networks, SVM

##### Unsupervised Learning:
- **Training Data**: Input data only (unlabeled)
- **Goal**: Discover hidden patterns or structure
- **Examples**: Clustering, dimensionality reduction, anomaly detection
- **Algorithms**: K-means, PCA, autoencoders, generative models

##### Reinforcement Learning:
- **Environment**: Agent interacts with environment
- **Feedback**: Receives rewards or penalties
- **Goal**: Learn optimal behavior through trial and error
- **Examples**: Game playing, robotics, autonomous systems
- **Algorithms**: Q-learning, policy gradients, actor-critic

### 3. Deep Learning

#### Principles:
- **Neural Networks**: Inspired by brain structure
- **Multiple Layers**: "Deep" architectures with many layers
- **Representation Learning**: Automatically learn relevant features
- **End-to-End Learning**: Learn entire mapping from raw inputs to outputs

#### Key Architectures:

##### Feedforward Networks:
- **Structure**: Layers connected in sequence
- **Data Flow**: Input → Hidden Layers → Output
- **Applications**: Basic classification and regression

##### Convolutional Neural Networks (CNNs):
- **Specialty**: Image processing and computer vision
- **Key Features**: Convolution, pooling, local connectivity
- **Applications**: Image recognition, medical imaging, autonomous vehicles

##### Recurrent Neural Networks (RNNs):
- **Specialty**: Sequential data processing
- **Key Features**: Memory, temporal dynamics
- **Variants**: LSTM, GRU
- **Applications**: Natural language processing, speech recognition, time series

##### Transformers:
- **Specialty**: Attention-based processing
- **Key Innovation**: Self-attention mechanism
- **Applications**: Language models (GPT, BERT), machine translation

## AI Application Domains

### 1. Computer Vision

#### Tasks:
- **Image Classification**: Categorizing entire images
- **Object Detection**: Locating and identifying objects
- **Semantic Segmentation**: Pixel-level image understanding
- **Face Recognition**: Identifying individuals
- **Medical Imaging**: Disease diagnosis from scans

#### Technologies:
- **Convolutional Neural Networks**
- **Transfer Learning**: Pre-trained models (ImageNet)
- **Data Augmentation**: Expanding training datasets
- **Real-time Processing**: Edge AI implementations

#### Applications:
- **Autonomous Vehicles**: Environmental perception
- **Healthcare**: Radiology, pathology assistance
- **Security**: Surveillance, access control
- **Manufacturing**: Quality control, defect detection
- **Agriculture**: Crop monitoring, pest detection

### 2. Natural Language Processing (NLP)

#### Tasks:
- **Language Understanding**: Parsing meaning from text
- **Language Generation**: Creating human-like text
- **Machine Translation**: Between different languages
- **Sentiment Analysis**: Determining emotional tone
- **Question Answering**: Extracting information from text

#### Technologies:
- **Transformer Models**: GPT, BERT, T5
- **Word Embeddings**: Word2Vec, GloVe
- **Sequence Models**: RNNs, LSTMs
- **Attention Mechanisms**: Focus on relevant information

#### Applications:
- **Virtual Assistants**: Siri, Alexa, Google Assistant
- **Content Creation**: Writing assistance, code generation
- **Customer Service**: Chatbots, automated support
- **Research**: Literature analysis, summarization
- **Education**: Language learning, tutoring systems

### 3. Robotics and Autonomous Systems

#### Challenges:
- **Sensor Fusion**: Combining multiple data sources
- **Real-time Decision Making**: Operating under time constraints
- **Physical Interaction**: Manipulating real-world objects
- **Safety and Reliability**: Critical system requirements

#### Applications:
- **Industrial Automation**: Manufacturing, assembly
- **Service Robots**: Cleaning, delivery, eldercare
- **Autonomous Vehicles**: Self-driving cars, drones
- **Space Exploration**: Mars rovers, satellite operations
- **Military and Defense**: Unmanned systems

### 4. Game Playing and Strategic Reasoning

#### Milestones:
- **1997**: Deep Blue defeats chess champion Garry Kasparov
- **2016**: AlphaGo defeats Go champion Lee Sedol
- **2019**: AlphaStar achieves Grandmaster level in StarCraft II
- **2022**: AI systems achieve superhuman performance in poker variants

#### Techniques:
- **Minimax Algorithm**: Game tree search
- **Monte Carlo Tree Search**: Probabilistic planning
- **Deep Reinforcement Learning**: Learning through self-play
- **Multi-agent Systems**: Modeling opponent behavior

## AI Development Process

### 1. Problem Definition
- **Identify Objectives**: What should the AI system accomplish?
- **Success Metrics**: How will you measure performance?
- **Constraints**: Time, computational resources, data availability
- **Ethical Considerations**: Fairness, privacy, safety implications

### 2. Data Collection and Preparation
- **Data Sources**: Identify relevant data streams
- **Data Quality**: Ensure accuracy, completeness, representativeness
- **Data Preprocessing**: Cleaning, normalization, feature engineering
- **Data Splitting**: Training, validation, test sets

### 3. Model Selection and Training
- **Algorithm Choice**: Based on problem type and data characteristics
- **Hyperparameter Tuning**: Optimizing model configuration
- **Training Process**: Iterative improvement through optimization
- **Validation**: Ensuring generalization to new data

### 4. Evaluation and Testing
- **Performance Metrics**: Accuracy, precision, recall, F1-score
- **Robustness Testing**: Performance under adversarial conditions
- **Bias Detection**: Identifying unfair treatment of different groups
- **Interpretability**: Understanding model decision-making

### 5. Deployment and Monitoring
- **Production Integration**: Incorporating AI into existing systems
- **Monitoring**: Tracking performance over time
- **Maintenance**: Updating models as data distributions change
- **Feedback Loops**: Continuous improvement processes

## Current Challenges and Limitations

### 1. Technical Challenges

#### Data Requirements:
- **Large Datasets**: Many ML algorithms require massive amounts of data
- **Data Quality**: Poor quality data leads to poor performance
- **Data Bias**: Historical biases embedded in training data
- **Data Privacy**: Protecting sensitive information during processing

#### Computational Resources:
- **Training Costs**: Large models require significant computational power
- **Energy Consumption**: Environmental impact of AI training
- **Infrastructure**: Need for specialized hardware (GPUs, TPUs)
- **Scalability**: Serving AI models to millions of users

#### Generalization:
- **Domain Transfer**: Models often fail when applied to new domains
- **Few-shot Learning**: Learning from limited examples
- **Robustness**: Performance degradation under adversarial conditions
- **Common Sense**: Lacking basic understanding of the world

### 2. Ethical and Societal Challenges

#### Bias and Fairness:
- **Algorithmic Bias**: Discriminatory outcomes for certain groups
- **Historical Bias**: Perpetuating past inequities
- **Representation Bias**: Underrepresentation in training data
- **Mitigation Strategies**: Fairness-aware machine learning

#### Privacy and Security:
- **Data Protection**: Safeguarding personal information
- **Adversarial Attacks**: Deliberately fooling AI systems
- **Model Theft**: Protecting intellectual property
- **Differential Privacy**: Mathematical privacy guarantees

#### Employment Impact:
- **Job Displacement**: Automation replacing human workers
- **Skill Gap**: Need for retraining and education
- **Economic Inequality**: Benefits concentrated among AI owners
- **New Job Creation**: Emerging roles in AI development and maintenance

### 3. Regulatory and Governance Challenges

#### AI Governance:
- **Regulatory Frameworks**: Need for appropriate oversight
- **International Coordination**: Cross-border AI governance
- **Standard Setting**: Technical and ethical standards
- **Accountability**: Determining responsibility for AI decisions

#### AI Safety:
- **Alignment Problem**: Ensuring AI systems pursue intended goals
- **Control Problem**: Maintaining human control over AI systems
- **Verification**: Proving AI systems behave as expected
- **Risk Assessment**: Understanding potential negative consequences

## Future Trends and Opportunities

### 1. Technical Advances

#### Foundation Models:
- **Large Language Models**: GPT, PaLM, Claude
- **Multimodal Models**: Combining text, images, audio
- **Few-shot Learning**: Learning new tasks with minimal examples
- **Transfer Learning**: Applying knowledge across domains

#### Edge AI:
- **Mobile Deployment**: AI on smartphones and IoT devices
- **Real-time Processing**: Low-latency applications
- **Privacy Preservation**: Processing data locally
- **Energy Efficiency**: Optimized for battery-powered devices

#### Quantum AI:
- **Quantum Machine Learning**: Leveraging quantum computing advantages
- **Hybrid Classical-Quantum**: Best of both computing paradigms
- **Quantum Simulation**: Modeling quantum systems
- **Cryptography**: Quantum-safe AI security

### 2. Application Areas

#### Healthcare:
- **Personalized Medicine**: Treatments tailored to individuals
- **Drug Discovery**: AI-designed pharmaceuticals
- **Diagnostics**: Earlier and more accurate disease detection
- **Mental Health**: AI-assisted therapy and monitoring

#### Climate and Environment:
- **Climate Modeling**: Better understanding of climate change
- **Clean Energy**: Optimizing renewable energy systems
- **Conservation**: Protecting endangered species and ecosystems
- **Sustainable Agriculture**: Precision farming techniques

#### Scientific Discovery:
- **Materials Science**: Discovering new materials with desired properties
- **Physics**: Understanding fundamental laws of nature
- **Biology**: Unraveling mysteries of life and evolution
- **Astronomy**: Analyzing vast amounts of observational data

## Hands-On Exercise: AI Problem Analysis

### Exercise 1: Problem Classification
Classify the following problems by AI approach (Symbolic, ML, DL):
1. Medical diagnosis based on symptoms
2. Image recognition in photos
3. Chess playing program
4. Speech recognition system
5. Expert system for tax preparation

### Exercise 2: Application Design
Design an AI system for a specific application:
1. **Choose a domain** (healthcare, education, transportation)
2. **Define the problem** clearly and specifically
3. **Select appropriate AI techniques**
4. **Identify data requirements**
5. **Consider ethical implications**
6. **Outline evaluation metrics**

### Exercise 3: Future Impact Analysis
Analyze the potential impact of AI in a specific industry:
1. **Current state**: How is AI currently used?
2. **Barriers**: What prevents wider adoption?
3. **Opportunities**: Where could AI have the biggest impact?
4. **Timeline**: When might these changes occur?
5. **Societal implications**: Who benefits and who might be harmed?

## Assessment Questions:

1. **Historical Understanding**: Compare and contrast the goals of AI research in the 1950s versus today. What has changed and what remains the same?

2. **Technical Comparison**: Explain the fundamental differences between symbolic AI and machine learning approaches. Give examples of problems best suited for each approach.

3. **Application Analysis**: Choose a specific AI application (e.g., autonomous vehicles, medical diagnosis) and analyze:
   - What AI techniques are involved?
   - What are the main technical challenges?
   - What are the societal implications?

4. **Critical Thinking**: Discuss the current limitations of AI systems. Which limitations do you think are most important to address, and why?

5. **Future Speculation**: What do you think will be the most significant AI development in the next 10 years? Justify your prediction with current trends and research directions.

## Key Takeaways:

- **AI encompasses multiple approaches**: Symbolic reasoning, machine learning, and deep learning each have strengths and limitations
- **Current AI is narrow**: All existing systems are specialized for specific tasks
- **Data is crucial**: The quality and quantity of data largely determines AI system performance  
- **Ethical considerations are paramount**: Bias, privacy, and societal impact must be considered
- **AI is a tool**: Success depends on appropriate application to suitable problems
- **Interdisciplinary field**: Combines computer science, mathematics, cognitive science, and domain expertise
- **Rapid evolution**: The field changes quickly, requiring continuous learning and adaptation

## Further Reading:
- "Artificial Intelligence: A Modern Approach" by Stuart Russell and Peter Norvig
- "The Master Algorithm" by Pedro Domingos
- "Human Compatible" by Stuart Russell  
- "Weapons of Math Destruction" by Cathy O'Neil
- AI research papers from conferences like NeurIPS, ICML, AAAI
"""
            }
        ]
    }
}

async def enhance_courses():
    """Enhance course content with comprehensive educational material"""
    # Connect to MongoDB
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.edtech_platform
    courses_collection = db.courses
    
    # Update courses with enhanced content
    enhanced_count = 0
    
    # Get all courses
    courses = await courses_collection.find({}).to_list(length=None)
    
    for course in courses:
        course_id = str(course['_id'])
        
        # Check if this course has enhanced content available
        enhanced_modules = None
        
        # Map course titles to enhanced content
        course_title = course.get('title', '').lower()
        if 'graphics' in course_title and 'evolution' in course_title:
            enhanced_modules = ENHANCED_CONTENT['graphics_evolution']['modules']
        elif 'quantum' in course_title:
            enhanced_modules = ENHANCED_CONTENT['quantum_computing']['modules']
        elif 'ai' in course_title or 'artificial intelligence' in course_title:
            enhanced_modules = ENHANCED_CONTENT['ai_fundamentals']['modules']
        
        if enhanced_modules and course.get('modules'):
            # Update first few modules with enhanced content
            modules = course['modules']
            for i, enhanced_module in enumerate(enhanced_modules):
                if i < len(modules):
                    modules[i].update({
                        'title': enhanced_module['title'],
                        'content': enhanced_module['content'],
                        'duration_minutes': len(enhanced_module['content']) // 50  # Estimate reading time
                    })
            
            # Update the course in database
            await courses_collection.update_one(
                {'_id': course['_id']},
                {'$set': {'modules': modules}}
            )
            
            enhanced_count += 1
            print(f"Enhanced course: {course.get('title')}")
    
    print(f"\nTotal courses enhanced: {enhanced_count}")
    client.close()

if __name__ == "__main__":
    asyncio.run(enhance_courses())
