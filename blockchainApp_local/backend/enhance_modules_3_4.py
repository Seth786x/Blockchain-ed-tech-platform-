#!/usr/bin/env python3

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Enhanced content for GPU course modules 3-4
ENHANCED_MODULES_3_4 = [
    {
        "title": "AMD/ATI Graphics Evolution",
        "description": "ATI Radeon series, AMD acquisition, and the RDNA architecture revolution",
        "content": """# AMD/ATI Graphics Evolution: The Rise of the Red Team

## The ATI Era (1985-2006)

### ATI Technologies: The Canadian Pioneer

Founded in 1985 in Markham, Ontario, **ATI Technologies** became one of the most innovative graphics companies in history, challenging NVIDIA's dominance and pushing the boundaries of GPU technology.

#### Early ATI History:
- **1985**: Founded by K.Y. Ho, Benny Lau, Lee Ka Lau, and Kwok Yuen Ho
- **1987**: First graphics card - ATI VGA Wonder
- **1991**: Mach8 accelerator - first dedicated 2D acceleration
- **1995**: 3D Rage series - entry into 3D graphics

### The Radeon Revolution (2000-2006)

#### **Radeon R100 (2000)**
The original **ATI Radeon** marked ATI's serious entry into high-performance 3D graphics:

**Technical Specifications:**
- **Memory**: 32MB or 64MB DDR SDRAM
- **Core Clock**: 166 MHz
- **Memory Clock**: 166 MHz (DDR)
- **Pixel Pipelines**: 3 pipelines
- **DirectX Support**: DirectX 7.0
- **Manufacturing**: 180nm process

**Key Features:**
- **HyperZ Technology**: Z-buffer compression and hierarchical Z
- **Charisma Engine**: Advanced geometry processing
- **Pixel Tapestry**: Pixel shader architecture
- **DVD Hardware Acceleration**: Integrated video processing

#### **Radeon R200 Series (2001-2002)**
The **Radeon 8500** series represented a major leap forward:

**Radeon 8500 Specifications:**
- **Memory**: 64MB or 128MB DDR
- **Core Clock**: 275 MHz
- **Memory Bandwidth**: 8.8 GB/s
- **Pixel Pipelines**: 4 pipelines
- **DirectX Support**: DirectX 8.1
- **Manufacturing**: 150nm process

**Revolutionary Features:**
- **Pixel Shaders 1.4**: Most advanced programmable shaders
- **TruForm**: Hardware tessellation for smooth surfaces
- **Smoothvision**: Advanced anti-aliasing technology
- **Video Shader**: Hardware video processing acceleration

#### **Radeon R300 Series (2002-2004)**
The **R300** architecture marked ATI's finest hour:

**Radeon 9700 Pro Specifications:**
- **Memory**: 128MB DDR
- **Core Clock**: 325 MHz
- **Memory Bandwidth**: 19.8 GB/s
- **Pixel Pipelines**: 8 pipelines
- **DirectX Support**: DirectX 9.0
- **Manufacturing**: 150nm process

**Groundbreaking Achievements:**
- **First DirectX 9.0 GPU**: Full shader model 2.0 support
- **256-bit Memory Bus**: Unprecedented memory bandwidth
- **F-Buffer**: Floating-point render targets
- **Advanced Anti-Aliasing**: Gamma-correct AA implementation

### The AMD Acquisition (2006)

#### **The $5.4 Billion Deal**
In July 2006, **Advanced Micro Devices (AMD)** acquired ATI Technologies for $5.4 billion, creating the world's only company with both CPU and GPU design capabilities.

**Strategic Reasoning:**
- **Platform Integration**: CPU-GPU synergy
- **Intel Competition**: Competing with Intel's integrated approach
- **Market Positioning**: Challenging NVIDIA-Intel partnerships
- **Technology Convergence**: Anticipating CPU-GPU convergence

#### **Integration Challenges:**
- **Cultural Differences**: Merging two distinct corporate cultures
- **Technical Integration**: Combining CPU and GPU roadmaps
- **Market Competition**: Competing simultaneously with Intel and NVIDIA
- **Resource Allocation**: Balancing CPU and GPU development

## The AMD Graphics Era (2006-Present)

### Early AMD Graphics (2006-2011)

#### **TeraScale Architecture (2007-2012)**
AMD's first unified architecture represented a clean break from ATI's legacy:

**Radeon HD 2000 Series (R600)**
- **Unified Shaders**: Single shader type for all operations
- **Superscalar Design**: Multiple operations per shader
- **Ring Bus**: High-bandwidth internal communication
- **GDDR4 Memory**: Next-generation memory technology

**Key Innovations:**
- **Stream Processing Units**: 320-800 unified shaders
- **CrossFireX**: Multi-GPU scaling technology
- **Avivo HD**: Hardware video acceleration
- **Eyefinity**: Multi-monitor gaming technology

### Graphics Core Next (GCN) Era (2012-2019)

#### **GCN 1.0 - Southern Islands (2012)**
**Radeon HD 7000 Series** introduced revolutionary GCN architecture:

**Architectural Principles:**
- **Compute Units**: 64 shader processors per CU
- **Wavefronts**: 64-thread SIMD execution
- **Scalar Units**: Efficient branch handling
- **Asynchronous Compute**: Overlapped graphics and compute

**Technical Specifications:**
- **Stream Processors**: Up to 2048 shaders
- **Memory**: GDDR5 with up to 384-bit bus
- **Manufacturing**: 28nm process technology
- **DirectX Support**: DirectX 11.1

#### **GCN Evolution:**
- **GCN 2.0 (2013)**: Improved power efficiency, TrueAudio
- **GCN 3.0 (2014)**: Tonga and Fiji chips, HBM memory
- **GCN 4.0 (2016)**: Polaris architecture, 14nm FinFET
- **GCN 5.0 (2017)**: Vega architecture, enhanced compute

### RDNA Revolution (2019-Present)

#### **RDNA 1.0 - Navi (2019)**
The **Radeon RX 5000 Series** marked a fundamental architectural shift:

**RDNA Architecture Principles:**
- **Work Group Processors (WGP)**: Dual compute unit design
- **Wave32**: 32-thread wavefronts for gaming efficiency
- **Primitive Shaders**: Geometry pipeline optimization
- **Variable Rate Shading**: Adaptive rendering quality

**Performance Improvements:**
- **50% Performance-per-Clock**: Over GCN architecture
- **1.5x Performance-per-Watt**: Significant efficiency gains
- **Lower Latency**: Reduced pipeline complexity
- **Higher Clocks**: Improved frequency scaling

#### **RDNA 2.0 (2020)**
**Radeon RX 6000 Series** brought ray tracing and console wins:

**Key Features:**
- **Ray Accelerators**: Hardware ray tracing support
- **Infinity Cache**: 128MB on-die cache
- **Smart Access Memory**: CPU-GPU memory sharing
- **DirectX 12 Ultimate**: Full feature support

**Console Success:**
- **PlayStation 5**: Custom RDNA 2 GPU
- **Xbox Series X/S**: RDNA 2 architecture
- **Steam Deck**: Custom RDNA 2 APU

#### **RDNA 3.0 (2022)**
**Radeon RX 7000 Series** introduced chiplet design:

**Architectural Innovations:**
- **Graphics Chiplet Design**: Modular GPU construction
- **5nm + 6nm Process**: Advanced manufacturing
- **DisplayPort 2.1**: 8K display support
- **AV1 Encoding**: Next-gen video codec

## AMD's Unique Approach

### **Open Standards Philosophy**
Unlike NVIDIA's proprietary approach, AMD champions open standards:
- **FreeSync**: Open adaptive sync technology
- **Mantle API**: Low-level graphics API (predecessor to Vulkan)
- **GPUOpen**: Open-source graphics tools and libraries
- **ROCm**: Open compute platform

### **Price-Performance Focus**
AMD consistently targets mainstream and value markets:
- **Competitive Pricing**: Better value propositions
- **Mainstream Focus**: Serving broader market segments
- **Console Partnerships**: Leveraging semi-custom business
- **APU Integration**: CPU-GPU integration leadership

### **Software Ecosystem**
AMD has invested heavily in software development:
- **Radeon Software**: Comprehensive driver suite
- **FidelityFX**: Open-source visual effects
- **FSR (FidelityFX Super Resolution)**: Open upscaling technology
- **Radeon Anti-Lag**: Input latency reduction

## Competitive Dynamics

### **The Eternal Rivalry**
AMD vs NVIDIA competition has driven industry innovation:

#### **Technology Leapfrogging:**
- **2002**: ATI R300 vs NVIDIA NV30 (ATI victory)
- **2006**: NVIDIA G80 unified shaders (NVIDIA victory)
- **2012**: AMD GCN compute focus (AMD advantage)
- **2018**: NVIDIA Turing ray tracing (NVIDIA victory)
- **2020**: AMD RDNA 2 console wins (AMD advantage)

#### **Market Positioning:**
- **High-End**: NVIDIA traditionally dominates
- **Mid-Range**: Competitive battleground
- **Value Segment**: AMD's traditional strength
- **Console Market**: AMD's exclusive domain

## Future Directions

### **RDNA 4 and Beyond**
AMD's roadmap focuses on:
- **Improved Ray Tracing**: Closing the gap with NVIDIA
- **AI Acceleration**: Machine learning workloads
- **Advanced Manufacturing**: 3nm and beyond
- **Unified Architecture**: CPU-GPU convergence

### **Market Opportunities**
- **Data Center**: Growing AI and compute markets
- **Edge Computing**: Integrated solutions
- **Automotive**: Autonomous vehicle graphics
- **Metaverse**: VR/AR acceleration

## Assessment Questions:

1. **Historical Analysis**: How did ATI's approach differ from 3Dfx and NVIDIA in the early 2000s?

2. **Technical Understanding**: What were the key architectural innovations of the GCN design?

3. **Business Strategy**: How did AMD's open standards approach impact the graphics market?

4. **Competitive Analysis**: Compare AMD's and NVIDIA's different strategies for market leadership.

5. **Future Prediction**: What advantages might AMD's CPU-GPU integration provide in future computing?

## Key Takeaways:

- **Innovation Leadership**: ATI/AMD has driven many industry innovations
- **Open Standards**: AMD's commitment to open technologies benefits the entire industry
- **Console Success**: AMD dominates the console graphics market
- **Competitive Balance**: AMD provides essential competition to NVIDIA
- **Integration Advantage**: CPU-GPU integration offers unique opportunities

The AMD/ATI story demonstrates how sustained innovation, strategic positioning, and commitment to open standards can create lasting impact in a highly competitive industry.
""",
        "order": 3
    },
    {
        "title": "NVIDIA's Rise to Dominance",
        "description": "From TNT to RTX: NVIDIA's journey to GPU leadership and AI acceleration",
        "content": """# NVIDIA's Rise to Dominance: The Green Revolution

## The Foundation Years (1993-1999)

### **NVIDIA Corporation: The Startup**
Founded on April 5, 1993, by Jensen Huang, Chris Malachowsky, and Curtis Priem in a Denny's restaurant in San Jose, California. The company name combines "NV" (next version) and "invidia" (Latin for envy).

#### **Early Products and Struggles:**
- **NV1 (1994)**: Quadratic texture mapping and audio - commercial failure
- **NV2 (1996)**: Cancelled due to industry moving to triangular primitives
- **Financial Crisis**: Nearly bankrupted by 1997
- **Riva 128 (1997)**: First successful product, DirectX 6 support

#### **The TNT Era (1998-1999)**
**TNT (TwiN Texel)** marked NVIDIA's entry into serious 3D competition:

**Technical Specifications:**
- **Memory**: 16MB SDRAM
- **Texture Units**: 2 texture units per pipeline
- **Core Clock**: 90-125 MHz
- **Manufacturing**: 350nm process
- **DirectX Support**: DirectX 6.0

**TNT2 Improvements:**
- **32MB Memory**: Doubled frame buffer
- **Higher Clocks**: Up to 150 MHz
- **AGP 4X Support**: Enhanced system interface
- **Improved Driver**: Better game compatibility

## The GeForce Revolution (1999-2006)

### **GeForce 256 (1999): The Birth of the GPU**
NVIDIA coined the term "GPU" (Graphics Processing Unit) with the GeForce 256:

**Revolutionary Features:**
- **Hardware Transform & Lighting**: Dedicated T&L engine
- **Quadro Architecture**: 4 pixel pipelines
- **256-bit Rendering**: Enhanced visual quality
- **DirectX 7 Support**: Hardware transform and lighting

**Market Impact:**
- **CPU Offloading**: Freed CPU from graphics calculations
- **Performance Leap**: 50-100% improvement over software T&L
- **Industry Shift**: Established GPU as essential component
- **Brand Recognition**: "GPU" became industry standard term

### **GeForce 2 Series (2000-2001)**
Building on the original success:

**GeForce 2 GTS:**
- **Memory Bandwidth**: 5.3 GB/s
- **Core Clock**: 200 MHz
- **Manufacturing**: 180nm process
- **Dual Display**: Hardware dual-monitor support

**GeForce 2 Ultra:**
- **First "Ultra" Branding**: Premium product positioning
- **Enhanced Performance**: Higher clocks and memory
- **Professional Validation**: Workstation applications

### **GeForce 3 Series (2001): Programmable Shaders**
The **GeForce 3** introduced programmable vertex shaders:

**Technical Innovations:**
- **Vertex Shaders**: Programmable vertex processing
- **Register Combiners**: Flexible pixel operations
- **Z-Occlusion Culling**: Efficiency improvements
- **DirectX 8.0**: First DirectX 8 GPU

**GeForce 3 Ti Series:**
- **Ti 200**: Value segment positioning
- **Ti 500**: Performance leadership
- **Anti-Aliasing**: Improved visual quality

### **GeForce 4 Series (2002-2003)**
Split into two distinct architectures:

**GeForce 4 Ti Series (NV25):**
- **Dual Vertex Shaders**: Enhanced geometry performance
- **Advanced AA**: Accuview anti-aliasing
- **AGP 8X**: Next-generation system interface
- **Lightspeed Memory**: Bandwidth optimizations

**GeForce 4 MX Series (NV17):**
- **Value Positioning**: DirectX 7 level features
- **Integrated Markets**: OEM and budget systems
- **Controversial Naming**: Criticized for feature limitations

### **GeForce FX Series (2003-2004): The Learning Experience**
The **NV30** architecture faced significant challenges:

**Technical Issues:**
- **Manufacturing Problems**: 130nm process difficulties
- **Power Consumption**: Extremely high power draw
- **Noise Levels**: "Dustbuster" cooling solution
- **DirectX 9 Performance**: Poor shader performance

**Market Reception:**
- **ATI Competition**: Radeon 9700 Pro superiority
- **Brand Damage**: First major NVIDIA misstep
- **Lessons Learned**: Importance of balanced design

## The Modern Era Begins (2004-2010)

### **GeForce 6 Series (2004-2005): The Comeback**
The **NV40** architecture restored NVIDIA's reputation:

**GeForce 6800 Ultra:**
- **16 Pixel Pipelines**: Unprecedented parallel processing
- **Shader Model 3.0**: Advanced programmable shaders
- **SLI Technology**: Multi-GPU scaling
- **110nm Process**: Advanced manufacturing

**Technical Achievements:**
- **PCI Express**: First native PCIe GPU
- **UltraShadow**: Advanced shadow techniques
- **Intellisample**: Intelligent anti-aliasing
- **Video Processing**: Hardware video decode

### **GeForce 7 Series (2005-2006)**
Refinement and market expansion:

**GeForce 7800 GTX:**
- **24 Pixel Shaders**: Enhanced shader processing
- **Memory Interface**: 256-bit GDDR3
- **90nm Process**: Improved efficiency
- **Transparent AA**: Advanced anti-aliasing

**Market Strategy:**
- **Performance Scaling**: Multiple SKUs
- **OEM Partnerships**: Broader market reach
- **Mobile Graphics**: Laptop GPU leadership

### **GeForce 8 Series (2006-2008): Unified Architecture**
The **G80** architecture revolutionized GPU design:

**Architectural Revolution:**
- **Unified Shaders**: Single processor type
- **CUDA Cores**: 128 stream processors
- **Shader Model 4.0**: DirectX 10 support
- **90nm Process**: Advanced manufacturing

**GeForce 8800 GTX Specifications:**
- **Stream Processors**: 128 unified shaders
- **Memory**: 768MB GDDR3
- **Memory Bandwidth**: 86.4 GB/s
- **Core Clock**: 575 MHz

**Industry Impact:**
- **Programming Model**: CUDA introduction
- **Compute Applications**: General-purpose GPU computing
- **Performance Leadership**: Dominant market position
- **Architecture Template**: Model for future designs

## The CUDA Revolution (2007-Present)

### **CUDA: Parallel Computing Revolution**
**Compute Unified Device Architecture** transformed GPUs from graphics processors to general-purpose parallel computers:

#### **CUDA Programming Model:**
- **Kernel Functions**: GPU-executed parallel code
- **Thread Hierarchy**: Grids, blocks, and threads
- **Memory Hierarchy**: Global, shared, and local memory
- **Synchronization**: Barrier and atomic operations

#### **Developer Ecosystem:**
- **cuBLAS**: Linear algebra library
- **cuFFT**: Fast Fourier Transform library
- **Thrust**: Parallel algorithms library
- **Academic Adoption**: Universities worldwide

#### **Application Areas:**
- **Scientific Computing**: Weather simulation, molecular modeling
- **Financial Services**: Risk analysis, algorithmic trading
- **Media Processing**: Video encoding, image processing
- **Machine Learning**: Neural network training (precursor to modern AI)

### **Fermi Architecture (2010): Compute Focus**
**GeForce GTX 400/500 Series** emphasized compute capabilities:

**Technical Features:**
- **ECC Memory**: Error correction for compute accuracy
- **L1/L2 Cache**: Cache hierarchy for better performance
- **IEEE 754-2008**: Double-precision floating point
- **Concurrent Kernels**: Multiple kernel execution

**Challenges:**
- **Power Consumption**: Very high power requirements
- **Heat Generation**: Thermal management issues
- **Manufacturing Yield**: 40nm process difficulties
- **Gaming Performance**: Compute focus impacted graphics

### **Kepler Architecture (2012-2014): Efficiency Focus**
**GeForce GTX 600/700 Series** prioritized power efficiency:

**Key Improvements:**
- **SMX Units**: Enhanced streaming multiprocessors
- **GPU Boost**: Dynamic clock adjustment
- **28nm Process**: Significant efficiency gains
- **NVENC**: Hardware video encoding

**GeForce GTX 680:**
- **1536 CUDA Cores**: High parallelism
- **Memory**: 2GB GDDR5
- **Power Efficiency**: 195W TDP
- **Performance**: Competitive with AMD's offerings

### **Maxwell Architecture (2014-2016): Performance Revolution**
**GeForce GTX 900 Series** delivered exceptional performance:

**Maxwell 2.0 Features:**
- **SMM Units**: Maxwell streaming multiprocessors
- **Color Compression**: Memory bandwidth savings
- **Dynamic Super Resolution**: AI upscaling precursor
- **MFAA**: Multi-frame anti-aliasing

**GeForce GTX 980:**
- **2048 CUDA Cores**: Maximum parallelism
- **Memory**: 4GB GDDR5
- **Power Efficiency**: 165W TDP
- **VR Ready**: Virtual reality preparation

## The AI Era (2016-Present)

### **Pascal Architecture (2016-2018): VR and AI**
**GeForce GTX 10 Series** targeted emerging markets:

**Technical Achievements:**
- **16nm FinFET**: Advanced process node
- **GDDR5X Memory**: Higher bandwidth memory
- **Simultaneous Multi-Projection**: VR optimization
- **Pascal GP100**: First AI-focused GPU

**GeForce GTX 1080:**
- **2560 CUDA Cores**: Unprecedented parallel processing
- **Memory**: 8GB GDDR5X
- **Memory Bandwidth**: 320 GB/s
- **Performance**: 60% faster than GTX 980

**AI Breakthrough:**
- **Tesla P100**: Data center AI acceleration
- **Deep Learning**: Neural network training acceleration
- **Academic Adoption**: Universities embracing GPU computing
- **Industry Recognition**: AI researchers choosing NVIDIA

### **Turing Architecture (2018-2020): Ray Tracing Revolution**
**GeForce RTX 20 Series** introduced real-time ray tracing:

**Revolutionary Features:**
- **RT Cores**: Dedicated ray tracing processors
- **Tensor Cores**: AI acceleration units
- **DLSS**: AI-powered upscaling
- **12nm FFN**: Optimized manufacturing

**GeForce RTX 2080 Ti:**
- **4352 CUDA Cores**: Massive parallelism
- **68 RT Cores**: Ray tracing acceleration
- **544 Tensor Cores**: AI processing
- **Memory**: 11GB GDDR6

**Industry Impact:**
- **Real-time Ray Tracing**: Photorealistic lighting
- **Game Development**: New visual possibilities
- **Content Creation**: Professional rendering acceleration
- **AI Gaming**: Intelligent upscaling and enhancement

### **Ampere Architecture (2020-2022): AI Dominance**
**GeForce RTX 30 Series** cemented NVIDIA's AI leadership:

**Technical Advances:**
- **Samsung 8nm**: Advanced process technology
- **2nd Gen RT Cores**: Improved ray tracing
- **3rd Gen Tensor Cores**: Enhanced AI performance
- **GDDR6X Memory**: Extreme bandwidth

**GeForce RTX 3090:**
- **10496 CUDA Cores**: Record parallelism
- **328 Tensor Cores**: AI acceleration
- **Memory**: 24GB GDDR6X
- **Performance**: 8K gaming capability

### **Ada Lovelace (2022-Present): Ultimate Performance**
**GeForce RTX 40 Series** pushes boundaries further:

**Cutting-Edge Features:**
- **TSMC 4N**: State-of-the-art manufacturing
- **3rd Gen RT Cores**: Ray tracing optimization
- **4th Gen Tensor Cores**: AI performance explosion
- **DLSS 3**: Frame generation technology

**GeForce RTX 4090:**
- **16384 CUDA Cores**: Unprecedented parallelism
- **Memory**: 24GB GDDR6X
- **Ray Tracing**: 2.8x RTX 3090 performance
- **AI Performance**: 5x improvement in AI workloads

## Market Leadership and Strategy

### **Technology Leadership:**
- **Architectural Innovation**: Consistent technical advancement
- **Software Ecosystem**: CUDA, cuDNN, TensorRT
- **Developer Support**: Comprehensive tools and libraries
- **Research Investment**: Significant R&D spending

### **Market Positioning:**
- **Premium Branding**: Performance and innovation focus
- **Vertical Integration**: Hardware-software optimization
- **Ecosystem Lock-in**: CUDA and proprietary technologies
- **Professional Markets**: Workstation and data center leadership

### **AI Revolution Leadership:**
- **Data Center Dominance**: 90%+ AI training market share
- **Automotive**: Self-driving car partnerships
- **Healthcare**: Medical imaging and drug discovery
- **Research**: Academic and industrial AI development

## Future Vision

### **Omniverse and Metaverse:**
- **Collaborative Platforms**: Virtual world creation
- **Real-time Rendering**: Photorealistic simulations
- **AI Integration**: Intelligent virtual assistants
- **Global Adoption**: Industry-wide platform adoption

### **Autonomous Systems:**
- **Self-Driving Cars**: Full autonomy achievement
- **Robotics**: Intelligent machine control
- **Smart Cities**: Urban intelligence infrastructure
- **Industrial Automation**: Factory and logistics optimization

## Assessment Questions:

1. **Strategic Analysis**: How did NVIDIA's CUDA strategy create competitive advantages?

2. **Technical Evolution**: What were the key architectural innovations that enabled NVIDIA's dominance?

3. **Market Dynamics**: How did NVIDIA transition from a graphics company to an AI company?

4. **Competitive Response**: How did NVIDIA respond to competitive threats throughout its history?

5. **Future Prediction**: What challenges might NVIDIA face in maintaining market leadership?

## Key Takeaways:

- **Strategic Vision**: NVIDIA anticipated and enabled new computing paradigms
- **Technical Excellence**: Consistent architectural innovation drove market leadership
- **Software Ecosystem**: CUDA created lasting competitive advantages
- **Market Timing**: Perfect positioning for AI revolution
- **Execution Excellence**: Ability to deliver on ambitious technical roadmaps

NVIDIA's journey from struggling startup to trillion-dollar company demonstrates how strategic vision, technical innovation, and perfect market timing can create transformational success in the technology industry.
""",
        "order": 4
    }
]

async def enhance_gpu_modules_3_4():
    """Enhance GPU course modules 3 and 4 with comprehensive content"""
    client = AsyncIOMotorClient('mongodb://localhost:27017')
    db = client.edtech_hardware
    courses_collection = db.courses
    
    # Find the GPU course
    gpu_course = await courses_collection.find_one({"title": "History of GPUs"})
    
    if gpu_course:
        modules = gpu_course.get('modules', [])
        
        # Update modules 3 and 4
        for i, enhanced_module in enumerate(ENHANCED_MODULES_3_4):
            module_index = i + 2  # Modules 3 and 4 (0-indexed: 2 and 3)
            if module_index < len(modules):
                modules[module_index].update({
                    'title': enhanced_module['title'],
                    'description': enhanced_module['description'], 
                    'content': enhanced_module['content'],
                    'order': enhanced_module['order']
                })
                print(f"✅ Enhanced module {module_index + 1}: {enhanced_module['title']}")
        
        # Update the course
        await courses_collection.update_one(
            {'_id': gpu_course['_id']},
            {'$set': {'modules': modules}}
        )
        
        print(f"🎉 Successfully enhanced modules 3-4 for: {gpu_course['title']}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(enhance_gpu_modules_3_4())
