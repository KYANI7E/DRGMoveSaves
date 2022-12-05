import os
import json
import sys
import subprocess

def getNumberShit(path):
    out = os.listdir(path)

    plasav = ''
    for i in out:
        temp = i
        if not 'container' in temp:
            plasav = temp
        
    return plasav

#choice should be either 'BackupsMicro\\' or 'BackupsSteam\\'
#homeLocation should end with \\
def backUp(homeLocation, choice):
    configPath = "/".join(sys.argv[0].split("/")[:-1])
    with open(configPath + '\\config.json', 'r') as myfile:
        data=myfile.read()
    config = json.loads(data)

    amount = config['amountBackUps'] -1
    out = os.listdir(homeLocation + choice)
    
    oo = []
    for i in out:
        temp = i
        oo.append(temp)

    for i,j in reversed(list(enumerate(oo))):
        n = int(j.replace('backup', ''))
        if n > amount:
            for k,l in reversed(list(enumerate(oo))):
                num = int(l.replace('backup', ''))
                if num > amount:
                    os.remove(homeLocation + choice + 'backup' + str(num))
            continue
        os.rename(homeLocation + choice + j, homeLocation + choice + 'backup' + str(n+1))


def steam_to_micro():
    configPath = "/".join(sys.argv[0].split("/")[:-1])
    with open(configPath + '\\config.json', 'r') as myfile:
        data=myfile.read()
    config = json.loads(data)

    microPath = config['microPath']
    steamPath = config['steamPathFile']
    homePath = config['homeLocation']


    plasav = getNumberShit(microPath)

    backUp(homePath, 'BackupsMicro/')

    cmd = 'powershell mv \'' + microPath + plasav +'\' \'' + homePath + 'BackupsMicro\\backup0\''
    subprocess.run(cmd, shell=True)
    cmd = 'powershell cp \''+ steamPath + '\' \'' + microPath + plasav + '\''
    subprocess.run(cmd, shell=True)

def mirco_to_steam():
    configPath = "/".join(sys.argv[0].split("/")[:-1])
    with open(configPath + '\\config.json', 'r') as myfile:
        data=myfile.read()
    config = json.loads(data)

    microPath = config['microPath']
    steamPath = config['steamPathFile']
    homePath = config['homeLocation']


    plasav = getNumberShit(microPath)

    backUp(homePath, 'BackupsSteam/')

    cmd = 'powershell mv \'' + steamPath +'\' \'' + homePath + 'BackupsSteam\\backup0\''
    subprocess.run(cmd, shell=True)
    cmd = 'powershell cp \''+  microPath + plasav + '\' \'' + steamPath + '\''
    subprocess.run(cmd, shell=True)

def transferSaveFile():
    try:
        version = sys.argv[1]
    except:
        version = None
    configPath = "/".join(sys.argv[0].split("/")[:-1])

    with open(configPath + '\config.json', 'r') as myfile:
        data=myfile.read()
    config = json.loads(data)

    microPath = config['microPath']
    steamPath = config['steamPathFile']

    plasav = getNumberShit(microPath)

    lastMicro = os.path.getmtime(microPath + plasav)
    lastSteam = os.path.getmtime(steamPath)
    if lastSteam > lastMicro and version != 'steam':
        input("TRANSFERING STEAM SAVE TO XBOX... press Enter to continue...")
        steam_to_micro()
    elif lastMicro > lastSteam and version != 'micro':
        input("TRANSFERING XBOX SAVE TO STEAM... press Enter to continue...")
        mirco_to_steam()
    elif lastMicro == lastSteam:
        input("THE SAVE FILES ARE THE SAME... press Enter to do nothing...")
    elif lastMicro < lastSteam and version == 'steam':
        input("steam save is more current than xbox save, press Enter to do nothing...")
    elif lastSteam < lastMicro and version == 'micro':
        input("xbox save is more current than steam save, press Enter to do nothing...")

if __name__ == "__main__":
    try:
        configPath = "/".join(sys.argv[0].split("/")[:-1])
        with open(configPath + '\config.json', 'r') as myfile:
            data=myfile.read()
        config = json.loads(data)

        steamStart = config['steamLink']
        microStart = config['xboxExe']

        transferSaveFile()
        try:
            if sys.argv[1] == "steam":            
                input("press Enter to start up STEAM DRG...")
                cmd = 'powershell start-process ' + steamStart
                subprocess.run(cmd, shell=True)
            elif sys.argv[1] == "micro":
                input("press Enter to start up MIRCOSOFT DRG...")
                cmd = 'powershell start-process ' + microStart
                subprocess.run(cmd, shell=True)
        except: 
            input("will not start up game because no secondary argument, press enter to exit...")

    except Exception as e:
        print(e)
        input("ERROROROROROR ABOVE^^^^^^^^^^^^^^^^^^...press enter")