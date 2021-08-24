// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import './fUSDStorage.sol';

contract LibraryLock is fUSDStorage {
  // Ensures no one can manipulate the Logic Contract once it is deployed.	
  // PARITY WALLET HACK PREVENTION	

  modifier delegatedOnly() {
    require(
      initialized == true,
      "The library is locked. No direct 'call' is allowed."
    );
    _;
  }

  function initialize() internal {
    initialized = true;
  }
}