def get_confirmation_email_html(username, confirmation_code):
    return f"""
    <h2>Добро пожаловать в YaMDb!</h2>
    <p>Здравствуйте, {username}!</p>
    <p>Ваш код подтверждения: <strong>{confirmation_code}</strong></p>
    <p>Используйте этот код для получения JWT токена.</p>
    """
