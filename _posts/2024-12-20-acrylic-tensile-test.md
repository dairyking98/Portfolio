---
title: Open-Ended Experiment - Tensile Testing of Acrylic with Geometric Discontinuities
date: 2024-12-20 09:00:00 -0500
tags:
  - materials-testing
  - mechanical-engineering
  - stress-analysis
  - school-project
category: School Projects
description: Investigated how cast acrylic specimens with holes and notches respond to tensile loading using Instron testing and stress concentration analysis.
---

ENGR 302 – Experimental Analysis at San Francisco State University culminated in an open-ended lab where my teammates (Tom Boivin, Driss Hakkou, Denis Steffen) and I characterized how geometric discontinuities influence the tensile performance of 1/4-inch cast acrylic. We modeled and fabricated "dog bone" specimens with circular, notched, square, and diamond cut-outs, then compared their behavior against a control sample to understand how stress concentration factors translate into real failures.

## Project Overview

- **Objective:** quantify the impact of different discontinuity geometries on acrylic tensile strength and ductility, and compare the findings against theoretical stress concentration predictions.
- **My focus:** coordinating specimen preparation, verifying the Instron 3369 test program, and consolidating the load–elongation data exported from Bluehill Universal into a clean dataset for team analysis.
- **Course context:** ENGR 302 — Experimental Analysis, Fall 2024 (Instructor: Dr. Ed Cheng).

## Experimental Setup

We used an Instron 3369 tensile test frame with a 50 kN load cell and threaded side-action grips to maintain alignment and avoid slippage. Each test ran at 2 in/min while Bluehill Universal logged force and displacement. An initial calibration sweep checked the load cell and grip tension before every pair of specimens.

Specimens were laser-cut from McMaster-Carr cast acrylic sheet (`4615T47`), sanded to remove machining marks, and measured to capture true cross-sectional areas. Control blanks retained the full gauge width, while the discontinuity specimens reduced the critical area to approximately 29.5 mm². Detailed dimensions and CAD sketches are included in the source report.

## Key Findings

- **Control baseline:** yielded at 11.1 MPa—roughly 80% lower than the manufacturer's 55 MPa specification—highlighting how processing and environmental factors can degrade acrylic strength.
- **Circular vs. notched specimens:** yielded at 18.96 MPa (Kt ≈ 1.71) and 21.56 MPa (Kt ≈ 1.94), respectively. The rounded notch distributed stress slightly better than the through-hole, aligning closely with handbook predictions.
- **Sharp corners matter:** square and diamond cut-outs experienced brittle failures at 17.25 MPa and 20.51 MPa with minimal elongation (≤1.76 mm), confirming how angular geometry acts like pre-existing cracks.
- **Ductility loss:** control specimens stretched to 10.2 mm before fracture, whereas discontinuity samples fractured almost immediately after yielding, showing how stress raisers strip away energy absorption capacity.

## Theoretical vs. Experimental Snapshot

| Specimen Type | Theoretical Yield Stress (MPa)† | Experimental Yield Stress (MPa) | Ratio (Actual ÷ Theoretical) |
|---------------|---------------------------------|---------------------------------|------------------------------|
| Control       | 11.11 (baseline)                | 11.11                           | 1.00                         |
| Circular Hole | 23.70                           | 18.96                           | 0.80 (Kt ≈ 1.71)             |
| Notched       | 19.74                           | 21.56                           | 1.09 (Kt ≈ 1.94)             |

†Derived using control yield stress as the nominal reference and handbook stress concentration factors.  
Note: We could not locate reliable theoretical data for the laser-cut square and diamond geometries—those specimens are discussed purely from experimental observations.

## Experimental Metrics Overview

| Specimen Type | Yield Force (N) | Yield Stress (MPa) | Ultimate Stress (MPa) | Fracture Stress (MPa) | Max Elongation (mm) | Modulus (MPa) |
|---------------|----------------:|-------------------:|----------------------:|----------------------:|--------------------:|--------------:|
| Control       | 750             | 11.11              | 57.04                 | 51.84                 | 10.20               | 1,743         |
| Circular Hole | 580             | 18.96              | 50.27                 | 50.27                 | 1.63                | 4,116.5       |
| Notched       | 625             | 21.56              | 71.63                 | 71.57                 | 2.25                | 4,098.5       |
| Square Hole   | 500             | 17.25              | 54.77                 | 54.77                 | 1.76                | 3,483         |
| Diamond Hole  | 600             | 20.51              | 34.70                 | 34.70                 | 0.89                | 4,478         |

Additional context:

- **Cross-sectional area:** control blanks averaged 67.51 mm²; all discontinuity specimens clustered around 29–31 mm².
- **Elongation at yield:** ranged from 0.39–0.55 mm, reinforcing the brittle response once discontinuities were introduced.
- **Stress concentration factors:** experimentally back-calculated Kt values were 1.00 (control), 1.71 (circle), and 1.94 (notch); the square and diamond data did not yield stable Kt values because the failure location varied specimen-to-specimen.

## Discussion and Recommendations

The close agreement between theoretical and experimental stress concentration factors for simple shapes validated our analytical approach. However, the scatter in the square and diamond data underlined the limits of handbook solutions for complex geometries. We recommended:

- Slowing the crosshead speed to 0.5 in/min for more stable strain measurements on brittle plastics.
- Polishing laser-cut edges to reduce micro-crack initiation sites.
- Extending the study with finite element analysis to visualize stress fields around sharp corners.
- Repeating the experiment across temperatures to capture acrylic's sensitivity to cold-induced embrittlement.

## Lessons Learned

- Material datasheet values can diverge dramatically from lab-prepared specimens; surface finish and fabrication technique matter.
- Precise dimensional metrology is essential when small area changes drive stress calculations.
- Capturing full test context (fixture setup, calibration steps, environmental notes) makes post-lab analysis and reporting far easier.

## Source Document

- [Open-Ended Experiment Report (PDF)](/documents/2024/engr302/OEE-Final-Report-12-20-24.pdf)

---

*Completed December 2024 for ENGR 302 — Experimental Analysis (Professor Ed Cheng).*

