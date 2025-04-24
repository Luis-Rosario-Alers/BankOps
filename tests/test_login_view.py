from unittest.mock import MagicMock, patch

from PySide6.QtCore import Qt  # noqa

from src.views.login_view import LoginView


class TestLoginView:

    @patch("src.views.login_view.APIClient")
    def test_on_authenticate_button_clicked(self, mock_api_client_class, qtbot):
        """Test the behavior of on_authenticate_button_clicked."""

        mock_model = MagicMock()

        mock_api_client_instance = mock_api_client_class.return_value

        mock_view = LoginView(mock_model)

        mock_view.usernameLineEdit.text = MagicMock(return_value="test_user")
        mock_view.passwordLineEdit.text = MagicMock(return_value="test_password")
        mock_view.usernameLineEdit.clear = MagicMock()
        mock_view.passwordLineEdit.clear = MagicMock()

        mock_view.on_authenticate_button_clicked()

        mock_model.process_login.assert_called_once_with(
            "test_user", "test_password", mock_api_client_instance
        )

        mock_view.usernameLineEdit.clear.assert_called_once()
        mock_view.passwordLineEdit.clear.assert_called_once()

    @patch("src.views.login_view.QMessageBox")
    def test_show_success(self, mock_qmessagebox, qtbot):
        """Test if show_success calls QMessageBox.information correctly."""
        # Arrange
        mock_model = MagicMock()
        view = LoginView(mock_model)
        qtbot.addWidget(view)

        test_username = "test_user"

        # Act
        view.show_success(test_username)

        # Assert
        mock_qmessagebox.information.assert_called_once_with(
            view, "Success", f"Thank you {test_username}, you are now logged in."
        )
        mock_qmessagebox.critical.assert_not_called()

    @patch("src.views.login_view.QMessageBox")
    def test_show_failure(self, mock_qmessagebox, qtbot):
        """Test if show_failure calls QMessageBox.critical correctly."""
        # Arrange
        mock_model = MagicMock()
        view = LoginView(mock_model)
        qtbot.addWidget(view)

        test_message = "Invalid credentials"

        # Act
        view.show_failure(test_message)

        # Assert
        mock_qmessagebox.critical.assert_called_once_with(view, "Failure", test_message)
        mock_qmessagebox.information.assert_not_called()
