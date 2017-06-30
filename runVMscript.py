import time
import os
import subprocess
import re
import argparse


testTimerVal = 20

""""Regular expression for parse VM status"""
regex = re.compile(r'^Value:\s*(?P<value>\d+)\s*$')

parser = argparse.ArgumentParser(
    description='Test VM starter script'
)

parser.add_argument(
    '--vm-name',
    dest='vmName',
    type=str,
    help='VBox virtual machine name'
)

parser.add_argument(
    '--user-name',
    dest='userName',
    type=str,
    help='VM OS user name'
)

parser.add_argument(
    '--test-file-name',
    dest='testFileName',
    type=str,
    help='Executing test name'
)


args = parser.parse_args()
if isinstance(args, argparse.Namespace):
    __vmName__ = args.vmName
    __userName__ = args.userName
    __testFileName__ = args.testFileName


def timeOut(sleepTime):
    time.sleep(sleepTime)

def runСommand(cmd):
    """given shell command, returns communication tuple of stdout and stderr"""
    return subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            stdin=subprocess.PIPE).communicate()

""""Process executing"""
def progress_executing():
    count = 10
    sleeptime = 1
    while count <= 100:
        print('{}%...'.format(count), sep=' ', end='', flush=True)
        timeOut(sleeptime)
        count = count + 10

def printSuccessMess(messtext):
    print(messtext)


def printFailedMess(messtext):
    print(messtext)

try:
    os.system('VBoxManage startvm {machineName}'.format(machineName=__vmName__))
except BaseException as err:
    printFailedMess('Failed starting VM')
    print(err)







if __name__ == '__main__':
    loadStatus = False
    while loadStatus != True:
        tryCount = 0
        checkStatus = 0

        res = runСommand('VBoxManage guestproperty get "{machineName}" "/VirtualBox/GuestInfo/OS/LoggedInUsers"'.format(machineName=__vmName__))

        try:
            pauseState = runСommand('VBoxManage controlvm {machineName} resume'.format(machineName=__vmName__))
        except BaseException as err:
            printFailedMess('Cant execute resume command')
            exit(2)

        timeOut(1)
        print('.*.', sep=' ', end='', flush=True)

        try:
            match = regex.match(res[0].decode('utf-8'))
            if match is None:
                raise ValueError('Wait for loading...')
            checkStatus = int(match.groupdict().get('value'), 10)

        except ValueError:
            tryCount += 1
            timeOut(20)
        if tryCount >= 20:
            printFailedMess(' VM  Loading Failed .....')
            exit(3)
            break

        if int(checkStatus) == 1:
            printSuccessMess('VM OS already Loaded')
            loadStatus = True
            timeOut(20)
            break

    '''
        Копіювання тестового файлу з C:\\Python_test_dir\\{testFileName} 
        до тестової директорії C:\\Test\\ на віртуальній машині
    '''
    try:
        printSuccessMess('Copy source files ...')
        os.system('vboxmanage guestcontrol {machineName} --username {userName} copyto --target-directory '
                  '"C:\\Test" "C:\\Python_test_dir\\{testFileName}"'.
                  format(machineName=__vmName__, userName=__userName__, testFileName=__testFileName__))

        os.system('vboxmanage guestcontrol {machineName} --username {userName} copyto --recursive --target-directory \
                  C:\\Test C:\\Python_test_dir\\PDFRedirect\\'.
                  format(machineName=__vmName__, userName=__userName__, testFileName=__testFileName__))
        printSuccessMess('Copying files done ...')
    except BaseException as err:
        printFailedMess('Failed copying to VM...!')
        print(err)
        exit(5)


    try:
        printSuccessMess('Run testing')
        '''
        Розблокування сесіївіртуальної машини
        '''
        os.system('vboxmanage guestcontrol {machineName} --username {userName} run --profile -- '
                  '"C:\\Program Files (x86)\\Python36-32\\python.exe" C:\\Test\\{testName}'.
                  format(machineName=__vmName__, userName=__userName__, testName=__testFileName__))
        printSuccessMess('Test executing done ...')
    except BaseException as err:
        printFailedMess('Test executing failed !')
        print(err)
        exit(4)

    '''
        Видалення тестового файлу з  C:\\Test\\ на віртуальній машині
    '''
    try:
        printSuccessMess('Deleting test file ...')
        os.system('vboxmanage guestcontrol {machineName} --username {userName} run --profile --exe C:\\cleanTemp.bat'.
                  format(machineName=__vmName__, userName=__userName__))
        timeOut(3)
        os.system('vboxmanage guestcontrol {machineName} --username {userName} stat "C:\\Test\\{testFileName}"'.
                  format(machineName=__vmName__, userName=__userName__, testFileName=__testFileName__))
        printSuccessMess('All files are deleted ...')
    except BaseException as err:
        printFailedMess('Failed deleting of the test file...!')
        print(err)
        exit(5)

    '''
        Вимкнення віртуальної машини з таймаутом в 3 секунди
    '''
    printSuccessMess('VM ShutDown')
    try:
        os.system('vboxmanage guestcontrol {machineName} --username {userName} run --profile -- '
                  'C:\\Windows\\System32\\shutdown.exe -s -t 3 -c "Bye bye!" -f -d p:0:0'.
                  format(machineName=__vmName__, userName=__userName__))
        timeOut(20)
        progress_executing()
    except BaseException as err:
        printFailedMess('Shutdown VM error!!!')
        print(err)
        exit(5)




