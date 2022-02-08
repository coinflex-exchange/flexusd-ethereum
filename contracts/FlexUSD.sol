// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import './Context.sol';
import './FlexUSDStorage.sol';
import './LibraryLock.sol';
import './Proxiable.sol';
import './SafeMath.sol';
import '../interfaces/IERC20.sol';

contract FlexUSD is FlexUSDStorage, Context, IERC20, Proxiable, LibraryLock {
  using SafeMath for uint256;

  event TokenBlacklist(address indexed account, bool blocked);
  event ChangeMultiplier(uint256 multiplier);
  event AdminChanged(address admin);
  event CodeUpdated(address indexed newCode);

  function initialize(uint256 _totalsupply) public {
    require(!initialized, "The library has already been initialized.");
    LibraryLock.initialize();
    admin = msg.sender;
    multiplier = 1 * DECI;
    _totalSupply = _totalsupply;
    _balances[msg.sender] = _totalSupply;
  }

  /// @dev Update the logic contract code	
  function updateCode(address newCode) external onlyAdmin delegatedOnly {
    updateCodeAddress(newCode);
    emit CodeUpdated(newCode);
  }

  function setMultiplier(uint256 _multiplier)
  external
  onlyAdmin()
  isPaused() {
    require(
      _multiplier > multiplier,
      "the multiplier should be greater than previous multiplier"
    );
    multiplier = _multiplier;
    emit ChangeMultiplier(multiplier);
  }

  function totalSupply() public override view returns(uint256) {
    return _totalSupply.mul(multiplier).div(DECI);
  }

  function setTotalSupply(uint256 inputTotalsupply) external onlyAdmin() {
    require(
      inputTotalsupply > totalSupply(),
      "the input total supply is not greater than present total supply"
    );
    multiplier = (inputTotalsupply.mul(DECI)).div(_totalSupply);
    emit ChangeMultiplier(multiplier);
  }

  function balanceOf(address account) public override view returns(uint256) {
    uint256 externalAmt;
    externalAmt = _balances[account].mul(multiplier).div(DECI);
    return externalAmt;
  }

  function transfer(address recipient, uint256 amount)
  public
  virtual
  override
  notblacklisted(msg.sender)
  notblacklisted(recipient)
  isPaused()
  returns(bool) {
    uint256 internalAmt;
    uint256 externalAmt = amount;
    internalAmt = (amount.mul(DECI)).div(multiplier);

    _transfer(msg.sender, recipient, externalAmt);
    return true;
  }

  function allowance(address owner, address spender)
  public
  virtual
  override
  view
  returns(uint256) {
    uint256 internalAmt;
    uint256 maxapproval = 115792089237316195423570985008687907853269984665640564039457584007913129639935;
    maxapproval = maxapproval.div(multiplier).mul(DECI);
    if (_allowances[owner][spender] > maxapproval) {
      internalAmt = 115792089237316195423570985008687907853269984665640564039457584007913129639935;
    } else {
      internalAmt = (_allowances[owner][spender]).mul(multiplier).div(DECI);
    }

    return internalAmt;
  }

  function approve(address spender, uint256 amount)
  public
  virtual
  override
  notblacklisted(spender)
  notblacklisted(msg.sender)
  isPaused()
  returns(bool) {
    uint256 internalAmt;
    uint256 externalAmt = amount;
    _approve(msg.sender, spender, externalAmt);
    return true;
  }

  /**
   * @dev Atomically increases the allowance granted to `spender` by the caller.
   *
   * This is an alternative to {approve} that can be used as a mitigation for
   * problems described in {IERC20-approve}.
   *
   * Emits an {Approval} event indicating the updated allowance.
   *
   * Requirements:
   *
   * - `spender` cannot be the zero address.
   */
  function increaseAllowance(address spender, uint256 addedValue) public
  notblacklisted(spender)
  notblacklisted(msg.sender)
  isPaused()
  returns(bool) {
    uint256 externalAmt = allowance(_msgSender(), spender);
    _approve(_msgSender(), spender, externalAmt.add(addedValue));
    return true;
  }

  /**
   * @dev Atomically decreases the allowance granted to `spender` by the caller.
   *
   * This is an alternative to {approve} that can be used as a mitigation for
   * problems described in {IERC20-approve}.
   *
   * Emits an {Approval} event indicating the updated allowance.
   *
   * Requirements:
   *
   * - `spender` cannot be the zero address.
   * - `spender` must have allowance for the caller of at least
   * `subtractedValue`.
   */
  function decreaseAllowance(address spender, uint256 subtractedValue) public
  notblacklisted(spender)
  notblacklisted(msg.sender)
  isPaused()
  returns(bool) {
    uint256 externalAmt = allowance(_msgSender(), spender);
    _approve(_msgSender(), spender, externalAmt.sub(subtractedValue, "ERC20: decreased allowance below zero"));
    return true;
  }

  function transferFrom(
    address sender,
    address recipient,
    uint256 amount
  )
  public
  virtual
  override
  notblacklisted(sender)
  notblacklisted(msg.sender)
  notblacklisted(recipient)
  isPaused()
  returns(bool) {
    uint256 externalAmt = allowance(sender, _msgSender());
    _transfer(sender, recipient, amount);
    _approve(
      sender,
      _msgSender(),
      externalAmt.sub(
        amount,
        "ERC20: transfer amount exceeds allowance"
      )
    );
    return true;
  }

  function _transfer(
    address sender,
    address recipient,
    uint256 externalAmt
  ) internal virtual {
    require(sender != address(0), "ERC20: transfer from the zero address");
    require(recipient != address(0), "ERC20: transfer to the zero address");
    uint256 internalAmt = externalAmt.mul(DECI).div(multiplier);
    _balances[sender] = _balances[sender].sub(
      internalAmt,
      "ERC20: transfer internalAmt exceeds balance"
    );
    _balances[recipient] = _balances[recipient].add(internalAmt);
    emit Transfer(sender, recipient, externalAmt);
  }

  function mint(address mintTo, uint256 amount)
  public
  virtual
  onlyAdmin()
  isPaused()
  returns(bool) {
    uint256 externalAmt = amount;
    uint256 internalAmt = externalAmt.mul(DECI).div(multiplier);
    _mint(mintTo, internalAmt, externalAmt);
    return true;
  }

  function _mint(
    address account,
    uint256 internalAmt,
    uint256 externalAmt
  ) internal virtual {
    require(account != address(0), "ERC20: mint to the zero address");

    _totalSupply = _totalSupply.add(internalAmt);
    _balances[account] = _balances[account].add(internalAmt);
    emit Transfer(address(0), account, externalAmt);
  }

  function burn(address burnFrom, uint256 amount)
  public
  virtual
  onlyAdmin()
  isPaused()
  returns(bool) {
    uint256 internalAmt;
    uint256 externalAmt = amount;
    internalAmt = externalAmt.mul(DECI).div(multiplier);

    _burn(burnFrom, internalAmt, externalAmt);
    return true;
  }

  function _burn(
    address account,
    uint256 internalAmt,
    uint256 externalAmt
  ) internal virtual {
    require(account != address(0), "ERC20: burn from the zero address");

    _balances[account] = _balances[account].sub(
      internalAmt,
      "ERC20: burn internaAmt exceeds balance"
    );
    _totalSupply = _totalSupply.sub(internalAmt);
    emit Transfer(account, address(0), externalAmt);
  }

  function _approve(
    address owner,
    address spender,
    uint256 externalAmt
  ) internal virtual {
    require(owner != address(0), "ERC20: approve from the zero address");
    require(spender != address(0), "ERC20: approve to the zero address");
    uint256 internalAmt;
    uint256 maxapproval = 115792089237316195423570985008687907853269984665640564039457584007913129639935;
    maxapproval = maxapproval.div(multiplier).mul(DECI);
    if (externalAmt > maxapproval) {
      internalAmt = 115792089237316195423570985008687907853269984665640564039457584007913129639935;
    } else {
      internalAmt = externalAmt.mul(DECI).div(multiplier);
    }
    _allowances[owner][spender] = internalAmt;
    emit Approval(owner, spender, externalAmt);
  }

  function transferOwnership(address account) public onlyAdmin() {
    require(account != address(0), "new owner account cannot be zero address");
    admin = account;
    emit AdminChanged(admin);
  }

  function pause() external onlyAdmin() {
    getpause = true;
  }

  function unpause() external onlyAdmin() {
    getpause = false;
  }

  // pause unpause

  modifier isPaused() {
    require(!getpause, "the contract is paused");
    _;
  }

  modifier onlyAdmin() {
    require(msg.sender == admin, "you are not the admin");
    _;
  }
  
  function addToBlacklist(address account) external onlyAdmin() {
    blacklist[account] = true;
    emit TokenBlacklist(account, true);
  }

  function removeFromBlacklist(address account) external onlyAdmin() {
    blacklist[account] = false;
    emit TokenBlacklist(account, false);
  }

  modifier notBlacklisted(address account) {
    require(!blacklist[account], "account is blacklisted");
    _;
  }
}