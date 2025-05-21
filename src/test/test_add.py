import pytest
from unittest.mock import MagicMock, create_autospec
from sqlalchemy.orm import Session
from app.services.user_service import UserService
from app.models.user import User


@pytest.fixture
def mock_db():
    db = create_autospec(Session)
    db.query.return_value = db
    db.filter.return_value = db
    db.first.return_value = None
    return db


class TestUserService:
    def test_create_user_success(self, mock_db):
        # Arrange
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        # Act
        result = UserService.create_user(
            mock_db,
            "testuser",
            "test@example.com",
            "password123"
        )

        # Assert
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        assert isinstance(result, User)
        assert result.username == "testuser"

    def test_create_duplicate_user(self, mock_db):
        # Arrange
        existing_user = MagicMock(spec=User)
        mock_db.query.return_value.filter.return_value.first.return_value = existing_user

        # Act & Assert
        with pytest.raises(ValueError) as excinfo:
            UserService.create_user(
                mock_db,
                "existinguser",
                "exist@example.com",
                "password"
            )

        assert "Username already exists" in str(excinfo.value)