# flexUSD (Ethereum Mainnet)

## Description

Collection of post deployments and deployment platform for upgrade for flexUSD on Ethereum Mainnet.
The working post

## History

Previous Deployments can be found under `versions/` directory located on reporitory's root folder. When deploying a new version, it is highly advised to flatten source code and make a copy under this directory as well with date convention observed under subdirectories.

## Getting Started

This repository primarily requires a working `python` environment, with verion 3.7.2 or above.
Assuming `python` command on your local device is set to the correct version, we will use `python` in the command line examples instead of `python3` (and `pip` instead of `pip3`)

The preferred package manager for the reporitory is `poetry`

To install `poetry` on your local environment, run the following command on your Terminal.

```bash
pip install -U poetry
```

Once poetry is installed, locate to the root directory of this folder and allow poetry to install project dependencies.

```bash
poetry install
```

This will automatically install these projects for your local environment

* [eth-brownie](https://github.com/eth-brownie/brownie) A Python-based development and testing framework for smart contracts targeting the Ethereum Virtual Machine.
* [pytest](github.com/pytest-dev/pytest) The pytest framework makes it easy to write small tests, yet scales to support complex functional testing

### Getting Started: Notes

* When `eth-brownie` is installed, you will also automatically install `ganache-cli`, an NPM package for local hosting of Ethereum Virtual Machine (EVM) 

## Run Tests

You can run all tests at the same time using the following command on your shell.

```bash
$ pytest tests/*
... results
```

Or run individual tests as such

```bash
$ pytest tests/transactions.py
... results
$ pytest tests/transactions.py -k test_show_accounts
... result
```

## Run Deployment Script

Local Deployment for interactive usage

```bash
brownie run deploy_flexusd -i
```

Prepare wallet yaml file in root folder with

```bash
python generate-wallet.py --filename wallet.[network]
```

Deploy on desired network

```bash
brownie run deploy_flexusd --network [network]
```

## Create Flattened Sourcecode

To publish sourcecode for verification on Chain Explorer, ie. etherscan, you must first create a flatten sourcecode with the following command

```bash
brownie run flatten
```

## Deployed Contracts Addresses 

### Production contracts deployed on Ethereum Mainnet

- Proxy (proxy contract): [0xa774FFB4AF6B0A91331C084E1aebAE6Ad535e6F3](https://etherscan.io/address/0xa774FFB4AF6B0A91331C084E1aebAE6Ad535e6F3)

- FlexUSD (logic contract): [0xb961Af52192D358e2700BD9c14A5ABEd5f37a201](https://etherscan.io/address/0xb961af52192d358e2700bd9c14a5abed5f37a201)
