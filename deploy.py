import sys, os

if sys.platform == "win32":
    args = []

elif sys.platform == "darwin":
    args = [
        'python3 -m nuitka',
        '--standalone',
        '--plugin-enable=pyside6',
        "--include-data-dir=./fonts=fonts",
        "--macos-create-app-bundle",
        "--macos-app-name=Anylang-Downloader",
        "--macos-app-icon=./images/logo.icns",
        "--macos-app-version=1.0.0",
        "--macos-disable-console",
        '--output-dir=dist',
        '--show-memory',
        "--show-progress",
        "Anylang-Downloader.py"
        ]

else:
    args = ["pyinstaller", "-w", "Anylang-Downloader.py"]

os.system(" ".join(args))