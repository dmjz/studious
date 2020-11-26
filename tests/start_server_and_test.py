import subprocess
import psutil
import requests
import time
import sys


serverCommand = 'chdir .. && .\\.venv\\Scripts\\activate.bat && python manage.py runserver'
testCommand = '..\\.venv\\Scripts\\activate.bat && pytest'

# Start server and ping until response is good
pServer = subprocess.Popen(serverCommand, shell=True)
TIMEOUT = 60
start = time.time()
while True:
    try:
        r = requests.get('http://localhost:8000/')
        if r.status_code == 200:
            print('Server is up')
            break
    except:
        if time.time() - start > TIMEOUT:
            raise TimeoutError(f'TIMEOUT={ TIMEOUT }s exceeded for server response')
        time.sleep(1)

# Run tests
pTest = subprocess.Popen(testCommand, shell=True)
testExitCode = pTest.wait()
print(f'Testing finished with exit_Code={ testExitCode }')

# Kill server/test processes
pTest.kill()
pTest.terminate()
pServer.kill()
pServer.terminate()

# Return testing exit code
sys.exit(testExitCode)