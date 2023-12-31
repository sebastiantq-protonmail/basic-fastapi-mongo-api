# handle_error
import re
from fastapi import HTTPException, status
from logging import Logger
from app.api.config.exceptions import bugReportsInstance
from app.api.config.env import IS_PRODUCTION, JIRA_PROJECT_ID

from typing import Union, List, Dict
from datetime import date

def is_valid_objectid(oid: str) -> bool:
    """
    Check if the given string is a valid ObjectId (typically for MongoDB).

    Args:
    - oid (str): The string to check.

    Returns:
    - bool: True if string is a valid ObjectId, otherwise False.
    """
    if not oid or not isinstance(oid, str):
        return False
    return bool(re.match(r'^[a-fA-F0-9]{24}$', oid))

def convert_objectid_to_str(data):
    """Convert ObjectId to string in a dictionary or list of dictionaries.
    
    Args:
    - data (Union[dict, List[dict]]): Data containing ObjectId.
    
    Returns:
    - Union[dict, List[dict]]: Data with ObjectId converted to str.
    """
    if isinstance(data, list):
        for item in data:
            item["id"] = str(item["_id"])
            del item["_id"]
    elif isinstance(data, dict):
        data["id"] = str(data["_id"])
        del data["_id"]

    return data

def convert_date_to_str(data: Union[Dict, List[Dict]], key: str) -> Union[Dict, List[Dict]]:
    """Convert datetime.date to string in a dictionary or list of dictionaries based on the provided key.
    
    Args:
    - data (Union[dict, List[dict]]): Data containing datetime.date object.
    - key (str): The key in the dictionary that corresponds to the datetime.date object.

    Returns:
    - Union[dict, List[dict]]: Data with datetime.date converted to str for the provided key.
    """
    
    if isinstance(data, list):
        for item in data:
            if key in item and isinstance(item[key], date):
                item[key] = item[key].strftime('%Y-%m-%d')
    elif isinstance(data, dict):
        if key in data and isinstance(data[key], date):
            data[key] = data[key].strftime('%Y-%m-%d')

    return data

# Centralized error handler
def handle_error(e: Exception, logger: Logger):
    """
    Centralized error handler which logs the error and, if applicable, creates a JIRA bug report.

    Args:
    - e (Exception): The exception to handle.
    - logger (Logger): Logger instance to log the error.

    Raises:
    - HTTPException: With a 500 status code.
    """
    logger.error(f"Error : {str(e)}")
    if int(IS_PRODUCTION) and (not hasattr(e, 'status_code') or (hasattr(e, 'status_code') and e.status_code == 500)): # Handling HTTP and no HTTP exceptions
        logger.info("Creating incidence on JIRA.")
        bugReportsInstance.bugReports(JIRA_PROJECT_ID, "[DEVELOPER]", str(e))
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))