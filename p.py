import os
from dotenv import load_dotenv
load_dotenv()
user= os.getenv('PRUEBA')

print(f"Esta es la clave {user}")