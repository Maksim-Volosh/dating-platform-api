from unittest.mock import Mock

import pytest

from app.application.services.geo_filter import GeoCandidateFilterService
from app.core.config import settings
from app.domain.entities import Gender, PreferGender, UserDistanceEntity, UserEntity


@pytest.fixture
def user() -> UserEntity:
    return UserEntity(
        telegram_id=1,
        name="me",
        age=18,
        latitude=10.0,
        longitude=20.0,
        gender=Gender.MALE,
        prefer_gender=PreferGender.FEMALE,
        description="desc",
    )


@pytest.fixture
def candidates() -> list[UserEntity]:
    c1 = UserEntity(
        telegram_id=101,
        name="c1",
        age=19,
        latitude=11.0,
        longitude=21.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="c1",
    )
    c2 = UserEntity(
        telegram_id=102,
        name="c2",
        age=20,
        latitude=12.0,
        longitude=22.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="c2",
    )
    return [c1, c2]


@pytest.mark.asyncio
async def test_geo_filter_returns_on_first_step(user, candidates, monkeypatch):
    monkeypatch.setattr(settings.deck, "radius_steps_km", [5, 10, 20])

    haversine_mock = Mock(side_effect=[4.0, 6.0])
    monkeypatch.setattr("app.application.services.geo_filter.haversine", haversine_mock)

    service = GeoCandidateFilterService()

    result = await service.filter(user, candidates)

    assert result == [
        UserDistanceEntity(
            telegram_id=candidates[0].telegram_id,
            name=candidates[0].name,
            age=candidates[0].age,
            distance=4.0,
            gender=candidates[0].gender,
            prefer_gender=candidates[0].prefer_gender,
            description=candidates[0].description,
        )
    ]
    assert haversine_mock.call_count == 2


@pytest.mark.asyncio
async def test_geo_filter_returns_on_second_step_when_first_empty(
    user, candidates, monkeypatch
):
    monkeypatch.setattr(settings.deck, "radius_steps_km", [5, 10, 20])

    haversine_mock = Mock(side_effect=[6.0, 12.0, 6.0, 12.0])
    monkeypatch.setattr("app.application.services.geo_filter.haversine", haversine_mock)

    service = GeoCandidateFilterService()
    result = await service.filter(user, candidates)

    assert len(result) == 1
    assert result[0].telegram_id == candidates[0].telegram_id
    assert result[0].distance == 6.0
    assert haversine_mock.call_count == 4


@pytest.mark.asyncio
async def test_geo_filter_returns_empty_when_no_one_fits_any_step(
    user, candidates, monkeypatch
):
    monkeypatch.setattr(settings.deck, "radius_steps_km", [5, 10, 20])

    haversine_mock = Mock(side_effect=[25.0, 30.0, 25.0, 30.0, 25.0, 30.0])
    monkeypatch.setattr("app.application.services.geo_filter.haversine", haversine_mock)

    service = GeoCandidateFilterService()
    result = await service.filter(user, candidates)

    assert result == []
    assert haversine_mock.call_count == 6
