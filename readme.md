# Voice Notes Backup

A Python utility for macOS that finds, processes, and backs up Voice Memos from Apple's Voice Memos app.

## Description

VoiceNotesBackup searches through your macOS Voice Memos database, processes the recordings, and creates organized backups with meaningful filenames. The program preserves metadata such as recording dates and organizes files based on their original folder structure.

## Features

- Automatically reads from the macOS Voice Memos database
- Preserves original folder structure
- Creates readable filenames with recording dates
- Maintains original file timestamps
- Configurable source and destination locations

## Requirements

- macOS (tested on macOS Monterey and newer)
- Python 3.9+
- Voice Memos app with existing recordings

## Installation

1. Clone or download this repository
2. Ensure Python 3.9+ is installed
3. Copy the `config.json.example` to `config.json` and update the configuration
4. Enable Full Disk Access for Python/Terminal (see instructions below)

## Full Disk Access

Since the program needs to access the Voice Memos database file in a protected location, you'll need to grant Full Disk Access to either:
- The Terminal app (if running the script from Terminal)
- Python.app (if using a Python launcher)
- Your IDE/code editor (if running from an editor like VS Code)

### Enabling Full Disk Access on macOS

1. Open **System Settings** (or **System Preferences** on older macOS versions)
2. Navigate to **Privacy & Security** → **Full Disk Access**
3. Click the lock icon in the bottom left and enter your password
4. Click the **+** button to add an application
5. Browse to and select your application:
   - `/Applications/Utilities/Terminal.app` (for Terminal)
   - `/Applications/Python 3.x/Python Launcher.app` (for Python Launcher)
   - Your IDE application (e.g., Visual Studio Code)
6. Make sure the checkbox next to the added application is **checked**
7. Restart the application for the changes to take effect

Without Full Disk Access, the program won't be able to read the Voice Memos database and will likely fail with a "Permission denied" error.

## Configuration

Edit the `config.json` file to set your source and destination directories:

```json
{
  "voice_notes_location": "/Users/username/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/",
  "output_location": "/Users/username/Documents/Voice Memos Backup/",
}
```

- `voice_notes_location`: The directory where Voice Memos stores recording files
- `output_location`: Where you want backup files to be saved

## Usage

Run the program with:

```bash
python main.py
```

The program will:
1. Read your Voice Memos database
2. Process all recordings and folders
3. Copy recordings to the backup location with organized names
4. Maintain the original timestamps

## File Structure

- `main.py`: Main program entry point
- `config.py`: Handles configuration management
- `db_management.py`: Database interaction module
- `entities.py`: Data model definitions
- `helpers.py`: Utility functions
- `config.json`: User configuration file

## Filename Format

Backed up files will follow this naming convention:
```
[Recording Name] - [YYYY-MM-DD].m4a
```

For example: `Important Meeting - 2025-04-05.m4a`

## Limitations

- Only works with the standard macOS Voice Memos app
- Requires read access to the Voice Memos database and recordings
- Does not handle encrypted recordings

## License

MIT License

## Acknowledgements

- Apple Voice Memos app for the recording functionality
- Python community for the libraries used in this project