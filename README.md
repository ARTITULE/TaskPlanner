# TaskPlanner

A minimal desktop task manager built with Python and PyQt5 built for fun and experience.

## Key Features
- **Advanced Calendar**: High-density, color-coded workload visualization (Important, Regular, Completed).
- **Hybrid Storage**: Seamless switching between local JSON persistence and remote Cloud Sync.
- **Dynamic Theming**: Full Light/Dark mode support with automatic system theme detection via QSS.
- **Secure Auth**: Integrated Login/Signup system for remote data synchronization.
- **Smart Filtering**: Dedicated views for "My Day", "Important", and historical "Completed" tasks.

## Auth and Cloud Sync
- The Cloud API is designed and maintained by [QAWSEDRH](https://github.com/QAWSEDRH). The app can be used with it. I am not responsible for the api development and uptime.

## Tech Stack
- **Language**: Python 3.10+
- **GUI Framework**: PyQt5
- **Networking**: Requests (Remote API sync)
- **Styling**: Qt Style Sheets (QSS)
- **Persistence**: Local JSON / Remote REST API

## Engineering Standards
- **Externalized Styles**: All visual properties are isolated in `.qss` files.
- **Centralized Resources**: Resource paths and icons are managed exclusively via `config.py`.

## Getting Started

### Prerequisites
- Python 3.10+
- PyQt5

### Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python src/task_planner/main.py
   ```

## Contributing
Contributions are welcome from those who appreciate minimal, clean code. Please ensure any PRs utilize the existing QSS architecture for any visual updates.  
