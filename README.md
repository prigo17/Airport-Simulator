# Airport Simulator

## Overview

Airport Simulator is a text-based Python game where you manage an airport over a 24-hour period. The objective is to maintain a high reputation by scheduling flights, managing runways, and handling emergencies amidst dynamic weather conditions.

## Key Features

- **Reputation System**: Starts at 100%. Successes increase it (+1%), while delays or failures decrease it (-2% or more).
- **Win/Loss Conditions**: Win by ending with ≥70% reputation; lose if it drops below 30%.
- **Flight Scheduling**: Manage 10 base flights and add extra ones for a challenge.
- **Runway Management**: Schedule maintenance without disrupting operations.
- **Dynamic Weather**: Clear, stormy, or foggy conditions impact scheduling.
- **Emergencies**: Handle random emergency landings.

## Requirements

- Python 3.6+
- Dependency: `python-dateutil` (install with `pip install python-dateutil`)

## Setup

1. Download or clone the `AirportSimulator.py` file.
2. Install the required package:

   ```bash
   pip install python-dateutil
   ```
3. Run the game:

   ```bash
   python AirportSimulator.py
   ```

## How to Play

1. **Start**: Launch the script to begin the 24-hour simulation.
2. **Menu Options**:
   - View airport status (reputation, runways, weather, time).
   - Advance time to process events.
   - Schedule additional flights.
   - Schedule runway maintenance.
   - View event logs.
   - Exit early.
3. **Objective**: Keep reputation ≥70% after 24 hours.
4. **Challenges**: Weather changes and emergencies test your strategy.

## Example

- Start with 100% reputation and 3 runways.
- Schedule an extra flight at 14:00.
- Advance time; a storm delays a landing (-2% reputation).
- Handle an emergency landing successfully (+1%).
- End with 70% reputation to win.

