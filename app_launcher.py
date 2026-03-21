import threading
import webbrowser
import time
import warnings

import waitress
from app import app

def run_server():
    waitress.serve(app, host="127.0.0.1", port=5000)

if __name__ == "__main__":
    def open_browser():
        time.sleep(1)
        webbrowser.open("http://127.0.0.1:5000")

    # Suppress warnings: we use start_requests method in our Spider
    warnings.filterwarnings("ignore")
    threading.Thread(target=open_browser, daemon=True).start()

    print("App running at http://127.0.0.1:5000")
    print("Close this terminal to stop the app.")

    run_server()
    input() # just so the terminal stays open

# Create .exe with `pyinstaller --onedir --name JobPostTokenAnalyzer --add-data ".;." .\app_launcher.py``
