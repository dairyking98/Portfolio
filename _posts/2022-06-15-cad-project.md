---
title: CAD Project - Self-Propelled Wall Leaper
date: 2022-11-29 10:00:00 -0500
tags:
  - cad
  - design
  - engineering
  - school-project
  - fusion360
  - 3d-printing
category: School Projects
description: A detailed CAD design project from my Intro to Engineering course, where I designed and built a self-propelled device that launches over a 3-foot wall using rubber band power and 3D printed components.
---

This project was completed for my Intro to Engineering course in November 2022, under Professor Khandani. The challenge was to create a device from scratch that is self-propelled and launches from one point to another 8 feet away while overcoming a 3-foot vertical height in the center.

## Video Demonstration

<iframe width="560" height="315" src="https://www.youtube.com/embed/YUEf5KbRb5A" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## 1: Define the Problem

### Problem Statement

I had to create a device from scratch that is self-propelled, and launches from one point to another 8 feet away while overcoming a 3-foot vertical height in the center.

### Criteria for Success

The criteria I wanted to impose upon a successful device design are the following:

- **Simplicity/complexity of design** - The device should be relatively simple and easy to understand the methods of operation and how trajectory is achieved. Parts should be easy to obtain.
- **Predictability of travel/consistency/repeatability** - Trajectory of the device should be almost the same with minimal variation between launches.
- **Ease/difficulty of triggering mechanism** - The device should be triggered without creating a large disturbance from the hands triggering it. A device sensitive to hand movements or difficult to trigger may not have an intended trajectory.
- **Build time** - The device should not take long to assemble and modify if necessary.
- **Safety** - The device should be relatively safe to operate. Minimize sharps, projectiles, accidental triggers.
- **3D printability** - The device should be easily 3D modeled and printed. I am very familiar with 3D prototyping and printing, so I will feel most comfortable and efficient working with 3D printed parts.

## 2: Gather Pertinent Information

- The device must travel together with nothing remaining at the launch point, and cannot be thrown from hands.
- The device may be powered mechanically or electrically. Chemical explosives, living creatures, remote control devices, CO2 cartridges, or pressurized gas or liquid tanks made of metal or plastic may not be used.
- The device must leap over a wall 3 feet high, starting 4 feet away from the base of the wall, and targeting 4 feet away from the base of the other side of the wall.
- The device must land as close to the target line as possible.
- The device must be made from scratch.
- The device must not expand or contract after landing.
- The device has only two opportunities to leap for the official test.
- The device is restricted to a total cost of $20.00.

## 3: Generate Multiple Solutions

### Design 1: Helicopter-like device

Rubber band powered propeller shaft connected to rigid lightweight frame with fins to counter the rotation induced by the propeller spinning. Release of trigger would be letting go of wound up propeller and device by hand.

### Design 2: Stick-leaper device

Rubber-band powered scissor-like linkages to propel mass at a high velocity to build momentum and carry the entire device over the wall. Mass is linearly propelled. Release of trigger would be balancing rubber band snap position at tension right before tipping point, and gentle push with finger past tipping point to trigger the release of tension and cause snapping together of linkages.

### Design 3: Mousetrap-catapult device

Mousetrap spring-powered self-catapulting system to fling mass towards trajectory over the wall to carry the catapult with it. Similar to the stick-leaper device, but mass is propelled somewhat angularly. Release of trigger would be some sort of hair trigger.

### Design 4: Blimp-balloon device

Rubber band powered propeller shaft attached to a helium balloon, counterweighted just enough so that it almost floats through the air with the same average density as air. Release of the trigger would be done by hand.

### Design 5: Spring-propelled javelin device

A javelin-like shaft is attached to and protruding through a spring. Spring is held in hands and the shaft is pulled back, aimed, and released. Or; shaft is propped on the ground and angled towards the desired trajectory. Mass on spring is pulled back and released. Velocity of mass generates momentum for the device to leap over the wall.

## 4: Analyze and Select a Solution

### Decision Matrix

| Criteria | Weight % | Design 1 | Design 2 | Design 3 | Design 4 | Design 5 |
|----------|----------|----------|----------|----------|----------|----------|
| Safety | 10 | 6 | 4 | 2 | 6 | 5 |
| Predictability | 20 | 2 | 8 | 2 | 3 | 6 |
| Build Time | 20 | 3 | 7 | 4 | 3 | 8 |
| Trigger | 10 | 4 | 8 | 3 | 4 | 4 |
| Simplicity | 20 | 3 | 6 | 5 | 4 | 8 |
| 3D Printability | 20 | 3 | 8 | 4 | 2 | 4 |
| **Total** | **100** | **320** | **800** | **350** | **340** | **610** |

**Design 2, the stick-leaper (in bold), is the design that has the most weight in the decision matrix above.**

Design 1 seems very unpredictable, and weight dependent. Design 2 seems most logical. It looks relatively simple to 3D model and print. Design 3 may break the Professor's rules, as it is not made completely from scratch. Design 4 seems very unpredictable and weight dependent. Design 5 seems like it would require a very strong spring, or break the Professor's rules.

## 5: Test and Implement the Solution

I began designing with Autodesk Fusion 360, which I am most familiar with and use to create models for 3D printing. I designed keeping in mind that my parts would be 3D printed, and thus the geometry must be accommodating for 3D printing.

### First Prototype

My first prototype was made exactly how I envisioned it, and I quickly found issues that presented themselves and would impede efficient operation of the leaper. 

Firstly, the slotted pin trigger release had too much friction to release with one hand quickly. Secondly, the linkages were arranged in such a way that energy would be lost at the launch. The linkages were inefficiently placed, and was probably overall a weaker and power-inefficient design.

### Second Iteration

The second iteration resolved the issue of the possibility of momentum being lost due to undesired angular rotation at the single axle by introducing two axles instead of one at the center joint, in addition to gearing the arms to constantly mesh them together. The arms were simplified and made much more rigid which significantly improved the design. At this stage, the leaper showed promising results.

I thought only one set of gears would suffice, but both top and bottom joints needed gears for optimal linear motion. This second iteration also deleted the slotted pin trigger, and instead allowed the linkages to fold past the maximum tension point, allowing the leaper to be in a constant tensile state. When ready to leap, the leaper would be balanced between the states of unfolding, and easily be nudged into its correct unfolding motion.

### Third Iteration (Final Design)

The third iteration optimized launch angle at 60 degrees, widened the base so it would stand easier, gusseted the bottom center joint to reduce mass, and embiggened holes to affix lead mass to. I also added gears to the top joint, and filleted sharp corners of the gears due to a failure from the second iteration at a sharp corner.

I began to use Silly Putty to increase friction between the surface of the launch and the bottom center joint of the leaper, which had a better time adhering due to the gusseting. This third iteration proved to be successful at the two official launches.

Pressed for time, I decided to increase the tension and mass by moving the screws to the outer threads and adding more rubber bands and mass. I recorded my two official launches successfully, and the leaper survived.

I was beginning to see flexing in the 3D printed arms from the amount of tension that was stored in the rubber bands. Additionally, upon leaping, the two arms came together very hard and showed signs of chipping and damage. The design through use began to get a little bit flimsy and loose, so the non-geared joints could be redesigned to withstand more strength and impact against each other. Despite this, the leaper made two successful leaps and survived.

## Physical Description of Operation

The final iteration of design 2 dubbed the "stick leaper" is 3D printed and rubber band powered. It works by propelling a mass of lead at a high velocity to generate momentum that will carry the entire stick leaper through the trajectory.

The lead mass is propelled by being affixed to the end of a pair of 3D printed folding arms. The arms are manually folded and tensioned with rubber bands, and when unfolded, propel the mass in a fast linear direction. The tensioned rubber bands are hooked around metric screws that are directly screwed into the folding arms. The tensioned rubber bands are held fast to the arms by a separate set of rubber bands wrapped around each pair of metric screws.

The folding motion of the arms is controlled by gearing the arms of the stick leaper so they move concurrently. The device is a bistable mechanism where the full folding motion extends just past the maximum rubber band tensile point, where the device can fall into a stable but tensioned position.

For the final launch, 10 rubber bands were used for tensioning, and 4 were used to retain the rubber bands to the screws after unfolding.

## Final Design Specifications

The final design features:
- **Launch angle**: 60 degrees
- **Power source**: 10 rubber bands for tensioning, 4 for retention
- **Mass**: Lead scraps affixed to the arms
- **Trigger mechanism**: Bistable mechanism - balanced at tipping point, nudged to trigger
- **Materials**: 3D printed PLA components with metal screws and copper rod axles

## List of Materials

| Material | Amount | Cost |
|----------|--------|------|
| 3D Printed PLA | 107.79 grams (final design only) | $2.16 |
| M4x0.7x10mm Screw | 8 pieces | $2.00 |
| Rubber Bands | 14 pieces | $1.00 |
| 1/16" copper rod | 12 inches | $1.00 |
| Silly Putty | 1 pack | $1.00 |
| Lead Scraps | 4 ounces | $1.00 |
| **Total** | | **$8.16** |

## Lessons Learned

This project taught me valuable lessons about:
- Iterative design and prototyping
- The importance of testing and refinement
- Working within constraints (budget, materials, safety)
- 3D printing considerations for mechanical parts
- Energy transfer and mechanical advantage in linkage systems

The project successfully demonstrated the engineering design process from problem definition through multiple iterations to a working solution.

## Source Documents

The following documents are available for reference:

- [CAD Project Final Report](/documents/2022/cad-project/CAD-Project-Final-Report.pdf) - Complete final report with design process, iterations, and analysis
- [Progress Report 056](/documents/2022/cad-project/DesignProjectAssignment8ProgressReport056.pdf) - Early progress documentation
- [Progress Report 057](/documents/2022/cad-project/DesignProjectAssignment8ProgressReport057.pdf) - Mid-project progress update
- [Progress Report 058](/documents/2022/cad-project/DesignProjectAssignment8ProgressReport058.pdf) - Final progress documentation

---

*This project was completed in November 2022 for Intro to Engineering (Professor Khandani) as part of my personal engineering coursework.*

