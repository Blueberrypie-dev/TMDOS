from pathlib import Path

AppDir = Path(__file__).resolve().parent.parent.parent
SettingsDir = AppDir / "System" / "SetApps"
UsersFile = AppDir / "Settings" / "users.json"