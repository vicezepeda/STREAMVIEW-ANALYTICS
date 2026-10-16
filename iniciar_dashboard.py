"""Abre el dashboard desde su propia carpeta, sin rutas fijas de este equipo."""
import importlib
from pathlib import Path
import subprocess
import sys
import socket

ROOT = Path(__file__).resolve().parent
MODULES = ['streamlit', 'pandas', 'numpy', 'plotly', 'pycountry']

def main():
    if sys.version_info < (3, 11):
        raise SystemExit('Se necesita Python 3.11 o superior.')
    missing = []
    for module in MODULES:
        try:
            imported = importlib.import_module(module)
            if module == 'streamlit' and not hasattr(imported, 'iframe'):
                missing.append('streamlit (se necesita 1.66)')
        except ImportError:
            missing.append(module)
    if missing:
        print('Se instalaran las dependencias del proyecto desde PyPI. Se necesita Internet.', flush=True)
        print('Faltan: ' + ', '.join(missing), flush=True)
        environment = ROOT / '.venv'
        interpreter = environment / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
        if not interpreter.exists():
            subprocess.run([sys.executable, '-m', 'venv', str(environment)], check=True)
        subprocess.run([str(interpreter), '-m', 'pip', 'install', '-r', str(ROOT / 'requirements.txt')], check=True)
    else:
        interpreter = Path(sys.executable)
    port = None
    for candidate in range(8501, 8511):
        try:
            with socket.socket() as probe:
                probe.bind(('127.0.0.1', candidate))
            port = candidate
            break
        except OSError:
            continue
    if port is None:
        raise SystemExit('No hay un puerto disponible entre 8501 y 8510. Cierre una instancia anterior y vuelva a abrir.')
    print('Mantenga esta ventana abierta. Para detener el dashboard: Ctrl+C.', flush=True)
    print(f'Dashboard: http://localhost:{port}', flush=True)
    return subprocess.call([
        str(interpreter), '-m', 'streamlit', 'run', str(ROOT / 'dashboard/dashboard.py'),
        '--server.address', '127.0.0.1', '--server.port', str(port),
        '--server.headless', 'false', '--browser.gatherUsageStats', 'false',
    ], cwd=ROOT)

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError:
        raise SystemExit('No se pudo preparar Python. Compruebe Internet y vuelva a abrir ABRIR_PYTHON.cmd.')
