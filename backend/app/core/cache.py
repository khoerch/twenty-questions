from datetime import datetime
from typing import Dict, Any, Callable, Awaitable, TypeVar, Optional
import functools
import logging

T = TypeVar('T')

# Global cache storage
caches: Dict[str, Dict[str, Any]] = {}

logger = logging.getLogger(__name__)

def ttl_cache(namespace: str = "default", maxsize: int = 128, ttl_seconds: int = 86400):
    """
    Time-based LRU cache decorator with TTL.
    
    Args:
        namespace: Cache namespace to group related cached items
        maxsize: Maximum size of the cache
        ttl_seconds: Time to live in seconds
    """
    def wrapper(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        # Create a namespace-specific cache if it doesn't exist
        if namespace not in caches:
            caches[namespace] = {}
        
        cache = caches[namespace]
        
        @functools.wraps(func)
        async def wrapped(*args: Any, **kwargs: Any) -> T:
            # Create a key from the function arguments
            key_parts = [str(arg) for arg in args]
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            key = ",".join(key_parts)
            
            # Check if key exists and is still valid
            now = datetime.now()
            if key in cache and (now - cache[key][1]).total_seconds() < ttl_seconds:
                # Update access time for LRU behavior
                cache[key] = (cache[key][0], cache[key][1], now)
                logger.debug(f"Cache hit for {namespace}:{key}")
                return cache[key][0]
            
            # Call the function and cache the result
            result = await func(*args, **kwargs)
            
            # If cache is full, remove the least recently used item
            if len(cache) >= maxsize:
                # Find least recently used item (by access time)
                lru_key = min(cache.keys(), key=lambda k: cache[k][2] if len(cache[k]) > 2 else cache[k][1])
                del cache[lru_key]
                logger.debug(f"Cache full, removed LRU item {namespace}:{lru_key}")
                
            cache[key] = (result, now, now)
            logger.debug(f"Cached result for {namespace}:{key}")
            return result
            
        return wrapped
    return wrapper

def reset_cache(namespace: Optional[str] = None) -> str:
    """
    Reset cache for a specific namespace or all caches.
    
    Args:
        namespace: Specific namespace to clear, or None to clear all caches
    
    Returns:
        Message indicating what was cleared
    """
    if namespace:
        if namespace in caches:
            caches[namespace].clear()
            logger.info(f"Cache for namespace '{namespace}' has been cleared")
            return f"Cache for namespace '{namespace}' has been cleared"
        logger.warning(f"Namespace '{namespace}' not found")
        return f"Namespace '{namespace}' not found"
    else:
        caches.clear()
        logger.info("All caches have been cleared")
        return "All caches have been cleared"

def reset_all_caches() -> None:
    """Reset all caches."""
    caches.clear()
    logger.info("All caches have been cleared") 