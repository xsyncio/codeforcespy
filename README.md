# codeforcespy

**Faster | Better | Type-Safe**

## Overview

**codeforcespy** is a high-performance, type-safe Python library that simplifies interacting with the Codeforces API. It provides both synchronous and asynchronous client handlers to suit different application needs, ensuring that your code remains efficient, reliable, and fully type-checked.

Built entirely based on the official [Codeforces API Documentation](https://codeforces.com/apiHelp/), codeforcespy adheres to industry best practices, offering a consistent API surface regardless of your chosen client mode.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
  - [Asynchronous Usage](#asynchronous-usage)
  - [Synchronous Usage](#synchronous-usage)
- [Customization and Advanced Usage](#customization-and-advanced-usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Dual Client Handlers:**  
  Choose between a synchronous handler (`SyncMethod`) or an asynchronous handler (`AsyncMethod`) based on your application requirements.

- **Type-Safe:**  
  Leverages static type checking to ensure reliable and maintainable code.

- **Authentication Support:**  
  Easily enable authentication by passing the `enable_auth` parameter to the client constructor to access user-specific endpoints.

- **Modular and Extensible:**  
  Customize types using the provided `abc` module for a tailored experience.

- **Optimized Serialization:**  
  Utilizes [msgspec](https://github.com/jcrist/msgspec) for fast data validation and serialization.

- **Code Quality:**  
  Enforced by [ruff](https://github.com/astral-sh/ruff) for consistent formatting and adherence to best practices.

## Installation

### As a User

Install codeforcespy via pip:

```sh
pip install codeforcespy
```

### As a Developer

For development, install with the extra dependencies:

```sh
pip install codeforcespy[dev]
```

## Quick Start

### Asynchronous Usage

Below is a basic example demonstrating how to retrieve user information asynchronously:

```python
import asyncio
import codeforcespy

async def main():
    # Initialize the asynchronous client
    api = codeforcespy.AsyncMethod()
    
    # Retrieve user information for multiple handles separated by semicolons
    users = await api.get_user(handles="DmitriyH;Fefer_Ivan")
    
    # Process and print the avatar for each user
    for user in users:
        print(user.avatar)

    # Close the client connection
    await api.close()

asyncio.run(main())
```

### Synchronous Usage

The synchronous client offers similar functionality:

```python
import codeforcespy

def main():
    # Initialize the synchronous client
    api = codeforcespy.SyncMethod()
    
    # Retrieve user information for multiple handles separated by semicolons
    users = api.get_user(handles="DmitriyH;Fefer_Ivan")
    
    # Process and print the avatar for each user
    for user in users:
        print(user.avatar)
    
    # Close the client connection
    api.close()

if __name__ == "__main__":
    main()
```

## Customization and Advanced Usage

- **Authentication:**  
  To enable authentication for endpoints that require it, simply pass `enable_auth=True` along with your API key and secret during client initialization.

- **Type Customization:**  
  If you need to customize or extend the data models, refer to the `abc` module which contains the abstract classes and objects used throughout the library.

- **Consistent API Surface:**  
  Both client types provide the same set of methods, ensuring that you can switch between asynchronous and synchronous programming with minimal changes.

## Contributing

Contributions are welcome! If you’d like to contribute:
- Please review the [Issues](https://github.com/xscynio/codeforcespy/issues) to see where you can help.
- Ensure that your changes maintain strict type-checking and adhere to the established coding guidelines.
- Submit a pull request against the production branch.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Thank you for checking out codeforcespy. If you find it useful, please give it a star!
