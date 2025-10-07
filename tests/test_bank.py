import pytest
from brownie import Bank, accounts

@pytest.fixture
def bank_contract():
    # Deploy a fresh Bank contract for each test
    return Bank.deploy({"from": accounts[0]})

def test_deposits(bank_contract):
    users = [accounts[0], accounts[1], accounts[2]]
    deposits = [1, 2, 1.5]  # ETH in decimal

    for user, amount in zip(users, deposits):
        bank_contract.deposit({"from": user, "value": int(amount * 10**18)})
        balance = bank_contract.getBalance({"from": user})
        assert balance == int(amount * 10**18)

def test_withdrawals(bank_contract):
    users = [accounts[0], accounts[1], accounts[2]]
    deposits = [1, 2, 1.5]
    withdrawals = [0.5, 1, 1]

    # First, deposit
    for user, amount in zip(users, deposits):
        bank_contract.deposit({"from": user, "value": int(amount * 10**18)})

    # Then, withdraw
    for user, amount, deposit in zip(users, withdrawals, deposits):
        bank_contract.withdraw(int(amount * 10**18), {"from": user})
        balance = bank_contract.getBalance({"from": user})
        expected_balance = int((deposit - amount) * 10**18)
        assert balance == expected_balance

def test_withdraw_insufficient(bank_contract):
    user = accounts[1]
    # No deposit yet
    with pytest.raises(Exception):
        bank_contract.withdraw(1 * 10**18, {"from": user})

def test_multiple_users_final_balance(bank_contract):
    users = [accounts[0], accounts[1], accounts[2]]
    deposits = [1, 2, 1.5]
    withdrawals = [0.5, 1, 1]

    # Deposit and withdraw
    for user, deposit in zip(users, deposits):
        bank_contract.deposit({"from": user, "value": int(deposit * 10**18)})
    for user, amount in zip(users, withdrawals):
        try:
            bank_contract.withdraw(int(amount * 10**18), {"from": user})
        except:
            pass

    # Check final balances
    expected_balances = [0.5, 1, 0.5]
    for user, expected in zip(users, expected_balances):
        balance = bank_contract.getBalance({"from": user}) / 10**18
        assert balance == expected
