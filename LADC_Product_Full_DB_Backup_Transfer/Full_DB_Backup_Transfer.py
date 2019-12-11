####modified for local
import os, glob, time, operator
from datetime import date, datetime, timedelta
import shutil


def modification_date(filename):
    t = os.path.getmtime(filename)
    modifiedDate = str(datetime.fromtimestamp(t))
    modifiedDate = modifiedDate[0:4] + '_' + modifiedDate[5:7] + '_' + modifiedDate[11:13]
    return modifiedDate


###245 GB=263066746880 Byte
###500 MB=524288000 Byte
maxFolderSizeCanBeArchived = 263066746880


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.3f %s" % (num, x)
        num /= 1024.0


def GetFileSize(filepath):
    fileSize = os.stat(filepath).st_size
    return fileSize


def getDates():
    days = []
    today = date.today()  ###will be in format YYYY-MM-DD
    for i in range(30):
        day = "day" + str(i)
        day = today - timedelta(days=int(i))
        day = str(day).split('-')
        day = day[0] + '_' + day[1] + '_' + day[2]
        days.append(day)
    return days


def get_oldest_file(files, _invert=False):
    """ Find and return the oldest file of input file names.
    Only one wins tie. Values based on time distance from present.
    Use of `_invert` inverts logic to make this a youngest routine,
    to be used more clearly via `get_youngest_file`.
    """
    gt = operator.lt if _invert else operator.gt
    # Check for empty list.
    if not files:
        return None
    # Raw epoch distance.
    now = time.time()
    # Select first as arbitrary sentinel file, storing name and age.
    oldest = files[0], now - os.path.getctime(files[0])
    # Iterate over all remaining files.
    for f in files[1:]:
        age = now - os.path.getctime(f)
        if gt(age, oldest[1]):
            # Set new oldest.
            oldest = f, age
    # Return just the name of oldest file.
    return oldest[0]


##log path
logPath = "c:\\Full_DB_Archival_History"
if (os.path.exists(logPath) == False):
    os.mkdir(logPath)
##creating log file
now = datetime.now()
log_date = str(now)
filepath = logPath + "\\log_" + log_date[0:11] + '.txt'
fileobject = open(filepath, "a+")
fileobject.close()

#backupPath = r"D:\laxisilon.pftla.local\Clear\ifs\PRODUCTION_BACKUPS\SQLDB\Full_Production_DB_Backup_Products"
backupPath=r"\\laxisilon.pftla.local\Clear\ifs\PRODUCTION_BACKUPS\SQLDB\Full_Production_DB_Backup_Products"

fileobject = open(filepath, "a+")
for roots, dirs, files in os.walk(backupPath):
    for dir in dirs:

        backupPath1 = backupPath + "\\" + dir
        fileSizeMoved = noOfFilesToMove = fileSizeToMoveInByte = startDate = endDate = 0
        filesToMove = []
        days = getDates()
        directoryNameLength = len(dir)
        ###getting the oldest file and its size
        files = glob.glob(backupPath1 + '\\*.bak')
        oldestFile=get_oldest_file(files)

        if (len(files) > 0):
            #moveToTemp1 = r"D:\filesToMoveToTN\\"
            #moveToTemp = r"D:\filesToMoveToTN\\" + dir
            ###Aspera hot folder Path
            moveToTemp1 = r"\\laxisilon.pftla.local\Clear\ifs\PRODUCTION_BACKUPS\LA-To-TN-ProdBackup\SQL DB\\"
            ###creating the sub folder in side aspera hot folder
            moveToTemp = r"\\laxisilon.pftla.local\Clear\ifs\PRODUCTION_BACKUPS\LA-To-TN-ProdBackup\SQL DB\\" + dir
            ###if directory is not available creating the same
            if (os.path.isdir(moveToTemp) == False):
                os.mkdir(moveToTemp)

            ###if individual file sixe gater than 245 GB
            if (GetFileSize(oldestFile) > maxFolderSizeCanBeArchived):
                tempFileName = oldestFile[94 + directoryNameLength::]
                modificationDate = modification_date(oldestFile)

                if (modificationDate not in days):
                    filesToMove.append(oldestFile)
                    fileSizeToMoveInByte += GetFileSize(oldestFile)
                    noOfFilesToMove += 1
                    shutil.move(oldestFile, moveToTemp + "\\" + tempFileName)
                    startFile = filesToMove[0]
                    endFile = filesToMove[len(filesToMove) - 1]
                    finalFoleder = (dir + "_full_backup_" + startFile[94 + (2 * len(dir)) + 9:94 + (
                            2 * len(dir)) + 19] + "_to_" +
                                    endFile[94 + (2 * len(dir)) + 9:94 + (2 * len(dir)) + 19])
                    os.rename(moveToTemp, moveToTemp1 + finalFoleder)
                    message = ("{} dropped on :-{} folder size :-{}\n".format(finalFoleder, str(date.today()),
                                                                              convert_bytes(fileSizeToMoveInByte)))
                    fileobject.write(message)
                else:
                    message = tempFileName + "is not 30 days older\n"
                    fileobject.write(message)

            else:
                ###if month has 31 days max 31 files can be clubbed in 1 folder
                if (
                        "_01_01_" or "_03_01_" or "_05_01_" or "_07_01_" or "_08_01_" or "_10_01_" or "_12_01_" in oldestFile):
                    maxIterate = 31
                ###if month is feb check leap year and decide max number of files can be clubbed in single folder
                elif ("_02_01_" in oldestFile):
                    maxIterate = 28
                    if (int(oldestFile[94 + (2 * len(dir)) + 9:94 + (2 * len(dir)) + 13]) % 4 == 0):
                        maxIterate = 29
                ###if month has 30 days max 30 files can be clubbed in 1 folder
                else:
                    maxIterate = 30

                condition = True
                ###for all the file in the sub folder checking the file
                while condition:
                    files = glob.glob(backupPath1 + '\\*.bak')
                    oldestFile = get_oldest_file(files)
                    modificationDate = modification_date(oldestFile)
                    if (
                            modificationDate not in days and noOfFilesToMove < maxIterate and fileSizeToMoveInByte <= maxFolderSizeCanBeArchived):
                        tempFileName = oldestFile[94 + directoryNameLength::]
                        filesToMove.append(oldestFile)
                        fileSizeToMoveInByte += GetFileSize(oldestFile)
                        noOfFilesToMove += 1
                        shutil.move(oldestFile, moveToTemp + "\\" + tempFileName)

                    else:
                        condition = False
                        break

                if condition == False:
                    if (len(filesToMove) != 0):
                        startFile = filesToMove[0]
                        endFile = filesToMove[len(filesToMove) - 1]
                        finalFoleder = (dir + "_full_backup_" + startFile[94 + (2 * len(dir)) + 9:94 + (
                                2 * len(dir)) + 19] + "_to_" +
                                        endFile[94 + (2 * len(dir)) + 9:94 + (2 * len(dir)) + 19])
                        os.rename(moveToTemp, moveToTemp1 + finalFoleder)
                        message = "{} dropped on :-{} folder size :-{}\n".format(finalFoleder, str(date.today()),
                                                                                 convert_bytes(
                                                                                     fileSizeToMoveInByte))
                        fileobject.write(message)

message = "-----------------------------------------------------------------------------------------------------------------------\n"
fileobject.write(message)
fileobject.close()
