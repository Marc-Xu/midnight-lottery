import pytest

from app.data_access_layer.models import Participant
from app.data_access_layer.general_repository import GeneralRepository


@pytest.fixture
def repo(db_session):
    return GeneralRepository(db_session, Participant)


def test_add_and_get(repo):
    r = repo.add(name="Test", email="test@example.com")
    assert isinstance(r, Participant)
    fetched = repo.get(r.id)
    assert fetched.id == r.id
    assert fetched.name == "Test"


def test_list_pagination(repo):
    # add 3 items
    for i in range(3):
        repo.add(name=f"R{i}", email=f"r{i}@example.com")
    all_rest = repo.list()
    assert len(all_rest) >= 3
    first_two = repo.list(limit=2)
    assert len(first_two) == 2


def test_find_by(repo):
    repo.add(name="Unique", email="unique@example.com")
    found: Participant = repo.find_by(name="Unique")[0]
    assert found is not None and found.name == "Unique"
    assert not repo.find_by(name="DoesNotExist")


def test_update(repo):
    r = repo.add(name="Old", email="old@example.com")
    updated = repo.update(r.id, {"name": "New", "email": "new@example.com"})
    assert updated.name == "New"
    assert updated.email == "new@example.com"
    # updating non-existing
    assert repo.update(9999, {}) is None


def test_delete(repo):
    r = repo.add(name="ToDelete", email="delete@example.com")
    deleted = repo.delete(r.id)
    assert deleted.id == r.id
    assert repo.get(r.id) is None
