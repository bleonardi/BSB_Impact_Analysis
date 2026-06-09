# Brent Spence Bridge: Home Price Event Study

## Overview
An event study measuring how major Brent Spence Bridge (BSB) corridor milestones affected residential home prices in nearby ZIP codes. The analysis identifies a significant "landing zone" effect — properties within 1 mile of the I-75/BSB corridor have outperformed the broader Cincinnati-Northern Kentucky region by roughly 8.5 percentage points since the 2020 fire.

## Key Data Science Skills
*   **Event Study Methodology:** Normalizing asset prices around discrete "shock" events (federal grants, contractor awards, groundbreaking).
*   **Distance-Band Analysis:** Segmenting ZIP codes into proximity zones relative to infrastructure corridors.
*   **Time-Series Visualization:** Tracking indexed price trajectories across pre/post event windows.

## Tech Stack
*   **R / Quarto:** Analysis and report generation.
*   **Python:** Data fetching and ZIP-to-corridor distance calculations.

## Data Sources
*   **Zillow ZHVI:** Home Value Index by ZIP code (sourced locally — excluded from repo due to file size).
*   **US Census Bureau:** ZIP code geometries and demographic context.

## Events Analyzed
1.  **$1.6B Federal Grant** (Dec 2022)
2.  **Contractor Award to Walsh Kokosing** (Jul 2023)
3.  **Groundbreaking Ceremony** (Jan 2024)
4.  **Physical Construction Start** (2024)
