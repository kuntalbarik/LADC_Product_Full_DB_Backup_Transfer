import os
currentBackpath=r"D:\laxisilon.pftla.local\Clear\ifs\PRODUCTION_BACKUPS\SQLDB\Full_Production_DB_Backup_Products"

for roots, dirs, files in os.walk(currentBackpath):
    for dir in dirs:
        print("inside directory{}".format(dir))
        temppath=currentBackpath+"\\"+dir
        for roots,dirs,files in os.walk(temppath):
            for file in files:
                fileName=file.split("_")
                fileName=dir+"_"+fileName[1]+"_"+fileName[2]+"_"+fileName[3]+"_"+fileName[4]+"_"+fileName[5]+"_"+fileName[6]
                os.rename(temppath+"\\"+file,temppath+"\\"+fileName)