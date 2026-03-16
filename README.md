# TaskPlanner

A minimal desktop task manager built with Python and PyQt5 built for fun and to gain experience.

## Key Features

- **Advanced Calendar**: High-density, color-coded workload visualization (Important, Regular, Completed).
- **Hybrid Storage**: Seamless switching between local JSON persistence and remote Cloud Sync.
- **Dynamic Theming**: Full Light/Dark mode support with automatic system theme detection via QSS.
- **Secure Auth**: Integrated Login/Signup system for remote data synchronization.
- **Smart Filtering**: Dedicated views for "My Day", "Important", and historical "Completed" tasks.

## 📂 Project Structure

```text
src/task_planner/
├── main.py             # Application entry point
├── app.py              # App initialization and event handling
├── config.py           # Centralized configuration (API, paths, icons)
├── auth/               # User authentication and session management
├── controllers/        # Business logic and state coordination
├── models/             # Data structures and visual representations
├── services/           # Persistence layers (local JSON & remote REST API)
└── ui/                 # PyQt5 UI components and styling
    ├── styles/         # External Qt Style Sheets (.qss)
    └── widgets.py      # Reusable custom UI components
```

## Tech Stack

- **Language**: Python 3.10+
- **GUI Framework**: PyQt5
- **Networking**: Requests (Remote API sync)
- **Styling**: Qt Style Sheets (QSS)
- **Persistence**: Local JSON / Remote REST API

## Engineering Standards

- **Externalized Styles**: All visual properties are isolated in `.qss` files.
- **Centralized Resources**: Resource paths and icons are managed exclusively via `config.py`.

## 🏁 Getting Started

### Prerequisites

- Python 3.10+
- `pip` (Python package installer)

### Installation

1. **Clone the repository**

2. **Create and activate a virtual environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```bash
   python src/task_planner/main.py
   ```

## 🤝 Contributing

Contributions are welcome. Please ensure any PRs utilize the existing QSS architecture for any visual updates.

## 📝 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## ☁️ API Disclaimer

The Cloud API integration is designed for use with an external service maintained by [QAWSEDRH](https://github.com/QAWSEDRH). I am not responsible for the uptime or maintenance of the remote API.
