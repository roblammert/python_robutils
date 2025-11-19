import datetime
import re
from typing import Optional, Union, Tuple

class DateTimeManager:
    """
    A comprehensive utility class for handling various date and time operations, 
    relying only on Python's standard 'datetime' module. Focuses on formatting, 
    arithmetic, conversions (timestamp/ISO), and calendar-based utilities 
    necessary for application development and database work.
    
    Timezone operations are based on fixed UTC offsets rather than named timezones.
    """
    
    # --- STATIC DATA: US TIME ZONES (Fixed UTC Offsets) ---
    # NOTE: These offsets are FIXED and do NOT automatically adjust for Daylight Saving Time (DST).
    # Both Standard Time (ST) and Daylight Time (DT) offsets are provided for convenience.
    US_TIME_OFFSETS = {
        # Pacific Time
        "PST": "-08:00",  # Pacific Standard Time
        "PDT": "-07:00",  # Pacific Daylight Time
        # Mountain Time
        "MST": "-07:00",  # Mountain Standard Time (also used for AZ year-round)
        "MDT": "-06:00",  # Mountain Daylight Time
        # Central Time
        "CST": "-06:00",  # Central Standard Time
        "CDT": "-05:00",  # Central Daylight Time
        # Eastern Time
        "EST": "-05:00",  # Eastern Standard Time
        "EDT": "-04:00",  # Eastern Daylight Time
        # Alaska Time
        "AKST": "-09:00", # Alaska Standard Time
        "AKDT": "-08:00", # Alaska Daylight Time
        # Hawaii Time
        "HST": "-10:00", # Hawaii Standard Time (No DST)
    }

    def __init__(self):
        """
        Initializes the DateTimeManager. The default timezone is set to UTC.
        """
        self.default_tz = datetime.timezone.utc

    @staticmethod
    def _parse_datetime(dt_str: Union[str, datetime.datetime]) -> Optional[datetime.datetime]:
        """
        Internal helper to parse a string into a datetime object.
        Handles common ISO-like formats and returns the object or None on failure.
        """
        if isinstance(dt_str, datetime.datetime):
            return dt_str

        # Common formats to try
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d',
            '%m/%d/%Y %I:%M:%S %p',
            '%m/%d/%Y'
        ]
        for fmt in formats:
            try:
                # Handle cases where microsecond precision is in the string but not format
                if len(dt_str) > len(fmt) and '.' in dt_str:
                    return datetime.datetime.strptime(dt_str.split('.')[0], fmt)
                return datetime.datetime.strptime(dt_str, fmt)
            except ValueError:
                continue
        
        # Fallback for ISO format with Z or standard offset (+HH:MM)
        try:
            return datetime.datetime.fromisoformat(dt_str)
        except ValueError:
            pass

        return None
    
    @staticmethod
    def _parse_offset_str(offset_str: str) -> Optional[datetime.timezone]:
        """
        Converts a UTC offset string (e.g., '+05:30', '-08:00') into a datetime.timezone object.
        """
        match = re.match(r'([+\-])(\d{1,2}):?(\d{2})$', offset_str.strip())
        if not match:
            return None

        sign, hours, minutes = match.groups()
        offset = datetime.timedelta(hours=int(hours), minutes=int(minutes))
        
        if sign == '-':
            offset = -offset
            
        return datetime.timezone(offset)

    def _ensure_aware(self, dt: datetime.datetime) -> datetime.datetime:
        """Helper to ensure a datetime object is timezone aware (defaulting to UTC if naive)."""
        if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
            return dt.replace(tzinfo=self.default_tz)
        return dt

    # --- CORE OPERATIONS ---

    def format_datetime(
        self,
        dt_obj: Union[str, datetime.datetime, None] = None,
        format_spec: str = '%Y-%m-%d %H:%M:%S %Z'
    ) -> str:
        """
        Formats a datetime object or string into a specified string format.
        If no object is provided, formats the current UTC time.
        """
        if dt_obj is None:
            dt = datetime.datetime.now(self.default_tz)
        else:
            dt = self._parse_datetime(dt_obj)
            if dt is None:
                return f"Error: Could not parse datetime object/string: {dt_obj}"
            
            dt = self._ensure_aware(dt)

        return dt.strftime(format_spec)

    def get_time_difference(
        self,
        dt1: Union[str, datetime.datetime],
        dt2: Union[str, datetime.datetime],
        unit: str = 'seconds'
    ) -> Union[int, float, str]:
        """
        Calculates the time difference between two datetime objects/strings.
        """
        parsed_dt1 = self._parse_datetime(dt1)
        parsed_dt2 = self._parse_datetime(dt2)

        if parsed_dt1 is None or parsed_dt2 is None:
            return "Error: Could not parse one or both datetime inputs."

        parsed_dt1 = self._ensure_aware(parsed_dt1)
        parsed_dt2 = self._ensure_aware(parsed_dt2)

        difference = abs(parsed_dt1 - parsed_dt2)

        if unit == 'seconds':
            return difference.total_seconds()
        elif unit == 'minutes':
            return difference.total_seconds() / 60
        elif unit == 'hours':
            return difference.total_seconds() / 3600
        elif unit == 'days':
            return difference.total_seconds() / 86400
        else:
            return "Error: Invalid unit specified. Use 'seconds', 'minutes', 'hours', or 'days'."

    def add_time(
        self,
        dt_obj: Union[str, datetime.datetime],
        **kwargs: Union[int, float]
    ) -> Optional[datetime.datetime]:
        """
        Adds specified time components (e.g., days=5, hours=3) to a datetime object.
        """
        dt = self._parse_datetime(dt_obj)
        if dt is None:
            print(f"Error: Could not parse datetime input: {dt_obj}")
            return None

        try:
            delta = datetime.timedelta(**kwargs)
            return dt + delta
        except TypeError as e:
            print(f"Error: Invalid time delta arguments provided: {e}")
            return None

    def convert_to_offset_timezone(
        self,
        dt_obj: Union[str, datetime.datetime],
        target_offset_str: str
    ) -> Union[datetime.datetime, str]:
        """
        Converts a datetime object/string from its current timezone (or assumed UTC
        if naive) to a new fixed UTC offset timezone.
        """
        dt = self._parse_datetime(dt_obj)
        if dt is None:
            return "Error: Could not parse datetime input."

        target_tz = self._parse_offset_str(target_offset_str)
        if target_tz is None:
            return f"Error: Invalid offset format '{target_offset_str}'. Use format like '+HH:MM' or '-HH:MM'."

        dt = self._ensure_aware(dt)
        converted_dt = dt.astimezone(target_tz)
        return converted_dt
    
    def get_current_time_with_offset(self, offset_str: str) -> Union[datetime.datetime, str]:
        """
        Returns the current time localized to a specified UTC offset.
        """
        target_tz = self._parse_offset_str(offset_str)
        if target_tz is None:
            return f"Error: Invalid offset format '{offset_str}'. Use format like '+HH:MM' or '-HH:MM'."

        return datetime.datetime.now(target_tz)

    # --- EXPANDED UTILITIES ---

    def to_iso_string(self, dt_obj: Union[str, datetime.datetime]) -> Union[str, None]:
        """
        Converts the datetime object to an ISO 8601 formatted string (standard for databases/APIs).
        Example: '2024-11-18T22:30:00+00:00'
        
        :param dt_obj: The datetime object or string.
        :return: The ISO 8601 string, or None on error.
        """
        dt = self._parse_datetime(dt_obj)
        if dt is None:
            print(f"Error: Could not parse datetime input for ISO conversion: {dt_obj}")
            return None
        
        # Ensure aware before conversion to get proper offset in the string
        dt = self._ensure_aware(dt)
        return dt.isoformat()

    def to_timestamp(self, dt_obj: Union[str, datetime.datetime]) -> Union[float, None]:
        """
        Converts the datetime object to a Unix timestamp (seconds since epoch).
        
        :param dt_obj: The datetime object or string.
        :return: The Unix timestamp (float), or None on error.
        """
        dt = self._parse_datetime(dt_obj)
        if dt is None:
            print(f"Error: Could not parse datetime input for timestamp conversion: {dt_obj}")
            return None
        
        # Must be timezone aware for timestamp()
        dt = self._ensure_aware(dt)
        return dt.timestamp()
    
    @staticmethod
    def simplify_time_duration(total_seconds: Union[int, float]) -> str:
        """
        Converts a total number of seconds into a simplified, human-readable string
        showing days, hours, minutes, and seconds. Only includes non-zero units.

        :param total_seconds: The duration in seconds.
        :return: A string like '1 day, 2 hours, 3 minutes, 4 seconds', only including non-zero units.
        """
        if total_seconds is None or total_seconds < 0:
            return "Duration must be a non-negative number."
        
        # Convert to integer seconds
        total_seconds = int(total_seconds)
        
        seconds_in_minute = 60
        seconds_in_hour = 3600
        seconds_in_day = 86400

        # Calculate time components
        days = total_seconds // seconds_in_day
        seconds_remainder = total_seconds % seconds_in_day

        hours = seconds_remainder // seconds_in_hour
        seconds_remainder %= seconds_in_hour

        minutes = seconds_remainder // seconds_in_minute
        seconds = seconds_remainder % seconds_in_minute
        
        # Build the descriptive string
        parts = []
        if days > 0:
            parts.append(f"{days} day{'s' if days > 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
        # Include seconds if > 0 or if the total duration was 0
        if seconds > 0 or not parts: 
            parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
            
        return ", ".join(parts)

    @staticmethod
    def convert_time_units(
        value: Union[int, float], 
        from_unit: str, 
        to_unit: str
    ) -> Union[float, str]:
        """
        Converts a time value from one unit to another.
        Supported units: 'seconds', 'minutes', 'hours', 'days'.

        :param value: The numeric time value.
        :param from_unit: The unit the value is currently in.
        :param to_unit: The unit to convert the value to.
        :return: The converted value as a float, or an error string.
        """
        unit_multipliers = {
            'seconds': 1.0,
            'minutes': 60.0,
            'hours': 3600.0,
            'days': 86400.0
        }
        
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        if from_unit not in unit_multipliers or to_unit not in unit_multipliers:
            return "Error: Invalid unit specified. Supported units: 'seconds', 'minutes', 'hours', 'days'."

        # Convert to seconds first
        seconds = value * unit_multipliers[from_unit]
        
        # Convert from seconds to target unit
        return seconds / unit_multipliers[to_unit]

    def is_weekend(self, dt_obj: Union[str, datetime.datetime]) -> Union[bool, str]:
        """
        Checks if the given date falls on a weekend (Saturday or Sunday).
        """
        dt = self._parse_datetime(dt_obj)
        if dt is None:
            return "Error: Could not parse datetime input."
        
        # weekday() returns 0 (Monday) to 6 (Sunday). Weekend is 5 (Sat) or 6 (Sun).
        return dt.weekday() >= 5

    def get_start_of_day(self, dt_obj: Union[str, datetime.datetime]) -> Union[datetime.datetime, str]:
        """
        Returns a datetime object representing the start of the day (00:00:00).
        """
        dt = self._parse_datetime(dt_obj)
        if dt is None:
            return "Error: Could not parse datetime input."
        
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    def get_end_of_day(self, dt_obj: Union[str, datetime.datetime]) -> Union[datetime.datetime, str]:
        """
        Returns a datetime object representing the very end of the day (23:59:59.999999).
        """
        dt = self._parse_datetime(dt_obj)
        if dt is None:
            return "Error: Could not parse datetime input."
        
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

    def get_day_name(self, dt_obj: Union[str, datetime.datetime]) -> Union[str, None]:
        """
        Gets the full name of the day (e.g., 'Monday').
        """
        dt = self._parse_datetime(dt_obj)
        if dt is None:
            print(f"Error: Could not parse datetime input for day name: {dt_obj}")
            return None

        return dt.strftime('%A')

    def is_future(self, dt_obj: Union[str, datetime.datetime]) -> Union[bool, str]:
        """
        Checks if the given datetime is in the future relative to the current UTC time.
        """
        dt = self._parse_datetime(dt_obj)
        if dt is None:
            return "Error: Could not parse datetime input."
        
        dt = self._ensure_aware(dt)
        now_utc = datetime.datetime.now(self.default_tz)
        
        return dt > now_utc


# Example Usage Demonstration
if __name__ == '__main__':
    dt_manager = DateTimeManager()
    
    print("--- 1. Duration Simplification (NEW FEATURE) ---")
    
    duration1 = 109 # 1 min, 49 sec
    duration2 = 90123 # 1 day, 1 hour, 22 minutes, 3 seconds
    duration3 = 0.5 # should handle floats but treat as 0 seconds
    duration4 = 0

    print(f"{duration1} seconds simplifies to: {dt_manager.simplify_time_duration(duration1)}")
    print(f"{duration2} seconds simplifies to: {dt_manager.simplify_time_duration(duration2)}")
    print(f"{duration3} seconds simplifies to: {dt_manager.simplify_time_duration(duration3)}")
    print(f"{duration4} seconds simplifies to: {dt_manager.simplify_time_duration(duration4)}")


    print("\n--- 2. Time Unit Conversion (Existing) ---")
    seconds_val = 7200 # 2 hours
    print(f"Original value: {seconds_val} seconds")
    minutes_val = dt_manager.convert_time_units(seconds_val, 'seconds', 'minutes')
    hours_val = dt_manager.convert_time_units(seconds_val, 'seconds', 'hours')
    print(f"Converted to minutes: {minutes_val}")
    print(f"Converted to hours: {hours_val}")
    
    print("\n--- 3. US Timezone Offsets (Static Data) ---")
    
    est_offset = dt_manager.US_TIME_OFFSETS.get('EDT')
    utc_time = '2024-12-01 15:00:00'
    
    if est_offset:
        est_time = dt_manager.convert_to_offset_timezone(utc_time, est_offset)
        if isinstance(est_time, datetime.datetime):
            print(f"Time {utc_time} (UTC) converted to EDT ({est_offset}):")
            print(dt_manager.format_datetime(est_time, '%Y-%m-%d %H:%M:%S %Z'))
    
    print("\n--- 4. Calendar and Boundary Calculations (Existing) ---")
    date_to_check = '2024-12-25 10:00:00'
    print(f"Date: {date_to_check} is a {dt_manager.get_day_name(date_to_check)}. Is it a weekend? {dt_manager.is_weekend(date_to_check)}")
    
    start_of_day = dt_manager.get_start_of_day(date_to_check)
    if isinstance(start_of_day, datetime.datetime):
        print(f"Start of Day: {dt_manager.format_datetime(start_of_day, '%Y-%m-%d %H:%M:%S.%f')}")