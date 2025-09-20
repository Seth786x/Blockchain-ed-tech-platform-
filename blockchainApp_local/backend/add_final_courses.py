#!/usr/bin/env python3
"""
Add final hardware component courses (PSU, Cooling, Case)
"""

from pymongo import MongoClient
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

# Final hardware component courses
FINAL_COURSES = [
    # POWER SUPPLY COURSES
    {
        "title": "Power Supply Design and Efficiency",
        "description": "Complete guide to PSU technology, 80+ ratings, modular designs, and power delivery systems",
        "category": "Power & Cooling",
        "difficulty": "intermediate",
        "duration": "7 weeks",
        "instructor": "Power Systems Team",
        "price": 0.000005,
        "is_featured": True,
        "modules": [
            {
                "title": "PSU Fundamentals and AC/DC Conversion",
                "description": "Understanding how power supplies convert AC mains power to DC for computer components",
                "content": """# PSU Fundamentals and AC/DC Conversion

## Introduction to Computer Power Supplies

A computer power supply unit (PSU) is responsible for converting alternating current (AC) from the wall outlet into the direct current (DC) voltages required by computer components. Modern PSUs are sophisticated switching power supplies that must deliver clean, stable power efficiently.

## Basic Electrical Concepts

### AC vs DC Power
**Alternating Current (AC)**:
- Voltage and current periodically reverse direction
- Standard household power (120V/240V, 50/60Hz)
- Efficient for power transmission over long distances
- Transformer compatible for voltage changes

**Direct Current (DC)**:
- Constant voltage and current direction
- Required by electronic circuits
- Different voltages needed by different components
- Battery-like power delivery

### Power Supply Requirements
**Multiple Output Voltages**:
- +12V: CPU, GPU, fans, drives (primary rail)
- +5V: Legacy devices, some ICs, USB power
- +3.3V: Memory, chipsets, modern ICs
- -12V: Some audio circuits, RS-232 (minimal current)
- +5V Standby: Always-on functions (wake-on-LAN, etc.)

## Switching Power Supply Operation

### Linear vs Switching Regulators
**Linear Regulators** (not used in PSUs):
- Simple voltage division with pass transistor
- Low efficiency (excess power dissipated as heat)
- Good regulation and low noise
- Impractical for high-power applications

**Switching Regulators** (modern PSU design):
- High-frequency switching of power transistors
- Energy stored in inductors and capacitors
- High efficiency (85-95% typical)
- More complex but practical for computer PSUs

### Switching Topology Types

**Forward Converter**:
- Single-ended primary topology
- Transformer isolates input and output
- Good for medium power levels
- Requires reset winding or clamp circuit

**Flyback Converter**:
- Energy stored in transformer core
- Suitable for multiple outputs
- Good regulation across wide load range
- Common in lower-power PSUs

**Half-Bridge/Full-Bridge**:
- Better transformer utilization
- Higher power capability
- More complex control circuits
- Used in high-end PSUs

### Power Factor Correction (PFC)

**Power Factor Definition**: Ratio of real power to apparent power
- Ideal power factor = 1.0 (purely resistive load)
- Poor power factor wastes grid capacity
- Many regions mandate PFC for high-power devices

**Active PFC**:
- Boost converter topology
- Shapes input current to follow voltage waveform
- Achieves power factor >0.95
- Standard in quality PSUs >75W

**Passive PFC**:
- Large inductor to smooth current
- Lower cost but less effective
- Power factor ~0.70-0.80
- Being phased out in many markets

## Voltage Regulation

### Primary-Side Regulation
**PWM Control**: Pulse Width Modulation of switching frequency
**Feedback Mechanisms**: Optoisolator or transformer-coupled feedback
**Reference Voltage**: Precise voltage standard for comparison
**Error Amplifier**: Adjusts PWM based on output deviation

### Secondary-Side Regulation
**Synchronous Rectification**: MOSFETs replace Schottky diodes
**DC-DC Conversion**: Further voltage regulation after isolation
**Multiple Rail Generation**: Individual control of each voltage
**Cross-Regulation**: Managing interaction between outputs

### Load Regulation
**Voltage Stability**: Maintaining voltage under varying loads
- ATX specification: ±5% for +12V, ±5% for +5V/+3.3V
- Better PSUs achieve ±3% or better
- Important for system stability

**Current Sharing**: Parallel operation of power circuits
**Thermal Compensation**: Adjusting for temperature effects

## Efficiency and 80+ Standards

### Power Loss Sources
**Switching Losses**: Transistor turn-on/turn-off energy
**Conduction Losses**: Resistance in current path
**Magnetic Losses**: Core and winding losses in transformers
**Control Circuit Power**: Housekeeping power consumption

### 80+ Certification Levels
**80+ (White)**: 80% efficiency at 20%, 50%, 100% load
**80+ Bronze**: 82%, 85%, 82% efficiency respectively
**80+ Silver**: 85%, 88%, 85% efficiency respectively
**80+ Gold**: 87%, 90%, 87% efficiency respectively
**80+ Platinum**: 90%, 92%, 89% efficiency respectively
**80+ Titanium**: 92%, 94%, 90% efficiency respectively

### Efficiency Benefits
**Reduced Heat Generation**: Less cooling required
**Lower Operating Costs**: Reduced electricity consumption
**Environmental Impact**: Reduced carbon footprint
**Component Longevity**: Cooler operation improves reliability

## Component Technologies

### Power Semiconductors
**MOSFETs (Metal-Oxide-Semiconductor Field-Effect Transistors)**:
- Primary switching elements
- Low on-resistance for efficiency
- Fast switching for reduced losses
- Require gate drive circuits

**Schottky Diodes**: 
- Fast recovery rectifiers
- Low forward voltage drop
- Used in secondary rectification
- Being replaced by synchronous rectification

### Magnetic Components
**Transformers**:
- Electrical isolation between primary and secondary
- Voltage scaling through turns ratio
- Energy transfer medium
- Core material affects efficiency and size

**Inductors**:
- Energy storage elements
- Smooth current ripple
- Filter high-frequency noise
- Core saturation must be avoided

### Capacitors
**Electrolytic Capacitors**:
- High capacitance for energy storage
- Primary and secondary side filtering
- Temperature and lifetime limitations
- Failure mode often causes PSU death

**Film Capacitors**:
- Superior high-frequency characteristics
- Lower ESR (Equivalent Series Resistance)
- Longer lifetime
- Used in critical locations

## Control and Protection Circuits

### PWM Controllers
**Fixed Frequency**: Constant switching frequency, variable duty cycle
**Variable Frequency**: Adjust frequency based on load
**Resonant Control**: Switch at resonant frequency for efficiency
**Digital Control**: Microcontroller-based regulation

### Protection Features
**Overvoltage Protection (OVP)**: Prevents excessive output voltage
**Undervoltage Protection (UVP)**: Shuts down on low voltage
**Overcurrent Protection (OCP)**: Limits maximum output current
**Short Circuit Protection (SCP)**: Protects against output shorts
**Overtemperature Protection (OTP)**: Thermal shutdown
**Overpower Protection (OPP)**: Limits total power consumption

## Ripple and Noise

### Output Ripple
**Definition**: AC component superimposed on DC output
**Measurement**: Peak-to-peak voltage variation
**ATX Specification**: 
  - +12V: 120mV max
  - +5V: 50mV max
  - +3.3V: 50mV max

**Sources of Ripple**:
- Incomplete filtering
- Load transients
- Switching frequency harmonics
- Cross-regulation between outputs

### Noise Considerations
**Electromagnetic Interference (EMI)**:
- Conducted emissions on power cord
- Radiated emissions from PSU case
- FCC/CE compliance required
- Input filters reduce conducted EMI

**Switch-Mode Noise**:
- High-frequency switching artifacts
- Can affect sensitive circuits
- Proper grounding and shielding important
- Linear post-regulators sometimes used

## Testing and Specifications

### Load Testing
**Static Load Testing**: Fixed load conditions
**Dynamic Load Testing**: Varying load conditions
**Cross-Load Testing**: Different loads on different rails
**Transient Response**: Response to sudden load changes

### Temperature Testing
**Ambient Temperature Effects**: Performance vs. temperature
**Hot Box Testing**: Elevated temperature operation
**Thermal Cycling**: Repeated temperature changes
**Component Temperature Monitoring**: Critical component temperatures

### Reliability Testing
**MTBF (Mean Time Between Failures)**: Statistical reliability measure
**Burn-in Testing**: Extended operation before shipment
**Environmental Testing**: Humidity, altitude, vibration
**Component Screening**: Parts selection and testing

## Real-World Applications

### Gaming Systems
- High +12V current for GPUs
- Transient response for load spikes
- Sufficient headroom for overclocking
- Quality components for reliability

### Workstations
- High efficiency for continuous operation
- Multiple high-current rails
- Enterprise-grade components
- Extended warranty coverage

### Servers
- Redundant PSU options
- Hot-swap capability
- High efficiency for operating costs
- Advanced monitoring and management

### Budget Builds
- Cost-effective solutions
- Basic protection features
- Adequate performance for non-demanding loads
- Balance of features and price

Understanding PSU fundamentals enables:
- Proper PSU selection for system requirements
- Troubleshooting power-related issues
- Appreciating quality differences between units
- Planning for system upgrades and expansion
- Optimizing system efficiency and reliability""",
                "order": 1
            }
        ]
    },
    {
        "title": "Modular PSUs and Cable Management",
        "description": "Master modular power supply benefits, cable types, and professional cable management techniques",
        "category": "Power & Cooling",
        "difficulty": "beginner",
        "duration": "5 weeks",
        "instructor": "Cable Management Team",
        "price": 0.000005,
        "is_featured": False,
        "modules": [
            {
                "title": "Modular vs Non-Modular PSUs",
                "description": "Understanding the benefits and considerations of modular power supply designs",
                "content": """# Modular vs Non-Modular PSUs

## Introduction to PSU Cable Types

Power supply units come in different cable configurations that affect system building, cable management, and upgrade flexibility. Understanding these differences helps in making informed purchasing decisions.

## Non-Modular Power Supplies

### Design Characteristics
**Fixed Cables**: All cables permanently attached to PSU
**Complete Cable Set**: Every possible connector included
**Single Unit Construction**: Cables emerge directly from PSU case
**Lower Manufacturing Cost**: Simpler assembly process

### Advantages
**Lower Cost**: Typically 20-30% less expensive than modular
**Reliability**: No additional connection points to fail
**Simplicity**: No cable compatibility concerns
**Availability**: Wider selection in budget segments

### Disadvantages
**Cable Clutter**: Unused cables must be managed
**Airflow Restriction**: Extra cables can impede cooling
**Aesthetic Impact**: More difficult to achieve clean look
**Future Upgrades**: May lack newer connector types

### Best Use Cases
**Budget Builds**: Cost-conscious systems
**Basic Configurations**: Standard component setups
**OEM/Prebuilt Systems**: Manufacturer cost optimization
**Non-Enthusiast Builds**: Users not concerned with aesthetics

## Semi-Modular Power Supplies

### Design Characteristics
**Fixed Essential Cables**: 24-pin ATX and 8-pin EPS permanently attached
**Modular Secondary Cables**: PCIe, SATA, Molex connectors detachable
**Balanced Approach**: Compromise between cost and flexibility
**Retained Compatibility**: Essential connections always available

### Advantages
**Cost Balance**: More affordable than fully modular
**Essential Reliability**: Critical connections permanently secured
**Reduced Clutter**: Remove unused peripheral cables
**Partial Flexibility**: Some customization capability

### Best Use Cases
**Mainstream Gaming**: Balance of features and cost
**General Purpose Builds**: Most common system configurations
**Upgrade-Friendly**: Systems with changing peripheral needs
**Clean Build Priority**: Users wanting better cable management

## Fully Modular Power Supplies

### Design Characteristics
**All Cables Detachable**: Including 24-pin ATX and CPU power
**Maximum Flexibility**: Use only required cables
**Premium Construction**: Higher-end PSUs typically
**Cable Compatibility**: Specific cables for each PSU model

### Advantages
**Maximum Customization**: Use only needed cables
**Best Airflow**: Minimal cable obstruction
**Aesthetic Excellence**: Cleanest appearance possible
**Cable Upgrades**: Custom or sleeved cable options
**Transport Friendly**: Easier to pack for moves

### Disadvantages
**Higher Cost**: Premium pricing for flexibility
**Cable Management**: Must organize and store extra cables
**Compatibility Risk**: Wrong cables can damage components
**Connection Points**: More potential failure points

### Best Use Cases
**Enthusiast Builds**: Premium system construction
**Show Builds**: Systems for display or competition
**SFF/ITX Builds**: Space-constrained environments
**Professional Workstations**: Clean, organized systems

## Cable Types and Functions

### Primary Power Cables
**24-pin ATX Main Power**:
- Primary motherboard power connection
- Supplies +3.3V, +5V, +12V, -12V rails
- Always required, sometimes split as 20+4 pin
- Heavy gauge wires for high current

**8-pin EPS CPU Power**:
- Dedicated CPU power delivery
- Supplies +12V rail to CPU VRM
- May be split as 4+4 pin configuration
- Sometimes dual 8-pin for high-end CPUs

### Graphics Power Cables
**6-pin PCIe Power**:
- Provides 75W additional power to graphics cards
- Supplements 75W available from PCIe slot
- Required for mid-range graphics cards
- +12V supply with ground connections

**8-pin PCIe Power**:
- Provides 150W additional power to graphics cards
- Higher current capacity than 6-pin
- Required for high-end graphics cards
- May be configured as 6+2 pin

**12-pin PCIe Power** (newer):
- NVIDIA RTX 30/40 series connector
- Compact connector for smaller cards
- Requires adapter for older PSUs
- Higher power density design

### Storage and Peripheral Cables
**SATA Power**:
- Standard drive power connector
- Supplies +3.3V, +5V, +12V to drives
- Flat connector design
- Multiple connectors per cable typical

**4-pin Molex**:
- Legacy peripheral power connector
- Supplies +5V and +12V
- Still used for fans and older devices
- Less common in modern builds

**Floppy Power** (legacy):
- Small 4-pin connector
- Rarely used in modern systems
- +5V and +12V supply
- Being phased out

## Cable Management Strategies

### Planning Phase
**System Component Inventory**:
- List all components requiring power
- Identify connector types needed
- Plan cable routing paths
- Consider future upgrade needs

**Case Assessment**:
- Identify cable routing holes and channels
- Measure available space behind motherboard tray
- Plan power supply orientation
- Consider cable length requirements

### Installation Techniques
**Route Before Connect**: Plan cable paths first
**Use Case Features**: Leverage built-in cable management
**Bundle Strategically**: Group cables by destination
**Secure Properly**: Use velcro ties or zip ties appropriately

### Advanced Techniques
**Custom Cable Length**: Minimize excess cable length
**Sleeved Cables**: Improve aesthetics and organization
**Cable Combs**: Maintain parallel cable spacing
**Hidden Routing**: Utilize case-specific features

## Cable Specifications and Safety

### Wire Gauge Considerations
**AWG (American Wire Gauge)**: Lower numbers = thicker wire
**Current Capacity**: Thicker wire handles more current
**Voltage Drop**: Longer/thinner wire increases resistance
**Safety Margins**: PSU cables overspec'd for safety

### Insulation and Safety
**Temperature Ratings**: Cables rated for PSU environment
**Insulation Types**: PVC, Teflon, silicone options
**Fire Safety**: Materials selected for safety standards
**Mechanical Protection**: Strain relief at connectors

### Connector Quality
**Contact Materials**: Gold plating for corrosion resistance
**Spring Tension**: Proper contact pressure
**Housing Materials**: Durable plastic construction
**Manufacturing Tolerances**: Precise fit requirements

## Custom and Aftermarket Cables

### Sleeved Cables
**Aesthetic Enhancement**: Improved visual appearance
**Material Options**: Paracord, PET, carbon fiber
**Color Coordination**: Match system theme
**Professional Look**: Clean, uniform appearance

### Cable Extensions
**Length Adjustment**: Extend existing cables
**Cost-Effective**: Cheaper than full custom sets
**Partial Customization**: Improve visible sections only
**Compatibility**: Works with any PSU

### Full Custom Cable Sets
**Perfect Fit**: Exact length for specific systems
**Maximum Customization**: Complete aesthetic control
**Premium Materials**: Highest quality construction
**Professional Installation**: Often requires expertise

## Troubleshooting Cable Issues

### Common Problems
**Loose Connections**: Insufficient insertion force
**Wrong Connectors**: Incompatible cable types
**Damaged Wires**: Physical damage or wear
**Overloaded Circuits**: Exceeding current capacity

### Diagnostic Techniques
**Visual Inspection**: Check for obvious damage
**Connection Verification**: Ensure proper seating
**Voltage Testing**: Multimeter verification
**Load Testing**: Verify performance under load

### Prevention Strategies
**Proper Installation**: Follow manufacturer instructions
**Cable Protection**: Avoid sharp edges and pinch points
**Regular Inspection**: Periodic system maintenance
**Quality Components**: Invest in reliable cables

## Future Trends

### Connector Evolution
**Higher Power Density**: Smaller connectors for same power
**Improved Safety**: Enhanced keying and locking
**Material Advances**: Better insulation and conductors
**Standardization**: Industry-wide compatibility improvements

### Cable Technology
**Flat Cables**: Improved airflow characteristics
**Integrated Solutions**: Motherboard-specific designs
**Wireless Power**: Emerging contactless technologies
**Smart Cables**: Embedded monitoring capabilities

Understanding modular PSUs and cable management enables:
- Informed PSU selection for specific needs
- Professional system assembly techniques
- Optimal airflow and thermal performance
- Enhanced system aesthetics
- Easier maintenance and upgrades""",
                "order": 1
            }
        ]
    },

    # COOLING COURSES
    {
        "title": "CPU Cooling Solutions and Thermal Management",
        "description": "Comprehensive guide to air cooling, liquid cooling, and thermal management in modern PCs",
        "category": "Cooling & Thermal",
        "difficulty": "intermediate",
        "duration": "8 weeks",
        "instructor": "Thermal Management Team",
        "price": 0.000005,
        "is_featured": True,
        "modules": [
            {
                "title": "Heat Transfer Fundamentals",
                "description": "Understanding conduction, convection, and radiation in computer cooling systems",
                "content": """# Heat Transfer Fundamentals

## Introduction to Thermal Management

Effective thermal management is crucial for modern computer systems. As processors become more powerful and compact, managing the heat they generate becomes increasingly challenging and important for system stability, performance, and longevity.

## Basic Heat Transfer Principles

### The Three Modes of Heat Transfer

**1. Conduction**
- **Definition**: Heat transfer through direct contact between materials
- **Mechanism**: Molecular/atomic energy transfer through collisions
- **Materials**: Solids are best conductors, gases are poorest
- **Application**: Heat movement from CPU die to heatsink base

**Key Factors Affecting Conduction**:
- **Thermal Conductivity**: Material property (W/m·K)
- **Cross-sectional Area**: Larger area = better heat transfer
- **Temperature Difference**: Greater ΔT = faster transfer
- **Distance**: Shorter path = less thermal resistance

**2. Convection**
- **Definition**: Heat transfer by fluid motion (air or liquid)
- **Natural Convection**: Buoyancy-driven fluid motion
- **Forced Convection**: Fan or pump-driven fluid motion
- **Application**: Heat removal from heatsink fins to surrounding air

**Convection Enhancement**:
- **Surface Area**: More fins increase heat transfer area
- **Airflow**: Higher velocity improves heat transfer coefficient
- **Turbulence**: Mixing improves heat transfer (within limits)
- **Fluid Properties**: Air vs. liquid coolant characteristics

**3. Radiation**
- **Definition**: Heat transfer via electromagnetic waves
- **No Medium Required**: Works in vacuum
- **Temperature Dependent**: T⁴ relationship (Stefan-Boltzmann law)
- **Application**: Limited in PC cooling, more important at high temperatures

## Thermal Resistance Concept

### Thermal Circuit Analogy
**Thermal Resistance (Rth)**: Temperature difference divided by heat flow
- **Units**: K/W or °C/W
- **Analogy**: Similar to electrical resistance
- **Series Addition**: Total resistance = sum of individual resistances
- **Parallel Paths**: 1/Rtotal = 1/R1 + 1/R2 + ...

### Thermal Resistance Chain in CPU Cooling
1. **Junction to Case (Rjc)**: CPU die to integrated heat spreader
2. **Interface Material**: Thermal paste or pad between CPU and cooler
3. **Conduction Through Heatsink**: Base to fins
4. **Convection to Air**: Fins to ambient air

### Total System Thermal Resistance
**Rtotal = Rjc + Rinterface + Rconductjon + Rconvection**

**Temperature Calculation**:
**Tjunction = Tambient + (Power × Rtotal)**

## Material Properties

### Thermal Conductivity Values
**Metals (High Conductivity)**:
- Silver: 429 W/m·K (theoretical best)
- Copper: 401 W/m·K (most practical)
- Aluminum: 237 W/m·K (lightweight option)
- Steel: 50 W/m·K (poor choice for heatsinks)

**Non-Metals**:
- Diamond: 2000+ W/m·K (exotic, expensive)
- Thermal Interface Materials: 1-15 W/m·K
- Air: 0.026 W/m·K (excellent insulator)
- Thermal Paste: 3-12 W/m·K typical

### Material Selection Criteria
**For Heatsinks**:
- **Thermal Conductivity**: Higher is better
- **Density**: Lighter materials reduce mounting stress
- **Cost**: Aluminum cheaper, copper performs better
- **Machinability**: Ease of manufacturing complex shapes
- **Corrosion Resistance**: Important for long-term reliability

## Heat Generation in Processors

### Power Consumption Sources
**Dynamic Power**: Switching activity of transistors
- **Formula**: P = α × C × V² × f
- α = activity factor, C = capacitance, V = voltage, f = frequency
- **Dominant** in active processing

**Static Power**: Leakage currents
- **Subthreshold Leakage**: Transistors never completely "off"
- **Gate Leakage**: Through thin gate oxides
- **Junction Leakage**: P-N junction currents
- **Increases** with temperature and smaller process nodes

### Thermal Design Power (TDP)
**Definition**: Maximum heat generation under normal conditions
- **Not Maximum Power**: Actual power can exceed TDP briefly
- **Design Target**: Cooling system must handle TDP continuously
- **Marketing Tool**: Often used for product comparison
- **Conservative**: Usually below worst-case scenarios

**TDP vs. Actual Power**:
- **Base TDP**: Standard operating conditions
- **Boost Power**: Short-term higher power consumption
- **Maximum Power**: Absolute limit (rare conditions)

### Heat Density Challenges
**Modern Processor Characteristics**:
- **High Heat Flux**: Power concentrated in small area
- **Hot Spots**: Localized high-temperature regions
- **Transient Behavior**: Rapid power changes
- **3D Structure**: Multiple layers complicate heat removal

## Cooling System Design Principles

### Heat Spreader Function
**Integrated Heat Spreader (IHS)**:
- **Purpose**: Distribute heat over larger area
- **Material**: Usually copper or copper-nickel alloy
- **Attachment**: Soldered or thermal interface material
- **Delidding**: Enthusiast modification to improve thermal transfer

### Heatsink Design Factors
**Base Design**:
- **Flatness**: Minimize thermal interface resistance
- **Thickness**: Balance conduction and weight
- **Surface Finish**: Mirror finish ideal for contact
- **Material**: Copper for performance, aluminum for cost

**Fin Design**:
- **Fin Density**: More fins = more area, but higher air resistance
- **Fin Height**: Taller fins provide more area but diminishing returns
- **Fin Thickness**: Thinner fins more efficient but harder to manufacture
- **Fin Shape**: Straight, curved, or optimized profiles

### Airflow Considerations
**Pressure vs. Flow Rate**:
- **Static Pressure**: Ability to move air through restrictions
- **Airflow (CFM)**: Volume of air moved per minute
- **System Resistance**: Determines operating point
- **Fan Curves**: Pressure vs. flow characteristics

**Airflow Direction**:
- **Intake**: Fresh cool air into system
- **Exhaust**: Remove heated air from system
- **Balance**: Positive, negative, or neutral pressure
- **Path**: Minimize recirculation and dead zones

## Temperature Monitoring and Control

### Temperature Sensors
**Diode-Based Sensors**:
- **Built into CPU**: Accurate die temperature
- **Multiple Locations**: Monitor hot spots
- **Digital Interface**: Easy integration with control systems
- **Calibration**: Factory calibrated for accuracy

**Thermistors and RTDs**:
- **External Sensors**: Monitor ambient and specific locations
- **Accuracy**: Good for system monitoring
- **Response Time**: Varies by sensor type and mounting

### Thermal Management Strategies
**Dynamic Frequency Scaling**: Reduce frequency under thermal stress
**Dynamic Voltage Scaling**: Lower voltage reduces power consumption
**Thermal Throttling**: Emergency reduction of performance
**Shutdown Protection**: Prevent damage from overheating

### Control Algorithms
**PWM Fan Control**:
- **Temperature Curves**: Fan speed vs. temperature mapping
- **Hysteresis**: Prevent oscillation around set points
- **Aggressive vs. Quiet**: Balance between cooling and noise

## Practical Applications

### Air Cooling Systems
**Tower Coolers**: Vertical orientation, gravity-assisted airflow
**Top-Down Coolers**: Horizontal orientation, motherboard cooling
**Low-Profile Coolers**: Height-restricted applications
**Passive Cooling**: No fans, rely on natural convection

### Liquid Cooling Advantages
**Higher Heat Capacity**: Water stores more thermal energy
**Better Heat Transport**: Liquid circulation moves heat efficiently
**Remote Heat Rejection**: Radiator can be placed optimally
**Lower Noise**: Potential for quieter operation

### System-Level Considerations
**Case Airflow**: Overall system thermal design
**Component Interaction**: Multiple heat sources affect each other
**Ambient Temperature**: External conditions impact performance
**Altitude Effects**: Lower air density at higher elevations

## Performance Metrics

### Thermal Resistance Measurement
**Junction-to-Ambient**: Overall system thermal performance
**Controlled Conditions**: Standard test procedures
**Power Level**: Specified heat load for testing
**Ambient Temperature**: Standardized conditions

### Temperature Targets
**Maximum Operating**: Safe continuous operation limit
**Throttling Point**: Performance reduction threshold  
**Shutdown Temperature**: Emergency protection limit
**Optimal Range**: Best performance and longevity balance

Understanding heat transfer fundamentals enables:
- Effective cooling solution selection
- Optimization of thermal systems
- Troubleshooting overheating issues
- Designing custom cooling solutions
- Maximizing system performance and reliability""",
                "order": 1
            }
        ]
    },
    {
        "title": "Advanced Cooling: Custom Loops and Maintenance",
        "description": "Master custom liquid cooling systems, component selection, and maintenance procedures",
        "category": "Cooling & Thermal",
        "difficulty": "advanced",
        "duration": "10 weeks",
        "instructor": "Custom Cooling Team",
        "price": 0.000005,
        "is_featured": False,
        "modules": [
            {
                "title": "Custom Loop Design and Planning",
                "description": "Planning and designing custom liquid cooling loops for optimal performance",
                "content": """# Custom Loop Design and Planning

## Introduction to Custom Liquid Cooling

Custom liquid cooling loops offer superior thermal performance, aesthetic appeal, and the satisfaction of building a unique system. However, they require careful planning, quality components, and ongoing maintenance to operate safely and effectively.

## Custom Loop Advantages

### Performance Benefits
**Superior Heat Capacity**: Water has 4x higher specific heat than air
**Efficient Heat Transport**: Liquid circulation moves heat effectively
**Lower Noise Levels**: Larger radiators allow slower, quieter fans
**Stable Temperatures**: Thermal mass reduces temperature spikes
**Scalability**: Add components to existing loop

### Aesthetic Appeal
**Visual Impact**: Transparent tubing shows coolant flow
**Custom Colors**: Colored coolants and lighting effects
**Unique Layouts**: Personalized routing and component placement
**Premium Components**: High-quality materials and finishes
**Show-Piece Value**: Impressive display systems

### Flexibility Advantages
**Component Choice**: Select specific pumps, radiators, blocks
**Upgradeability**: Change components without rebuilding entire system
**Multiple Components**: Cool CPU and GPU(s) in single loop
**Custom Fit**: Tailor to specific case and requirements

## System Planning Phase

### Component Inventory
**Heat Sources**:
- CPU: TDP rating and socket type
- GPU(s): Power consumption and compatibility
- Additional components: RAM, VRMs, chipsets

**Case Assessment**:
- Available space for radiators
- Pump and reservoir mounting options
- Tubing routing possibilities
- Drainage and filling access

### Loop Configuration Options

**Single Loop Design**:
- **All components in series**: CPU → GPU → Radiator → Pump
- **Advantages**: Simpler design, fewer components
- **Considerations**: Component order has minimal temperature impact
- **Best for**: Most custom loops

**Parallel Loop Design**:
- **Separate paths for different components**
- **Advantages**: Independent flow rates, potential temperature benefits
- **Disadvantages**: More complex, additional components required
- **Use cases**: Extreme cooling requirements

### Flow Rate Planning
**Minimum Flow Rate**: 0.5 GPM per component typical
**Pressure Drop Calculation**: Sum of all restrictions in loop
**Pump Selection**: Match head pressure and flow requirements
**Safety Margin**: Plan for 25-50% above minimum requirements

## Component Selection

### Water Blocks
**CPU Water Blocks**:
- **Full Coverage**: Cool CPU and VRM simultaneously
- **Socket Compatibility**: Ensure mounting system compatibility
- **Flow Characteristics**: Internal design affects pressure drop
- **Materials**: Copper base preferred for thermal performance

**GPU Water Blocks**:
- **Full Coverage vs. GPU Only**: Cool entire card or just GPU chip
- **Reference vs. Custom**: Different blocks for different PCB designs
- **Compatibility**: Verify exact GPU model support
- **Warranty**: May void graphics card warranty

**Universal Blocks**:
- **RAM Cooling**: DIMMs can benefit from active cooling
- **VRM Cooling**: Important for high-end motherboards
- **Chipset Cooling**: Sometimes beneficial for extreme systems

### Radiators
**Size Selection**:
- **120mm per 100W**: Conservative rule of thumb
- **Thicker Radiators**: Better performance, require higher static pressure fans
- **Multiple Radiators**: Distribute heat rejection, improve efficiency

**Construction Types**:
- **Tube and Fin**: Traditional automotive-style construction
- **Brazed**: More durable, better thermal performance
- **Materials**: Copper/brass preferred, aluminum possible but not mixed

**Fan Configuration**:
- **Push vs. Pull**: Push slightly more effective
- **Push-Pull**: Maximum performance, double the fans
- **Fan Speed**: Lower RPM possible with larger radiators

### Pumps
**D5 Pumps**:
- **Industry Standard**: Reliable, proven design
- **Variable Speed**: PWM control available
- **High Pressure**: Good for restrictive loops
- **Longevity**: 50,000+ hour rating

**DDC Pumps**:
- **Compact Size**: Good for space-constrained builds
- **High Pressure**: Excellent for restrictive systems
- **Quieter**: Generally quieter than D5
- **Mounting**: More mounting options due to size

**Integrated Pump/Reservoir**: Convenience vs. flexibility trade-off

### Reservoirs
**Functions**:
- **Air Separation**: Prevent air bubbles in loop
- **Fill Port**: Easy system filling and maintenance
- **Visual Appeal**: Show coolant level and flow
- **Expansion**: Accommodate thermal expansion

**Types**:
- **Cylindrical**: Traditional design, good capacity
- **Flat**: Space-saving design
- **Integrated**: Combined with pump for convenience
- **Custom**: Unique shapes and materials

### Tubing and Fittings
**Tubing Types**:
- **PETG**: Easy to work with, clear, moderate temperature rating
- **Acrylic**: Crystal clear, higher temperature rating, more brittle
- **Soft Tubing**: Flexible, easy installation, less aesthetic impact

**Fitting Quality**:
- **Materials**: Brass preferred for durability
- **Seal Design**: O-rings and threads must be reliable
- **Flow Characteristics**: Minimize turbulence and restriction
- **Aesthetics**: Match overall system theme

## Loop Design Principles

### Flow Path Optimization
**Component Order**: Temperature difference between components minimal
**Minimize Restrictions**: Reduce unnecessary fittings and sharp bends
**Avoid Air Traps**: Design for air bubble removal
**Drain Points**: Plan for system maintenance

### Pressure Management
**Pump Curves**: Understand head pressure vs. flow rate
**System Resistance**: Calculate total pressure drop
**Operating Point**: Where pump curve meets system curve
**Multiple Pumps**: Series for pressure, parallel for flow

### Thermal Design
**Radiator Sizing**: Conservative approach prevents overheating
**Coolant Temperature**: Maintain reasonable operating temperatures
**Component Limits**: Respect maximum operating temperatures
**Safety Margins**: Plan for worst-case scenarios

## Safety Considerations

### Leak Prevention
**Quality Components**: Invest in reliable fittings and tubing
**Proper Assembly**: Follow manufacturer instructions carefully
**Leak Testing**: Pressure test before adding electronics
**Monitoring**: Regular inspection for signs of leakage

### Electrical Safety
**Isolated Testing**: Test cooling system separately from electronics
**GFCI Protection**: Use ground fault circuit interrupters
**Water Detection**: Consider leak detection systems
**Emergency Procedures**: Plan for leak response

### Chemical Safety
**Coolant Compatibility**: Ensure materials compatibility
**Corrosion Prevention**: Use appropriate coolants and additives
**Toxicity**: Some coolants require careful handling
**Disposal**: Proper disposal of coolants and components

## Installation Process

### Preparation Phase
**Component Layout**: Plan component placement and tubing routes
**Tool Preparation**: Ensure all necessary tools available
**Work Area**: Clean, well-lit workspace
**Documentation**: Take photos for reference during assembly

### Assembly Sequence
1. **Install Water Blocks**: Mount blocks on components first
2. **Mount Radiators**: Position radiators and fans in case
3. **Install Pump and Reservoir**: Ensure secure mounting
4. **Route Tubing**: Connect components with tubing
5. **System Integration**: Install in computer case

### Testing Procedure
1. **Visual Inspection**: Check all connections
2. **Leak Test**: Fill system and check for leaks (24+ hours)
3. **Flow Test**: Verify pump operation and flow
4. **Temperature Test**: Monitor temperatures under load
5. **Final Inspection**: Ensure system operates correctly

## Maintenance Requirements

### Regular Maintenance
**Visual Inspection**: Monthly check for leaks and buildup
**Temperature Monitoring**: Watch for performance degradation
**Cleaning**: External radiator and component cleaning
**Coolant Level**: Check reservoir level regularly

### Periodic Maintenance
**Coolant Replacement**: 6-12 months depending on coolant type
**Component Cleaning**: Deep cleaning of blocks and radiators
**Seal Replacement**: Replace O-rings and gaskets as needed
**Performance Verification**: Test thermal performance

### Long-term Maintenance
**Component Replacement**: Pumps and other wear items
**System Upgrades**: Adding or changing components
**Case Modifications**: Modifications for better integration
**Performance Optimization**: Tuning for improved performance

## Troubleshooting Common Issues

### Temperature Problems
**High Temperatures**: Insufficient cooling, air bubbles, pump issues
**Uneven Temperatures**: Flow distribution problems
**Temperature Spikes**: Inadequate thermal mass or flow rate
**Thermal Throttling**: Cooling system inadequacy

### Flow Issues
**Low Flow Rate**: Pump problems, blockages, air bubbles
**No Flow**: Pump failure, severe blockage, electrical issues
**Noise**: Air bubbles, pump problems, turbulence
**Vibration**: Pump mounting, resonance issues

### Leak Issues
**Fitting Leaks**: Improper installation, worn seals
**Tubing Issues**: Poor bends, material degradation
**Component Leaks**: Manufacturing defects, age-related failures
**System Pressure**: Over-pressurization, thermal expansion

## Performance Optimization

### Fine-Tuning
**Fan Curves**: Optimize noise vs. cooling balance
**Pump Speed**: Find optimal flow rate for system
**Coolant Selection**: Choose appropriate coolant for application
**System Balance**: Optimize overall thermal performance

### Advanced Techniques
**Flow Sensors**: Monitor system performance
**Temperature Sensors**: Multiple monitoring points
**Automation**: Automatic system control
**Data Logging**: Track performance over time

Understanding custom loop design enables:
- Planning effective cooling systems
- Selecting appropriate components
- Avoiding common mistakes
- Maintaining system performance
- Achieving optimal cooling results""",
                "order": 1
            }
        ]
    },

    # CASE COURSES
    {
        "title": "PC Case Design and Airflow Optimization",
        "description": "Master case selection, airflow design, and system layout for optimal performance and aesthetics",
        "category": "Cases & Enclosures",
        "difficulty": "beginner",
        "duration": "6 weeks",
        "instructor": "Case Design Team",
        "price": 0.000005,
        "is_featured": True,
        "modules": [
            {
                "title": "Case Form Factors and Layout Design",
                "description": "Understanding different case sizes and internal layout options",
                "content": """# Case Form Factors and Layout Design

## Introduction to PC Cases

The computer case is more than just a protective enclosure—it's the foundation that determines component compatibility, thermal performance, upgrade potential, and aesthetic appeal of your system. Understanding case design principles helps in building better systems.

## Case Functions and Requirements

### Primary Functions
**Component Protection**: Shield components from dust, damage, and static
**Structural Support**: Provide mounting points for all system components
**Thermal Management**: Enable proper airflow for cooling
**Electromagnetic Shielding**: Reduce EMI/RFI emissions and interference
**Accessibility**: Allow easy installation, maintenance, and upgrades

### Design Considerations
**Size Constraints**: Balance footprint with component capacity
**Material Selection**: Steel, aluminum, tempered glass, plastic
**Aesthetics**: Visual appeal and style preferences
**Functionality**: Cable management, tool-free installation
**Expandability**: Room for future upgrades and additions

## ATX Form Factor Family

### Full Tower (E-ATX Support)
**Dimensions**: Typically 24"+ height, 9"+ width, 22"+ depth
**Motherboard Support**: E-ATX, ATX, Micro-ATX, Mini-ITX
**Expansion**: 8-10 expansion slots, multiple drive bays
**Cooling**: 360mm+ radiator support, multiple fan mounting points

**Advantages**:
- Maximum expansion capability
- Superior cooling potential
- Easy working space
- Multiple GPU support
- Extensive drive capacity

**Use Cases**:
- Workstations and servers
- Multi-GPU gaming systems
- Content creation systems
- Extreme overclocking builds
- Storage-heavy applications

### Mid Tower (ATX Support)
**Dimensions**: Typically 18-20" height, 8-9" width, 16-20" depth
**Motherboard Support**: ATX, Micro-ATX, Mini-ITX
**Expansion**: 7 expansion slots, standard drive support
**Cooling**: Up to 280mm radiators, good fan support

**Advantages**:
- Good expansion vs. size balance
- Wide compatibility
- Reasonable desktop footprint
- Cost-effective
- Most popular choice

**Use Cases**:
- Gaming systems
- General purpose builds
- Mainstream workstations
- Budget to high-end systems

### Mini Tower (Micro-ATX)
**Dimensions**: Typically 15-18" height, 7-8" width, 14-18" depth
**Motherboard Support**: Micro-ATX, Mini-ITX
**Expansion**: 4 expansion slots, limited drives
**Cooling**: Smaller radiator support, fewer fans

**Advantages**:
- Compact footprint
- Lower cost
- Adequate for most builds
- Good for office environments

**Use Cases**:
- Budget systems
- Office computers
- HTPC builds
- Space-constrained setups

## Small Form Factor (SFF)

### Mini-ITX Cases
**Dimensions**: Highly variable, typically very compact
**Motherboard Support**: Mini-ITX only
**Expansion**: 1-2 expansion slots, minimal drives
**Cooling**: Limited options, creative solutions required

**Categories**:
- **Sandwich Layout**: GPU parallel to motherboard
- **Traditional Layout**: GPU perpendicular to motherboard
- **Console Style**: HTPC-focused designs
- **Cube Style**: Compact square designs

**Advantages**:
- Very small footprint
- Portable systems
- Living room friendly
- Unique aesthetics
- Challenge and satisfaction

**Challenges**:
- Limited expansion
- Cooling constraints
- Higher component costs
- Build complexity
- Upgrade limitations

### Specialized SFF Forms
**HTPC (Home Theater PC)**:
- Low profile, living room aesthetic
- Quiet operation priority
- Remote control compatibility
- AV connectivity focus

**Portable Gaming**:
- Handle integration
- Robust construction
- Efficient cooling
- Travel-friendly design

## Case Materials and Construction

### Steel Construction
**Advantages**:
- Cost-effective
- Good structural strength
- Excellent EMI shielding
- Easy to manufacture

**Considerations**:
- Heavier than alternatives
- Potential rust issues
- Paint quality varies
- Sharp edges possible

### Aluminum Construction
**Advantages**:
- Lightweight construction
- Natural corrosion resistance
- Premium appearance
- Good thermal conductivity

**Considerations**:
- Higher cost
- Softer material (denting)
- Limited color options
- Manufacturing complexity

### Glass Panels
**Tempered Glass**:
- Premium appearance
- Component visibility
- Scratch resistance
- Safety when broken

**Acrylic/Polycarbonate**:
- Lower cost alternative
- Lighter weight
- More flexible
- Easier to modify

### Mixed Material Design
**Steel Frame + Glass**: Balance of cost and aesthetics
**Aluminum + Steel**: Combine material advantages
**Plastic Accents**: Cost reduction and design elements

## Internal Layout Design

### Traditional Layout
**Motherboard Position**: Vertical mounting on right side
**PSU Position**: Bottom rear, fan down or up
**Drive Cages**: Front section, removable design
**Expansion**: Horizontal slots on rear panel

**Advantages**:
- Familiar layout
- Good compatibility
- Proven airflow patterns
- Cost-effective manufacturing

### Inverted Layout
**Motherboard Position**: Flipped orientation
**PSU Position**: Top mounted
**Advantages**: CPU cooler mounting assistance (gravity)
**Considerations**: Less common, may confuse builders

### Dual-Chamber Design
**Separate Compartments**: Main components vs. PSU/drives
**Advantages**: 
- Clean component separation
- Better cable management
- Improved aesthetics
- Thermal isolation

**Examples**: Corsair Obsidian series, Fractal Define R6

## Drive Support and Storage

### 3.5" Drive Bays
**Traditional Cages**: Front-mounted, multiple drives
**Modular Systems**: Removable cages for flexibility
**Tool-Free Installation**: Quick-release mechanisms
**Vibration Dampening**: Reduce HDD noise and vibration

### 2.5" Drive Support
**Dedicated Mounts**: SSD-specific mounting points
**Bracket Systems**: 3.5" to 2.5" adapters
**Behind-Motherboard**: Clean installation, hidden drives
**Multiple Locations**: Flexibility for drive placement

### M.2/NVMe Considerations
**Direct Motherboard**: No case mounting required
**Thermal Management**: Case airflow affects M.2 temperatures
**Accessibility**: Consider installation and heatsink clearance

## Expansion and Upgrade Potential

### PCIe Slot Access
**Full-Length Cards**: Ensure adequate clearance
**Multi-GPU**: Spacing and power considerations
**Specialty Cards**: Audio, network, storage controllers
**Future Expansion**: Plan for unknown future needs

### Cable Management
**Routing Holes**: Strategic placement for clean routing
**Tie-Down Points**: Secure cable bundles
**Behind-Motherboard Space**: Hidden cable routing area
**Modular Cables**: PSU compatibility considerations

### Tool-Free Features
**Thumbscrews**: No tools required for panels
**Quick-Release**: Drive and expansion card installation
**Modular Components**: Easy reconfiguration
**User-Friendly Design**: Reduce installation time and complexity

## Airflow Design Principles

### Positive vs Negative Pressure
**Positive Pressure**: More intake than exhaust fans
- **Advantages**: Reduced dust infiltration, predictable airflow
- **Disadvantages**: Possible hot air recirculation

**Negative Pressure**: More exhaust than intake fans
- **Advantages**: Guaranteed hot air removal
- **Disadvantages**: Dust infiltration through gaps

**Balanced Pressure**: Equal intake and exhaust
- **Advantages**: Compromise approach
- **Considerations**: Difficult to achieve perfectly

### Airflow Path Design
**Front-to-Rear**: Traditional horizontal airflow
**Bottom-to-Top**: Natural convection assistance
**Side Panel**: Direct component cooling
**Multi-Directional**: Complex but effective systems

### Fan Placement Strategy
**Intake Locations**: Front, bottom, side (cool air sources)
**Exhaust Locations**: Rear, top (hot air removal)
**Component-Specific**: Direct GPU or CPU cooling
**Avoid Conflicts**: Prevent airflow interference

## Aesthetics and Visual Design

### Window Panels
**Size and Placement**: Component visibility optimization
**Tinting**: Subtle component visibility
**RGB Integration**: Lighting effect enhancement
**Cable Management**: Critical for visual appeal

### Internal Aesthetics
**Color Coordination**: Component and cable matching
**RGB Lighting**: Programmable effects and themes
**Custom Modifications**: Unique personalization
**Clean Layout**: Minimize visual clutter

### External Design
**Minimalist**: Clean lines, subtle branding
**Gaming Style**: Aggressive angles, RGB accents
**Professional**: Business environment appropriate
**Unique Designs**: Artistic or themed cases

## Selection Criteria

### Size Requirements
**Available Space**: Desk, floor, or shelf placement
**Component Compatibility**: Current and future components
**Portability**: Moving system frequency
**Aesthetic Fit**: Environment integration

### Feature Priority
**Expansion Needs**: Current and future requirements
**Cooling Priority**: Performance vs. noise balance
**Build Complexity**: Skill level and time available
**Budget Constraints**: Feature vs. cost balance

### Quality Indicators
**Build Quality**: Materials, fit, and finish
**Design Thoughtfulness**: User-friendly features
**Manufacturer Support**: Documentation and warranty
**Community Feedback**: User reviews and recommendations

Understanding case design and selection enables:
- Optimal case selection for specific builds
- Effective system planning and layout
- Proper airflow design implementation
- Future upgrade path planning
- Balanced performance and aesthetic goals""",
                "order": 1
            }
        ]
    },
    {
        "title": "Case Modding and Custom Builds",
        "description": "Learn advanced case modification techniques, custom paint jobs, and unique build projects",
        "category": "Cases & Enclosures", 
        "difficulty": "advanced",
        "duration": "9 weeks",
        "instructor": "Case Modding Team",
        "price": 0.000005,
        "is_featured": False,
        "modules": [
            {
                "title": "Introduction to Case Modding",
                "description": "Planning, tools, and basic modification techniques for custom PC cases",
                "content": """# Introduction to Case Modding

## What is Case Modding?

Case modding (modification) is the art and practice of modifying computer cases to achieve unique aesthetics, improved functionality, or both. It combines technical skills, creativity, and craftsmanship to create personalized computer systems that stand out from mass-produced builds.

## History and Evolution of Case Modding

### Early Days (1990s-2000s)
**Origins**: Enthusiasts modifying beige boxes for better cooling and aesthetics
**Simple Modifications**: Window cutting, LED additions, paint jobs
**Community**: Early internet forums and local computer clubs
**Challenges**: Limited tools, few aftermarket parts

### Golden Age (2000s-2010s)
**Commercial Recognition**: Manufacturers began offering modding-friendly cases
**Advanced Techniques**: Custom cooling loops, complex modifications
**Competition Scene**: ModX, QuakeCon, and other modding competitions
**Media Coverage**: Tech magazines featuring modding projects

### Modern Era (2010s-Present)
**Mainstream Adoption**: RGB lighting, tempered glass panels standard
**Professional Modders**: Career modders working with manufacturers
**Advanced Materials**: 3D printing, CNC machining, laser cutting
**Social Media**: Instagram, YouTube showcasing builds globally

## Types of Case Modding

### Aesthetic Modifications
**Window Cutting**: Adding transparent panels to show internals
**Paint Jobs**: Custom colors, patterns, and finishes
**Lighting**: LED strips, fans, RGB systems
**Decals and Graphics**: Vinyl wraps, etching, printing

### Functional Modifications
**Cooling Enhancements**: Additional fan mounts, radiator support
**Drive Bay Modifications**: Custom storage solutions
**Cable Management**: Hidden routing, custom channels
**Airflow Optimization**: Vent additions, flow redirection

### Complete Custom Builds
**Scratch Building**: Creating cases from raw materials
**Themed Builds**: Movie, game, or character-inspired designs
**Artistic Projects**: Cases as art pieces or sculptures
**Extreme Modifications**: Completely reimagined designs

## Planning a Modding Project

### Project Definition Phase
**Goals and Objectives**: 
- What do you want to achieve?
- Performance improvements vs. aesthetic goals
- Skill development vs. final result focus
- Time and budget constraints

**Inspiration Sources**:
- Online galleries and forums
- Movies, games, and pop culture
- Industrial design and architecture
- Nature and artistic movements

### Design Process
**Concept Development**:
- Sketch initial ideas
- Create mood boards
- Define color schemes
- Establish overall theme

**Technical Planning**:
- Component compatibility verification
- Structural integrity assessment
- Thermal impact analysis
- Manufacturing feasibility review

### Project Documentation
**Design Documentation**: Detailed plans and measurements
**Photo Documentation**: Before, during, and after shots
**Build Log**: Progress tracking and problem solving
**Learning Journal**: Techniques learned and mistakes made

## Essential Tools and Materials

### Basic Hand Tools
**Cutting Tools**:
- **Hacksaw**: Manual cutting for light materials
- **Angle Grinder**: Power cutting and grinding
- **Dremel Rotary Tool**: Precision cutting and shaping
- **Metal Snips**: Sheet metal cutting
- **Jigsaw**: Curved cuts in various materials

**Measuring and Marking**:
- **Rulers and Tape Measures**: Accurate measurements
- **Squares and Protractors**: Right angles and precise angles
- **Scribes and Markers**: Permanent marking on metals
- **Templates**: Consistent hole patterns and shapes

**Assembly Tools**:
- **Drill and Bits**: Hole creation and assembly
- **Screwdrivers**: Standard computer assembly
- **Files and Sandpaper**: Surface finishing and fitting
- **Clamps**: Holding work pieces during assembly

### Advanced Equipment
**Power Tools**:
- **Band Saw**: Accurate straight cuts
- **Drill Press**: Precise hole drilling
- **Belt Sander**: Surface preparation and finishing
- **Router**: Edge profiling and decorative cuts

**Specialized Tools**:
- **Nibbler**: Clean rectangular cuts in sheet metal
- **Step Drill Bits**: Various hole sizes in thin materials
- **Hole Saws**: Large circular holes
- **Metal Brake**: Accurate bends in sheet metal

### Materials and Supplies
**Sheet Materials**:
- **Steel**: Strong, magnetic, moderate cost
- **Aluminum**: Lightweight, corrosion resistant, higher cost
- **Acrylic**: Transparent, easy to work, moderate strength
- **Polycarbonate**: Impact resistant alternative to acrylic

**Fasteners and Hardware**:
- **Machine Screws**: Standard computer hardware
- **Rivets**: Permanent assembly method
- **Standoffs**: Spacing and mounting solutions
- **Adhesives**: Structural and decorative bonding

## Basic Modification Techniques

### Window Cutting
**Planning Phase**:
- Measure and mark cut lines carefully
- Consider structural impact of material removal
- Plan for window material mounting method
- Account for tool width and cutting allowances

**Cutting Process**:
1. **Mark Cut Lines**: Use templates or careful measurement
2. **Drill Corner Holes**: Start points for cutting tools
3. **Cut Edges**: Use appropriate cutting tool for material
4. **File and Smooth**: Remove sharp edges and burrs
5. **Test Fit**: Verify window material fits properly

**Window Installation**:
- **Gaskets**: Rubber sealing for professional appearance
- **Mechanical Fasteners**: Screws with washers or clips
- **Adhesive Mounting**: Structural adhesives for permanent installation
- **Frame Systems**: Custom or commercial window frames

### Surface Preparation and Painting
**Preparation Steps**:
1. **Disassembly**: Remove all components and hardware
2. **Cleaning**: Degrease and remove contaminants
3. **Sanding**: Rough existing paint for adhesion
4. **Masking**: Protect areas not to be painted
5. **Primer Application**: Base coat for paint adhesion

**Painting Techniques**:
- **Spray Cans**: Convenient but limited color options
- **Airbrush**: Precise control, professional results
- **HVLP Gun**: High-volume, low-pressure professional spraying
- **Brush and Roller**: Limited applications, texture effects

**Paint Types**:
- **Enamel**: Durable, glossy finish, longer cure time
- **Acrylic**: Fast-drying, easy cleanup, good durability
- **Powder Coating**: Professional, extremely durable finish
- **Specialty Finishes**: Metallic, pearl, color-changing effects

### Lighting Integration
**LED Strip Installation**:
- **Planning**: Determine lighting zones and effects desired
- **Power Requirements**: Calculate current draw and power supply needs
- **Mounting**: Adhesive backing or mechanical mounting
- **Control**: Manual switches, PWM controllers, or RGB systems

**Fan Lighting**:
- **LED Fans**: Pre-integrated lighting in cooling fans
- **Retrofit Kits**: Add lighting to existing fans
- **Controller Integration**: Synchronize with system lighting
- **Color Coordination**: Match overall system theme

## Safety Considerations

### Personal Safety
**Eye Protection**: Safety glasses during cutting and grinding
**Respiratory Protection**: Dust masks for sanding and painting
**Hand Protection**: Cut-resistant gloves for sharp materials
**Ventilation**: Proper airflow for chemical fumes

### Tool Safety
**Power Tool Operation**: Follow manufacturer instructions
**Blade and Bit Condition**: Keep cutting tools sharp and in good condition
**Electrical Safety**: Proper grounding and GFCI protection
**Fire Prevention**: Metal cutting sparks and flammable materials

### Component Protection
**ESD Prevention**: Anti-static procedures during electronics handling
**Debris Control**: Prevent metal shavings from entering components
**Chemical Protection**: Mask and protect sensitive components during painting
**Reassembly Care**: Clean thoroughly before reassembly

## Planning Your First Mod

### Beginner-Friendly Projects
**Simple Window**: Single side panel window addition
**Basic Paint Job**: Solid color respray of existing case
**LED Addition**: Simple accent lighting installation
**Fan Upgrade**: Replace stock fans with LED versions

### Skill Development Path
1. **Start Simple**: Master basic techniques first
2. **Document Everything**: Learn from successes and mistakes
3. **Join Community**: Learn from experienced modders
4. **Progressive Complexity**: Gradually tackle more challenging projects

### Common Beginner Mistakes
**Inadequate Planning**: Rushing into cutting without proper planning
**Tool Quality**: Using inappropriate tools for the job
**Measurement Errors**: "Measure twice, cut once" principle
**Structural Damage**: Removing too much material and weakening case
**Poor Finish Quality**: Inadequate surface preparation

## Project Examples

### Window Mod Project
**Planning**: Determine window size and position
**Execution**: Cut opening, install window material, finish edges
**Enhancement**: Add LED backlighting for internal illumination
**Skills Developed**: Measuring, cutting, finishing, hardware installation

### Custom Paint Project
**Design**: Choose colors and patterns
**Preparation**: Complete disassembly and surface prep
**Execution**: Primer, base coat, detail work, clear coat
**Skills Developed**: Surface preparation, painting technique, color theory

### Cooling Enhancement
**Analysis**: Identify thermal bottlenecks
**Modification**: Add fan mounts, improve airflow paths
**Testing**: Verify temperature improvements
**Skills Developed**: Thermal analysis, airflow dynamics, performance testing

## Building a Modding Workshop

### Space Requirements
**Work Area**: Adequate space for case and tools
**Ventilation**: Proper airflow for dust and chemical removal
**Storage**: Organization for tools, materials, and hardware
**Lighting**: Good illumination for detailed work

### Budget Considerations
**Tool Investment**: Start with basics, add specialty tools as needed
**Material Costs**: Plan for waste and experimentation
**Safety Equipment**: Never compromise on safety gear
**Learning Resources**: Books, videos, and community access

Understanding case modding fundamentals enables:
- Planning and executing successful modification projects
- Developing technical and artistic skills
- Creating unique, personalized computer systems
- Participating in the modding community
- Combining functionality with aesthetic appeal""",
                "order": 1
            }
        ]
    }
]

def create_course_thumbnail(title, category, output_path):
    """Create a custom thumbnail for the course"""
    # Create image
    img = Image.new('RGB', (400, 300), color='#1e3a8a')
    draw = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 20)
        category_font = ImageFont.truetype("arial.ttf", 14)
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
    y = 85 - (len(lines) * 10)
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        x = (400 - bbox[2]) // 2
        draw.text((x, y), line, fill='white', font=title_font)
        y += 25
    
    # Draw category
    bbox = draw.textbbox((0, 0), category, font=category_font)
    x = (400 - bbox[2]) // 2
    draw.text((x, 225), category, fill='#60a5fa', font=category_font)
    
    # Add some decorative elements
    draw.rectangle([50, 50, 350, 54], fill='#60a5fa')
    draw.rectangle([50, 246, 350, 250], fill='#60a5fa')
    
    # Save image
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path)
    return output_path

if __name__ == "__main__":
    # Run sync version
    client = MongoClient('mongodb://localhost:27017')
    db = client.edtech_hardware
    
    # Ensure uploads directory exists
    uploads_dir = "uploads/thumbnails"
    os.makedirs(uploads_dir, exist_ok=True)
    
    courses_added = 0
    
    for course_data in FINAL_COURSES:
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
    
    print(f"\n🎉 Successfully added {courses_added} final hardware courses!")
    client.close()
