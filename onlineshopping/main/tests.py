import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
x=os.path.join(BASE_DIR, '/static')
print(str(BASE_DIR)+'/static/images')
print(x)
