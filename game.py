# An adaption of Mario Code by Maarten Hus found at http://huscorp.nl/tag/pygame/
import subprocess

# Start both server and client (this game.py file needs to be deprecated at some point)
subprocess.Popen( ["python", "server.py" ] )
subprocess.Popen( ["python", "client.py", "localhost" ] )
