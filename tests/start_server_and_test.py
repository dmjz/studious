import subprocess
import psutil
import requests
import time

# def kill_process_and_children(pid):
#     process = psutil.Process(pid)
#     children = process.children(recursive=True)
#     for child in children:
#         child.terminate()
#     gone, alive = psutil.wait_procs(children, timeout=5)
#     for p in alive:
#         p.kill()
#     process.kill()


# Start server and ping until response is good
pServer = subprocess.Popen('start_server.bat')
# time.sleep(1)
# kill_process_and_children(pServer.pid)

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
pTest = subprocess.Popen('run_tests.bat')
testExitCode = pTest.wait()
print(f'Testing finished with exit_Code={ testExitCode }')

# Kill server/test processes
pTest.kill()
pTest.terminate()
pServer.kill()
pServer.terminate()