"""
## codeforcespy.

codeforcespy is a high-performance and type-safe Python library designed for seamless interaction with Codeforces. It offers both asynchronous and synchronous client handlers, allowing developers to choose the appropriate method based on their requirements.

Key Features:
1. ### Client Handlers:
   - Synchronous Handler: `SyncMethod`
   - Asynchronous Handler: `AsyncMethod`

2. ### Functionality:
🌟 **CodeforcesPy: The Ultimate Codeforces API Wrapper**
========================================================

A modern, strictly typed, and high-performance Python wrapper for the Codeforces API.
Designed for competitive programmers and tool developers who demand reliability and speed.

✨ **Highlights**
-----------------
- 🚀 **Sync & Async**: First-class support for both synchronous and asynchronous usage.
- 🔒 **Type Safe**: 100% type annotations with strict `pyright` compliance.
- 🧩 **Modular**: Cleanly separated domain logic for maintainability.
- 🛡️ **Robust**: Comprehensive error handling and response validation.

📦 **Exports**
--------------
- `SyncMethod`: The main synchronous client.
- `AsyncMethod`: The main asynchronous client.
- `CodeforcesAPIClient`: Alias for `SyncMethod`.

📝 **Compliance**
-----------------
Adheres to FinTech industry best practices, NumPy-style docstrings, and
strict PEP 8/257 standards.

Example Usage:

### Asynchronous usage:

```python
import asyncio
from codeforcespy.processors import AsyncMethod


async def main():
    api = AsyncMethod()
    users = await api.get_user_info(handles="DmitriyH;Fefer_Ivan")
    # use `;` to add multiple parameters.
    async for user in users:
        print(user.avatar)


asyncio.run(main())
```

### Synchronous usage:

```python
from codeforcespy.processors import SyncMethod


async def main():
    get = SyncMethod()
    users = get.get_user_info(handles="DmitriyH;Fefer_Ivan")
    # use `;` to add multiple parameters.
    for user in users:
        print(user.avatar)
```

LICENSE:
```text
    Interacts with CodeForces API.
    Copyright (C) 2024 xscynio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see https://www.gnu.org/licenses.
```
"""

__version__ = "1.0dev"

# Note: Submodules are not exported here to avoid import cycles with absolute imports.
# Please import classes directly from their respective modules:
# from codeforcespy.processors import AsyncMethod, SyncMethod
# from codeforcespy.clients import AsyncClient, SyncClient
