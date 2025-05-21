from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.controllers.user_controller import router

client = TestClient(router)

@patch("app.controllers.user_controller.UserService")
def test_create_user_success(mock_service):
    # Mock服务层返回
    mock_user = MagicMock()
    mock_user.to_dict.return_value = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }
    mock_service.create_user.return_value = mock_user

    # 执行请求
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "secret"
        }
    )

    # 验证
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    mock_service.create_user.assert_called_once()

@patch("app.controllers.user_controller.UserService")
def test_login_failure(mock_service):
    # 配置mock返回空值
    mock_service.authenticate_user.return_value = None

    response = client.post(
        "/login",
        json={
            "username": "wronguser",
            "password": "wrongpass"
        }
    )

    assert response.status_code == 401
    assert "Invalid credentials" in response.text