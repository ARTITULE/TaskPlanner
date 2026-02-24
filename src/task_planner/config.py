from pathlib import Path

Base_URL = "https://introspectional-scalelike-ria.ngrok-free.dev"

DATA_PATH = Path("src/task_planner/data/tasks.json")

Categories = ["None",
              "Important" 
              "Work",
              "Personal", 
              "School", 
              "Home",
              "Family",
              "Errands",
              "Calls",
              "Urgent",
              "Learning",
              "Health",
              "Inbox",
              ]

MENU_ICONS = {
    "My Day": "src/task_planner/icons/sun/icons8-sun.svg",
    "Important": "src/task_planner/icons/star/star.svg",
    "Completed": "src/task_planner/icons/check_box/icons8-check-mark-checked.svg",
    "Tasks": "src/task_planner/icons/home/icons8-home.svg",
    "Calendar": "src/task_planner/icons/calendar/calendar.svg",
    "Groups": "",
    "Settings": "src/task_planner/icons/settings/icons8-settings.svg",
        "User": "src/task_planner/icons/user/user.svg",
    }
    
USER_WINDOW_ICONS = {
        "Login": "src/task_planner/icons/user/log-in.svg",
        "Sign Up": "",
        "Logout": "src/task_planner/icons/user/log-out.svg",
    }

CHECK_MARK_ICONS = {
    "Checked": "src/task_planner/icons/check_box/icons8-check-mark-checked.svg",
    "Unchecked": "src/task_planner/icons/check_box/icons8-check-mark-unchecked.svg",
}

IMPORTANT_ICONS = {
    "Filled": "src/task_planner/icons/star/filled-star.svg",
    "Outline": "src/task_planner/icons/star/star.svg",
}
    