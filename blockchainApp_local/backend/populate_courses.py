#!/usr/bin/env python3
"""
Populate database with comprehensive hardware courses and modules
"""

import asyncio
import sys
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, DATABASE_NAME

# Course data with comprehensive modules
COURSES_DATA = [
    # 🧠 Core Hardware Evolution Topics
    {
        "title": "History of GPUs",
        "description": "Comprehensive exploration of Graphics Processing Unit evolution from early 3D accelerators to modern AI powerhouses",
        "price": 0.000005,
        "category": "Core Hardware Evolution",
        "difficulty": "intermediate",
        "duration": "8 weeks",
        "instructor": "Hardware Evolution Team",
        "modules": [
            {
                "title": "The Dawn of 3D Graphics",
                "description": "Early 3D accelerators, Voodoo Graphics, and the birth of consumer 3D",
                "content": "Explore the revolutionary Voodoo Graphics cards that changed PC gaming forever",
                "order": 1
            },
            {
                "title": "NVIDIA's Rise: GeForce Series",
                "description": "From GeForce 256 to RTX 4090 - NVIDIA's journey to GPU dominance",
                "content": "Deep dive into NVIDIA's architectural innovations and market strategies",
                "order": 2
            },
            {
                "title": "AMD/ATI Graphics Evolution",
                "description": "ATI Radeon series, AMD acquisition, and the RDNA architecture revolution",
                "content": "Understanding AMD's graphics philosophy and competitive positioning",
                "order": 3
            },
            {
                "title": "GPU Architecture Deep Dive",
                "description": "Shader units, ROPs, memory controllers, and modern GPU design",
                "content": "Technical analysis of how modern GPUs process graphics and compute workloads",
                "order": 4
            },
            {
                "title": "CUDA and GPU Computing",
                "description": "How GPUs became general-purpose computing powerhouses",
                "content": "From graphics-only to AI acceleration - the GPGPU revolution",
                "order": 5
            },
            {
                "title": "Ray Tracing and Real-Time Graphics",
                "description": "RTX, RDNA 2, and the future of photorealistic gaming",
                "content": "Understanding ray tracing technology and its impact on visual fidelity",
                "order": 6
            },
            {
                "title": "AI and Machine Learning on GPUs",
                "description": "Tensor cores, DLSS, FSR, and AI-accelerated graphics",
                "content": "How modern GPUs leverage AI for better performance and image quality",
                "order": 7
            },
            {
                "title": "Future of Graphics Technology",
                "description": "Quantum computing, neuromorphic chips, and next-gen graphics",
                "content": "Exploring emerging technologies that will shape future graphics processing",
                "order": 8
            }
        ]
    },
    {
        "title": "Evolution of CPUs",
        "description": "From Pentium 4 to modern i9, Ryzen 9, and Threadripper - the complete CPU evolution story",
        "price": 0.000005,
        "category": "Core Hardware Evolution",
        "difficulty": "intermediate",
        "duration": "10 weeks",
        "instructor": "CPU Architecture Team",
        "modules": [
            {
                "title": "The Pentium 4 Era and NetBurst",
                "description": "Understanding Intel's ambitious but flawed NetBurst architecture",
                "content": "Deep dive into why Pentium 4's high clock speeds didn't translate to performance",
                "order": 1
            },
            {
                "title": "AMD's Athlon Revolution",
                "description": "How AMD challenged Intel with superior architecture",
                "content": "The rise of Athlon 64 and the introduction of 64-bit computing",
                "order": 2
            },
            {
                "title": "Intel's Core Architecture Comeback",
                "description": "From Core Duo to Core i7 - Intel's architectural renaissance",
                "content": "Understanding Intel's return to efficiency-focused design",
                "order": 3
            },
            {
                "title": "Multi-core Revolution",
                "description": "Dual-core to many-core: How CPUs embraced parallelism",
                "content": "Technical deep dive into multi-core design challenges and solutions",
                "order": 4
            },
            {
                "title": "AMD Ryzen and Zen Architecture",
                "description": "AMD's comeback with revolutionary Zen architecture",
                "content": "How chiplet design and advanced manufacturing changed the CPU landscape",
                "order": 5
            },
            {
                "title": "Intel vs AMD: The Modern CPU Wars",
                "description": "Current generation CPUs and their architectural differences",
                "content": "Comparing Intel 13th gen vs AMD Ryzen 7000 series performance",
                "order": 6
            },
            {
                "title": "HEDT and Workstation CPUs",
                "description": "Threadripper, EPYC, Xeon - CPUs for extreme workloads",
                "content": "Understanding high-end desktop and server CPU architectures",
                "order": 7
            },
            {
                "title": "ARM and Alternative Architectures",
                "description": "Apple Silicon, ARM servers, and RISC-V emergence",
                "content": "Exploring non-x86 architectures and their growing importance",
                "order": 8
            },
            {
                "title": "CPU Performance Optimization",
                "description": "Overclocking, cooling, and getting maximum CPU performance",
                "content": "Practical guide to CPU tuning and performance optimization",
                "order": 9
            },
            {
                "title": "Future CPU Technologies",
                "description": "Quantum computing, neuromorphic processors, and beyond silicon",
                "content": "Exploring next-generation CPU technologies and architectures",
                "order": 10
            }
        ]
    },
    {
        "title": "Storage Device Evolution",
        "description": "From mechanical HDDs to lightning-fast NVMe SSDs - the complete storage evolution",
        "price": 0.000005,
        "category": "Core Hardware Evolution",
        "difficulty": "beginner",
        "duration": "6 weeks",
        "instructor": "Storage Technology Team",
        "modules": [
            {
                "title": "Mechanical Hard Drive Fundamentals",
                "description": "Understanding HDD technology, platters, heads, and mechanical operation",
                "content": "Deep dive into how traditional hard drives store and retrieve data",
                "order": 1
            },
            {
                "title": "SSD Technology Revolution",
                "description": "NAND flash memory, controllers, and the solid-state advantage",
                "content": "How SSDs eliminated moving parts and revolutionized storage performance",
                "order": 2
            },
            {
                "title": "Interface Evolution: SATA to NVMe",
                "description": "From parallel ATA to SATA to NVMe - storage interface progression",
                "content": "Understanding how storage interfaces have evolved to meet speed demands",
                "order": 3
            },
            {
                "title": "NVMe and PCIe Storage",
                "description": "Next-generation storage leveraging PCIe lanes for maximum speed",
                "content": "Technical analysis of NVMe protocol and PCIe integration benefits",
                "order": 4
            },
            {
                "title": "Storage Performance and Optimization",
                "description": "IOPS, throughput, latency, and storage performance metrics",
                "content": "Understanding and optimizing storage performance for different workloads",
                "order": 5
            },
            {
                "title": "Future Storage Technologies",
                "description": "Optane, MRAM, and emerging storage technologies",
                "content": "Exploring next-generation storage technologies beyond NAND flash",
                "order": 6
            }
        ]
    },
    {
        "title": "Motherboard Evolution",
        "description": "Chipsets, form factors, and features - how motherboards have evolved with PC technology",
        "price": 0.000005,
        "category": "Core Hardware Evolution",
        "difficulty": "intermediate",
        "duration": "7 weeks",
        "instructor": "Motherboard Design Team",
        "modules": [
            {
                "title": "Motherboard Fundamentals",
                "description": "Understanding PCB design, traces, and motherboard basics",
                "content": "Foundation knowledge of motherboard construction and design principles",
                "order": 1
            },
            {
                "title": "Chipset Evolution",
                "description": "Northbridge/Southbridge to modern unified chipsets",
                "content": "How chipset design has evolved to support modern CPU architectures",
                "order": 2
            },
            {
                "title": "Form Factor Development",
                "description": "ATX, microATX, Mini-ITX, and specialized form factors",
                "content": "Understanding different motherboard sizes and their use cases",
                "order": 3
            },
            {
                "title": "Expansion Slot Evolution",
                "description": "From ISA to PCIe 5.0 - expansion slot progression",
                "content": "How expansion slots have evolved to support faster components",
                "order": 4
            },
            {
                "title": "Power Delivery Systems",
                "description": "VRMs, power phases, and clean power delivery to components",
                "content": "Understanding motherboard power delivery and its impact on performance",
                "order": 5
            },
            {
                "title": "Connectivity and I/O Evolution",
                "description": "USB, networking, audio, and I/O advancement on motherboards",
                "content": "How motherboard connectivity has expanded with technology",
                "order": 6
            },
            {
                "title": "Modern Motherboard Features",
                "description": "RGB lighting, WiFi 6E, and premium motherboard features",
                "content": "Exploring advanced features in modern high-end motherboards",
                "order": 7
            }
        ]
    },
    # 🔌 Component-Based Topics
    {
        "title": "Rise of RAM: From SDRAM to DDR5",
        "description": "Memory evolution from early SDRAM to cutting-edge DDR5 technology",
        "price": 0.000005,
        "category": "Component-Based",
        "difficulty": "intermediate",
        "duration": "5 weeks",
        "instructor": "Memory Technology Team",
        "modules": [
            {
                "title": "Memory Fundamentals",
                "description": "Understanding how computer memory works at the fundamental level",
                "content": "Basic principles of volatile memory and data storage",
                "order": 1
            },
            {
                "title": "SDRAM and Early DDR",
                "description": "Synchronous DRAM and the first DDR memory standards",
                "content": "Evolution from SDRAM to DDR and early performance improvements",
                "order": 2
            },
            {
                "title": "DDR2 and DDR3 Advancement",
                "description": "Higher speeds, lower voltages, and improved efficiency",
                "content": "Technical improvements in DDR2 and DDR3 generations",
                "order": 3
            },
            {
                "title": "DDR4 Revolution",
                "description": "Modern memory with improved bandwidth and capacity",
                "content": "DDR4 features, performance benefits, and widespread adoption",
                "order": 4
            },
            {
                "title": "DDR5 and Beyond",
                "description": "Latest memory technology with unprecedented speeds",
                "content": "DDR5 innovations and future memory technology roadmap",
                "order": 5
            }
        ]
    },
    {
        "title": "Cooling Systems Evolution",
        "description": "From basic air coolers to advanced AIO and custom liquid cooling solutions",
        "price": 0.000005,
        "category": "Component-Based",
        "difficulty": "beginner",
        "duration": "6 weeks",
        "instructor": "Thermal Management Team",
        "modules": [
            {
                "title": "Heat Management Fundamentals",
                "description": "Understanding thermal dynamics in computer systems",
                "content": "Physics of heat generation and dissipation in PCs",
                "order": 1
            },
            {
                "title": "Air Cooling Technologies",
                "description": "CPU coolers, case fans, and airflow optimization",
                "content": "Comprehensive guide to air-based cooling solutions",
                "order": 2
            },
            {
                "title": "All-in-One Liquid Coolers",
                "description": "AIO coolers: convenience meets performance",
                "content": "Understanding AIO technology and installation best practices",
                "order": 3
            },
            {
                "title": "Custom Liquid Cooling",
                "description": "Building custom loops for maximum cooling performance",
                "content": "Advanced liquid cooling with pumps, radiators, and reservoirs",
                "order": 4
            },
            {
                "title": "Thermal Interface Materials",
                "description": "Thermal paste, pads, and heat transfer optimization",
                "content": "Choosing and applying thermal interface materials effectively",
                "order": 5
            },
            {
                "title": "Cooling System Maintenance",
                "description": "Keeping cooling systems clean and effective long-term",
                "content": "Maintenance schedules and troubleshooting cooling issues",
                "order": 6
            }
        ]
    },
    {
        "title": "Power Supply Evolution",
        "description": "PSU development, 80+ ratings, and modular design advancement",
        "price": 0.000005,
        "category": "Component-Based",
        "difficulty": "intermediate",
        "duration": "5 weeks",
        "instructor": "Power Systems Team",
        "modules": [
            {
                "title": "Power Supply Fundamentals",
                "description": "AC to DC conversion and power delivery basics",
                "content": "Understanding how PSUs convert and deliver clean power",
                "order": 1
            },
            {
                "title": "Efficiency and 80+ Certification",
                "description": "Power efficiency standards and environmental impact",
                "content": "Understanding 80+ ratings from Bronze to Titanium",
                "order": 2
            },
            {
                "title": "Modular PSU Design",
                "description": "Cable management and modular power supply benefits",
                "content": "Evolution from fixed cables to fully modular designs",
                "order": 3
            },
            {
                "title": "Power Requirements and Sizing",
                "description": "Calculating power needs for different PC configurations",
                "content": "Proper PSU sizing for various system configurations",
                "order": 4
            },
            {
                "title": "Power Quality and Protection",
                "description": "Clean power delivery and component protection features",
                "content": "Understanding PSU protection circuits and power quality",
                "order": 5
            }
        ]
    },
    {
        "title": "PC Case Design Evolution",
        "description": "From beige boxes to RGB-heavy gaming towers and modern aesthetics",
        "price": 0.000005,
        "category": "Component-Based",
        "difficulty": "beginner",
        "duration": "4 weeks",
        "instructor": "Case Design Team",
        "modules": [
            {
                "title": "Early PC Case Design",
                "description": "Beige box era and functional-first design philosophy",
                "content": "Understanding early PC case design priorities and limitations",
                "order": 1
            },
            {
                "title": "Gaming Case Revolution",
                "description": "Transparent panels, LED lighting, and gaming aesthetics",
                "content": "How gaming culture influenced PC case design",
                "order": 2
            },
            {
                "title": "Airflow and Thermal Design",
                "description": "Case ventilation, fan placement, and thermal optimization",
                "content": "Engineering optimal airflow in modern PC cases",
                "order": 3
            },
            {
                "title": "RGB and Modern Aesthetics",
                "description": "RGB lighting systems and contemporary case styling",
                "content": "Modern case features including RGB integration and cable management",
                "order": 4
            }
        ]
    },
    {
        "title": "Monitor Technology Evolution",
        "description": "From CRT monitors to OLED displays and high refresh rate gaming",
        "price": 0.000005,
        "category": "Component-Based",
        "difficulty": "beginner",
        "duration": "6 weeks",
        "instructor": "Display Technology Team",
        "modules": [
            {
                "title": "CRT Monitor Technology",
                "description": "Understanding cathode ray tube displays and their characteristics",
                "content": "Deep dive into CRT technology and its advantages/limitations",
                "order": 1
            },
            {
                "title": "LCD Revolution",
                "description": "Liquid crystal displays and the flat panel transition",
                "content": "How LCD technology replaced CRTs and improved portability",
                "order": 2
            },
            {
                "title": "LED Backlighting and Improvements",
                "description": "LED backlights, local dimming, and enhanced contrast",
                "content": "Evolution from CCFL to LED backlighting systems",
                "order": 3
            },
            {
                "title": "High Refresh Rate Gaming",
                "description": "60Hz to 360Hz displays for competitive gaming",
                "content": "Understanding refresh rates and their impact on gaming performance",
                "order": 4
            },
            {
                "title": "OLED and Premium Display Tech",
                "description": "Organic LED displays with perfect blacks and infinite contrast",
                "content": "OLED technology benefits and current limitations",
                "order": 5
            },
            {
                "title": "Future Display Technologies",
                "description": "MicroLED, quantum dot, and emerging display innovations",
                "content": "Exploring next-generation display technologies",
                "order": 6
            }
        ]
    },
    {
        "title": "Peripheral Evolution",
        "description": "Keyboards, mice, and gaming peripherals through the decades",
        "price": 0.000005,
        "category": "Component-Based",
        "difficulty": "beginner",
        "duration": "5 weeks",
        "instructor": "Peripheral Technology Team",
        "modules": [
            {
                "title": "Keyboard Technology Evolution",
                "description": "From mechanical to membrane and back to mechanical",
                "content": "Complete history of keyboard switch technology and design",
                "order": 1
            },
            {
                "title": "Mouse Technology Advancement",
                "description": "Ball mice to optical to gaming laser mice",
                "content": "Evolution of mouse sensors and gaming-focused features",
                "order": 2
            },
            {
                "title": "Gaming Controller Evolution",
                "description": "From simple joysticks to modern wireless controllers",
                "content": "Development of gaming controllers and their PC integration",
                "order": 3
            },
            {
                "title": "Wireless Peripheral Technology",
                "description": "Bluetooth, 2.4GHz, and low-latency wireless solutions",
                "content": "Wireless technology advancement in PC peripherals",
                "order": 4
            },
            {
                "title": "Specialized Gaming Peripherals",
                "description": "Gaming headsets, streaming equipment, and esports gear",
                "content": "Professional gaming peripherals and their technical advantages",
                "order": 5
            }
        ]
    },
    # 💾 Storage & Data Topics
    {
        "title": "File Systems Deep Dive",
        "description": "FAT32, NTFS, ext4, and modern file system technologies",
        "price": 0.000005,
        "category": "Storage & Data",
        "difficulty": "advanced",
        "duration": "7 weeks",
        "instructor": "File Systems Team",
        "modules": [
            {
                "title": "File System Fundamentals",
                "description": "Understanding how operating systems organize and access data",
                "content": "Basic concepts of file systems and data organization",
                "order": 1
            },
            {
                "title": "FAT and Early File Systems",
                "description": "File Allocation Table systems and early DOS/Windows storage",
                "content": "Historical perspective on early PC file systems",
                "order": 2
            },
            {
                "title": "NTFS Advanced Features",
                "description": "New Technology File System and Windows storage management",
                "content": "NTFS features including journaling, encryption, and compression",
                "order": 3
            },
            {
                "title": "Linux File Systems",
                "description": "ext2/3/4, XFS, and Linux storage solutions",
                "content": "Understanding Linux file system options and characteristics",
                "order": 4
            },
            {
                "title": "Modern File Systems",
                "description": "ZFS, Btrfs, and next-generation storage management",
                "content": "Advanced features like snapshots, deduplication, and checksumming",
                "order": 5
            },
            {
                "title": "Network and Cloud File Systems",
                "description": "NFS, SMB, and distributed storage solutions",
                "content": "File systems designed for network and cloud environments",
                "order": 6
            },
            {
                "title": "File System Performance",
                "description": "Optimization techniques and performance considerations",
                "content": "Tuning file systems for different workloads and use cases",
                "order": 7
            }
        ]
    },
    {
        "title": "RAID Configurations and Performance",
        "description": "Understanding RAID levels, performance impacts, and redundancy strategies",
        "price": 0.000005,
        "category": "Storage & Data",
        "difficulty": "advanced",
        "duration": "6 weeks",
        "instructor": "Storage Systems Team",
        "modules": [
            {
                "title": "RAID Fundamentals",
                "description": "Redundant Array of Independent Disks concepts and benefits",
                "content": "Understanding why RAID was developed and its core principles",
                "order": 1
            },
            {
                "title": "RAID 0, 1, and 10",
                "description": "Basic RAID levels for performance and redundancy",
                "content": "Striping, mirroring, and combined approaches",
                "order": 2
            },
            {
                "title": "RAID 5 and 6",
                "description": "Parity-based RAID for balanced performance and protection",
                "content": "Understanding parity calculations and distributed redundancy",
                "order": 3
            },
            {
                "title": "Hardware vs Software RAID",
                "description": "RAID controller cards vs operating system implementations",
                "content": "Comparing hardware and software RAID solutions",
                "order": 4
            },
            {
                "title": "RAID Performance Analysis",
                "description": "Benchmarking and optimizing RAID array performance",
                "content": "Understanding RAID performance characteristics and bottlenecks",
                "order": 5
            },
            {
                "title": "Modern Storage Alternatives",
                "description": "SSD RAID, storage pools, and software-defined storage",
                "content": "How modern storage technology is changing RAID implementation",
                "order": 6
            }
        ]
    },
    {
        "title": "BIOS to UEFI Evolution",
        "description": "Firmware evolution from legacy BIOS to modern UEFI systems",
        "price": 0.000005,
        "category": "Storage & Data",
        "difficulty": "intermediate",
        "duration": "5 weeks",
        "instructor": "Firmware Systems Team",
        "modules": [
            {
                "title": "Legacy BIOS Fundamentals",
                "description": "Understanding traditional BIOS and boot process",
                "content": "How legacy BIOS initializes hardware and loads operating systems",
                "order": 1
            },
            {
                "title": "BIOS Limitations",
                "description": "16-bit constraints and legacy BIOS restrictions",
                "content": "Understanding why BIOS needed to be replaced",
                "order": 2
            },
            {
                "title": "UEFI Architecture",
                "description": "Unified Extensible Firmware Interface design and capabilities",
                "content": "Modern firmware architecture and its advantages",
                "order": 3
            },
            {
                "title": "Secure Boot and Security",
                "description": "UEFI security features and secure boot process",
                "content": "Understanding UEFI security enhancements",
                "order": 4
            },
            {
                "title": "UEFI Features and Tools",
                "description": "UEFI shell, applications, and advanced features",
                "content": "Exploring UEFI's enhanced capabilities and tools",
                "order": 5
            }
        ]
    },
    # 🧠 Architecture & Integration Topics
    {
        "title": "Multi-core CPUs and SMT",
        "description": "Rise of multi-core processors and Simultaneous Multithreading technology",
        "price": 0.000005,
        "category": "Architecture & Integration",
        "difficulty": "advanced",
        "duration": "8 weeks",
        "instructor": "CPU Architecture Team",
        "modules": [
            {
                "title": "Single-core Limitations",
                "description": "Understanding why CPU manufacturers moved to multi-core designs",
                "content": "Power walls and frequency scaling limitations",
                "order": 1
            },
            {
                "title": "Dual-core Revolution",
                "description": "First dual-core processors and parallel computing concepts",
                "content": "Intel Core Duo and AMD Athlon X2 introduction",
                "order": 2
            },
            {
                "title": "Quad-core and Beyond",
                "description": "Scaling to 4, 6, 8, and more cores",
                "content": "Challenges and benefits of increasing core counts",
                "order": 3
            },
            {
                "title": "Hyper-Threading Technology",
                "description": "Intel's SMT implementation and virtual cores",
                "content": "How Hyper-Threading doubles thread capacity per core",
                "order": 4
            },
            {
                "title": "AMD's SMT Implementation",
                "description": "AMD's approach to simultaneous multithreading",
                "content": "Comparing Intel and AMD SMT technologies",
                "order": 5
            },
            {
                "title": "Many-core Architectures",
                "description": "16, 32, 64+ core processors for specialized workloads",
                "content": "Server and workstation many-core CPU designs",
                "order": 6
            },
            {
                "title": "Parallel Programming Challenges",
                "description": "Software adaptation to multi-core hardware",
                "content": "How software has evolved to utilize multiple cores",
                "order": 7
            },
            {
                "title": "Future of Multi-core Design",
                "description": "Heterogeneous computing and specialized cores",
                "content": "Big.LITTLE, efficiency cores, and future CPU designs",
                "order": 8
            }
        ]
    },
    {
        "title": "Integrated Graphics Evolution",
        "description": "On-die GPU integration from Intel HD Graphics to modern APUs",
        "price": 0.000005,
        "category": "Architecture & Integration",
        "difficulty": "intermediate",
        "duration": "6 weeks",
        "instructor": "Integrated Graphics Team",
        "modules": [
            {
                "title": "Early Integrated Graphics",
                "description": "First attempts at CPU-integrated graphics solutions",
                "content": "Early chipset graphics and their limitations",
                "order": 1
            },
            {
                "title": "Intel HD Graphics Revolution",
                "description": "Intel's on-die graphics integration strategy",
                "content": "How Intel integrated GPU functionality into CPUs",
                "order": 2
            },
            {
                "title": "AMD APU Innovation",
                "description": "Accelerated Processing Units combining CPU and GPU",
                "content": "AMD's approach to heterogeneous computing",
                "order": 3
            },
            {
                "title": "Performance Evolution",
                "description": "Integrated graphics performance improvements over generations",
                "content": "How integrated graphics became viable for gaming",
                "order": 4
            },
            {
                "title": "Modern Integrated Solutions",
                "description": "Intel Xe Graphics and AMD RDNA integration",
                "content": "Current state of integrated graphics technology",
                "order": 5
            },
            {
                "title": "Future of Integration",
                "description": "Chiplet designs and advanced GPU integration",
                "content": "Where integrated graphics technology is heading",
                "order": 6
            }
        ]
    },
    {
        "title": "Chiplet Design Revolution",
        "description": "Modern CPU and GPU chiplet architecture and its impact",
        "price": 0.000005,
        "category": "Architecture & Integration",
        "difficulty": "advanced",
        "duration": "7 weeks",
        "instructor": "Advanced Architecture Team",
        "modules": [
            {
                "title": "Monolithic Design Limitations",
                "description": "Why traditional single-die designs reached their limits",
                "content": "Manufacturing challenges with large monolithic dies",
                "order": 1
            },
            {
                "title": "Chiplet Concept Introduction",
                "description": "Breaking large processors into smaller, specialized dies",
                "content": "Fundamental principles of chiplet architecture",
                "order": 2
            },
            {
                "title": "AMD's Zen Chiplet Implementation",
                "description": "How AMD revolutionized CPU design with chiplets",
                "content": "Zen 2/3/4 chiplet designs and Infinity Fabric",
                "order": 3
            },
            {
                "title": "Intel's Response to Chiplets",
                "description": "Intel's chiplet strategy and implementation",
                "content": "Intel's approach to multi-die processor design",
                "order": 4
            },
            {
                "title": "GPU Chiplet Designs",
                "description": "Multi-chip GPU architectures and challenges",
                "content": "How chiplets are being applied to graphics processors",
                "order": 5
            },
            {
                "title": "Interconnect Technologies",
                "description": "High-speed links between chiplets",
                "content": "Infinity Fabric, EMIB, and other chiplet interconnects",
                "order": 6
            },
            {
                "title": "Future of Chiplet Design",
                "description": "Mix-and-match processors and heterogeneous computing",
                "content": "Where chiplet technology is heading in the future",
                "order": 7
            }
        ]
    },
    {
        "title": "PCIe Generations and Impact",
        "description": "PCIe evolution and its impact on GPU and SSD performance",
        "price": 0.000005,
        "category": "Architecture & Integration",
        "difficulty": "intermediate",
        "duration": "5 weeks",
        "instructor": "Interface Technology Team",
        "modules": [
            {
                "title": "PCIe Fundamentals",
                "description": "Understanding PCI Express architecture and lanes",
                "content": "How PCIe replaced older expansion interfaces",
                "order": 1
            },
            {
                "title": "PCIe Generations 1.0 to 3.0",
                "description": "Early PCIe development and bandwidth increases",
                "content": "Performance evolution through the first three PCIe generations",
                "order": 2
            },
            {
                "title": "PCIe 4.0 and Modern Storage",
                "description": "PCIe 4.0's impact on NVMe SSD performance",
                "content": "How PCIe 4.0 enabled next-generation storage speeds",
                "order": 3
            },
            {
                "title": "PCIe 5.0 and Beyond",
                "description": "Latest PCIe generation and future roadmap",
                "content": "PCIe 5.0/6.0 capabilities and implementation challenges",
                "order": 4
            },
            {
                "title": "PCIe Impact on System Performance",
                "description": "How PCIe generations affect overall system performance",
                "content": "Real-world performance differences between PCIe generations",
                "order": 5
            }
        ]
    },
    # 🌐 Networking & Connectivity Topics
    {
        "title": "PC Networking Evolution",
        "description": "From Ethernet to Wi-Fi 6E - comprehensive networking advancement",
        "price": 0.000005,
        "category": "Networking & Connectivity",
        "difficulty": "intermediate",
        "duration": "8 weeks",
        "instructor": "Networking Technology Team",
        "modules": [
            {
                "title": "Early PC Networking",
                "description": "Dial-up modems and early network connections",
                "content": "Understanding how PCs first connected to networks and the internet",
                "order": 1
            },
            {
                "title": "Ethernet Technology Evolution",
                "description": "10Base-T to Gigabit Ethernet advancement",
                "content": "Wired networking speed progression and technology improvements",
                "order": 2
            },
            {
                "title": "Wireless Networking Introduction",
                "description": "802.11 standards and wireless networking adoption",
                "content": "How Wi-Fi revolutionized PC connectivity",
                "order": 3
            },
            {
                "title": "Wi-Fi Standards Progression",
                "description": "802.11a/b/g/n/ac advancement and capabilities",
                "content": "Evolution of wireless standards and performance improvements",
                "order": 4
            },
            {
                "title": "Modern Wi-Fi: Wi-Fi 6 and 6E",
                "description": "Latest wireless technology with improved efficiency",
                "content": "Wi-Fi 6/6E features and performance enhancements",
                "order": 5
            },
            {
                "title": "Network Security Evolution",
                "description": "WEP to WPA3 - wireless security advancement",
                "content": "How wireless security has evolved to protect connections",
                "order": 6
            },
            {
                "title": "High-Speed Networking",
                "description": "10 Gigabit Ethernet and beyond for enthusiasts",
                "content": "Advanced networking for high-performance applications",
                "order": 7
            },
            {
                "title": "Future Networking Technologies",
                "description": "Wi-Fi 7, 5G integration, and next-generation connectivity",
                "content": "Emerging networking technologies and their potential impact",
                "order": 8
            }
        ]
    },
    {
        "title": "USB Standards Evolution",
        "description": "From USB 1.0 to USB4 and Type-C - complete USB progression",
        "price": 0.000005,
        "category": "Networking & Connectivity",
        "difficulty": "beginner",
        "duration": "6 weeks",
        "instructor": "USB Technology Team",
        "modules": [
            {
                "title": "USB 1.0/1.1 Introduction",
                "description": "Universal Serial Bus concept and early implementation",
                "content": "How USB simplified PC peripheral connections",
                "order": 1
            },
            {
                "title": "USB 2.0 High-Speed Era",
                "description": "480 Mbps and widespread USB adoption",
                "content": "USB 2.0's impact on peripheral performance and adoption",
                "order": 2
            },
            {
                "title": "USB 3.0/3.1/3.2 SuperSpeed",
                "description": "Multi-gigabit USB and backwards compatibility",
                "content": "USB 3.x generations and their performance improvements",
                "order": 3
            },
            {
                "title": "USB-C and USB4",
                "description": "Reversible connector and unified standard",
                "content": "USB-C's versatility and USB4's advanced capabilities",
                "order": 4
            },
            {
                "title": "USB Power Delivery",
                "description": "Charging laptops and devices through USB",
                "content": "How USB evolved to deliver significant power",
                "order": 5
            },
            {
                "title": "USB in Modern PCs",
                "description": "USB hubs, controllers, and system integration",
                "content": "Understanding USB implementation in modern systems",
                "order": 6
            }
        ]
    },
    {
        "title": "Port Wars: Connectivity Standards",
        "description": "Thunderbolt vs USB-C vs DisplayPort vs HDMI comparison",
        "price": 0.000005,
        "category": "Networking & Connectivity",
        "difficulty": "intermediate",
        "duration": "5 weeks",
        "instructor": "Connectivity Standards Team",
        "modules": [
            {
                "title": "Display Interface Evolution",
                "description": "VGA to DVI to HDMI to DisplayPort progression",
                "content": "How display interfaces have evolved with monitor technology",
                "order": 1
            },
            {
                "title": "HDMI Technology and Versions",
                "description": "High-Definition Multimedia Interface development",
                "content": "HDMI versions and their capabilities for audio/video",
                "order": 2
            },
            {
                "title": "DisplayPort Innovation",
                "description": "VESA's DisplayPort standard and its advantages",
                "content": "DisplayPort features and its competition with HDMI",
                "order": 3
            },
            {
                "title": "Thunderbolt Technology",
                "description": "Intel's high-speed interface combining data and display",
                "content": "Thunderbolt 1/2/3/4 evolution and capabilities",
                "order": 4
            },
            {
                "title": "USB-C Versatility",
                "description": "USB-C as a universal connector for multiple protocols",
                "content": "How USB-C can carry different signals and protocols",
                "order": 5
            }
        ]
    },
    # 🔧 Software & Tools Topics
    {
        "title": "Overclocking Evolution",
        "description": "From BIOS tweaks to AI-powered automatic tuning",
        "price": 0.000005,
        "category": "Software & Tools",
        "difficulty": "advanced",
        "duration": "7 weeks",
        "instructor": "Performance Tuning Team",
        "modules": [
            {
                "title": "Early Overclocking Methods",
                "description": "Jumpers, DIP switches, and manual frequency adjustment",
                "content": "Historical methods of overclocking PC components",
                "order": 1
            },
            {
                "title": "BIOS/UEFI Overclocking",
                "description": "Firmware-based performance tuning and settings",
                "content": "Understanding BIOS overclocking options and safety",
                "order": 2
            },
            {
                "title": "Software Overclocking Tools",
                "description": "MSI Afterburner, Intel XTU, and other tuning utilities",
                "content": "Using software tools for component overclocking",
                "order": 3
            },
            {
                "title": "Memory Overclocking",
                "description": "RAM timing optimization and frequency increases",
                "content": "Advanced memory overclocking techniques and stability",
                "order": 4
            },
            {
                "title": "GPU Overclocking",
                "description": "Graphics card performance optimization",
                "content": "Safe GPU overclocking for improved gaming performance",
                "order": 5
            },
            {
                "title": "AI-Powered Tuning",
                "description": "Automatic overclocking using artificial intelligence",
                "content": "Modern AI systems that optimize PC performance automatically",
                "order": 6
            },
            {
                "title": "Overclocking Safety and Monitoring",
                "description": "Temperature monitoring and system stability testing",
                "content": "Ensuring system safety while maximizing performance",
                "order": 7
            }
        ]
    },
    {
        "title": "PC Benchmarking Evolution",
        "description": "From early benchmarks to modern testing suites like 3DMark and Cinebench",
        "price": 0.000005,
        "category": "Software & Tools",
        "difficulty": "intermediate",
        "duration": "5 weeks",
        "instructor": "Benchmarking Team",
        "modules": [
            {
                "title": "Early Benchmarking Tools",
                "description": "Norton SI, PC Magazine benchmarks, and early testing",
                "content": "Historical perspective on PC performance measurement",
                "order": 1
            },
            {
                "title": "3DMark Legacy",
                "description": "3DMark evolution from 3DMark99 to modern versions",
                "content": "How 3DMark became the standard for graphics benchmarking",
                "order": 2
            },
            {
                "title": "CPU Benchmarking",
                "description": "Cinebench, CPU-Z, and processor performance testing",
                "content": "Understanding CPU benchmark methodologies and results",
                "order": 3
            },
            {
                "title": "Storage and Memory Benchmarks",
                "description": "CrystalDiskMark, AIDA64, and system component testing",
                "content": "Benchmarking storage devices and memory performance",
                "order": 4
            },
            {
                "title": "Modern Benchmarking Suites",
                "description": "PCMark, PassMark, and comprehensive system testing",
                "content": "Current benchmarking tools and their applications",
                "order": 5
            }
        ]
    },
    {
        "title": "Operating System Evolution",
        "description": "From DOS and Windows 95 to Windows 11 and modern Linux distributions",
        "price": 0.000005,
        "category": "Software & Tools",
        "difficulty": "intermediate",
        "duration": "9 weeks",
        "instructor": "Operating Systems Team",
        "modules": [
            {
                "title": "DOS Era and Command Line",
                "description": "MS-DOS and early PC operating system concepts",
                "content": "Understanding how early PCs operated without graphical interfaces",
                "order": 1
            },
            {
                "title": "Windows 3.1 and Early GUI",
                "description": "First mainstream Windows graphical interface",
                "content": "Transition from command line to graphical user interfaces",
                "order": 2
            },
            {
                "title": "Windows 95/98/ME Consumer Era",
                "description": "32-bit Windows and mainstream PC adoption",
                "content": "How Windows 95 revolutionized personal computing",
                "order": 3
            },
            {
                "title": "Windows NT/2000/XP Professional",
                "description": "Business-class Windows with improved stability",
                "content": "Professional Windows versions and their enterprise features",
                "order": 4
            },
            {
                "title": "Windows Vista/7/8 Modern Era",
                "description": "64-bit adoption and modern Windows features",
                "content": "Evolution of Windows with improved security and features",
                "order": 5
            },
            {
                "title": "Windows 10/11 Current Generation",
                "description": "Modern Windows with cloud integration and security",
                "content": "Current Windows features and future direction",
                "order": 6
            },
            {
                "title": "Linux on Desktop",
                "description": "Ubuntu, Fedora, and Linux desktop evolution",
                "content": "How Linux became viable for desktop PC users",
                "order": 7
            },
            {
                "title": "macOS and Alternative Systems",
                "description": "Apple's desktop OS and other alternatives",
                "content": "Alternative operating systems and their unique features",
                "order": 8
            },
            {
                "title": "Future of PC Operating Systems",
                "description": "Cloud integration, ARM support, and OS evolution",
                "content": "Where PC operating systems are heading in the future",
                "order": 9
            }
        ]
    },
    # 🎮 Gaming-Specific Topics
    {
        "title": "Game Engine Hardware Evolution",
        "description": "How game engines have evolved with PC hardware capabilities",
        "price": 0.000005,
        "category": "Gaming-Specific",
        "difficulty": "intermediate",
        "duration": "8 weeks",
        "instructor": "Game Technology Team",
        "modules": [
            {
                "title": "Early 3D Game Engines",
                "description": "Doom, Quake, and pioneering 3D graphics engines",
                "content": "How early engines pushed the boundaries of PC hardware",
                "order": 1
            },
            {
                "title": "Hardware Acceleration Era",
                "description": "Engines adapting to 3D accelerator cards",
                "content": "Game engine evolution with dedicated graphics hardware",
                "order": 2
            },
            {
                "title": "Multi-core CPU Utilization",
                "description": "Game engines adapting to multi-core processors",
                "content": "How modern engines distribute work across CPU cores",
                "order": 3
            },
            {
                "title": "Modern Engine Features",
                "description": "Unreal Engine 5, Unity, and current-generation capabilities",
                "content": "Advanced rendering techniques in modern game engines",
                "order": 4
            },
            {
                "title": "Ray Tracing Integration",
                "description": "Real-time ray tracing in game engines",
                "content": "How engines implement hardware-accelerated ray tracing",
                "order": 5
            },
            {
                "title": "AI and Machine Learning",
                "description": "DLSS, FSR, and AI integration in gaming",
                "content": "Artificial intelligence enhancing game engine performance",
                "order": 6
            },
            {
                "title": "VR and AR Engine Support",
                "description": "Game engines supporting virtual and augmented reality",
                "content": "How engines adapt to VR/AR hardware requirements",
                "order": 7
            },
            {
                "title": "Future Engine Technologies",
                "description": "Next-generation rendering and game engine innovation",
                "content": "Emerging technologies that will shape future game engines",
                "order": 8
            }
        ]
    },
    {
        "title": "Graphics API Evolution",
        "description": "DirectX, OpenGL, Vulkan, and low-level graphics programming",
        "price": 0.000005,
        "category": "Gaming-Specific",
        "difficulty": "advanced",
        "duration": "7 weeks",
        "instructor": "Graphics API Team",
        "modules": [
            {
                "title": "Early Graphics APIs",
                "description": "Software rendering and early 3D programming interfaces",
                "content": "Understanding how early games communicated with graphics hardware",
                "order": 1
            },
            {
                "title": "DirectX Development",
                "description": "Microsoft's DirectX evolution from version 1 to 12",
                "content": "How DirectX became the dominant PC gaming API",
                "order": 2
            },
            {
                "title": "OpenGL and Cross-Platform Graphics",
                "description": "OpenGL's role in professional and cross-platform graphics",
                "content": "Understanding OpenGL's strengths and industry applications",
                "order": 3
            },
            {
                "title": "Low-Level API Revolution",
                "description": "Vulkan, DirectX 12, and reduced driver overhead",
                "content": "How modern APIs give developers more direct hardware control",
                "order": 4
            },
            {
                "title": "API Performance Comparison",
                "description": "Benchmarking different graphics APIs and their strengths",
                "content": "Understanding when to use different graphics APIs",
                "order": 5
            },
            {
                "title": "Ray Tracing APIs",
                "description": "DirectX Raytracing (DXR) and Vulkan RT extensions",
                "content": "How modern APIs support hardware ray tracing",
                "order": 6
            },
            {
                "title": "Future Graphics Programming",
                "description": "Next-generation APIs and graphics programming evolution",
                "content": "Where graphics API development is heading",
                "order": 7
            }
        ]
    },
    {
        "title": "Game Streaming and Cloud Gaming",
        "description": "GeForce NOW, Xbox Cloud Gaming, and remote gaming evolution",
        "price": 0.000005,
        "category": "Gaming-Specific",
        "difficulty": "intermediate",
        "duration": "6 weeks",
        "instructor": "Cloud Gaming Team",
        "modules": [
            {
                "title": "Early Remote Gaming Attempts",
                "description": "OnLive, Gaikai, and pioneering cloud gaming services",
                "content": "Understanding the challenges of early cloud gaming",
                "order": 1
            },
            {
                "title": "Network Requirements",
                "description": "Bandwidth, latency, and infrastructure needs for game streaming",
                "content": "Technical requirements for viable cloud gaming experiences",
                "order": 2
            },
            {
                "title": "NVIDIA GeForce NOW",
                "description": "GeForce NOW technology and service evolution",
                "content": "How NVIDIA created a successful cloud gaming platform",
                "order": 3
            },
            {
                "title": "Microsoft Xbox Cloud Gaming",
                "description": "Xbox Game Pass Ultimate and Microsoft's cloud strategy",
                "content": "Microsoft's approach to cloud gaming and console integration",
                "order": 4
            },
            {
                "title": "Google Stadia and Lessons Learned",
                "description": "Stadia's technology, challenges, and market lessons",
                "content": "Understanding why some cloud gaming services succeed and others fail",
                "order": 5
            },
            {
                "title": "Future of Cloud Gaming",
                "description": "5G, edge computing, and next-generation game streaming",
                "content": "How emerging technologies will improve cloud gaming",
                "order": 6
            }
        ]
    },
    # 🔒 Security & Protection Topics
    {
        "title": "Hardware-Level Security",
        "description": "TPM, Secure Boot, Intel SGX, and hardware security evolution",
        "price": 0.000005,
        "category": "Security & Protection",
        "difficulty": "advanced",
        "duration": "7 weeks",
        "instructor": "Hardware Security Team",
        "modules": [
            {
                "title": "Early PC Security Limitations",
                "description": "Why early PCs had minimal security features",
                "content": "Understanding the security challenges of early personal computers",
                "order": 1
            },
            {
                "title": "Trusted Platform Module (TPM)",
                "description": "Hardware-based cryptographic security chip",
                "content": "How TPM provides secure key storage and system integrity",
                "order": 2
            },
            {
                "title": "UEFI Secure Boot",
                "description": "Preventing unauthorized bootloader execution",
                "content": "Understanding Secure Boot's role in system security",
                "order": 3
            },
            {
                "title": "Intel Software Guard Extensions (SGX)",
                "description": "CPU-based application isolation and protection",
                "content": "How SGX creates secure enclaves for sensitive computations",
                "order": 4
            },
            {
                "title": "AMD Security Technologies",
                "description": "AMD's approach to hardware-level security",
                "content": "AMD Secure Memory Encryption and Platform Security Processor",
                "order": 5
            },
            {
                "title": "Hardware Security Keys",
                "description": "FIDO2, WebAuthn, and hardware authentication devices",
                "content": "Physical security keys for multi-factor authentication",
                "order": 6
            },
            {
                "title": "Future Hardware Security",
                "description": "Quantum-resistant cryptography and next-generation security",
                "content": "Preparing hardware security for future threats",
                "order": 7
            }
        ]
    },
    {
        "title": "PC Gaming Security Evolution",
        "description": "Anti-cheat systems, antivirus integration, and gaming security",
        "price": 0.000005,
        "category": "Security & Protection",
        "difficulty": "intermediate",
        "duration": "5 weeks",
        "instructor": "Gaming Security Team",
        "modules": [
            {
                "title": "Early Gaming Security Challenges",
                "description": "Cheating, piracy, and early security concerns in PC gaming",
                "content": "Understanding security challenges unique to PC gaming",
                "order": 1
            },
            {
                "title": "Anti-Cheat Technology Evolution",
                "description": "VAC, BattlEye, EasyAntiCheat, and cheat prevention",
                "content": "How anti-cheat systems detect and prevent gaming exploits",
                "order": 2
            },
            {
                "title": "Kernel-Level Anti-Cheat",
                "description": "Vanguard, BattlEye, and deep system integration",
                "content": "Understanding the controversy and necessity of kernel-level protection",
                "order": 3
            },
            {
                "title": "DRM and Game Protection",
                "description": "Denuvo, Steam DRM, and digital rights management",
                "content": "How game publishers protect their intellectual property",
                "order": 4
            },
            {
                "title": "Balancing Security and Performance",
                "description": "Security measures vs gaming performance optimization",
                "content": "Finding the right balance between protection and user experience",
                "order": 5
            }
        ]
    },
    # 🌍 Trends & Culture Topics
    {
        "title": "DIY PC Building Culture",
        "description": "Rise of DIY PC building and PC Master Race (PCMR) culture",
        "price": 0.000005,
        "category": "Trends & Culture",
        "difficulty": "beginner",
        "duration": "6 weeks",
        "instructor": "PC Culture Team",
        "modules": [
            {
                "title": "Early PC Enthusiast Community",
                "description": "BBS systems, early forums, and enthusiast culture origins",
                "content": "How PC enthusiast communities formed and grew",
                "order": 1
            },
            {
                "title": "Rise of PC Building Guides",
                "description": "Online tutorials, YouTube channels, and DIY culture",
                "content": "How building guides democratized custom PC assembly",
                "order": 2
            },
            {
                "title": "PCMR Culture and Gaming",
                "description": "PC Master Race community and gaming superiority discussions",
                "content": "Understanding PC gaming culture and community dynamics",
                "order": 3
            },
            {
                "title": "RGB and Aesthetic Trends",
                "description": "RGB lighting, custom loops, and PC beauty culture",
                "content": "How PCs became aesthetic showcases and art pieces",
                "order": 4
            },
            {
                "title": "Streaming and Content Creation",
                "description": "How content creators influenced PC building culture",
                "content": "Impact of YouTube and Twitch on PC enthusiast community",
                "order": 5
            },
            {
                "title": "Modern PC Building Community",
                "description": "Reddit, Discord, and current community platforms",
                "content": "Where PC enthusiasts gather and share knowledge today",
                "order": 6
            }
        ]
    },
    {
        "title": "Cryptocurrency Mining Impact",
        "description": "Mining booms and their impact on the GPU market and PC hardware",
        "price": 0.000005,
        "category": "Trends & Culture",
        "difficulty": "intermediate",
        "duration": "5 weeks",
        "instructor": "Cryptocurrency Analysis Team",
        "modules": [
            {
                "title": "Early Bitcoin and CPU Mining",
                "description": "Bitcoin's early days and CPU-based mining",
                "content": "Understanding cryptocurrency's early impact on PC hardware",
                "order": 1
            },
            {
                "title": "GPU Mining Revolution",
                "description": "How GPUs became the preferred mining hardware",
                "content": "Technical reasons why GPUs excelled at cryptocurrency mining",
                "order": 2
            },
            {
                "title": "Mining Boom Market Impact",
                "description": "GPU shortages, price inflation, and market disruption",
                "content": "How mining affected GPU availability for gamers and creators",
                "order": 3
            },
            {
                "title": "ASIC Development and GPU Recovery",
                "description": "Application-Specific Integrated Circuits and market stabilization",
                "content": "How dedicated mining hardware affected the GPU market",
                "order": 4
            },
            {
                "title": "Proof of Stake and Mining's Future",
                "description": "Ethereum 2.0 and the shift away from energy-intensive mining",
                "content": "How changes in cryptocurrency affected hardware demand",
                "order": 5
            }
        ]
    },
    {
        "title": "Right to Repair Movement",
        "description": "Repair rights, custom PC builders, and consumer hardware freedom",
        "price": 0.000005,
        "category": "Trends & Culture",
        "difficulty": "beginner",
        "duration": "4 weeks",
        "instructor": "Consumer Rights Team",
        "modules": [
            {
                "title": "Right to Repair Origins",
                "description": "Why the right to repair movement started and its goals",
                "content": "Understanding consumer rights and repair restrictions",
                "order": 1
            },
            {
                "title": "PC Hardware and Repairability",
                "description": "How PCs compare to other devices in terms of repairability",
                "content": "PC's natural advantage in the right to repair discussion",
                "order": 2
            },
            {
                "title": "Manufacturer Restrictions",
                "description": "Warranty voiding, proprietary components, and repair barriers",
                "content": "How some manufacturers limit user repair and modification",
                "order": 3
            },
            {
                "title": "DIY Culture as Repair Advocacy",
                "description": "How PC building culture supports repair rights",
                "content": "PC enthusiasts as advocates for consumer hardware rights",
                "order": 4
            }
        ]
    }
]

async def populate_courses():
    """Populate the database with comprehensive course data"""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        courses_collection = db.courses
        
        print("🚀 Starting course population...")
        
        # Clear existing courses (optional - remove if you want to keep existing data)
        await courses_collection.delete_many({})
        print("🗑️ Cleared existing courses")
        
        # Insert all courses
        courses_inserted = 0
        for course_data in COURSES_DATA:
            # Add timestamps
            course_data["created_at"] = datetime.utcnow()
            course_data["updated_at"] = datetime.utcnow()
            course_data["is_published"] = True
            course_data["enrollment_count"] = 0
            course_data["rating"] = 4.8  # Default high rating
            course_data["rating_count"] = 0
            course_data["prerequisites"] = []
            course_data["learning_outcomes"] = [
                "Master core concepts and terminology",
                "Understand historical context and evolution", 
                "Gain practical knowledge for real-world application",
                "Develop technical expertise in the subject area"
            ]
            
            # Insert course
            result = await courses_collection.insert_one(course_data)
            courses_inserted += 1
            
            print(f"✅ Added course: {course_data['title']} ({len(course_data['modules'])} modules)")
        
        print(f"\n🎉 Successfully added {courses_inserted} comprehensive courses!")
        print(f"📊 Total modules across all courses: {sum(len(course['modules']) for course in COURSES_DATA)}")
        
        # Print summary by category
        categories = {}
        for course in COURSES_DATA:
            category = course['category']
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
        
        print("\n📋 Courses by category:")
        for category, count in categories.items():
            print(f"  • {category}: {count} courses")
        
    except Exception as e:
        print(f"❌ Error populating courses: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(populate_courses())
