import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize(
    "num1, num2, result",
    [
        (3, 2, 5),
        (7, 1, 8),
        (12, 4, 16),
    ]
)
def test_add(num1, num2, result):
    print("Testing add function")
    assert add(num1, num2) == result


@pytest.mark.parametrize(
    "num1, num2, result",
    [
        (3, 2, 1),
        (7, 1, 6),
        (12, 4, 8),
    ]
)
def test_subtract(num1, num2, result):
    print("Testing subtract function")
    assert subtract(num1, num2) == result


@pytest.mark.parametrize(
    "num1, num2, result",
    [
        (3, 2, 6),
        (7, 1, 7),
        (12, 4, 48),
    ]
)
def test_multiply(num1, num2, result):
    print("Testing multiply function")
    assert multiply(num1, num2) == result


@pytest.mark.parametrize(
    "num1, num2, result",
    [
        (3, 2, 1.5),
        (7, 1, 7),
        (12, 4, 3),
    ]
)
def test_divide(num1, num2, result):
    print("Testing divide function")
    assert divide(num1, num2) == result
    
    
    
def test_bank_set_init_amount(bank_account):
    assert bank_account.balance == 50
    
def test_bank_set_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0
    
def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30
    
def test_deposite(bank_account):
    bank_account.deposit(100)
    assert bank_account.balance == 150
    
def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55
    

@pytest.mark.parametrize(
    "deposited, withdrawn, balance",
    [
        (200, 100, 100),
        (50, 10, 40),
        (1200, 200, 1000),
    ]
)
def test_bank_trasaction(zero_bank_account, deposited, withdrawn, balance):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == balance
    
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)