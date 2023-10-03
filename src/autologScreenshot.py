from pyautogui import screenshot
import sys
import os
import time

def help():
    print("Usage:")
    print(f"{os.path.basename(__file__)}")
    print(f"{os.path.basename(__file__)} -h")
    #print(f"{os.path.basename(__file__)} [logDir]")
    print(f"{os.path.basename(__file__)} [logDir] [interval]")
    exit(0)

def checkArgs():
    args = sys.argv
    if "-h" in args:
        help()
    argslen = len(args)
    if argslen > 3:
        print("More then 2 arguments have been detected.")
        print("Make sure your path is enclosed within \" symbols.")
        exit("Exiting...")
    if argslen == 3:
        return getDir(args[1]), getInterval(args[2])
    if argslen == 2:
        print(f"I am sorry I cannot take in only 1 argument just yet. May I advise running:\n{os.path.basename(__file__)} {args[1]} 300")
        exit()
        
    return default()

def default():
    targetPath = os.path.join(os.path.expanduser("~"), 'Pictures', 'autoLogScr')
    return getDir(targetPath), 300
        
def getDir(targetDir: str) -> str:
    targetDir = os.path.join(targetDir, getTime())
    if os.path.isdir(targetDir):
        print("Target directory somehow already exists, if you continue files might be overwritten. \nctrl-c to cancel!")
        time.sleep(3)
        for i in range(5, 0, -1):
            time.sleep(1)
            print(i)
    try:
        os.makedirs(targetDir)
    except OSError:
        print("Something went wrong while creating the directories.\nDying gracefully")
        exit()
    return targetDir

def getTime() -> str:
    curTime = time.localtime(time.time())
    yearmondayhms = [curTime.tm_year, curTime.tm_mon, curTime.tm_mday, curTime.tm_hour, curTime.tm_min, curTime.tm_sec]
    return '-'.join(str(e) for e in yearmondayhms)

def getInterval(interval: str) -> int:
    try:
        interval = interval.upper()
        if interval.endswith('H'):
            print("Warning, you have selected a interval in hours")
            return int(interval.removesuffix('H')) * 3600
        if interval.endswith('M'):
            return int(interval.removesuffix('M')) * 60
        if interval.endswith('S'):
            return int(interval.removesuffix('S'))
        else:
            return int(interval)
    except ValueError:
        print("Something went wrong while trying to convert interval to integer.")
        exit()

def run():
    targetDir, interval = checkArgs()
    timeStart = time.time()
    i = 0
    print(f"target: {targetDir}")
    print(f"interval: {interval}")
    time.sleep(10)
    screenshot().save(os.path.join(targetDir, f"autoScreenshot_{getTime()}.png"))
    try:
        while(True):
            curTime = getTime()
            if i == interval:
                i = 0
                path = os.path.join(targetDir, f"autoScreenshot_{curTime}.png")
                print("Screenshot!")
                screenshot().save(path)
            time.sleep(1)
            i+=1
    except KeyboardInterrupt:
        print("Goodbye!")
        print(f"total time spent: {time.time() - timeStart}")

defaultdir = os.path.join(os.path.expanduser("~"), 'Pictures', 'take.png')
#screenshot().save(defaultdir)
curTime = time.localtime(time.time())


try:
    run()
except KeyboardInterrupt:
    print("Caught KeyboardInterrupt, quitting!")
    exit()