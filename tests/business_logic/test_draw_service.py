import pytest

from datetime import datetime

from app.exceptions import ValidationError
from app.business_logic.draw_service import DrawService


@pytest.fixture
def service(db_session):
    return DrawService(db_session)


def test_create_and_unique(service):
    r1 = service.create(draw_data={})
    assert r1.draw_date == datetime.now().date()
    # duplicate date business rule
    with pytest.raises(ValidationError) as exc:
        service.create(draw_data={})
    assert "already exists" in str(exc.value)
