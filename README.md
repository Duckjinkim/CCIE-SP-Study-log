# CCIE SP Study LAB Time Tracker

## Overview
Welcome to the **CCIE SP Study LAB Time Tracker**! This project is part of my journey as a network engineer preparing for the **CCIE Service Provider (SP)** certification. I built this tool to track my study time, visualize my progress through GitHub Contributions, and sharpen the time-management skills that the CCIE LAB exam demands. This repository serves as a portfolio piece demonstrating my dedication to CCIE SP preparation and my Python automation skills.

### Why I Built This
The CCIE LAB exam is a rigorous, multi-hour test that demands exceptional time management, troubleshooting, implementation, deployment, and design skills under pressure. To prepare effectively, I needed a tool to:

- **Track Study Time**: Monitor how much time I spend on lab practice to ensure consistent progress.
- **Visualize Contributions**: Use the GitHub contribution graph to visually represent my study efforts over time.
- **Practice Time Management**: Simulate the time constraints of the CCIE LAB by tracking and optimizing each lab session.
- **Sharpen Lab Skills**: Focus on troubleshooting, meeting requirements, implementing solutions, deploying configurations, and designing networks within a fixed timeframe.

## How It Works
The **CCIE SP Study LAB Time Tracker** is a Python application built with Tkinter for the GUI. It tracks the time spent on each practice session and automatically logs the data to `CCIE-SP-Study-log.txt`, which is then committed and pushed to this GitHub repository.

- **Start/Stop Timer**: Use the **Start** button to begin a lab session and **Stop** to pause it. The timer counts down in real time from the configured lab length.
- **Section Tracking**: The app includes Section 1 through Section 6 to mark the completion of specific lab tasks. When a section is checked, the remaining time at that moment is recorded.
- **Automatic GitHub Updates**: On exit (or when the timer hits zero), the log file is updated, committed, and pushed to GitHub, keeping my contribution graph in sync with my study progress.

### Key Features
- **Real-Time Countdown Timer** for each lab session.
- **Section-Based Tracking** that records the time taken to reach each section.
- **GitHub Integration** that automatically commits and pushes updates.
- **Configurable Settings** — lab length, number of sections, repo path, and branch are all set at the top of `lab_tracker.py`.

## Configuration
All key settings live in a single block at the top of `lab_tracker.py`:

```python
TRACK_NAME    = "CCIE SP"
REPO_DIR      = r"Z:\CCIE EI\CCIE SP\CCIE-SP-Study-Log"
LOG_FILENAME  = "CCIE-SP-Study-log.txt"
GIT_BRANCH    = "main"
LAB_HOURS     = 5
NUM_SECTIONS  = 6
```

## Setup

### Prerequisites
- **Python 3.x** — https://www.python.org/downloads/
- **Git** — https://git-scm.com/
- **GitHub account** with this repository.

### First-time repo setup
```bash
cd "Z:\CCIE EI\CCIE SP\CCIE-SP-Study-Log"
git init
git remote add origin https://github.com/Duckjinkim/CCIE-SP-Study-log.git
git branch -M main
git add .
git commit -m "Initial commit"
git push -u origin main
```

### Run the application
```bash
python lab_tracker.py
```

### Usage
- **Start a Session**: Click **Start** to begin tracking.
- **Pause a Session**: Click **Stop** to pause the timer.
- **Mark Sections**: Check the boxes (Section 1–6) to record the time reached for each section.
- **Exit and Save**: Click **Exit** to save the session and push it to GitHub.

## My CCIE Journey
Having previously prepared for and pursued CCIE Enterprise Wireless, I'm now focused on the **CCIE Service Provider** track. Each commit in this repository represents a study session, letting me visualize my investment over time and identify areas to improve.

## License
This project is open-source under the [MIT License](LICENSE).

## Contact
- GitHub: [DJ Kim](https://github.com/Duckjinkim)
- Email: [ccie68155@gmail.com](mailto:ccie68155@gmail.com)
- LinkedIn: https://www.linkedin.com/in/dj-duckjin-kim-55727827b/
- Blog: https://ccie68155.tistory.com/

Happy studying, and good luck on your CCIE SP journey!
