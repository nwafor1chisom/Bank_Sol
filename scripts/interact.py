from brownie import Bank, accounts, network
from scripts.helpful_scripts import get_account

def main():
    print(f"\n🌐 Active network: {network.show_active()}")

    # Pick account(s)
    if network.show_active() == "development":
        users = [accounts[0], accounts[1], accounts[2]]  # Ganache provides many accounts
    else:
        users = [get_account()]  # Only your .env PRIVATE_KEY account is available

    # Attach to last deployed contract
    if len(Bank) == 0:
        print("❌ No Bank contract found. Deploy it first with: brownie run scripts/deploy.py --network", network.show_active())
        return

    bank = Bank[-1]
    print(f"✅ Connected to Bank at: {bank.address}\n")

    # Example: Deposit only with the first user
    user = users[0]
    print(f"💰 Depositing 0.1 ETH from {user}...")
    tx = bank.deposit({"from": user, "value": 5 * 10**16})  # 0.05 ETH

    tx.wait(1)

    balance = bank.getBalance({"from": user})
    print(f"📊 Balance of {user}: {balance / 10**18} ETH")

    # Example: Withdraw 0.05 ETH
    print(f"🏧 Withdrawing 0.05 ETH...")
    tx = bank.withdraw(5 * 10**16, {"from": user})
    tx.wait(1)

    balance = bank.getBalance({"from": user})
    print(f"📊 Final balance of {user}: {balance / 10**18} ETH")
