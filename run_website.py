import sys
import os
import subprocess
import time
import webbrowser
import socket
import threading
import signal
from http.server import HTTPServer, SimpleHTTPRequestHandler

def get_process_on_port(port):
    """Finds the PID of the process using the specified port."""
    try:
        cmd = f"lsof -t -i:{port}"
        pid = subprocess.check_output(cmd, shell=True).decode().strip()
        if pid:
            return int(pid.split('\n')[0])
    except subprocess.CalledProcessError:
        return None
    return None

def kill_process_on_port(port):
    """Kills the process using the specified port."""
    pid = get_process_on_port(port)
    if pid:
        print(f"⚠️  Port {port} is in use by PID {pid}. Killing it...")
        try:
            os.kill(pid, signal.SIGKILL)
            time.sleep(1)
            print(f"✅ Port {port} freed.")
        except Exception as e:
            print(f"❌ Failed to kill PID {pid}: {e}")

def run_asset_server():
    kill_process_on_port(8002)
    print("Starting Asset Server (Port 8002)...")
    return subprocess.Popen([sys.executable, 'serve_assets.py'], cwd=os.getcwd())

def run_static_dashboard():
    kill_process_on_port(8000)
    print("Starting Dashboard Landing Page (Port 8000)...")
    # Using subprocess to keep it independent
    return subprocess.Popen([sys.executable, '-m', 'http.server', '8000'], cwd=os.getcwd())

def run_streamlit_app():
    kill_process_on_port(8501)
    print("Starting AI Engine (Port 8501)...")
    
    app_path = os.path.join(os.path.dirname(os.getcwd()), 'skillmap', 'app.py')
    skillmap_dir = os.path.dirname(app_path)
    env = os.environ.copy()
    env['PYTHONPATH'] = skillmap_dir
    
    return subprocess.Popen([sys.executable, '-m', 'streamlit', 'run', app_path, '--server.port', '8501', '--server.headless', 'true'], env=env, cwd=skillmap_dir)

def wait_for_port(port, timeout=10):
    """Wait until a port is open."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                return True
        except (ConnectionRefusedError, socket.timeout):
            time.sleep(0.1)
    return False

def open_browser():
    print("Waiting for Dashboard (8000) and AI Engine (8501) to synchronize...")
    # Wait for both critical ports
    if wait_for_port(8000) and wait_for_port(8501):
        url = 'http://localhost:8000/dashboard.html'
        print(f"🚀 Systems Ready! Opening Command Center: {url}")
        webbrowser.open(url)
    else:
        print("⚠️  Warning: Systems took too long to boot. Opening browser anyway...")
        webbrowser.open('http://localhost:8000/dashboard.html')

if __name__ == '__main__':
    print("\nINITIALIZING SMART TRAFFIC ECOSYSTEM...")
    print("---------------------------------------")
    
    # 1. Asset Server (8002)
    asset_proc = run_asset_server()
    
    # 2. Static Dashboard (8000)
    static_proc = run_static_dashboard()
    
    # 3. AI Streamlit App (8501)
    streamlit_proc = run_streamlit_app()
    
    # 4. Open Browser
    threading.Thread(target=open_browser, daemon=True).start()
    
    print("\n✅ SYSTEM ONLINE. Press Ctrl+C to stop.\n")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping system...")
        if asset_proc: asset_proc.terminate()
        if static_proc: static_proc.terminate()
        if streamlit_proc: streamlit_proc.terminate()
        sys.exit(0)
