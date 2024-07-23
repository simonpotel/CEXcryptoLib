# CEXcryptoLib

<img src="https://github.com/simonpotel/CEXcryptoLib/blob/916ce9f6ac090f228c21c36278dcce9632909c62/logo.jpeg" width="300" height="300" alt="CEXcryptoLib Logo">

CEXcryptoLib is a Python library designed to simplify the use of the Binance API and other centralized exchange (CEX) APIs, enabling you to execute transactions and retrieve information efficiently.

## Deployment

### Installation

To add this project as a submodule to your own project, run:

```bash
git submodule add https://github.com/simonpotel/CEXcryptoLib
```

To update the submodule to the latest version, use:

```bash
git submodule update --remote
```

## Important Considerations

> **Note:**  
> The methods provided in the `Client` class are tailored for creating a trading bot. Currently, the focus is on market orders, and other order types have not been implemented as they are not needed for the current scope. If you would like to add support for additional order types, please feel free to create a new branch and submit a pull request!

> **Caution:**  
> This library facilitates interaction with the API and is designed to streamline code for trading projects. However, it does not handle transaction security comprehensively. Any issues encountered during transactions may be due to factors beyond the library's control. Ensure you understand the API and its risks when using this library for automated trading.

## Usage Examples

For examples of how to use the library, please refer to the test files located in the `tests/` directory. These examples demonstrate how to interact with various APIs, such as Binance.
