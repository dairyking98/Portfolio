---
title: Analog Voltmeter Clock - Time and Environmental Monitor
date: 2024-12-15 10:00:00 -0500
tags:
  - arduino
  - electronics
  - embedded-systems
  - sensors
  - 3d-printing
  - school-project
  - personal-project
category: School Projects
description: A unique clock project combining analog voltmeters with environmental monitoring, featuring custom 3D-printed enclosure and Arduino-based control system.
---

This project was completed for Assignment 4 in Fall 2024, under Professor Jonathan Song. The challenge was to design and build a device that displays time using analog voltmeters, with the added functionality of monitoring pressure, temperature, and humidity.

## Project Overview

The device I built is a clock combined with a pressure, temperature, and humidity monitor using analog voltmeters for an engaging and unique display. The analog voltmeters feature custom legends that indicate the current hour, minute, and second, or pressure, temperature, and humidity on a graduated scale. I was inspired by the idea of using analog displays to show time, which has a classic and visually engaging aesthetic. To further challenge myself, I integrated environmental monitoring features, making the device multi-functional.

All components and the encoder knob assembly are securely fastened to a custom 3D-printed enclosure made of PLA on an Ender 5 printer. Time adjustments are made using a homemade rotary encoder and a button. The display toggles with a short press of the button.

## Physical Design

For the physical design, I aimed to create something large and unique—a device that would instill curiosity at first glance. The analog voltmeters and vintage embossed labels provide a sense of nostalgia. The oversized rotary encoder is a deliberate design choice, serving both functional and educational purposes. The method of function of an incremental rotary encoder can now be felt, seen, and heard. It offers a satisfying, hands-on experience and acts as a demonstration tool to illustrate the inner workings of a rotary encoder.

The analog voltmeter's original 0-30V graduated display was modified with custom-designed and printed legends that indicate:
- **Hours**: 0-12
- **Minutes and Seconds**: 0-60
- **Pressure**: 950-1030 hPa
- **Relative Humidity**: 0-100%

These values were chosen as the range at which this device is estimated to function. The voltmeters, originally rated for 30V, had to be further modified to operate at 5V by removing their internal resistors and installing adjustable potentiometers for calibration.

## System Architecture

A DS3231 real-time clock module (RTC) is used to keep accurate time and maintain the time even when the Arduino is fully powered off, thanks to an external watch battery. It communicates with the Arduino via I2C protocol. The current time provided by the RTC is obtained constantly and stored as variables in the Arduino.

The BMP180 pressure sensor also communicates via I2C, and the current pressure is stored as a variable. The DHT22 humidity sensor operates via pulse-width modulated input, which is handled by a library, and its variable is also stored.

The time and environmental variables are converted to integers in the range of 0 to 255 to provide pulse-width modulated outputs for the voltmeters. When the display mode is set to TIME, the voltmeters display the current hour, minute, and second at quarter-second intervals to provide for a sweeping second hand, and the HOURS, MINUTES, and SECONDS LEDs remain on. When the display mode is set to PTH (pressure, temperature, and humidity), the voltmeters display the current pressure, temperature, and humidity, and the PRESSURE, TEMPERATURE, and HUMIDITY LEDs remain on.

## User Interface

The display mode is toggleable via a short press of a user-interaction arcade button. Upon a long press of the arcade button, a TIME CHANGE mode is entered, in which the rotary encoder is used to select the new HOUR, MINUTE, and SECOND. This is indicated by a blinking corresponding LED and isolated operation of the selected voltmeter. A new value is confirmed by pressing the arcade button until the last parameter, SECONDS, has been updated, returning to TIME display mode.

The rotary encoder operates on two input signals that are treated as interrupts, performing interrupt service routines (ISRs) when their signal values change, providing for a responsive and effective incremental rotary encoder.

## Components and Materials

The device is built using the following components:

- **Arduino Nano** (microcontroller)
- **Two limit switches** (used for rotary encoder input)
- **One arcade button** (for toggling the display and time adjustment)
- **One DHT22 sensor** (for temperature and humidity sensing)
- **One BMP180 sensor** (for pressure sensing)
- **Six 6V LEDs** (for illumination and visual feedback)
- **One DS3231 RTC** (Real-Time Clock) module (for accurate timekeeping)
- **Three analog voltmeters** (to display time and environmental data)
- **Three 5kΩ potentiometers** (for analog voltmeter calibration)
- **3D-printed PLA enclosure** (custom-designed housing)
- Various resistors, wires, and mounting hardware

## Key Features

1. **Dual Display Modes**: Toggle between time display and environmental monitoring
2. **Quarter-Second Updates**: Smooth sweeping second hand using PWM interpolation
3. **Custom Calibrated Voltmeters**: Modified from 30V to 5V operation with custom legends
4. **Homemade Rotary Encoder**: Built from limit switches for educational demonstration
5. **3D-Printed Enclosure**: Custom-designed housing for all components
6. **Real-Time Clock**: Maintains accurate time even when powered off

## Technical Implementation

The Arduino code handles:
- Reading time from the DS3231 RTC module
- Reading environmental data from BMP180 and DHT22 sensors
- Converting values to PWM signals (0-255) for voltmeter control
- Managing rotary encoder interrupts for time adjustment
- Button press detection (short press for mode toggle, long press for time adjustment)
- LED control for visual feedback
- Quarter-second interpolation for smooth second hand movement

## Development Process

The project involved several key development steps:

1. **Conceptual Design**: Initial idea for using analog voltmeters as displays
2. **Component Selection**: Choosing appropriate sensors and microcontroller
3. **Voltmeter Modification**: Removing internal resistors and adding potentiometers for 5V operation
4. **Custom Legend Design**: Creating and printing custom scales for each voltmeter
5. **3D Enclosure Design**: Designing and printing the housing in Fusion 360
6. **Arduino Programming**: Implementing the control logic and sensor interfaces
7. **Calibration**: Adjusting potentiometers to match voltmeter readings with actual values
8. **Testing and Refinement**: Iterative testing to ensure accuracy and reliability

## Lessons Learned

This project taught me valuable lessons about:
- Interfacing multiple sensors with Arduino (I2C and digital protocols)
- PWM signal generation and calibration
- Real-time clock integration and time management
- Rotary encoder implementation using interrupts
- 3D printing considerations for electronics enclosures
- Analog display calibration and modification
- User interface design for embedded systems

## Source Documents

The following documents are available for reference:

- [Clock Report](/documents/2024/clock-project/Clock-Report.pdf) - Complete project report with detailed design, implementation, and analysis
- [Assignment 4 Project Idea](/documents/2024/clock-project/Assignment-4-Project-Idea.pdf) - Initial project proposal and concept
- [Arduino Clock Code](/documents/2024/clock-project/Arduino-Clock-Code.md) - Complete source code with detailed comments
- [Clock Presentation](/documents/2024/clock-project/Clock-Presentation.pdf) - Project presentation slides

---

*This project was completed in December 2024 for Assignment 4 (Professor Jonathan Song) as part of my academic coursework.*

