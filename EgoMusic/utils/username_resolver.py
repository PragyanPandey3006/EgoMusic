"""
Utility functions for resolving usernames to chat IDs
"""

from EgoMusic import app
from EgoMusic.logging import LOGGER


async def resolve_username_to_id(username_or_id):
    """
    Resolve a username or return the ID if it's already an ID
    
    Args:
        username_or_id: Either a username (@channel) or chat ID (-1001234567890)
        
    Returns:
        int: The resolved chat ID
        
    Raises:
        Exception: If username cannot be resolved
    """
    if isinstance(username_or_id, int):
        return username_or_id
    
    if isinstance(username_or_id, str):
        if username_or_id.startswith('@'):
            try:
                chat = await app.get_chat(username_or_id)
                LOGGER(__name__).info(f"Resolved username {username_or_id} to ID: {chat.id}")
                return chat.id
            except Exception as ex:
                LOGGER(__name__).error(f"Failed to resolve username {username_or_id}: {ex}")
                raise ex
        else:
            # Try to convert string ID to int
            try:
                return int(username_or_id)
            except ValueError:
                raise ValueError(f"Invalid chat ID format: {username_or_id}")
    
    raise ValueError(f"Invalid username_or_id type: {type(username_or_id)}")
