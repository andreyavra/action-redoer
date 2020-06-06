import os, shutil

STORING_DIR = "./logger_scripts/"

def deleteScript(file_path):
    os.remove(file_path)
    try:
        os.rmdir(STORING_DIR)
    except:
        pass

def deleteAll():
    shutil.rmtree(STORING_DIR)

def getFileName():
    return input("What sequence do you want to delete (without the .vfd)? ").replace(' ','_') + '.vfd'

def main():
    if not os.path.exists(STORING_DIR):
        print("You have not created any sequences. This program is for deleting scripts.")
        return

    print("Note: if you want to delete all sequences, type: DEL_ALL")
    file_name = getFileName()
    if file_name == "DEL_ALL":
        deleteAll()
        return

    file_path = STORING_DIR + file_name

    while not os.path.exists(file_path):
        print("File name invalid. Trying again.")
        file_name = getFileName()
        file_path = STORING_DIR + file_name
    
    deleteScript(file_path)

if __name__ == "__main__":
    main()

    

    