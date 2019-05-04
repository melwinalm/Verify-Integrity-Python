from pathlib import Path
import sqlite3

conn = sqlite3.connect('files.db')
cur = conn.cursor()


print("Opened database successfully")


def FileOperations(fileLocation):
    if cur.execute("SELECT count(*) FROM allfiles WHERE filelocation=?", (fileLocation, )).fetchone()[0] > 0:
        print('Already exists - ' + fileLocation)
    else:
        print('New File - ' + fileLocation)
        cur.execute(
            '''INSERT INTO allfiles (filelocation, hashvalue) VALUES (?, ?)''', (fileLocation, 'text'))
        conn.commit()

def AddExceptionToDatabase(fileLocation, message):
    print('Exception - ' + message)
    cur.execute('''INSERT INTO allfiles (filelocation, hashvalue) VALUES (?, ?)''', (fileLocation, message))
    conn.commit()

def GetFilesAndFolders(base_dir):
    entries = Path(base_dir)
    for entry in entries.iterdir():

        _fileloc = str(entry)
        try:
            if entry.is_dir():
                GetFilesAndFolders(_fileloc)
            else:
                FileOperations(_fileloc)

        except Exception as e:
            AddExceptionToDatabase(_fileloc, str(e))


GetFilesAndFolders('E:/')
