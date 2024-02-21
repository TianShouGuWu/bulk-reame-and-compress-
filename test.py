from ctypes.wintypes import HACCEL
import os
import shutil
import tkinter as tk
from tkinter import filedialog
import math


# 1 processing a lot of artistCG use for _Notest and _text version , need separate first
ARTISTCG_FILE_HAVE_FOLDERNAME = True
# exp 
# inputfolder/artistCG folder 1-n/_text
#                               -/_Notest
# 2 make all folder in dir to rar
# 3 processing AI generator photo to separeate folder
# 4 rename all fodler subfile
HAVE_FOLDER_NAME = True
#   if true
#   exp fodername/..... to fodername/fodername_number
MOVE_LAST_TO_FIRST = True # not work or no code
#   if false
#   exp fodername/..... to fodername/number

WORKING_MODE = 2 # working mode


RECOVER_RATE = 10
TEXTED = "_Text"
NOT_TEXTED = "_No-Text"
DOUBLE_QUOTES = '\"'
RAR_CORE_PATH = DOUBLE_QUOTES +str(os.path.abspath("C:\Program Files\WinRAR\Rar.exe"))+ DOUBLE_QUOTES
RAR_EXT = ".rar"
COMPRESSIOM_RATIO = "-m5"
LOG = "log.txt"
CD = "cd /d"

def makeRar (targetDir, recoverRate):
    if not os.path.isabs(targetDir):
        exit("not abs direcectory")
    
    rootDir,targetFileName = os.path.split(os.path.abspath(targetDir))
    moveCommand = DOUBLE_QUOTES + CD+" " +str(rootDir) + DOUBLE_QUOTES

    moveCommand = CD+" " +str(rootDir)

    # print("CMD creative RAR working command")
    # print("first operation "+ moveCommand)
  


    compressCommand = RAR_CORE_PATH +" " + COMPRESSIOM_RATIO + " a "
    compressCommand += DOUBLE_QUOTES + targetFileName + DOUBLE_QUOTES+" "
    #compressCommand += "* " + DOUBLE_QUOTES + targetFileName + DOUBLE_QUOTES 
    compressCommand += DOUBLE_QUOTES + targetFileName + DOUBLE_QUOTES 

    # print("second operation " + compressCommand)

    addRecovery = RAR_CORE_PATH + " rr"+ str(recoverRate) + "p " + DOUBLE_QUOTES+targetFileName + DOUBLE_QUOTES

    # print("third operation " + addRecovery)
    cmd = moveCommand + " && " + compressCommand + " && " + addRecovery
    # print()
    # print("total operation "+ cmd)
    os.system(cmd)

# rename all file in a folder
def renameFileInFolder(dir:str, log, FileHaveFolderName : bool):

    # if total number of file in a folder, rename it without parent folder
    # else with parent folder
    NUM_FILE_TAR = 90

    fileList = os.listdir(dir)
    fileList.sort()
    for name in fileList:
            print(name)
    print("total: " + str(len(fileList)))
    print()

    numberOfFile = len(fileList)
    pad =2 +  int(math.log10(numberOfFile))

    restPath, foldername = os.path.split(dir)

    curr = 0
    for filename in fileList:
        curr +=1
        oldFilePath = os.path.join(dir, filename)
        name,extension = os.path.splitext(filename)

        fileNumber = str(curr)
        fileNumber=fileNumber.zfill(pad)


        newFileName = ""
        if not FileHaveFolderName:
            newFileName =  "_" +fileNumber+extension
        else :
            newFileName =foldername + "_" +fileNumber+extension
        newFilePath = os.path.join(dir,newFileName)

        processOutput = filename + " -----to----> "+ newFileName

        print(processOutput)
        if log != None:
            print(processOutput, file= log)
        os.rename(oldFilePath,newFilePath)

# rename for a airtist cg folder 
def renameAndMakeRAR(dir,log,needRenameWithFolder:bool):

    if not os.path.isabs(dir):
        exit("not abs workingDir")

    root, baseFolderName = os.path.split(dir)

    floderList = os.listdir(dir)
    for foldername in floderList:
        folderPath = os.path.join(dir,foldername)
        if os.path.isdir(folderPath):
            newFolderName = baseFolderName+foldername
            newFolderPath = os.path.join(dir,newFolderName)
            os.rename(folderPath,newFolderPath)
            fileList = os.listdir(newFolderPath)
            fileList.sort()

            print(newFolderName)
            if log != None:
                log.write("\n-------------------------------------------------------------------------------------------------\n\nfolder : ")
                print(newFolderName, file= log)


            renameFileInFolder(newFolderPath,log,needRenameWithFolder) # rename file
            curr = len(fileList)
            print("total: " + str(curr))
            if log != None:
                print("total: " + str(curr), file= log)

            print()
            
            makeRar(newFolderPath,RECOVER_RATE)

            


def processAllArtistCG(dir,log):

    if not os.path.isabs(dir):
        exit("not abs workingDir")

    folderList = os.listdir(dir)
    for folder in folderList:
        folderPath = os.path.join(dir,folder)
        if os.path.isdir(folderPath):
            renameAndMakeRAR(folderPath,log , ARTISTCG_FILE_HAVE_FOLDERNAME)
        



def moveRARto (workingDir):

    if not os.path.isabs(workingDir):
        exit("not abs workingDir")

    fileList = os.listdir(workingDir)

    #build folder for copy
    testedRARFolderPath = os.path.join(workingDir,TEXTED)
    notestedRARFolderPath = os.path.join(workingDir,NOT_TEXTED)
    if not os.path.exists(testedRARFolderPath):
       os.mkdir(testedRARFolderPath)
    if not os.path.exists(notestedRARFolderPath):
        os.mkdir(notestedRARFolderPath)

    totalRARMoved = 0
    for foldername in fileList:

        folderPath = os.path.join(workingDir,foldername)
        print(folderPath)
        if os.path.isdir(folderPath):
            folderFileList = os.listdir(folderPath)
            print(folderFileList)

            #find rar
            for rarFileName in folderFileList:
                rarFilePath = os.path.join(folderPath,rarFileName)
                extsion = os.path.splitext(rarFileName) # extsion at second pos
                extsion = extsion[1]
                if os.path.isfile(rarFilePath) and extsion == ".rar":

                    if TEXTED in rarFileName:
                        shutil.copy(rarFilePath,testedRARFolderPath)
                        totalRARMoved+=1
                    if NOT_TEXTED in rarFileName:
                        shutil.copy(rarFilePath,notestedRARFolderPath)
                        totalRARMoved+=1
    print("total moved RAR: " + str(totalRARMoved))
    print("total moved RAR: " + str(totalRARMoved), file= log)

def makeAllsubFoldersToRAR(dir, log):
    folderList = os.listdir(dir)
    printInlog = False
    if log != None:
        printInlog = True
    count =0
    for folder in folderList:
        folderPath = os.path.join(dir,folder)
        if os.path.isdir(folderPath):
            count +=1
            print("Processing folder : " + folder)
            if printInlog:
                print("Processing folder : " + folder, file= log)
            makeRar(folderPath,RECOVER_RATE)
    print("total processing RAR: " + str(count))
    if printInlog:
        print("total processing RAR: " + str(count), file= log)

#process AI generated pack
# need pre process format id_number.ext

def processAIpack(dir):
    filelist = os.listdir(dir)
    filelist.sort()

    log = open(os.path.join(dir,LOG), "a", encoding= 'utf-8')
    count = 0
    folderCount = 0
    for file in filelist:
        count += 1
        nameParts = str(file).split("_")
        newFolderPath = os.path.join(dir,nameParts[0])

        if not os.path.exists(newFolderPath):
            os.mkdir(newFolderPath)
            folderCount +=1
            print("created folder: " + str(nameParts[0]), file= log) 
        
        oldFilePath = os.path.join(dir,file)
        newFilePath = os.path.join(newFolderPath,file)
        shutil.move(oldFilePath,newFilePath)
        # shutil.copy(oldFilePath,newFilePath)
        # os.remove(oldFilePath)
        
    print("total folder Created: " + str(folderCount), file= log)
    print("total folder Created: " + str(folderCount))
    print("total process: " + str(count), file= log)
    print("total process: " + str(count))
    log.close()


def renameAllFolderSubfile(dir):
    log = open(os.path.join(dir,LOG), "a", encoding= 'utf-8')
    folderList = os.listdir(dir)
    for folderName in folderList:
        folderPath = os.path.join(dir,folderName)
        if os.path.isdir(folderPath):
            print("processing filder: " + folderName)
            print("processing filder: " + folderName,file=log)
            renameFileInFolder(folderPath,log,HAVE_FOLDER_NAME)
            print("---------------------------------------------------------")
            print("---------------------------------------------------------",file=log)

    log.close()
        
if __name__ == "__main__":
    
    root = tk.Tk()
    root.withdraw()
    workingDir = filedialog.askdirectory()

    if workingDir == "":
        exit(print("no path select"))
    print(workingDir)
    

    match WORKING_MODE:
        case 1 :
            log = open(os.path.join(workingDir,LOG), "a", encoding= 'utf-8')
            processAllArtistCG(workingDir, log)
            moveRARto(workingDir)
            log.close()
        case 2:
            log = open(os.path.join(workingDir,LOG), "a", encoding= 'utf-8')
            makeAllsubFoldersToRAR(workingDir,log)
            log.close()
        case 3:
            processAIpack(workingDir)
        case 4:
            renameAllFolderSubfile(workingDir)
    
