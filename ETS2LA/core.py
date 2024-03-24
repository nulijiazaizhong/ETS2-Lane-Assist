import time
import ETS2LA.networking.webserver as webserver
import ETS2LA.backend.backend as backend
from ETS2LA.utils.logging import *

# Initialize the backend
logger = SetupGlobalLogging()
webserver.run() # External webserver for the UI

# This is how we temporarily enable plugins
backend.AddPluginRunner("ScreenCapture")
backend.AddPluginRunner("ShowImage")

logging.info("ETS2LA backend has been started successfully.")

while True:
    # Print the FPS values
    time.sleep(1)
    fpsString = "Plugins are running at: \n"
    for frameTime in backend.frameTimes:
        frametime = backend.frameTimes[frameTime]['frametime']*1000
        execTime = backend.frameTimes[frameTime]['executiontime']*1000
        fpsString += f"{frameTime}: {round(1 / (frametime/1000),2)} FPS\n (Execution time: {round(execTime,2)}ms / {round(frametime,2)}ms)\n"
    logging.info(fpsString)
    pass
    