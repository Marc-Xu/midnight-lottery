import pytest

from app.exceptions import NotFoundError
from app.business_logic.ballot_service import BallotService


@pytest.fixture
def service(db_session):
    return BallotService(db_session)


def test_create_without_draw(service):
    data = {"participant_id": 1}
    with pytest.raises(NotFoundError) as exc:
        service.create(data)
    assert "has not been created" in str(exc.value)
