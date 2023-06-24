// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HelloWorld {
  event Log(uint time, string message);
  event Money(string message, address reciptient, uint balance);
  string message;
  constructor(string memory myMessage) {
  message = myMessage;
  }

 function getBalance() public view returns (uint) {
        return address(this).balance;
    }  

receive() external payable {
 emit Money("money received",msg.sender,msg.value);
}

function getMessage() public view returns (string memory) {
  return message;
  }
function setMessage(string memory NewString) public {
  message = NewString;
  }

// amount in gwei
function sendEther(address payable recipient, uint _amount) public {
    uint amount = _amount * 1e9;
    require(address(this).balance >= amount, "Insufficient balance in contract");
    (bool sent, ) = recipient.call{value: amount}("");
    require(sent, "Failed to send Ether");
    emit Money("paiement fait", recipient, amount);
}

function emptyWallet(address payable recipient) public {
  uint balance = address(this).balance;
    (bool sent, ) = recipient.call{value: balance}("");
    require(sent, "Failed to send Ether");
    emit Money("paiement fait", recipient, balance);
}


function sentStatus() public {
  emit Log(block.timestamp,message);
  }
}
