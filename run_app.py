import os
import sys
import subprocess


def main():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))

    app_path = os.path.join(base_path, 'app.py')

    cmd = [
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.headless=true",
        "--global.developmentMode=false"
    ]

    subprocess.Popen(cmd)


if __name__ == "__main__":
    main()