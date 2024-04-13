import os
from pathlib import Path

from dotenv import load_dotenv
env_path = Path('.') / '.env'
load_dotenv(env_path)

DEBUG = os.getenv('DEBUG', False)

if DEBUG:
    print('DEBUG selected. Proceeding with debug mode')
    print(f'TOKEN: {os.getenv("BOT_TOKEN")}')
    from settings_module.development import *
else:
    print('DEBUG NOT selected. Proceeding with production mode')
    from settings_module.production import *
