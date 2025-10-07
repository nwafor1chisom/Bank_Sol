from brownie import Bank, network
from scripts.helpful_scripts import get_account


def main():
    account = get_account()
    print(f"🚀 Deploying Bank contract from {account} on {network.show_active()}...")

    bank = Bank.deploy({"from": account})
    print(f"✅ Bank deployed at: {bank.address}")

    return bank
