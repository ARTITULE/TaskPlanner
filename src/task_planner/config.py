from pathlib import Path

Base_URL = "https://introspectional-scalelike-ria.ngrok-free.dev"

DATA_PATH = Path("src/task_planner/data/tasks.json")

Categories = ["None",
              "Important", 
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
        "Sign Up": "src/task_planner/icons/user/user-plus.svg",
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

PASSWORD_ICONS = {
    "Visible": "src/task_planner/icons/user/eye.svg",
    "Hidden": "src/task_planner/icons/user/eye-off.svg",
}

CALENDAR_ICONS = {
    "Previous": "src/task_planner/icons/arrow/arrow-left-circle.svg",
    "Next": "src/task_planner/icons/arrow/arrow-right-circle.svg",
}

THEME_ICONS = {
    "Light": "src/task_planner/icons/settings/theme/sun.svg",
    "Dark": "src/task_planner/icons/settings/theme/moon.svg",
    "Device": "src/task_planner/icons/settings/theme/smartphone.svg",
}

ANIMATIONS = {
    "Check": "src/task_planner/icons/check_box/icons8-check-mark.gif",
    "Star": "src/task_planner/icons/star/icons8-star-gif.gif",
}

WEEK_START_ICONS = {
    "Device": "",
    "Monday": "",
    "Sunday": "",
}
    