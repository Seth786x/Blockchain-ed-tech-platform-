#!/usr/bin/env python3
"""
Add comprehensive content and images to courses
"""

import asyncio
import sys
import os
import requests
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, DATABASE_NAME
from PIL import Image, ImageDraw, ImageFont
import io
import base64
from pathlib import Path

# Create upload directories
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
(UPLOAD_DIR / "courses").mkdir(exist_ok=True)
(UPLOAD_DIR / "thumbnails").mkdir(exist_ok=True)

def create_course_thumbnail(course_title, category, filename):
    """Create a custom thumbnail for each course"""
    try:
        # Create image with course-specific colors
        color_map = {
            "Core Hardware Evolution": "#FF6B6B",      # Red
            "Component-Based": "#4ECDC4",              # Teal  
            "Storage & Data": "#45B7D1",               # Blue
            "Architecture & Integration": "#96CEB4",    # Green
            "Networking & Connectivity": "#FFEAA7",     # Yellow
            "Software & Tools": "#DDA0DD",              # Plum
            "Gaming-Specific": "#FF7675",               # Light Red
            "Security & Protection": "#6C5CE7",         # Purple
            "Trends & Culture": "#FD79A8"               # Pink
        }
        
        bg_color = color_map.get(category, "#74B9FF")
        
        # Create image
        img = Image.new('RGB', (400, 250), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        # Try to use a nice font, fall back to default if not available
        try:
            title_font = ImageFont.truetype("arial.ttf", 20)
            category_font = ImageFont.truetype("arial.ttf", 14)
        except:
            title_font = ImageFont.load_default()
            category_font = ImageFont.load_default()
        
        # Add text
        # Category text at top
        draw.text((20, 20), category.upper(), fill="white", font=category_font)
        
        # Course title (wrap text if too long)
        words = course_title.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = " ".join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=title_font)
            if bbox[2] > 360:  # If line too wide
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]
                else:
                    lines.append(test_line)
                    current_line = []
        
        if current_line:
            lines.append(" ".join(current_line))
        
        # Draw title lines
        y_offset = 80
        for i, line in enumerate(lines[:3]):  # Max 3 lines
            draw.text((20, y_offset + i * 30), line, fill="white", font=title_font)
        
        # Add icon/symbol based on category
        icon_map = {
            "Core Hardware Evolution": "⚙️",
            "Component-Based": "🔧", 
            "Storage & Data": "💾",
            "Architecture & Integration": "🏗️",
            "Networking & Connectivity": "🌐",
            "Software & Tools": "💻",
            "Gaming-Specific": "🎮",
            "Security & Protection": "🔒",
            "Trends & Culture": "📈"
        }
        
        icon = icon_map.get(category, "📚")
        draw.text((350, 200), icon, fill="white", font=ImageFont.load_default())
        
        # Save image
        img.save(filename, "JPEG", quality=95)
        print(f"✅ Created thumbnail: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Error creating thumbnail for {course_title}: {e}")
        return False

# Enhanced course content with actual educational material
ENHANCED_COURSES = [
    {
        "title": "History of GPUs",
        "thumbnail": "gpu_history.jpg",
        "modules": [
            {
                "title": "The Dawn of 3D Graphics (1990-1995)",
                "description": "Understanding the revolutionary early 3D accelerators",
                "content": """
# The Dawn of 3D Graphics (1990-1995)

## Introduction
The early 1990s marked a pivotal moment in computer graphics history. Before dedicated 3D graphics cards, personal computers relied on software rendering, which was painfully slow and limited.

## Key Players and Innovations

### 3dfx Voodoo Graphics (1996)
- **Revolutionary Impact**: First mainstream 3D accelerator
- **Technical Specs**: 4MB EDO DRAM, 50MHz processor
- **Supported APIs**: Glide (proprietary), later OpenGL
- **Games That Changed Everything**: Quake, Tomb Raider, Need for Speed

### Early Competitors
- **Rendition Verite**: Early DirectX support
- **ATI Rage**: 2D/3D combo cards
- **Matrox Mystique**: Budget 3D acceleration

## Technical Foundations

### Texture Mapping
Before 3D accelerators, texture mapping was:
- Performed entirely by the CPU
- Limited to low resolutions (320x240)
- Resulted in slideshow-like frame rates

With hardware acceleration:
- Dedicated texture memory
- Hardware-accelerated filtering
- Real-time texture mapping at higher resolutions

### Z-Buffering
- **Problem Solved**: Proper depth sorting of 3D objects
- **Technical Implementation**: Dedicated depth buffer memory
- **Visual Impact**: Eliminated polygon sorting artifacts

## Impact on Gaming Industry
The introduction of 3D accelerators:
1. Created the modern PC gaming market
2. Established hardware upgrade cycles
3. Drove software innovation in game engines
4. Led to the consolidation of graphics standards

## Programming Interface Evolution
- **Early Days**: Direct hardware access
- **Glide API**: 3dfx's proprietary interface
- **OpenGL**: Industry-standard 3D API
- **DirectX**: Microsoft's gaming-focused API

## Market Transformation
The success of early 3D accelerators:
- Created a billion-dollar graphics card industry
- Established NVIDIA and ATI as major players
- Led to rapid innovation cycles
- Made 3D gaming mainstream

## Conclusion
The dawn of 3D graphics acceleration transformed personal computing from a text-and-2D environment into the rich, immersive 3D world we know today. Understanding this history helps appreciate the incredible technological journey that brought us modern GPUs.
                """,
                "order": 1
            },
            {
                "title": "NVIDIA's Rise: GeForce Series Evolution",
                "description": "From GeForce 256 to RTX 4090 - The path to GPU dominance",
                "content": """
# NVIDIA's Rise: GeForce Series Evolution

## The Beginning: RIVA Series (Pre-GeForce)
Before the GeForce brand, NVIDIA produced the RIVA series:
- **RIVA 128**: First viable NVIDIA 3D accelerator
- **RIVA TNT**: Challenged 3dfx's dominance
- **RIVA TNT2**: Improved performance and features

## GeForce 256 (1999): "The World's First GPU"
### Revolutionary Features
- **Hardware Transform & Lighting (T&L)**: Moved vertex processing from CPU to GPU
- **Cube Environment Mapping**: Advanced reflection techniques
- **32-bit Color Depth**: Superior color accuracy
- **AGP 4X Support**: Faster data transfer

### Technical Specifications
- Manufacturing Process: 220nm
- Transistors: 23 million
- Memory: 32MB DDR SDRAM
- Fill Rate: 480 million pixels/second

## GeForce 2 Series (2000-2001)
### GeForce2 GTS
- **Performance**: 2x faster than GeForce 256
- **Memory**: Up to 64MB DDR
- **New Features**: Hardware motion compensation

### GeForce2 MX
- **Market Strategy**: Budget-friendly 3D acceleration
- **Compromises**: Reduced memory bandwidth
- **Success**: Brought hardware T&L to mainstream market

## GeForce 3 Series (2001): DirectX 8 Pioneer
### Breakthrough Technologies
- **Vertex Shaders**: Programmable vertex processing
- **Pixel Shaders**: Programmable fragment processing  
- **Lightspeed Memory Architecture**: Advanced memory controller

### Impact on Gaming
- Enabled games like Morrowind and Splinter Cell
- Introduced programmable shading to mainstream
- Set foundation for modern GPU architecture

## GeForce 4 Series (2002)
### GeForce4 Ti
- **Performance Leadership**: Fastest GPU of its time
- **Advanced Features**: Improved shader capabilities
- **Market Position**: Premium gaming solution

### GeForce4 MX Series
- **Controversy**: DirectX 7-class features with GeForce4 branding
- **Market Confusion**: Led to consumer education issues
- **Lesson Learned**: Clear product positioning importance

## GeForce FX Series (2003-2004): Learning From Mistakes
### Technical Challenges
- **Manufacturing**: Early 130nm process difficulties
- **Heat Issues**: Required loud cooling solutions
- **Performance**: Struggled against ATI Radeon 9700/9800

### Innovations Despite Problems
- **CineFX Engine**: Advanced shader architecture
- **Intellisample**: Anti-aliasing improvements
- **UltraShadow**: Hardware shadow volume acceleration

## GeForce 6 Series (2004-2005): Return to Form
### Major Improvements
- **SLI Technology**: Multi-GPU rendering
- **Shader Model 3.0**: Advanced programmable shaders
- **PCI Express**: New high-speed interface

### GeForce 6800 Ultra
- Performance: Dominated high-end market
- Features: Full DirectX 9c support
- Architecture: Foundation for future designs

## GeForce 7 Series (2005-2006)
### GeForce 7800 GTX
- **90nm Process**: Improved power efficiency
- **Performance**: Solid generational improvement
- **Features**: Enhanced video processing

## GeForce 8 Series (2006-2007): Unified Architecture
### Revolutionary Changes
- **Unified Shaders**: Single shader units for vertex/pixel processing
- **CUDA Cores**: Foundation for general-purpose GPU computing
- **DirectX 10**: Next-generation graphics API support

### GeForce 8800 GTX
- **Performance**: Massive leap over previous generation
- **Architecture**: Stream processor design
- **Impact**: Enabled Crysis and other demanding games

## Modern Era: RTX Series (2018-Present)
### RTX 20 Series: Ray Tracing Revolution
- **RT Cores**: Dedicated ray tracing hardware
- **Tensor Cores**: AI acceleration for DLSS
- **Real-Time Ray Tracing**: Photorealistic lighting and reflections

### RTX 30 Series: Ampere Architecture
- **Performance**: Significant generational leap
- **Efficiency**: Improved performance per watt
- **Features**: Enhanced ray tracing and DLSS 2.0

### RTX 40 Series: Ada Lovelace
- **DLSS 3**: Frame generation technology
- **AV1 Encoding**: Next-gen streaming support
- **Efficiency**: Industry-leading performance per watt

## NVIDIA's Strategic Advantages
### Software Ecosystem
- **CUDA**: Parallel computing platform
- **GameWorks**: Developer tools and libraries
- **GeForce Experience**: User experience software

### Market Positioning
- **Gaming**: High-end performance leadership
- **Professional**: Quadro/RTX professional cards
- **Data Center**: AI and machine learning acceleration

## Conclusion
NVIDIA's journey from RIVA to RTX represents one of the most successful technology company transformations in history. By consistently innovating in architecture, manufacturing, and software, NVIDIA transformed from a scrappy startup to the world's most valuable semiconductor company.

The key lessons from NVIDIA's rise:
1. **Innovation Leadership**: Continuous technological advancement
2. **Market Timing**: Entering new markets at the right moment
3. **Software Strategy**: Building comprehensive ecosystems
4. **Brand Building**: Creating aspirational premium products
5. **Diversification**: Expanding beyond gaming into AI and data centers
                """,
                "order": 2
            }
        ]
    }
]

async def enhance_all_courses():
    """Add comprehensive content and thumbnails to all courses"""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        courses_collection = db.courses
        
        print("🚀 Starting course enhancement...")
        
        # Get all courses
        courses = await courses_collection.find({}).to_list(None)
        print(f"📚 Found {len(courses)} courses to enhance")
        
        enhanced_count = 0
        
        for course in courses:
            try:
                course_title = course.get("title", "Unknown Course")
                category = course.get("category", "General")
                
                # Create thumbnail
                thumbnail_filename = f"course_{course['_id']}.jpg"
                thumbnail_path = UPLOAD_DIR / "courses" / thumbnail_filename
                
                if create_course_thumbnail(course_title, category, thumbnail_path):
                    # Update course with thumbnail URL
                    update_data = {
                        "thumbnail_url": f"/api/media/courses/{thumbnail_filename}",
                        "updated_at": datetime.utcnow()
                    }
                    
                    # Add detailed content to modules if they exist
                    if "modules" in course and course["modules"]:
                        enhanced_modules = []
                        for i, module in enumerate(course["modules"]):
                            enhanced_module = {
                                "title": module.get("title", f"Module {i+1}"),
                                "description": module.get("description", "Course module content"),
                                "content": create_detailed_module_content(
                                    course_title, 
                                    module.get("title", f"Module {i+1}"),
                                    module.get("description", "")
                                ),
                                "order": module.get("order", i+1),
                                "duration_minutes": 15 + (i * 5),  # Realistic reading time
                                "image_urls": [],
                                "content_url": None,
                                "video_url": None
                            }
                            enhanced_modules.append(enhanced_module)
                        
                        update_data["modules"] = enhanced_modules
                    
                    # Update in database
                    await courses_collection.update_one(
                        {"_id": course["_id"]},
                        {"$set": update_data}
                    )
                    
                    enhanced_count += 1
                    print(f"✅ Enhanced: {course_title}")
                
            except Exception as e:
                print(f"❌ Error enhancing {course.get('title', 'Unknown')}: {e}")
        
        print(f"\n🎉 Successfully enhanced {enhanced_count} courses!")
        
        # Now let's set 3 featured courses for the homepage
        await set_featured_courses(courses_collection)
        
    except Exception as e:
        print(f"❌ Error in course enhancement: {e}")
        return False
    
    return True

def create_detailed_module_content(course_title, module_title, module_description):
    """Generate comprehensive educational content for each module"""
    
    content_templates = {
        "History": f"""
# {module_title}

## Overview
{module_description}

## Historical Context
Understanding the historical development of {module_title.lower()} requires examining the technological, economic, and social factors that drove innovation in this field.

### Key Timeline Events
- **Early Development**: Initial concepts and prototype implementations
- **Commercial Introduction**: First mass-market products and their reception
- **Technological Breakthroughs**: Major innovations that changed the landscape
- **Market Evolution**: How competition and consumer demand shaped development
- **Modern Era**: Current state and recent innovations

## Technical Deep Dive
### Architecture and Design
The fundamental architecture underlying {module_title.lower()} involves several key components:
1. **Core Components**: Essential elements and their functions
2. **Interface Design**: How different parts communicate
3. **Performance Characteristics**: Speed, efficiency, and capability metrics
4. **Compatibility**: Standards and interoperability considerations

### Manufacturing and Production
- **Materials**: Key materials and their properties
- **Process Technology**: Manufacturing techniques and capabilities
- **Quality Control**: Testing and validation procedures
- **Cost Factors**: Economic considerations affecting design decisions

## Impact and Significance
### Industry Impact
The development of {module_title.lower()} had significant effects on:
- Hardware manufacturers and their strategies
- Software developers and application design
- End users and their computing experiences
- Market dynamics and competitive landscape

### Technical Innovations
Key innovations introduced by {module_title.lower()} include:
- Performance improvements over previous solutions
- New capabilities that weren't previously possible
- Efficiency gains in power, space, or cost
- Foundation for future technological developments

## Learning Objectives
By the end of this module, you should understand:
1. The historical progression and key milestones
2. Technical architecture and design principles
3. Manufacturing and implementation challenges
4. Market impact and competitive dynamics
5. Relevance to modern computing systems

## Practical Applications
Real-world applications where this technology is crucial:
- Gaming and entertainment systems
- Professional workstations and creative tools
- Enterprise and server environments
- Mobile and embedded devices
- Emerging technologies and future applications

## Summary
{module_title} represents a crucial chapter in the evolution of computer technology. Understanding its development helps appreciate both historical context and modern computing capabilities.
        """,
        
        "Evolution": f"""
# {module_title}

## Introduction to Evolution
The evolution of {module_title.lower()} represents one of the most dynamic areas of technological advancement in computing history.

## Evolutionary Stages

### Generation 1: Foundation
- **Initial Concepts**: Basic principles and early implementations
- **Limitations**: Technical constraints of the era
- **Breakthrough Moments**: Key innovations that enabled progress
- **Market Reception**: How early adopters responded

### Generation 2: Refinement
- **Improved Design**: Addressing first-generation limitations
- **Enhanced Performance**: Measurable improvements in key metrics
- **Broader Adoption**: Expanding market acceptance
- **Competitive Dynamics**: Multiple players entering the market

### Generation 3: Maturation
- **Standardization**: Industry-wide standards and protocols
- **Optimization**: Fine-tuning for efficiency and performance
- **Feature Integration**: Combining multiple capabilities
- **Market Leadership**: Emergence of dominant players

### Generation 4: Innovation
- **Revolutionary Changes**: Fundamental architecture improvements
- **New Capabilities**: Previously impossible features
- **Ecosystem Development**: Supporting technologies and services
- **Industry Transformation**: Changing the broader market

### Current Generation: Excellence
- **State-of-the-Art**: Current best-in-class implementations
- **Performance Benchmarks**: Industry-leading specifications
- **Advanced Features**: Cutting-edge capabilities
- **Future Readiness**: Preparation for next-generation requirements

## Technical Analysis
### Performance Metrics
Key performance indicators for {module_title.lower()}:
- **Speed**: Throughput and latency characteristics
- **Efficiency**: Power consumption and thermal performance
- **Capacity**: Storage, processing, or handling capabilities
- **Reliability**: Error rates and durability metrics

### Design Principles
Fundamental design principles that have guided evolution:
1. **Performance Optimization**: Maximizing speed and efficiency
2. **Cost Effectiveness**: Balancing performance with affordability
3. **Compatibility**: Maintaining backward and forward compatibility
4. **Scalability**: Supporting different performance tiers
5. **Innovation**: Incorporating new technologies and techniques

## Market Impact
### Economic Significance
- **Market Size**: Revenue and unit volume growth over time
- **Price Trends**: How costs have changed with technological advancement
- **Competitive Landscape**: Major players and their market positions
- **Investment**: R&D spending and capital requirements

### Consumer Benefits
Evolution has provided consumers with:
- Better performance at lower costs
- New capabilities and applications
- Improved reliability and longevity
- Enhanced user experiences

## Future Outlook
### Emerging Trends
Current developments that will shape the future:
- Advanced manufacturing processes
- New materials and design approaches
- Integration with artificial intelligence
- Sustainability and environmental considerations

### Predicted Developments
Anticipated advances in the next 5-10 years:
- Performance improvements and capability expansions
- New application areas and use cases
- Integration with emerging technologies
- Market and industry changes

## Conclusion
The evolution of {module_title} demonstrates the rapid pace of technological advancement in computing. Understanding this progression provides valuable insight into both current capabilities and future possibilities.
        """,
        
        "Technology": f"""
# {module_title}

## Technical Overview
{module_description}

This comprehensive guide explores the technology behind {module_title.lower()}, examining both fundamental principles and advanced implementations.

## Core Technology Concepts

### Fundamental Principles
Understanding {module_title.lower()} requires mastery of several core concepts:
1. **Basic Operation**: How the technology functions at its most fundamental level
2. **Key Components**: Essential parts and their specific roles
3. **System Integration**: How components work together effectively
4. **Performance Characteristics**: Metrics that define capability and efficiency

### Technical Specifications
#### Physical Characteristics
- **Dimensions**: Size constraints and form factor considerations
- **Power Requirements**: Electrical specifications and consumption
- **Thermal Properties**: Heat generation and cooling requirements
- **Material Composition**: Key materials and their properties

#### Performance Parameters
- **Speed Metrics**: Processing rates and response times
- **Capacity Limits**: Maximum handling or storage capabilities
- **Efficiency Ratings**: Performance per unit of power or cost
- **Reliability Measures**: Expected lifespan and failure rates

## Advanced Features and Capabilities

### Modern Implementations
Current state-of-the-art implementations include:
- **High-Performance Variants**: Optimized for maximum capability
- **Efficiency-Focused Designs**: Optimized for power consumption
- **Compact Solutions**: Space-constrained implementations
- **Cost-Optimized Options**: Budget-friendly alternatives

### Specialized Applications
{module_title} technology is specifically optimized for:
- **Gaming and Entertainment**: High-performance consumer applications
- **Professional Workloads**: Business and creative professional needs
- **Enterprise Solutions**: Large-scale organizational requirements
- **Embedded Systems**: Integrated and specialized implementations

## Implementation Challenges

### Technical Challenges
Major engineering challenges include:
1. **Performance Optimization**: Maximizing speed while managing constraints
2. **Power Management**: Balancing performance with energy efficiency
3. **Thermal Design**: Managing heat generation and dissipation
4. **Manufacturing**: Achieving consistent quality at scale
5. **Cost Control**: Maintaining affordability while adding features

### Solution Approaches
Industry approaches to addressing challenges:
- **Advanced Materials**: Using superior materials for better performance
- **Innovative Design**: New architectural approaches
- **Manufacturing Innovation**: Improved production processes
- **System Optimization**: Whole-system approach to efficiency

## Industry Standards and Protocols

### Standards Organizations
Key organizations that define industry standards:
- **IEEE**: International standards for electrical and electronic systems
- **JEDEC**: Semiconductor standards organization
- **PCI-SIG**: Peripheral component interconnect standards
- **Industry Consortiums**: Collaborative standards development

### Compatibility and Interoperability
Ensuring different implementations work together:
- **Interface Standards**: Common connection and communication protocols
- **Performance Tiers**: Standardized capability levels
- **Backward Compatibility**: Support for older implementations
- **Future-Proofing**: Design considerations for upcoming standards

## Performance Analysis

### Benchmarking and Testing
Standard methods for evaluating performance:
- **Synthetic Benchmarks**: Standardized performance tests
- **Real-World Applications**: Actual use case performance
- **Stress Testing**: Performance under extreme conditions
- **Longevity Testing**: Long-term reliability assessment

### Optimization Techniques
Methods for maximizing performance:
- **Hardware Optimization**: Physical design improvements
- **Software Optimization**: Driver and firmware enhancements
- **System Tuning**: Configuration adjustments for specific uses
- **Cooling Solutions**: Thermal management for sustained performance

## Future Technology Developments

### Emerging Technologies
Next-generation technologies that will impact the field:
- **Advanced Manufacturing**: Smaller, more efficient production processes
- **New Materials**: Novel substances with superior properties
- **AI Integration**: Artificial intelligence for optimization and control
- **Quantum Technologies**: Potential quantum computing integration

### Predicted Advances
Anticipated improvements in the next decade:
- **Performance Scaling**: Continued improvements in capability
- **Efficiency Gains**: Better performance per unit of power
- **New Features**: Capabilities not currently available
- **Cost Reductions**: Making advanced technology more accessible

## Conclusion
{module_title} represents a critical technology in modern computing systems. Understanding both its current implementations and future potential is essential for anyone working with or interested in computer technology.

Mastery of this technology enables:
- Better decision-making when selecting components
- More effective troubleshooting and optimization
- Appreciation for the engineering excellence involved
- Preparation for future technological developments
        """
    }
    
    # Choose template based on module title keywords
    if any(word in module_title.lower() for word in ["history", "origin", "dawn", "early"]):
        return content_templates["History"]
    elif any(word in module_title.lower() for word in ["evolution", "development", "progression", "advancement"]):
        return content_templates["Evolution"]
    else:
        return content_templates["Technology"]

async def set_featured_courses(courses_collection):
    """Set 3 featured courses for the homepage"""
    try:
        # First, clear any existing featured courses
        await courses_collection.update_many(
            {},
            {"$unset": {"featured": ""}}
        )
        
        # Select 3 diverse and interesting courses to feature
        featured_courses = [
            "History of GPUs",
            "Multi-core CPUs and SMT", 
            "DIY PC Building Culture"
        ]
        
        for course_title in featured_courses:
            result = await courses_collection.update_one(
                {"title": course_title},
                {"$set": {"featured": True, "featured_order": featured_courses.index(course_title) + 1}}
            )
            if result.modified_count > 0:
                print(f"✅ Set as featured: {course_title}")
        
        print(f"\n🌟 Set {len(featured_courses)} featured courses for homepage")
        
    except Exception as e:
        print(f"❌ Error setting featured courses: {e}")

if __name__ == "__main__":
    asyncio.run(enhance_all_courses())
