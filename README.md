# 🏦 Bank_Sol Smart Contract

A simple **Ethereum-based bank** smart contract built with **Solidity** and **Brownie**.  
This contract allows users to securely deposit and withdraw ETH, while maintaining individual balances and emitting events for transparency.

---

## 🚀 Features
- 💰 **Deposit ETH** into the contract  
- 💸 **Withdraw only your own funds**  
- 📊 **View individual balances**  
- 🔔 **Emit events** for every deposit and withdrawal  

---

## ⚙️ Tech Stack
- **Language:** Solidity (`^0.8.x`)
- **Framework:** Brownie  
- **Network:** Sepolia Testnet  
- **Wallet:** MetaMask  
- **Provider:** Infura / Alchemy  

---

## 🧩 Example Smart Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract Bank {
    mapping(address => uint256) public balances;

    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);

    function deposit() public payable {
        require(msg.value > 0, "Deposit must be greater than zero");
        balances[msg.sender] += msg.value;
        emit Deposit(msg.sender, msg.value);
    }

    function withdraw(uint256 _amount) public {
        require(_amount > 0, "Withdraw amount must be greater than zero");
        require(balances[msg.sender] >= _amount, "Insufficient balance");
        balances[msg.sender] -= _amount;
        payable(msg.sender).transfer(_amount);
        emit Withdrawal(msg.sender, _amount);
    }

    function getBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
}
