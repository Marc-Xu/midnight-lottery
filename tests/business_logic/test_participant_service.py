import pytest

from app.exceptions import NotFoundError, ValidationError
from app.business_logic.participant_service import ParticipantService


@pytest.fixture
def service(db_session):
    return ParticipantService(db_session)


def test_create_and_unique(service):
    data = {"name": "Test", "email": "R1@example.com"}
    data_duplicate = {"name": "Duplicate", "email": "R1@example.com"}
    r1 = service.create(data)
    assert r1.name == "Test"
    # duplicate email business rule
    with pytest.raises(ValidationError) as exc:
        service.create(data_duplicate)
    assert "already exists" in str(exc.value)


def test_get_not_found(service):
    with pytest.raises(NotFoundError):
        service.get(9999)


def test_get_participant_by_attributes(service):
    data1 = {"name": "R1", "email": "R1@example.com"}
    data2 = {"name": "R1", "email": "R2@example.com"}
    service.create(data1)
    service.create(data2)
    top = service.get_by_attributes(
        {"name": "R1"}, limit=2, order_by="email", descending=True
    )
    assert top is not None and len(top) == 2
    assert top[0].email == "R2@example.com"
    assert top[1].email == "R1@example.com"


def test_update_and_not_found(service):
    data = {"name": "Up", "email": "up@example.com"}
    r = service.create(data)
    update_data = {"email": "up2@example.com"}
    r2 = service.update(r.id, update_data)
    assert r2.email == "up2@example.com"
    with pytest.raises(NotFoundError):
        service.update(9999, update_data)


def test_delete_and_not_found(service):
    data = {"name": "Del", "email": "del@example.com"}
    r = service.create(data)
    d = service.delete(r.id)
    assert d.id == r.id
    with pytest.raises(NotFoundError):
        service.delete(9999)
