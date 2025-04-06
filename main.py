#read the sqlite database from CloudRecordings.db
import sqlite3
import json
from datetime import datetime, timedelta
import os
from entities import Recording, Folder
from config import get_param
from db_management import get_database_manager
from helpers import sanitize


# Get required configuration parameters
memo_location = get_param("voice_notes_location", required=True)
output_location = get_param("output_location", required=True)

db_path = f'{memo_location}/CloudRecordings.db'

# Create database manager
db_manager = get_database_manager(db_path)

try:
    # Connect to database
    db_manager.connect()
    
    # Get recordings data
    recordings_data, _ = db_manager.get_table_data("ZCLOUDRECORDING")
    recordings = [Recording.from_db_record(record, memo_location) for record in recordings_data]
    
    # Get folders data
    folders_data, _ = db_manager.get_table_data("ZFOLDER")
    folders = [Folder.from_db_record(record) for record in folders_data]
    
finally:
    # Ensure connection is closed
    db_manager.disconnect()

# loop through the recordings copy the file to a new location
for recording in recordings:
    # get the file name
    file_name = recording.filename
    recorded_date = recording.converted_date
    # get the path to the file
    path = recording.path
    if path and not os.path.exists(path):
        print (f'File not found: {file_name}')
        continue
    # get the folder id
    folder_id = recording.folder_id
    # get the folder name
    folder_name = next((folder.name for folder in folders if folder.id == folder_id), None)

    # create the new folder path
    new_folder_path = f'{output_location}/{folder_name}'
    # create the new folder if it doesn't exist
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)

    file_format_date = datetime.fromisoformat(recorded_date).strftime("%Y-%m-%d")
    new_file_name = f'{sanitize(recording.name)} - {sanitize(file_format_date)}.m4a'
    # create the new file path
    new_path = f'{new_folder_path}/{new_file_name}'
    # check if the file exists
    i = 1
    while os.path.exists(new_path):
        # add a number to the end of the file name
        new_file_name = f'{sanitize(recording.name)} - {sanitize(file_format_date)} ({i}).m4a'
        new_path = f'{new_folder_path}/{new_file_name}'
        i += 1
    # copy the file to the new location
    os.system(f'cp "{path}" "{new_path}"')
    # convert the recorded date to the format needed for the date command
    touch_format_date = datetime.fromisoformat(recorded_date).strftime("%Y%m%d%H%M.%S")
    # print the recorded date
    print(f'Moved: {recording.name}')
    # change the date of the file to the recorded date
    os.system(f'touch -t "{touch_format_date}" "{new_path}"')