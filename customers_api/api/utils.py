import asyncio
from functools import wraps
from urllib.request import urlopen

from aiohttp import ClientResponseError


def retry(*exceptions, retries=3, cooldown=1, verbose=True):
    """
    Decorate an async function to execute it a few times before giving up.
    Hopes that problem is resolved by another side shortly.

    Args:
        exceptions (Tuple[Exception]) : The exceptions expected during function execution
        retries (int): Number of retries of function execution.
        cooldown (int): Seconds to wait before retry.
        verbose (bool): Specifies if we should log about not successful attempts.
    """

    def wrap(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            retries_count = 0

            while True:
                try:
                    result = await func(*args, **kwargs)
                except exceptions as err:
                    retries_count += 1

                    if retries_count > retries:
                        raise RetryExhaustedError(
                            func.__qualname__, args, kwargs) from err

                    if cooldown:
                        await asyncio.sleep(cooldown)
                else:
                    return result
        return inner
    return wrap


@retry(ClientResponseError)
async def fetch(url, session):
    async with session.get(url, raise_for_status=True) as response:
        return await response.read()


def check_product_id(product_id):
    response = urlopen(f"http://challenge-api.luizalabs.com/api/product/{product_id}")
    if response.getcode() == 200:
        return True
    return False
