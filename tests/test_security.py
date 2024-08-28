from http import HTTPStatus
from unittest.mock import patch

from jwt import ExpiredSignatureError, decode

from user_todo_api.security import create_access_token, settings


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    assert decoded['test'] == data['test']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao token


def test_jwt_invalid_token(client):
    response = client.delete('/users/1', headers={'Authorization': 'Bearer token-invalido'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_invalid_token_exception(client):
    # Token inválido (não decodificável)
    response = client.delete('/users/1', headers={'Authorization': 'Bearer token-invalido'})
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

    # Token expirado
    with patch('user_todo_api.security.decode', side_effect=ExpiredSignatureError):
        response = client.delete('/users/1', headers={'Authorization': 'Bearer token-expirado'})
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}

    # Token sem o campo 'sub'
    with patch('user_todo_api.security.decode', return_value={'some_other_field': 'value'}):
        response = client.delete('/users/1', headers={'Authorization': 'Bearer token-sem-sub'})
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}

    # Usuário não encontrado
    with patch(
        'user_todo_api.security.decode', return_value={'sub': 'non_existent_user@example.com'}
    ):
        response = client.delete(
            '/users/1', headers={'Authorization': 'Bearer token-usuario-nao-encontrado'}
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}
