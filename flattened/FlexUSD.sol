// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;



// Part: Context

contract Context {
  // Empty internal constructor, to prevent people from mistakenly deploying
  // an instance of this contract, which should be used via inheritance.
  constructor() internal {}

  function _msgSender() internal view returns(address payable) {
    return msg.sender;
  }

  function _msgData() internal view returns(bytes memory) {
    this; // silence state mutability warning without generating bytecode - see https://github.com/USDereum/solidity/issues/2691
    return msg.data;
  }
}

// Part: FlexUSDStorage

contract FlexUSDStorage {
  /** WARNING: NEVER RE-ORDER VARIABLES! 
   *  Always double-check that new variables are added APPEND-ONLY.
   *  Re-ordering variables can permanently BREAK the deployed proxy contract.
   */

  bool public initialized;

  mapping(address => uint256) internal _balances;

  mapping(address => mapping(address => uint256)) internal _allowances;

  mapping(address => bool) public blacklist;

  uint256 internal _totalSupply;

  string public constant name = "flexUSD";
  string public constant symbol = "flexUSD";
  uint256 public multiplier;
  uint8 public constant decimals = 18;
  address public admin;
  uint256 internal constant DECI = 1e18;

  bool internal getPause;
}

// Part: IERC20

interface IERC20 {
  /**
   * @dev Returns the amount of tokens in existence.
   */
  function totalSupply() external view returns(uint256);

  /**
   * @dev Returns the amount of tokens owned by `account`.
   */
  function balanceOf(address account) external view returns(uint256);

  /**
   * @dev Moves `amount` tokens from the caller's account to `recipient`.
   *
   * Returns a boolean value indicating whUSDer the operation succeeded.
   *
   * Emits a {Transfer} event.
   */
  function transfer(address recipient, uint256 amount)
  external
  returns(bool);

  /**
   * @dev Returns the remaining number of tokens that `spender` will be
   * allowed to spend on behalf of `owner` through {transferFrom}. This is
   * zero by default.
   *
   * This value changes when {approve} or {transferFrom} are called.
   */
  function allowance(address owner, address spender)
  external
  view
  returns(uint256);

  /**
   * @dev Sets `amount` as the allowance of `spender` over the caller's tokens.
   *
   * Returns a boolean value indicating whUSDer the operation succeeded.
   *
   * IMPORTANT: Beware that changing an allowance with this mUSDod brings the risk
   * that someone may use both the old and the new allowance by unfortunate
   * transaction ordering. One possible solution to mitigate this race
   * condition is to first reduce the spender's allowance to 0 and set the
   * desired value afterwards:
   * https://github.com/USDereum/EIPs/issues/20#issuecomment-263524729
   *
   * Emits an {Approval} event.
   */
  function approve(address spender, uint256 amount) external returns(bool);

  /**
   * @dev Moves `amount` tokens from `sender` to `recipient` using the
   * allowance mechanism. `amount` is then deducted from the caller's
   * allowance.
   *
   * Returns a boolean value indicating whUSDer the operation succeeded.
   *
   * Emits a {Transfer} event.
   */
  function transferFrom(
    address sender,
    address recipient,
    uint256 amount
  ) external returns(bool);

  /**
   * @dev Emitted when `value` tokens are moved from one account (`from`) to
   * another (`to`).
   *
   * Note that `value` may be zero.
   */
  event Transfer(address indexed from, address indexed to, uint256 value);

  /**
   * @dev Emitted when the allowance of a `spender` for an `owner` is set by
   * a call to {approve}. `value` is the new allowance.
   */
  event Approval(
    address indexed owner,
    address indexed spender,
    uint256 value
  );
}

// Part: Proxiable

contract Proxiable {
  // Code position in storage is keccak256("PROXIABLE") = "0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7"

  function updateCodeAddress(address newAddress) internal {
    require(
      bytes32(
        0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7
      ) == Proxiable(newAddress).proxiableUUID(),
      "Not compatible"
    );
    assembly {
      // solium-disable-line
      sstore(
        0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7,
        newAddress
      )
    }
  }

  function proxiableUUID() public pure returns(bytes32) {
    return
    0xc5f16f0fcc639fa48a6947836d9850f504798523bf8c9a3a87d5876cf622bcf7;
  }
}

// Part: SafeMath

library SafeMath {
  /**
   * @dev Returns the addition of two unsigned integers, reverting on
   * overflow.
   *
   * Counterpart to Solidity's `+` operator.
   *
   * Requirements:
   * - Addition cannot overflow.
   */
  function add(uint256 a, uint256 b) internal pure returns(uint256) {
    uint256 c = a + b;
    require(c >= a, "SafeMath: addition overflow");

    return c;
  }

  /**
   * @dev Returns the subtraction of two unsigned integers, reverting on
   * overflow (when the result is negative).
   *
   * Counterpart to Solidity's `-` operator.
   *
   * Requirements:
   * - Subtraction cannot overflow.
   */
  function sub(uint256 a, uint256 b) internal pure returns(uint256) {
    return sub(a, b, "SafeMath: subtraction overflow");
  }

  /**
   * @dev Returns the subtraction of two unsigned integers, reverting with custom message on
   * overflow (when the result is negative).
   *
   * Counterpart to Solidity's `-` operator.
   *
   * Requirements:
   * - Subtraction cannot overflow.
   */
  function sub(
    uint256 a,
    uint256 b,
    string memory errorMessage
  ) internal pure returns(uint256) {
    require(b <= a, errorMessage);
    uint256 c = a - b;

    return c;
  }

  /**
   * @dev Returns the multiplication of two unsigned integers, reverting on
   * overflow.
   *
   * Counterpart to Solidity's `*` operator.
   *
   * Requirements:
   * - Multiplication cannot overflow.
   */
  function mul(uint256 a, uint256 b) internal pure returns(uint256) {
    // Gas optimization: this is cheaper than requiring 'a' not being zero, but the
    // benefit is lost if 'b' is also tested.
    // See: https://github.com/OpenZeppelin/openzeppelin-contracts/pull/522
    if (a == 0) {
      return 0;
    }

    uint256 c = a * b;
    require(c / a == b, "SafeMath: multiplication overflow");

    return c;
  }

  /**
   * @dev Returns the integer division of two unsigned integers. Reverts on
   * division by zero. The result is rounded towards zero.
   *
   * Counterpart to Solidity's `/` operator. Note: this function uses a
   * `revert` opcode (which leaves remaining gas untouched) while Solidity
   * uses an invalid opcode to revert (consuming all remaining gas).
   *
   * Requirements:
   * - The divisor cannot be zero.
   */
  function div(uint256 a, uint256 b) internal pure returns(uint256) {
    return div(a, b, "SafeMath: division by zero");
  }

  /**
   * @dev Returns the integer division of two unsigned integers. Reverts with custom message on
   * division by zero. The result is rounded towards zero.
   *
   * Counterpart to Solidity's `/` operator. Note: this function uses a
   * `revert` opcode (which leaves remaining gas untouched) while Solidity
   * uses an invalid opcode to revert (consuming all remaining gas).
   *
   * Requirements:
   * - The divisor cannot be zero.
   */
  function div(
    uint256 a,
    uint256 b,
    string memory errorMessage
  ) internal pure returns(uint256) {
    // Solidity only automatically asserts when dividing by 0
    require(b > 0, errorMessage);
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold

    return c;
  }

  /**
   * @dev Returns the remainder of dividing two unsigned integers. (unsigned integer modulo),
   * Reverts when dividing by zero.
   *
   * Counterpart to Solidity's `%` operator. This function uses a `revert`
   * opcode (which leaves remaining gas untouched) while Solidity uses an
   * invalid opcode to revert (consuming all remaining gas).
   *
   * Requirements:
   * - The divisor cannot be zero.
   */
  function mod(uint256 a, uint256 b) internal pure returns(uint256) {
    return mod(a, b, "SafeMath: modulo by zero");
  }

  /**
   * @dev Returns the remainder of dividing two unsigned integers. (unsigned integer modulo),
   * Reverts with custom message when dividing by zero.
   *
   * Counterpart to Solidity's `%` operator. This function uses a `revert`
   * opcode (which leaves remaining gas untouched) while Solidity uses an
   * invalid opcode to revert (consuming all remaining gas).
   *
   * Requirements:
   * - The divisor cannot be zero.
   */
  function mod(
    uint256 a,
    uint256 b,
    string memory errorMessage
  ) internal pure returns(uint256) {
    require(b != 0, errorMessage);
    return a % b;
  }
}

// Part: LibraryLock

contract LibraryLock is FlexUSDStorage {
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

// File: FlexUSD.sol

contract FlexUSD is FlexUSDStorage, Context, IERC20, Proxiable, LibraryLock {
  using SafeMath for uint256;

  event TokenBlacklist(address indexed account, bool blocked);
  event ChangeMultiplier(uint256 multiplier);
  event AdminChanged(address admin);
  event CodeUpdated(address indexed newCode);

  function initialize(uint256 _totalsupply)
    external
  {
    require(!initialized, "The library has already been initialized.");
    LibraryLock.initialize();
    admin = msg.sender;
    multiplier = 1 * DECI;
    _totalSupply = _totalsupply;
    _balances[msg.sender] = _totalSupply;
  }

  /// @dev Update the logic contract code	
  function updateCode(address newCode)
    external
    onlyAdmin
    delegatedOnly
  {
    updateCodeAddress(newCode);
    emit CodeUpdated(newCode);
  }

  function setMultiplier(uint256 _multiplier)
    external
    onlyAdmin()
    isNotPaused()
  {
    require(
      _multiplier > multiplier,
      "The multiplier should be greater than previous multiplier."
    );
    multiplier = _multiplier;
    emit ChangeMultiplier(multiplier);
  }

  function totalSupply()
    public
    view
    override
    returns (uint256)
  {
    return _totalSupply.mul(multiplier).div(DECI);
  }

  function setTotalSupply(uint256 inputTotalSupply)
    external
    onlyAdmin()
  {
    require(
      inputTotalSupply > totalSupply(),
      "The input total supply is not greater than present total supply."
    );
    multiplier = (inputTotalSupply.mul(DECI)).div(_totalSupply);
    emit ChangeMultiplier(multiplier);
  }

  function balanceOf(address account)
    external
    view
    override
    returns (uint256)
  {
    uint256 externalAmt;
    externalAmt = _balances[account].mul(multiplier).div(DECI);
    return externalAmt;
  }

  function transfer(address recipient, uint256 amount)
    external
    virtual
    override
    notBlacklisted(msg.sender)
    notBlacklisted(recipient)
    isNotPaused()
    returns (bool)
  {
    uint256 externalAmt = amount;
    _transfer(msg.sender, recipient, externalAmt);
    return true;
  }

  function allowance(address owner, address spender)
    public
    view
    virtual
    override
    returns (uint256)
  {
    uint256 externalAmt;
    uint256 maxApproval = type(uint256).max;
    maxApproval = maxApproval.div(multiplier).mul(DECI);
    if (_allowances[owner][spender] >= maxApproval) {
      externalAmt = type(uint256).max;
    } else {
      externalAmt = (_allowances[owner][spender]).mul(multiplier).div(DECI);
    }

    return externalAmt;
  }

  function approve(address spender, uint256 amount)
    external
    virtual
    override
    notBlacklisted(spender)
    notBlacklisted(msg.sender)
    isNotPaused()
    returns (bool)
  {
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
  function increaseAllowance(address spender, uint256 addedValue)
    external
    notBlacklisted(spender)
    notBlacklisted(msg.sender)
    isNotPaused()
    returns (bool)
  {
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
  function decreaseAllowance(address spender, uint256 subtractedValue)
    external
    notBlacklisted(spender)
    notBlacklisted(msg.sender)
    isNotPaused()
    returns (bool)
  {
    uint256 externalAmt = allowance(_msgSender(), spender);
    _approve(_msgSender(), spender, externalAmt.sub(subtractedValue, "ERC20: decreased allowance below zero."));
    return true;
  }

  function transferFrom(
    address sender,
    address recipient,
    uint256 amount
  )
    external
    virtual
    override
    notBlacklisted(sender)
    notBlacklisted(msg.sender)
    notBlacklisted(recipient)
    isNotPaused()
    returns (bool)
  {
    uint256 externalAmt = allowance(sender, _msgSender());
    _transfer(sender, recipient, amount);
    _approve(
      sender,
      _msgSender(),
      externalAmt.sub(
        amount,
        "ERC20: transfer amount exceeds allowance."
      )
    );
    return true;
  }

  function _transfer(
    address sender,
    address recipient,
    uint256 externalAmt
  )
    internal
    virtual
  {
    require(sender != address(0), "ERC20: transfer from the zero address.");
    require(recipient != address(0), "ERC20: transfer to the zero address.");
    uint256 internalAmt = externalAmt.mul(DECI).div(multiplier);
    _balances[sender] = _balances[sender].sub(
      internalAmt,
      "ERC20: transfer internalAmt exceeds balance."
    );
    _balances[recipient] = _balances[recipient].add(internalAmt);
    emit Transfer(sender, recipient, externalAmt);
  }

  function mint(address mintTo, uint256 amount)
    external
    virtual
    onlyAdmin()
    isNotPaused()
    returns (bool)
  {
    uint256 externalAmt = amount;
    uint256 internalAmt = externalAmt.mul(DECI).div(multiplier);
    _mint(mintTo, internalAmt, externalAmt);
    return true;
  }

  function _mint(
    address account,
    uint256 internalAmt,
    uint256 externalAmt
  )
    internal
    virtual
  {
    require(account != address(0), "ERC20: mint to the zero address.");
    _totalSupply = _totalSupply.add(internalAmt);
    _balances[account] = _balances[account].add(internalAmt);
    emit Transfer(address(0), account, externalAmt);
  }

  function burn(address burnFrom, uint256 amount)
    external
    virtual
    onlyAdmin()
    isNotPaused()
    returns (bool)
  {
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
  )
    internal
    virtual
  {
    require(account != address(0), "ERC20: burn from the zero address.");

    _balances[account] = _balances[account].sub(
      internalAmt,
      "ERC20: burn internaAmt exceeds balance."
    );
    _totalSupply = _totalSupply.sub(internalAmt);
    emit Transfer(account, address(0), externalAmt);
  }

  function _approve(
    address owner,
    address spender,
    uint256 externalAmt
  )
    internal
    virtual
  {
    require(owner != address(0), "ERC20: approve from the zero address.");
    require(spender != address(0), "ERC20: approve to the zero address.");
    uint256 internalAmt;
    uint256 maxUInt = type(uint256).max;
    uint256 maxApproval = maxUInt.div(multiplier).mul(DECI);
    if (externalAmt <= maxUInt.div(DECI)) {
      internalAmt = externalAmt.mul(DECI).div(multiplier);
      if (internalAmt > maxApproval)
      {
        internalAmt = maxApproval;
      }
    } else {
      internalAmt = maxApproval;
    }
    _allowances[owner][spender] = internalAmt;
    emit Approval(owner, spender, externalAmt);
  }

  function transferOwnership(address account)
    external
    onlyAdmin()
  {
    require(account != address(0), "New owner account cannot be zero address.");
    admin = account;
    emit AdminChanged(admin);
  }

  function pause()
    external
    onlyAdmin()
  {
    getPause = true;
  }

  function unpause()
    external
    onlyAdmin()
  {
    getPause = false;
  }

  // pause unpause

  modifier isNotPaused() {
    require(!getPause, "The contract is paused.");
    _;
  }

  modifier onlyAdmin() {
    require(msg.sender == admin, "You are not the admin.");
    _;
  }
  
  function addToBlacklist(address account)
    external
    onlyAdmin()
  {
    blacklist[account] = true;
    emit TokenBlacklist(account, true);
  }

  function removeFromBlacklist(address account)
    external
    onlyAdmin()
  {
    blacklist[account] = false;
    emit TokenBlacklist(account, false);
  }

  modifier notBlacklisted(address account) {
    require(!blacklist[account], "Account is blacklisted.");
    _;
  }
}
