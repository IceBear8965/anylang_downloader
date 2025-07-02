import sys, os

if sys.platform == "win32":
    args = [
        "nuitka",
        "--standalone",
        "--onefile",
        "--msvc=latest",
        "--windows-disable-console",
        "--plugin-enable=pyside6",
        "--include-data-dir=./fonts=fonts",
        "--include-data-files=./images/logo.ico=images/logo.ico"
        "--assume-yes-for-downloads",
        "--show-memory",
        "--show-progress",
        "--windows-icon-from-ico=./images/logo.ico",
        "--windows-file-version=1.0.0",
        '--windows-file-description="Anylang Downloader"',
        "--output-dir=dist",
        "Anylang-Downloader.py"
        ]

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