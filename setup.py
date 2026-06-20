import subprocess
import sys
import os
import shutil
from pathlib import Path

def is_venv():
    return (
        hasattr(sys, "real_prefix") or
        (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix)
    )

def setup():
    base_dir = Path(__file__).resolve().parent
    venv_dir = base_dir / "venv"
    
    if venv_dir.exists():
        pyvenv_cfg = venv_dir / "pyvenv.cfg"
        is_valid = False
        if pyvenv_cfg.exists():
            try:
                with open(pyvenv_cfg, "r", encoding="utf-8") as f:
                    if str(venv_dir) in f.read():
                        is_valid = True
            except Exception:
                pass
                
        if not is_valid:
            print("Found broken or moved virtual environment. Removing it to recreate...")
            shutil.rmtree(venv_dir)
            
    if not is_venv():
        if not venv_dir.exists():
            print("Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        
        print("\n⚠️  You are NOT in a virtual environment.")
        if os.name == "nt":
            activate_cmd = ".\\venv\\Scripts\\activate"
        else:
            activate_cmd = "source venv/bin/activate"
            
        print(f"Please activate the virtual environment and run setup again:")
        print(f"  {activate_cmd}")
        print(f"  python setup.py")
        sys.exit(0)

    print("Installing requirements...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)

    print("Installing Playwright browsers...")
    subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)

    print("\n✅ Setup complete! Run 'python main.py' to start MARK XXV.")

if __name__ == "__main__":
    try:
        setup()
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)