import os
import sys

# Add the src directory to the path so it can find app.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import streamlit.web.cli as stcli

def handler(request):
    # This points to your existing app.py file
    sys.argv = ["streamlit", "run", "src/app.py", "--server.port", "8080"]
    stcli.main()
