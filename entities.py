from datetime import datetime
from typing import Dict, Any, Optional
from zoneinfo import ZoneInfo  # Python 3.9+
from datetime import timedelta
from helpers import sanitize

class Recording:
    """
    Entity class representing a voice recording.
    Handles conversion between database column names and readable property names.
    """
    
    def __init__(self, 
                 filename: str = None, 
                 path: str = None,
                 recorded_date: float = None, 
                 converted_date: str = None,
                 custom_label: str = None, 
                 name: str = None,
                 encrypted_title: str = None, 
                 id: str = None,
                 duration: float = None, 
                 folder_id: int = None,
                 is_test: bool = False):
        
        self.filename = filename
        self.path = path
        self.recorded_date = recorded_date
        self.converted_date = converted_date
        self.custom_label = custom_label
        self.name = name
        self.encrypted_title = encrypted_title
        self.id = id
        self.duration = duration
        self.folder_id = folder_id
        self.raw = None
    
    def __str__(self) -> str:
        """
        Return a string representation of the Recording object.
        Useful for debugging and logging.
        """
        return f"Recording: {self.name or 'Unnamed'} ({self.converted_date or 'No date'})"
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the Recording object.
        Used in debugger output.
        """
        duration_fmt = f"{int(self.duration // 60)}:{int(self.duration % 60):02d}" if self.duration else "Unknown"
        return f"Recording(name='{self.name or 'Unnamed'}', date='{self.converted_date or 'No date'}', duration={duration_fmt}, id='{self.id}')"

    @classmethod
    def from_db_record(cls, record: Dict[str, Any], memo_location: str) -> 'Recording':
        """
        Create a Recording object from a database record dictionary.
        
        Args:
            record: Dictionary containing database column values
            memo_location: Base path for voice memo files
            
        Returns:
            Recording: A new Recording object
        """
        recording = cls()
        recording.filename = record.get("ZPATH")
        recording.path = f'{memo_location}/{record.get("ZPATH")}' if record.get("ZPATH") else None
        recording.recorded_date = record.get("ZDATE")
        recording.converted_date = cls._convert_custom_timestamp_to_et(record.get("ZDATE")) if record.get("ZDATE") else None
        recording.custom_label = record.get("ZCUSTOMLABEL")
        recording.name = record.get("ZCUSTOMLABELFORSORTING")
        recording.encrypted_title = record.get("ZENCRYPTEDTITLE")
        recording.id = record.get("ZUNIQUEID")
        recording.duration = record.get("ZDURATION")
        recording.folder_id = record.get("ZFOLDER")
        recording.raw = record
        
        return recording

    @staticmethod
    def _convert_custom_timestamp_to_et(custom_seconds: float) -> str:
        """
        Convert a custom timestamp to Eastern Time ISO format.
        
        Args:
            custom_seconds: Seconds since custom epoch (2000-12-31T00:00:00Z)
            
        Returns:
            str: Eastern Time date in ISO format
        """
        # Custom epoch: 2000-12-31T00:00:00Z
        custom_epoch = datetime(2000, 12, 31, tzinfo=ZoneInfo("UTC"))
        
        # Add the custom timestamp seconds to the epoch
        utc_time = custom_epoch + timedelta(seconds=custom_seconds)
        
        # Convert to Eastern Time (with DST handled automatically)
        eastern_time = utc_time.astimezone(ZoneInfo("America/New_York"))
        
        # Return in ISO format with timezone
        return eastern_time.isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the Recording object to a dictionary."""
        return {
            "filename": self.filename,
            "path": self.path,
            "recorded_date": self.recorded_date,
            "converted_date": self.converted_date,
            "custom_label": self.custom_label,
            "name": self.name,
            "encrypted_title": self.encrypted_title,
            "id": self.id,
            "duration": self.duration,
            "folder_id": self.folder_id,
            "is_test": self.is_test,
            "raw": self.raw
        }


class Folder:
    """
    Entity class representing a folder that contains recordings.
    Handles conversion between database column names and readable property names.
    """
    
    def __init__(self, id: int = None, name: str = None):
        self.id = id
        self.name = name
        self.raw = None
    
    def __str__(self) -> str:
        """
        Return a string representation of the Folder object.
        Useful for debugging and logging.
        """
        return f"Folder: {self.name or 'Unnamed'} (ID: {self.id})"
    
    def __repr__(self) -> str:
        """
        Return a detailed string representation of the Folder object.
        Used in debugger output.
        """
        return f"Folder(id={self.id}, name='{self.name or 'Unnamed'}')"
    
    @classmethod
    def from_db_record(cls, record: Dict[str, Any]) -> 'Folder':
        """
        Create a Folder object from a database record dictionary.
        
        Args:
            record: Dictionary containing database column values
            
        Returns:
            Folder: A new Folder object
        """
        folder = cls()
        folder.id = record.get("Z_PK")
        folder.name = record.get("ZENCRYPTEDNAME")
        folder.raw = record
        
        return folder
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the Folder object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "raw": self.raw
        }