from http import HTTPStatus

import pytest

from tests.conftest import TodoFactory
from user_todo_api.models import TodoState


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Test todo', 'description': 'Test todo description', 'state': 'draft'},
    )
    data = response.json()

    assert response.status_code == HTTPStatus.CREATED

    assert 'id' in data
    assert 'title' in data
    assert 'description' in data
    assert 'state' in data

    assert data['title'] == 'Test todo'
    assert data['description'] == 'Test todo description'
    assert data['state'] == 'draft'


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_2_todos(session, user, client, token):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos

@pytest.mark.parametrize(
    ('filter_params', 'expected_todos'),
    [
        ({'title': 'Test todo 1'}, 5),
        ({'description': 'desc'}, 5),
        ({'state': 'draft'}, 5),
        ({'title': 'Test todo combined', 'description': 'combined', 'state': 'done'}, 5),
    ],
)

    
def test_list_todos_filters(test_context, filter_params, expected_todos):
    session = test_context['session']
    user = test_context['user']

    if filter_params == {'title': 'Test todo combined', 'description': 'combined', 'state': 'done'}:
        session.bulk_save_objects(
            TodoFactory.create_batch(
                5,
                user_id=user.id,
                title='Test todo combined',
                description='combined description',
                state=TodoState.done,
            )
        )
        session.bulk_save_objects(
            TodoFactory.create_batch(
                3,
                user_id=user.id,
                title='Other title',
                description='other description',
                state=TodoState.todo,
            )
        )
    else:
        session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id, **filter_params))
    session.commit()

    query_params = '&'.join([f'{key}={value}' for key, value in filter_params.items()])
    response = test_context['client'].get(
        f'/todos/?{query_params}',
        headers={'Authorization': f'Bearer {test_context["token"]}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'teste!'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'teste!'


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()

    response = client.delete(f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully.'}


def test_delete_todo_error(client, token):
    response = client.delete(f'/todos/{10}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found.'}
