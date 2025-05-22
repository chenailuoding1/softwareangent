
import pytest
from unittest.mock import MagicMock
from app.services.user_service import UserService
from app.models.user import User

# 模拟哈希策略（你可能使用 passlib）
def fake_hash(password):
    return "hashed_" + password

def fake_verify(password, hashed):
    return hashed == "hashed_" + password


@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_user():
    return User(id=1, username="testuser", email="test@example.com", hashed_password=fake_hash("123456"))

def test_create_user_success(mock_db):
    mock_db.query().filter().first.return_value = None  # 模拟用户名不存在

    result = UserService.create_user(mock_db, "newuser", "new@example.com", "mypassword")

    assert result.username == "newuser"
    assert result.email == "new@example.com"
    assert result.hashed_password == fake_hash("mypassword")
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once_with(result)


def test_create_user_duplicate(mock_db):
    # 模拟已有用户名
    mock_db.query().filter().first.return_value = User(username="testuser")

    with pytest.raises(ValueError) as excinfo:
        UserService.create_user(mock_db, "testuser", "abc@example.com", "123")

    assert "Username already exists" in str(excinfo.value)


def test_authenticate_user_success(mock_db, mock_user):
    mock_user.hashed_password = fake_hash("123456")
    mock_db.query().filter().first.return_value = mock_user

    # monkey patch密码验证函数
    UserService.get_user_by_username = lambda db, username: mock_user

    result = UserService.authenticate_user(mock_db, "testuser", "123456")
    assert result == mock_user


def test_authenticate_user_fail_wrong_password(mock_db, mock_user):
    mock_user.hashed_password = fake_hash("correctpass")
    UserService.get_user_by_username = lambda db, username: mock_user

    result = UserService.authenticate_user(mock_db, "testuser", "wrongpass")
    assert result is None


def test_authenticate_user_fail_not_found(mock_db):
    UserService.get_user_by_username = lambda db, username: None

    result = UserService.authenticate_user(mock_db, "nouser", "any")
    assert result is None
