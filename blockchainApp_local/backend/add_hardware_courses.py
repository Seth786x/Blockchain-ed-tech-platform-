#!/usr/bin/env python3
"""
Add comprehensive hardware component courses with detailed readable content
Creates 2 courses per hardware component (16 total courses)
"""

from pymongo import MongoClient
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

# Hardware component courses data with comprehensive content
HARDWARE_COURSES = [
    # CPU COURSES
    {
        "title": "CPU Architecture Deep Dive",
        "description": "Master CPU design principles from instruction sets to microarchitecture, exploring Intel and AMD processors",
        "category": "CPU & Processors",
        "difficulty": "advanced",
        "duration": "12 weeks",
        "instructor": "CPU Architecture Team",
        "price": 0.000005,
        "is_featured": True,
        "modules": [
            {
                "title": "Introduction to CPU Fundamentals",
                "description": "Basic CPU operation, instruction cycles, and processor components",
                "content": """# Introduction to CPU Fundamentals

## What is a CPU?

The Central Processing Unit (CPU) is often called the "brain" of a computer. It's responsible for executing instructions and performing calculations that drive all computer operations.

### Key CPU Components:

**1. Control Unit (CU)**
- Manages instruction flow
- Coordinates operations between components
- Handles branching and jumps
- Controls timing signals

**2. Arithmetic Logic Unit (ALU)**
- Performs mathematical operations (addition, subtraction, multiplication, division)
- Handles logical operations (AND, OR, NOT, XOR)
- Compares values for decision making
- Processes both integer and floating-point operations

**3. Registers**
- High-speed storage locations within the CPU
- Store temporary data and instructions
- Include program counter, instruction register, and general-purpose registers
- Provide fastest data access (faster than cache or RAM)

**4. Cache Memory**
- Small, fast memory integrated into the CPU
- Stores frequently accessed data and instructions
- Multiple levels: L1 (fastest, smallest), L2, L3 (largest, shared)
- Reduces memory latency significantly

## CPU Operation Cycle

Every CPU operation follows the fetch-decode-execute cycle:

### 1. Fetch
- Retrieve instruction from memory
- Program counter points to next instruction
- Instruction loaded into instruction register

### 2. Decode
- Control unit interprets the instruction
- Determines what operation to perform
- Identifies required operands and destination

### 3. Execute
- ALU performs the actual operation
- Results stored in registers or memory
- Flags updated to reflect operation status

### 4. Store
- Write results back to memory if needed
- Update program counter for next instruction
- Handle any exceptions or interrupts

## Real-World Applications

Understanding CPU fundamentals helps you:
- Choose the right processor for specific tasks
- Optimize software for better performance
- Troubleshoot system performance issues
- Make informed upgrade decisions

Modern CPUs handle billions of these cycles per second, making complex software operations possible.""",
                "order": 1
            },
            {
                "title": "Instruction Set Architectures (ISA)",
                "description": "x86, ARM, RISC-V and other instruction sets that define how CPUs communicate with software",
                "content": """# Instruction Set Architectures (ISA)

## What is an Instruction Set Architecture?

An Instruction Set Architecture (ISA) is the interface between hardware and software. It defines:
- Available instructions the CPU can execute
- Data types and formats
- Addressing modes
- Register organization
- Memory architecture

## Major ISA Families

### x86 Architecture
**History**: Developed by Intel in 1978, evolved through 8086, 80286, 80386, to modern x86-64
**Characteristics**:
- Complex Instruction Set Computing (CISC)
- Variable-length instructions
- Rich addressing modes
- Backward compatibility maintained for decades

**Key Features**:
- Support for 8, 16, 32, and 64-bit operations
- Extensive instruction set (over 1000 instructions)
- Segmented memory model (legacy)
- Hardware support for virtual memory

**Modern x86-64 Extensions**:
- SSE (Streaming SIMD Extensions) for multimedia
- AVX (Advanced Vector Extensions) for parallel processing
- AES-NI for encryption acceleration
- Intel Memory Protection Extensions (MPX)

### ARM Architecture
**History**: Originally Acorn RISC Machine, now Advanced RISC Machine
**Characteristics**:
- Reduced Instruction Set Computing (RISC)
- Fixed-length instructions (32-bit in ARM, 16/32-bit in Thumb)
- Load-store architecture
- Energy efficiency focus

**Key Features**:
- Conditional execution on most instructions
- Barrel shifter for efficient bit manipulation
- Multiple processor modes (User, System, Supervisor, etc.)
- Thumb instruction set for code density

**ARM Versions**:
- ARMv7: 32-bit, includes Cortex-A series
- ARMv8: 64-bit (AArch64) with 32-bit compatibility
- ARMv9: Latest with enhanced security and AI features

### RISC-V Architecture
**Philosophy**: Open-source, modular ISA design
**Characteristics**:
- Base integer instruction set (RV32I, RV64I)
- Optional extensions (M, A, F, D, C)
- Clean slate design avoiding legacy issues

**Advantages**:
- No licensing fees or restrictions
- Customizable for specific applications
- Growing ecosystem support
- Academic and research friendly

## ISA Design Principles

### CISC (Complex Instruction Set Computing)
**Philosophy**: Hardware handles complexity, software stays simple
**Advantages**:
- Reduced code size
- Complex operations in single instructions
- Better memory utilization (historically)

**Disadvantages**:
- Complex hardware design
- Variable execution times
- Harder to optimize and pipeline

### RISC (Reduced Instruction Set Computing)
**Philosophy**: Simple instructions, sophisticated compiler
**Advantages**:
- Simpler hardware design
- Consistent execution times
- Easier pipelining and optimization
- Better performance per transistor

**Disadvantages**:
- More instructions needed for complex operations
- Larger code size
- Heavier reliance on compiler optimization

## Impact on Software Development

Understanding ISAs helps developers:
- Write more efficient code
- Choose appropriate target architectures
- Optimize for specific platforms
- Understand performance characteristics

## Future Trends

**Specialized Instructions**: AI acceleration, cryptography, compression
**Custom ISAs**: Domain-specific architectures for IoT, edge computing
**Heterogeneous Computing**: Multiple ISAs on same platform""",
                "order": 2
            },
            {
                "title": "CPU Microarchitecture",
                "description": "Internal CPU design including pipelines, superscalar execution, and branch prediction",
                "content": """# CPU Microarchitecture

## Understanding Microarchitecture

While ISA defines what a CPU can do, microarchitecture defines how it does it internally. Modern CPUs use sophisticated designs to execute instructions efficiently.

## Pipelining

### Basic Pipeline Concepts
Pipelining breaks instruction execution into stages, allowing multiple instructions to be processed simultaneously.

**Classic 5-Stage Pipeline**:
1. **Instruction Fetch (IF)**: Get instruction from memory
2. **Instruction Decode (ID)**: Interpret instruction and read registers
3. **Execute (EX)**: Perform operation in ALU
4. **Memory Access (MEM)**: Read/write data memory
5. **Write Back (WB)**: Store results in registers

### Pipeline Hazards
**Structural Hazards**: Resource conflicts
**Data Hazards**: Instructions depend on previous results
**Control Hazards**: Branch instructions change program flow

**Solutions**:
- Forwarding/Bypassing for data hazards
- Branch prediction for control hazards
- Pipeline stalling when necessary

## Superscalar Architecture

### Multiple Execution Units
Modern CPUs have multiple functional units operating in parallel:
- Integer ALUs
- Floating-point units
- Load/store units
- Branch units

### Instruction-Level Parallelism (ILP)
CPUs analyze instructions to find opportunities for parallel execution:
- **Static scheduling**: Compiler arranges instructions
- **Dynamic scheduling**: Hardware reorders during execution

## Out-of-Order Execution

### Reorder Buffer
- Instructions executed when operands available
- Results stored temporarily
- In-order retirement maintains program correctness

### Register Renaming
- Eliminates false dependencies
- More physical registers than architectural
- Allows more parallel execution

## Branch Prediction

### Why Branch Prediction Matters
- Branches occur every 4-7 instructions on average
- Wrong predictions cause pipeline flushes
- Critical for maintaining high performance

### Prediction Techniques
**Static Prediction**: 
- Always predict taken/not taken
- Compiler hints
- Simple but limited accuracy

**Dynamic Prediction**:
- Branch history tables
- Two-level adaptive predictors
- Correlating predictors
- Neural predictors

**Advanced Techniques**:
- Tournament predictors (combine multiple methods)
- Indirect branch prediction
- Return address stack for function calls

## Cache Hierarchy

### Cache Levels
**L1 Cache**: 
- Fastest, smallest (16-64KB per core)
- Split instruction and data caches
- 1-2 cycle access time

**L2 Cache**: 
- Larger (256KB-1MB per core)
- Unified or separate I/D
- 3-8 cycle access time

**L3 Cache**: 
- Shared among cores (8-32MB)
- 12-30 cycle access time
- Reduces memory bandwidth pressure

### Cache Coherency
In multi-core systems, caches must maintain consistency:
- **MESI Protocol**: Modified, Exclusive, Shared, Invalid
- **Directory-based**: Centralized coherency information
- **Snooping**: Monitors bus transactions

## Modern Microarchitecture Examples

### Intel Core Architecture
- Wide superscalar design (4+ instructions per cycle)
- Deep out-of-order execution
- Advanced branch prediction
- Hyper-Threading for SMT

### AMD Zen Architecture
- Modular chiplet design
- Unified scheduler design
- Improved branch prediction
- Higher core counts

### ARM Cortex-A Series
- In-order and out-of-order variants
- Energy efficiency focus
- Heterogeneous big.LITTLE designs

## Performance Metrics

**Instructions Per Cycle (IPC)**: Measure of architectural efficiency
**Clock Speed**: Raw execution frequency
**Thermal Design Power (TDP)**: Heat and power constraints
**Performance per Watt**: Efficiency metric

Understanding microarchitecture helps in:
- Performance tuning
- Selecting appropriate processors
- Writing cache-friendly code
- Optimizing parallel algorithms""",
                "order": 3
            }
        ]
    },
    {
        "title": "CPU Performance and Benchmarking",
        "description": "Learn to evaluate CPU performance, understand benchmarks, and optimize processor selection for different workloads",
        "category": "CPU & Processors", 
        "difficulty": "intermediate",
        "duration": "8 weeks",
        "instructor": "Performance Analysis Team",
        "price": 0.000005,
        "is_featured": False,
        "modules": [
            {
                "title": "CPU Performance Fundamentals",
                "description": "Understanding factors that affect CPU performance and how to measure them",
                "content": """# CPU Performance Fundamentals

## What Determines CPU Performance?

CPU performance is a complex interaction of multiple factors. Understanding these helps make informed decisions about processors and system optimization.

## Primary Performance Factors

### 1. Clock Speed (Frequency)
**Definition**: Number of cycles per second, measured in Hertz (Hz)
- Modern CPUs: 2-5 GHz typical
- Higher frequency ≠ always better performance
- Limited by power consumption and heat generation

**Clock Speed Evolution**:
- 1980s: MHz range
- 1990s-2000s: GHz range achieved
- 2000s-present: Focus shifted to efficiency over raw speed

### 2. Instructions Per Cycle (IPC)
**Definition**: Average number of instructions completed per clock cycle
- More important than raw frequency
- Improved through better microarchitecture
- Varies significantly between CPU designs

**IPC Improvements**:
- Pipelining: Multiple instructions in flight
- Superscalar: Multiple execution units
- Out-of-order execution: Optimal instruction scheduling

### 3. Core Count and Threading
**Core Count**: Number of independent processing units
- Single-core → Multi-core evolution
- More cores = better parallel performance
- Diminishing returns without parallel software

**Simultaneous Multithreading (SMT)**:
- Intel Hyper-Threading
- AMD SMT
- 2 threads per core typical
- ~20-30% performance improvement

### 4. Cache Performance
**Cache Hierarchy Impact**:
- L1 Cache: Fastest access, most critical
- L2/L3 Cache: Reduces memory latency
- Cache misses cause significant slowdowns

**Cache-Friendly Programming**:
- Locality of reference
- Sequential data access
- Appropriate data structures

## Performance Measurement

### 1. Synthetic Benchmarks
**CPU-Z Benchmark**: Simple integer performance
**Cinebench**: Rendering workload simulation
**Geekbench**: Multi-platform comparison
**SPEC CPU**: Industry standard suite

### 2. Real-World Workloads
**Gaming**: Frame rates, minimum FPS
**Content Creation**: Encoding times, render speeds
**Productivity**: Application launch times, responsiveness
**Scientific Computing**: Calculation throughput

### 3. Power Efficiency
**Performance per Watt**: Critical for mobile and datacenter
**Thermal Design Power (TDP)**: Heat generation limits
**Dynamic power scaling**: Boost vs. base clocks

## Benchmark Types and Applications

### Integer Performance
- General computing tasks
- System responsiveness
- Basic calculations
- Control flow operations

**Key Benchmarks**:
- Dhrystone (legacy but still referenced)
- CoreMark (embedded systems)
- SPEC CINT (comprehensive suite)

### Floating-Point Performance
- Scientific computing
- Graphics rendering
- Signal processing
- Financial modeling

**Key Benchmarks**:
- Linpack (linear algebra)
- SPEC CFP (floating-point suite)
- Whetstone (legacy floating-point)

### Memory Performance
- Memory bandwidth utilization
- Cache hierarchy effectiveness
- Memory latency impact

**Key Benchmarks**:
- STREAM (memory bandwidth)
- LMbench (memory latency)
- Memory latency checker tools

## Workload-Specific Considerations

### Gaming Performance
**Factors**:
- Single-threaded performance still important
- GPU bottleneck more common
- Memory speed impact on frame rates
- Background task impact

**Optimization**:
- Higher frequency over more cores
- Fast memory (DDR4-3200+ or DDR5)
- Good single-core IPC

### Content Creation
**Video Encoding**:
- Highly multi-threaded
- AVX instructions beneficial
- Memory bandwidth important
- Hardware acceleration (QuickSync, NVENC)

**3D Rendering**:
- Scales well with core count
- Memory capacity for complex scenes
- Cache performance for ray tracing

### Productivity Workloads
**Office Applications**:
- Single-threaded performance
- Quick responsiveness
- Efficient idle power

**Development/Compilation**:
- Multi-threaded builds
- Fast storage more important
- Memory for large projects

## Comparing CPU Performance

### Performance per Dollar
- Total cost of ownership
- Platform costs (motherboard, memory)
- Longevity and upgrade path

### Performance per Watt
- Operating costs
- Cooling requirements
- Battery life (laptops)

### Platform Considerations
- Socket compatibility
- Memory support
- PCIe lanes
- Integrated graphics

## Common Performance Pitfalls

### 1. Over-Focusing on Clock Speed
Modern marketing often emphasizes frequency, but IPC and architecture matter more.

### 2. Ignoring Thermal Throttling
High-performance CPUs may throttle under sustained loads.

### 3. Mismatched Components
CPU bottlenecking GPU or vice versa.

### 4. Inadequate Cooling
Thermal throttling reduces performance significantly.

## Future Performance Trends

**More Cores**: Continued core count increases
**Specialized Units**: AI accelerators, crypto engines
**3D Stacking**: Vertical integration
**Advanced Materials**: Beyond silicon limitations

Understanding CPU performance helps in:
- Selecting appropriate hardware
- Optimizing system configurations
- Writing performance-conscious code
- Planning system upgrades""",
                "order": 1
            }
        ]
    },
    
    # GPU COURSES  
    {
        "title": "Modern GPU Architecture",
        "description": "Comprehensive exploration of graphics processing unit design, from rendering pipelines to compute acceleration",
        "category": "GPU & Graphics",
        "difficulty": "advanced", 
        "duration": "10 weeks",
        "instructor": "Graphics Architecture Team",
        "price": 0.000005,
        "is_featured": True,
        "modules": [
            {
                "title": "GPU Fundamentals and Evolution",
                "description": "History of GPUs from basic graphics accelerators to parallel computing powerhouses",
                "content": """# GPU Fundamentals and Evolution

## What is a GPU?

A Graphics Processing Unit (GPU) is a specialized electronic circuit designed to rapidly manipulate and alter memory to accelerate the creation of images in a frame buffer intended for output to a display device.

## GPU vs CPU Architecture

### CPU Design Philosophy
- Optimized for low-latency access to cached data sets
- Control logic for out-of-order and speculative execution
- Powerful ALUs for complex operations
- Large caches to reduce memory latency

### GPU Design Philosophy  
- Optimized for data-parallel, throughput computation
- Architecture built around executing thousands of threads
- Relatively simple control logic
- Memory bandwidth over low latency

## Historical Evolution

### Era 1: Fixed-Function Graphics (1990s)
**Characteristics**:
- Hardware-accelerated specific graphics operations
- 2D acceleration, basic 3D primitives
- No programmable shaders

**Notable Cards**:
- 3dfx Voodoo Graphics (1996)
- NVIDIA RIVA 128 (1997)
- ATI Rage series

**Limitations**:
- Inflexible rendering pipeline
- Limited to predefined effects
- Poor general-purpose computing capability

### Era 2: Programmable Shaders (2000s)
**DirectX 8/9 Era (2001-2004)**:
- Vertex shaders (geometry processing)
- Pixel shaders (per-pixel effects)
- Still separate functional units

**DirectX 10/11 Era (2006-2009)**:
- Unified shader architecture
- Geometry shaders
- Compute shaders introduction

**Key Innovations**:
- NVIDIA GeForce 3 (first programmable GPU)
- ATI Radeon 9700 (advanced pixel shaders)
- Unified architecture in Xbox 360 GPU

### Era 3: GPGPU and Parallel Computing (2007-present)
**CUDA Introduction (2007)**:
- NVIDIA's parallel computing platform
- C-like programming language
- General-purpose computing on GPUs

**OpenCL Standard (2009)**:
- Cross-platform parallel computing
- CPU and GPU code execution
- Industry-wide adoption

## Modern GPU Architecture

### Streaming Multiprocessors (SMs)
**NVIDIA Terminology**:
- Basic processing unit
- Contains multiple CUDA cores
- Shared memory and registers
- Thread scheduling logic

**AMD Terminology**:
- Compute Units (CUs)
- Stream Processors
- Similar concept, different implementation

### Memory Hierarchy

**1. Registers**
- Private to each thread
- Fastest access (1 cycle)
- Limited capacity per thread

**2. Shared Memory** 
- Shared among thread block/workgroup
- Low latency (few cycles)
- Manually managed cache

**3. Global Memory**
- Accessible by all threads
- High capacity (GB range)
- Higher latency (hundreds of cycles)

**4. Constant Memory**
- Read-only for kernels
- Cached and optimized for broadcast
- Good for parameters shared across threads

### Thread Execution Model

**Threads and Thread Blocks**:
- Thousands of lightweight threads
- Grouped into blocks/workgroups
- Blocks scheduled on SMs

**Warps and Wavefronts**:
- 32 threads (NVIDIA warp) or 64 threads (AMD wavefront)
- Execute in lockstep (SIMD)
- Branch divergence causes serialization

## GPU Programming Models

### Graphics Pipeline Programming
**Vertex Shaders**:
- Process vertex data
- Transform coordinates
- Lighting calculations per vertex

**Fragment/Pixel Shaders**:
- Process each pixel/fragment
- Texturing and lighting
- Per-pixel effects

**Geometry Shaders**:
- Process primitives
- Generate new geometry
- Tessellation control

### Compute Programming
**CUDA (NVIDIA)**:
- C++ with extensions
- Rich development ecosystem
- Extensive library support

**OpenCL (Cross-platform)**:
- Industry standard
- CPU and GPU execution
- More verbose syntax

**DirectCompute (Microsoft)**:
- Windows/Xbox platform
- DirectX integration
- Graphics and compute interop

## Performance Characteristics

### Throughput vs Latency
**GPU Strengths**:
- High throughput for parallel work
- Excellent memory bandwidth utilization
- Efficient for SIMD operations

**GPU Weaknesses**:
- High latency for individual operations
- Poor performance for serial algorithms
- Context switching overhead

### Memory Bandwidth
Modern GPUs provide 500+ GB/s memory bandwidth:
- HBM (High Bandwidth Memory)
- GDDR6/6X memory
- Wide memory interfaces (384-bit+)

## Applications Beyond Graphics

### Scientific Computing
- Computational fluid dynamics
- Molecular dynamics
- Climate modeling
- N-body simulations

### Machine Learning
- Neural network training
- Deep learning inference
- Tensor operations
- Parallel matrix multiplication

### Cryptocurrency
- Mining algorithms
- Proof-of-work calculations
- Hash function acceleration

### Video Processing
- Video encoding/decoding
- Real-time video effects
- Streaming optimization

## Modern GPU Examples

### NVIDIA Ada Lovelace (RTX 40 series)
- 4nm process technology
- 3rd gen RT cores for ray tracing
- 4th gen Tensor cores for AI
- AV1 encoding support

### AMD RDNA 3 (RX 7000 series)
- 5nm process technology
- Chiplet design approach
- Enhanced compute units
- DisplayPort 2.1 support

### Apple M1/M2 GPU
- Unified memory architecture
- Tile-based deferred rendering
- Energy efficiency focus
- Custom ISA design

## Future Trends

**Ray Tracing Hardware**: Real-time photorealistic rendering
**AI Acceleration**: Dedicated tensor/matrix units  
**Chiplet Designs**: Modular GPU construction
**Advanced Memory**: HBM3, processing-in-memory
**Quantum-Classical Hybrid**: Emerging computing paradigms

Understanding GPU architecture enables:
- Efficient parallel algorithm design
- Performance optimization strategies
- Appropriate hardware selection
- Future technology adoption""",
                "order": 1
            }
        ]
    },
    {
        "title": "GPU Computing and CUDA Programming", 
        "description": "Master parallel programming with CUDA, OpenCL, and GPU acceleration for scientific computing and AI",
        "category": "GPU & Graphics",
        "difficulty": "advanced",
        "duration": "12 weeks", 
        "instructor": "CUDA Development Team",
        "price": 0.000005,
        "is_featured": False,
        "modules": [
            {
                "title": "Introduction to Parallel Computing",
                "description": "Fundamental concepts of parallel programming and GPU computing paradigms",
                "content": """# Introduction to Parallel Computing

## Why Parallel Computing?

As CPU clock speeds have plateaued, parallel computing has become essential for achieving higher performance. GPUs offer massive parallelism for suitable workloads.

## Parallel Computing Concepts

### Types of Parallelism

**1. Task Parallelism**
- Different tasks executed simultaneously
- Heterogeneous workloads
- Pipeline parallelism
- Example: Audio processing while rendering graphics

**2. Data Parallelism** 
- Same operation on multiple data elements
- SIMD (Single Instruction, Multiple Data)
- Most suitable for GPUs
- Example: Applying filter to image pixels

**3. Pipeline Parallelism**
- Different stages of computation overlap
- Assembly line approach
- Graphics rendering pipeline
- Example: Vertex → Geometry → Rasterization → Fragment

### Flynn's Taxonomy

**SISD**: Single Instruction, Single Data (traditional CPU)
**SIMD**: Single Instruction, Multiple Data (GPU cores, vector units)
**MISD**: Multiple Instruction, Single Data (rare)
**MIMD**: Multiple Instruction, Multiple Data (multi-core CPUs)

## GPU Parallel Programming Model

### Thread Hierarchy

**Thread**: Basic execution unit
- Executes kernel code
- Has private registers and memory
- Lightweight creation/destruction

**Thread Block** (CUDA) / **Work Group** (OpenCL):
- Collection of threads
- Share memory and synchronization
- Scheduled as unit on SM/CU

**Grid**: Collection of thread blocks
- Entire kernel launch
- Can span multiple SMs/CUs
- No synchronization between blocks

### Memory Model

**Thread-Level**: Registers, local memory
**Block-Level**: Shared memory
**Grid-Level**: Global memory, constant memory
**Application-Level**: Host memory

### Execution Model

**Kernel Launch**: Host initiates GPU computation
**Thread Scheduling**: Hardware manages thread execution
**Synchronization**: Within blocks, not between blocks
**Memory Management**: Explicit data transfer

## CUDA Programming Basics

### CUDA Kernel Syntax
```cpp
__global__ void vectorAdd(float* A, float* B, float* C, int N) {
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    if (idx < N) {
        C[idx] = A[idx] + B[idx];
    }
}
```

### Kernel Launch
```cpp
dim3 blockSize(256);
dim3 gridSize((N + blockSize.x - 1) / blockSize.x);
vectorAdd<<<gridSize, blockSize>>>(d_A, d_B, d_C, N);
```

### Memory Management
```cpp
// Allocate GPU memory
float* d_A;
cudaMalloc(&d_A, size * sizeof(float));

// Copy data to GPU
cudaMemcpy(d_A, h_A, size * sizeof(float), cudaMemcpyHostToDevice);

// Copy results back
cudaMemcpy(h_C, d_C, size * sizeof(float), cudaMemcpyDeviceToHost);

// Free GPU memory
cudaFree(d_A);
```

## Performance Considerations

### Memory Access Patterns

**Coalesced Access**: Threads access consecutive memory
- Optimal memory bandwidth utilization
- Hardware combines transactions
- Critical for performance

**Non-Coalesced Access**: Random or strided access
- Reduced bandwidth utilization
- Multiple memory transactions
- Performance penalty

### Thread Divergence

**Warp Execution**: 32 threads execute in lockstep
**Branch Divergence**: Different threads take different paths
- Serializes execution
- Reduces occupancy
- Algorithmic consideration needed

### Occupancy Optimization

**Active Warps**: Number of warps per SM
**Resource Limits**: Registers, shared memory
**Block Size**: Affects occupancy and efficiency
**Memory Bandwidth**: Often the bottleneck

## Common Parallel Patterns

### 1. Map Pattern
Apply operation to each element independently
```cpp
// Square each element
output[i] = input[i] * input[i];
```

### 2. Reduce Pattern
Combine all elements into single result
```cpp
// Sum reduction
for (int stride = blockDim.x/2; stride > 0; stride >>= 1) {
    if (threadIdx.x < stride) {
        sdata[threadIdx.x] += sdata[threadIdx.x + stride];
    }
    __syncthreads();
}
```

### 3. Scan Pattern
Compute prefix sums
```cpp
// Exclusive scan implementation
// Complex algorithm with multiple phases
```

### 4. Stencil Pattern
Update elements based on neighbors
```cpp
// 2D stencil operation
output[i][j] = input[i-1][j] + input[i+1][j] + 
               input[i][j-1] + input[i][j+1];
```

## Debugging and Profiling

### CUDA Debugging Tools
**cuda-gdb**: Command-line debugger
**Nsight Compute**: Kernel profiling
**Nsight Systems**: System-wide analysis
**CUDA-MEMCHECK**: Memory error detection

### Performance Analysis
**Occupancy Calculator**: Theoretical occupancy
**Memory Throughput**: Actual vs. peak bandwidth
**Instruction Throughput**: ALU utilization
**Bottleneck Analysis**: Compute vs. memory bound

## Real-World Applications

### Scientific Computing
- Computational Fluid Dynamics (CFD)
- Molecular Dynamics simulations
- Climate modeling
- Finite element analysis

### Image and Signal Processing
- Convolution operations
- FFT (Fast Fourier Transform)
- Computer vision algorithms
- Medical image processing

### Machine Learning
- Matrix multiplication (GEMM)
- Convolution neural networks
- Training and inference acceleration
- Tensor operations

### Financial Computing
- Monte Carlo simulations
- Risk analysis
- Algorithmic trading
- Portfolio optimization

## Best Practices

### Algorithm Design
1. Identify parallel components
2. Minimize data dependencies
3. Design for GPU memory hierarchy
4. Consider thread divergence

### Implementation
1. Coalesce memory access
2. Maximize occupancy
3. Minimize host-device transfers
4. Use appropriate data types

### Optimization
1. Profile before optimizing
2. Focus on memory bandwidth
3. Optimize hot kernels first
4. Consider algorithmic improvements

Understanding parallel computing concepts enables effective GPU programming and acceleration of computationally intensive applications.""",
                "order": 1
            }
        ]
    },

    # RAM COURSES
    {
        "title": "Memory Systems and RAM Technology",
        "description": "Deep dive into computer memory hierarchy, RAM types, and memory system optimization",
        "category": "Memory & Storage",
        "difficulty": "intermediate",
        "duration": "9 weeks",
        "instructor": "Memory Systems Team", 
        "price": 0.000005,
        "is_featured": True,
        "modules": [
            {
                "title": "Memory Hierarchy Fundamentals",
                "description": "Understanding how different types of memory work together in modern computer systems",
                "content": """# Memory Hierarchy Fundamentals

## The Memory Hierarchy Concept

Modern computer systems use a hierarchy of memory technologies, each optimized for different characteristics: speed, capacity, and cost. Understanding this hierarchy is crucial for system design and optimization.

## Why Do We Need a Memory Hierarchy?

### The Memory Wall Problem
- CPU performance has grown faster than memory speed
- Large gap between processor and memory performance
- Need to bridge this gap efficiently

### Trade-offs in Memory Design
**Speed vs. Capacity**: Faster memory is typically smaller
**Cost vs. Performance**: Faster memory costs more per bit
**Power vs. Performance**: Faster memory often consumes more power

## Levels of the Memory Hierarchy

### Level 1: CPU Registers
**Characteristics**:
- Fastest access (0-1 cycles)
- Smallest capacity (typically 32-256 registers)
- Highest cost per bit
- Directly accessible by instructions

**Types of Registers**:
- General-purpose registers
- Floating-point registers  
- Vector/SIMD registers
- Special-purpose registers (PC, SP, flags)

**Programming Impact**:
- Compiler optimization crucial
- Register allocation algorithms
- RISC vs. CISC register usage

### Level 2: CPU Cache Memory

**L1 Cache**:
- Access time: 1-3 cycles
- Capacity: 16-64 KB per core
- Split instruction/data or unified
- Highest hit rate priority

**L2 Cache**:
- Access time: 3-10 cycles  
- Capacity: 256 KB - 1 MB per core
- Usually unified (instructions + data)
- Balance between size and speed

**L3 Cache**:
- Access time: 10-30 cycles
- Capacity: 8-32 MB shared
- Shared among multiple cores
- Reduces memory bandwidth pressure

#### Cache Organization

**Direct-Mapped Cache**:
- Each memory location maps to one cache line
- Simple implementation
- Higher conflict miss rate

**Set-Associative Cache**:
- Each memory location maps to a set
- Multiple lines per set
- Reduced conflict misses, more complex

**Fully Associative Cache**:
- Any memory location can map anywhere
- Lowest miss rate
- Most complex implementation

#### Cache Replacement Policies

**Least Recently Used (LRU)**:
- Replace least recently accessed line
- Good temporal locality exploitation
- Complex hardware implementation

**Random Replacement**:
- Simple to implement
- Reasonable performance
- No pathological cases

**First-In-First-Out (FIFO)**:
- Replace oldest cache line
- Simple implementation
- May not reflect usage patterns

### Level 3: Main Memory (RAM)

**Characteristics**:
- Access time: 100-300 cycles
- Capacity: 4-128 GB typical
- Volatile storage
- Primary working space

**DRAM Technology**:
- Dynamic refresh required
- Capacitor-based storage
- High density, moderate speed

**Memory Controllers**:
- Interface between CPU and RAM
- Handle timing and refresh
- Multiple channels for bandwidth

### Level 4: Secondary Storage

**Solid State Drives (SSD)**:
- Access time: 10,000-100,000 cycles
- Capacity: 256 GB - 8 TB
- NAND flash technology
- No moving parts

**Hard Disk Drives (HDD)**:
- Access time: 1-10 million cycles
- Capacity: 500 GB - 20 TB
- Magnetic storage
- Mechanical seek time

### Level 5: Tertiary Storage

**Network Attached Storage**:
- Access over network
- Very high capacity
- High latency

**Optical Storage**:
- DVD, Blu-ray
- Long-term archival
- Read-mostly applications

## Memory Performance Characteristics

### Latency vs. Bandwidth

**Latency**: Time for single memory access
- More important for random access
- Affected by distance and complexity
- Difficult to reduce

**Bandwidth**: Data transfer rate
- More important for streaming access
- Easier to increase with parallelism
- Critical for multimedia applications

### Access Patterns

**Sequential Access**: 
- Reading/writing consecutive locations
- Exploits spatial locality
- Optimal for bandwidth utilization

**Random Access**:
- Accessing arbitrary locations
- Tests latency characteristics
- Worst-case performance

**Strided Access**:
- Regular pattern with gaps
- Common in scientific computing
- Cache behavior depends on stride size

## Principles of Locality

### Temporal Locality
**Concept**: Recently accessed data likely to be accessed again
**Examples**:
- Loop variables
- Frequently called functions
- Active data structures

**Exploitation**:
- CPU caches
- Buffer caches
- Working set management

### Spatial Locality  
**Concept**: Data near recently accessed data likely to be accessed
**Examples**:
- Array elements
- Sequential file access
- Code execution sequence

**Exploitation**:
- Cache line sizes
- Prefetching
- Page-based virtual memory

## Virtual Memory System

### Address Translation
**Virtual Addresses**: Program's view of memory
**Physical Addresses**: Hardware memory locations
**Translation Lookaside Buffer (TLB)**: Address translation cache

### Memory Management
**Paging**: Fixed-size memory blocks
**Segmentation**: Variable-size memory regions
**Page Replacement**: Managing physical memory allocation

### Benefits of Virtual Memory
- Memory protection between processes
- Larger address space than physical memory
- Memory sharing between processes
- Simplified memory management

## Performance Optimization Strategies

### Software Optimization
**Cache-Friendly Programming**:
- Sequential data access
- Blocking/tiling algorithms
- Data structure reorganization

**Memory Access Patterns**:
- Avoid pointer chasing
- Prefetch critical data
- Minimize working set size

### Hardware Optimization
**Memory Interleaving**: Parallel access to memory banks
**Prefetching**: Predict and fetch future data
**Write Buffering**: Overlap write operations

## Measuring Memory Performance

### Common Metrics
**Hit Rate**: Percentage of accesses found in cache
**Miss Rate**: Percentage of accesses requiring next level
**Average Access Time**: Weighted time considering all levels

### Performance Analysis Tools
**Hardware Counters**: CPU-specific measurement
**Profiling Tools**: Software-based analysis
**Simulation**: Detailed architectural modeling

## Future Trends

### Emerging Technologies
**3D Stacked Memory**: Vertical integration
**Processing-in-Memory**: Computation near storage
**Non-Volatile RAM**: Persistent main memory
**Optical Interconnects**: High-bandwidth, low-latency

### Architecture Evolution
**Near-Data Computing**: Reduce data movement
**Heterogeneous Memory**: Mix of memory technologies
**Memory-Centric Computing**: Design around memory characteristics

Understanding memory hierarchy helps in:
- Writing efficient code
- System architecture decisions
- Performance debugging
- Technology selection""",
                "order": 1
            }
        ]
    },
    {
        "title": "DDR Memory and Performance Optimization",
        "description": "Master DDR memory standards, timing, and optimization techniques for maximum system performance",
        "category": "Memory & Storage",
        "difficulty": "advanced",
        "duration": "10 weeks",
        "instructor": "DDR Optimization Team",
        "price": 0.000005,
        "is_featured": False,
        "modules": [
            {
                "title": "DDR Memory Standards Evolution",
                "description": "Complete history and technical progression of DDR memory from DDR1 to DDR5",
                "content": """# DDR Memory Standards Evolution

## Introduction to DDR Memory

Double Data Rate (DDR) SDRAM is the foundation of modern computer memory systems. Understanding its evolution helps appreciate current capabilities and future directions.

## Pre-DDR Era: SDR SDRAM

### Single Data Rate SDRAM (1993-2000)
**Characteristics**:
- Single data transfer per clock cycle
- 66-133 MHz operation
- 64-bit data path
- Synchronous operation

**Limitations**:
- Low bandwidth compared to CPU needs
- Single edge data transfer
- Limited scalability

## DDR1 SDRAM (2000-2005)

### Technical Innovations
**Double Data Rate Transfer**:
- Data transferred on both clock edges
- Effective doubling of data rate
- Same external clock frequency

**Key Specifications**:
- 100-200 MHz base clock
- DDR-200 to DDR-400 speeds
- 184-pin DIMM form factor
- 2.5V operating voltage

### Memory Organization
**Bank Architecture**: 4 internal banks
**Burst Length**: 2, 4, or 8 beats
**Prefetch**: 2n (2 bits per clock)
**CAS Latency**: 2, 2.5, 3 clocks

### Performance Characteristics
- Peak bandwidth: 1.6-3.2 GB/s (single channel)
- Latency: ~50-60ns
- Power consumption: ~3-4W per DIMM

## DDR2 SDRAM (2003-2009)

### Architectural Improvements
**Higher Frequencies**: 200-533 MHz base clock
**Lower Voltage**: 1.8V operation
**4n Prefetch**: 4 bits per clock cycle
**On-Die Termination (ODT)**: Improved signal integrity

### Technical Specifications
**Speed Grades**: DDR2-400 to DDR2-1066
**Form Factor**: 240-pin DIMM
**Bank Count**: 4 or 8 banks
**Burst Length**: 4 or 8 beats

### Performance Benefits
- Peak bandwidth: 3.2-8.5 GB/s
- Better power efficiency
- Higher density capabilities
- Improved signal quality

### Limitations
- Higher latency than DDR1
- Complex manufacturing
- Heat generation at high speeds

## DDR3 SDRAM (2007-2015)

### Major Enhancements
**8n Prefetch Architecture**: 8 bits per clock
**Lower Operating Voltage**: 1.5V standard
**Higher Frequencies**: 400-1066 MHz base
**Improved ODT**: Better signal integrity

### Advanced Features
**Point-to-Point Topology**: Reduced loading
**Fly-by Topology**: Command/address signals
**Write Leveling**: Timing optimization
**ZQ Calibration**: Impedance matching

### Speed and Performance
**Speed Grades**: DDR3-800 to DDR3-2133
**Peak Bandwidth**: 6.4-17 GB/s
**Latency**: CL 7-11 typical
**Power**: ~30% reduction vs. DDR2

### Memory Training
**SPD (Serial Presence Detect)**: Automatic configuration
**XMP (Extreme Memory Profile)**: Overclocking profiles
**Training Algorithms**: Optimal timing discovery

## DDR4 SDRAM (2014-present)

### Revolutionary Changes
**Bank Groups**: 4 bank groups × 4 banks
**16n Prefetch**: 16 bits per clock cycle  
**1.2V Operation**: Further power reduction
**Higher Densities**: Up to 32GB per DIMM

### Advanced Technologies
**Target Row Refresh (TRR)**: Row hammer mitigation
**Command/Address Parity**: Error detection
**Data Bus Inversion (DBI)**: Power optimization
**Gear Down Mode**: Half-rate command/address

### Performance Specifications
**Speed Range**: DDR4-1600 to DDR4-3200 (JEDEC)
**Overclocked Speeds**: Up to DDR4-5000+
**Peak Bandwidth**: 12.8-25.6 GB/s
**Latency**: CL 14-19 typical

### Power Management
**Deep Power-Down Mode**: Ultra-low power
**Self-Refresh**: Reduced refresh power
**Temperature Compensated Self-Refresh (TCSR)**: Adaptive refresh

## DDR5 SDRAM (2020-present)

### Next-Generation Features
**32n Prefetch**: 32 bits per clock cycle
**Dual-Channel per DIMM**: Two independent 32-bit channels
**1.1V Core Voltage**: Lowest yet
**On-DIMM Power Management (PMIC)**: Voltage regulation

### Advanced Capabilities
**Same-Bank Refresh**: Improved availability
**Real-Time Clock**: Precise timing reference
**Enhanced Refresh Management**: Better efficiency
**Improved Error Correction**: On-die ECC

### Performance Targets
**Speed Range**: DDR5-3200 to DDR5-6400 (JEDEC)
**Overclocked Potential**: DDR5-8000+
**Peak Bandwidth**: 25.6-51.2 GB/s per channel
**Latency**: Similar absolute latency to DDR4

### New Technologies
**Decision Feedback Equalization (DFE)**: Signal conditioning
**Write and Read DQS Training**: Precision timing
**Improved Signal Integrity**: Better high-speed operation

## Future: DDR6 and Beyond (2025+)

### Expected Improvements
**Higher Speeds**: 8000+ MHz potential
**Lower Voltage**: Sub-1V operation
**Advanced Prefetch**: 64n or adaptive
**3D Integration**: Vertical memory stacking

### Emerging Technologies
**Processing-in-Memory**: Computation in DRAM
**Hybrid Memory Cubes**: 3D architecture
**Optical Interconnects**: Light-based communication
**Quantum Memory**: Revolutionary storage

## Comparison Summary

| Standard | Year | Voltage | Prefetch | Max Speed | Peak BW |
|----------|------|---------|----------|-----------|---------|
| DDR1     | 2000 | 2.5V    | 2n       | 400 MHz   | 3.2 GB/s |
| DDR2     | 2003 | 1.8V    | 4n       | 533 MHz   | 8.5 GB/s |
| DDR3     | 2007 | 1.5V    | 8n       | 1066 MHz  | 17 GB/s |
| DDR4     | 2014 | 1.2V    | 16n      | 1600 MHz  | 25.6 GB/s |
| DDR5     | 2020 | 1.1V    | 32n      | 3200 MHz  | 51.2 GB/s |

## Practical Implications

### System Design Considerations
- Memory controller complexity increases
- Power delivery requirements
- Thermal management needs
- Signal integrity challenges

### Application Performance Impact
- Bandwidth-sensitive applications benefit most
- Latency-sensitive applications see less improvement
- Memory-intensive workloads show significant gains

### Cost and Adoption Factors
- New standards initially expensive
- Gradual price reduction over time
- Platform support requirements
- Backward compatibility limitations

Understanding DDR evolution helps in:
- Making informed upgrade decisions
- Optimizing system configurations
- Planning for future technologies
- Troubleshooting memory issues""",
                "order": 1
            }
        ]
    }
]

# Add more hardware components (Motherboard, Storage, Power Supply, Cooling, Case)
# [Additional course data would continue here with same detailed structure]

def create_course_thumbnail(title, category, output_path):
    """Create a custom thumbnail for the course"""
    # Create image
    img = Image.new('RGB', (400, 300), color='#1e3a8a')
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
        category_font = ImageFont.truetype("arial.ttf", 16)
    except:
        title_font = ImageFont.load_default()
        category_font = ImageFont.load_default()
    
    # Draw background gradient effect
    for i in range(300):
        color = int(30 + (i * 0.3))  # Gradient effect
        draw.line([(0, i), (400, i)], fill=(30, 58, color))
    
    # Draw title (wrap text if too long)
    words = title.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=title_font)
        if bbox[2] <= 360:  # 400 - margin
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
                current_line = word
            else:
                lines.append(word)
    if current_line:
        lines.append(current_line)
    
    # Draw title lines
    y = 100 - (len(lines) * 15)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        x = (400 - bbox[2]) // 2
        draw.text((x, y), line, fill='white', font=title_font)
        y += 30
    
    # Draw category
    bbox = draw.textbbox((0, 0), category, font=category_font)
    x = (400 - bbox[2]) // 2
    draw.text((x, 220), category, fill='#60a5fa', font=category_font)
    
    # Add some decorative elements
    draw.rectangle([50, 50, 350, 54], fill='#60a5fa')
    draw.rectangle([50, 246, 350, 250], fill='#60a5fa')
    
    # Save image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    return output_path

async def add_hardware_courses():
    """Add comprehensive hardware courses to the database"""
    client = MongoClient('mongodb://localhost:27017')
    db = client.edtech_hardware
    
    # Ensure uploads directory exists
    uploads_dir = "uploads/thumbnails"
    os.makedirs(uploads_dir, exist_ok=True)
    
    courses_added = 0
    
    for course_data in HARDWARE_COURSES:
        # Check if course already exists
        existing = db.courses.find_one({"title": course_data["title"]})
        if existing:
            print(f"Course '{course_data['title']}' already exists, skipping...")
            continue
            
        # Create thumbnail
        safe_filename = "".join(c for c in course_data["title"] if c.isalnum() or c in (' ', '-')).rstrip()
        safe_filename = safe_filename.replace(' ', '_').lower()
        thumbnail_path = f"{uploads_dir}/course_{safe_filename}.jpg"
        
        create_course_thumbnail(
            course_data["title"],
            course_data["category"], 
            thumbnail_path
        )
        
        # Prepare course document
        course_doc = {
            **course_data,
            "thumbnail_url": f"/uploads/thumbnails/course_{safe_filename}.jpg",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_published": True,
            "enrollment_count": 0,
            "rating": 4.8,
            "rating_count": 0,
            "prerequisites": [],
            "learning_outcomes": [
                "Master core concepts and terminology",
                "Understand historical context and evolution", 
                "Gain practical knowledge for real-world application",
                "Develop technical expertise in the subject area"
            ]
        }
        
        # Add duration_minutes to modules
        for module in course_doc["modules"]:
            module["duration_minutes"] = 45  # Default 45 minutes per module
            module["content_url"] = None
            module["video_url"] = None
            module["image_urls"] = []
        
        # Insert course
        result = db.courses.insert_one(course_doc)
        print(f"✅ Added course: {course_data['title']}")
        courses_added += 1
    
    print(f"\n🎉 Successfully added {courses_added} new hardware courses!")
    client.close()

if __name__ == "__main__":
    # Run sync version since we're not in async context
    client = MongoClient('mongodb://localhost:27017')
    db = client.edtech_hardware
    
    # Ensure uploads directory exists  
    uploads_dir = "uploads/thumbnails"
    os.makedirs(uploads_dir, exist_ok=True)
    
    courses_added = 0
    
    for course_data in HARDWARE_COURSES:
        # Check if course already exists
        existing = db.courses.find_one({"title": course_data["title"]})
        if existing:
            print(f"Course '{course_data['title']}' already exists, skipping...")
            continue
            
        # Create thumbnail
        safe_filename = "".join(c for c in course_data["title"] if c.isalnum() or c in (' ', '-')).rstrip()
        safe_filename = safe_filename.replace(' ', '_').lower()
        thumbnail_path = f"{uploads_dir}/course_{safe_filename}.jpg"
        
        create_course_thumbnail(
            course_data["title"],
            course_data["category"],
            thumbnail_path
        )
        
        # Prepare course document
        course_doc = {
            **course_data,
            "thumbnail_url": f"/uploads/thumbnails/course_{safe_filename}.jpg", 
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_published": True,
            "enrollment_count": 0,
            "rating": 4.8,
            "rating_count": 0,
            "prerequisites": [],
            "learning_outcomes": [
                "Master core concepts and terminology",
                "Understand historical context and evolution",
                "Gain practical knowledge for real-world application", 
                "Develop technical expertise in the subject area"
            ]
        }
        
        # Add duration_minutes to modules
        for module in course_doc["modules"]:
            module["duration_minutes"] = 45  # Default 45 minutes per module
            module["content_url"] = None
            module["video_url"] = None
            module["image_urls"] = []
        
        # Insert course
        result = db.courses.insert_one(course_doc)
        print(f"✅ Added course: {course_data['title']}")
        courses_added += 1
    
    print(f"\n🎉 Successfully added {courses_added} new hardware courses!")
    client.close()
