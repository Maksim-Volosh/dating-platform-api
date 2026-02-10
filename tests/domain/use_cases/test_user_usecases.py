from unittest.mock import AsyncMock, Mock

import pytest

from app.application.use_cases import (CreateUserUseCase,
                                       GetUserProfileViewUseCase,
                                       UpdateUserDescriptionUseCase,
                                       UpdateUserUseCase, UserUseCase)
from app.core.config import settings
from app.domain.entities import (Gender, PreferGender, UserDistanceEntity,
                                 UserEntity)
from app.domain.exceptions import (UserAlreadyExists, UserNotFoundById,
                                   UsersNotFound)


@pytest.fixture
def fake_user() -> UserEntity:
    return UserEntity(
        telegram_id=1,
        name="name",
        age=18,
        latitude=10.0,
        longitude=20.0,
        gender=Gender.MALE,
        prefer_gender=PreferGender.FEMALE,
        description="description",
    )


@pytest.fixture
def candidate_user() -> UserEntity:
    return UserEntity(
        telegram_id=2,
        name="cand",
        age=19,
        latitude=11.0,
        longitude=21.0,
        gender=Gender.FEMALE,
        prefer_gender=PreferGender.MALE,
        description="cand desc",
    )


@pytest.fixture
def fake_distance_candidate(candidate_user) -> UserDistanceEntity:
    return UserDistanceEntity(
        telegram_id=candidate_user.telegram_id,
        name=candidate_user.name,
        age=candidate_user.age,
        distance=1.123,
        gender=candidate_user.gender,
        prefer_gender=candidate_user.prefer_gender,
        description=candidate_user.description,
    )


# -------------------------------
# Tests for UserUseCase
# -------------------------------

@pytest.mark.asyncio
async def test_get_by_id_success(fake_user):
    repo = AsyncMock()
    repo.get_by_id.return_value = fake_user

    use_case = UserUseCase(repo)

    user = await use_case.get_by_id(1)

    assert user == fake_user
    repo.get_by_id.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_get_by_id_not_found():
    repo = AsyncMock()
    repo.get_by_id.return_value = None

    use_case = UserUseCase(repo)

    with pytest.raises(UserNotFoundById):
        await use_case.get_by_id(99)

    repo.get_by_id.assert_awaited_once_with(99)


@pytest.mark.asyncio
async def test_get_all_success(fake_user):
    repo = AsyncMock()
    repo.get_all.return_value = [fake_user]

    use_case = UserUseCase(repo)

    users = await use_case.get_all()

    assert users == [fake_user]
    repo.get_all.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_all_empty():
    repo = AsyncMock()
    repo.get_all.return_value = None

    use_case = UserUseCase(repo)

    with pytest.raises(UsersNotFound):
        await use_case.get_all()

    repo.get_all.assert_awaited_once()


# -------------------------------
# Tests for CreateUserUseCase (NEW DECK LOGIC)
# -------------------------------

@pytest.mark.asyncio
async def test_create_user_success_builds_deck(fake_user, fake_distance_candidate, candidate_user, monkeypatch):
    repo = AsyncMock()
    repo.create.return_value = fake_user

    deck_builder = AsyncMock()

    candidate_repo = AsyncMock()
    candidates = [candidate_user]
    candidate_repo.find_by_preferences_and_bbox.return_value = candidates

    swipe_filter = AsyncMock()
    swipe_filtered = candidates
    swipe_filter.filter.return_value = swipe_filtered

    geo_filter = AsyncMock()
    geo_filtered = [fake_distance_candidate]
    geo_filter.filter.return_value = geo_filtered

    bbx_sentinel = object()
    bounding_box_mock = Mock(return_value=bbx_sentinel)
    monkeypatch.setattr("app.application.use_cases.user.bounding_box", bounding_box_mock)
    monkeypatch.setattr(settings.deck, "radius_steps_km", [5, 10, 30])

    use_case = CreateUserUseCase(repo, deck_builder, candidate_repo, geo_filter, swipe_filter)

    user = await use_case.execute(fake_user)

    assert user == fake_user
    repo.create.assert_awaited_once_with(fake_user)

    bounding_box_mock.assert_called_once_with(fake_user.latitude, fake_user.longitude, 30)
    candidate_repo.find_by_preferences_and_bbox.assert_awaited_once_with(fake_user, bbx_sentinel)
    swipe_filter.filter.assert_awaited_once_with(fake_user.telegram_id, candidates)
    geo_filter.filter.assert_awaited_once_with(fake_user, swipe_filtered)

    deck_builder.build.assert_awaited_once_with(fake_user, geo_filtered)


@pytest.mark.asyncio
async def test_create_user_does_not_build_when_no_geo_candidates(fake_user, candidate_user, monkeypatch):
    repo = AsyncMock()
    repo.create.return_value = fake_user

    deck_builder = AsyncMock()

    candidate_repo = AsyncMock()
    candidate_repo.find_by_preferences_and_bbox.return_value = [candidate_user]

    swipe_filter = AsyncMock()
    swipe_filter.filter.return_value = [candidate_user]

    geo_filter = AsyncMock()
    geo_filter.filter.return_value = []  

    bbx_sentinel = object()
    monkeypatch.setattr("app.application.use_cases.user.bounding_box", Mock(return_value=bbx_sentinel))
    monkeypatch.setattr(settings.deck, "radius_steps_km", [5, 10, 30])

    use_case = CreateUserUseCase(repo, deck_builder, candidate_repo, geo_filter, swipe_filter)

    user = await use_case.execute(fake_user)

    assert user == fake_user
    deck_builder.build.assert_not_awaited()


@pytest.mark.asyncio
async def test_create_user_already_exists(fake_user):
    repo = AsyncMock()
    repo.create.return_value = None

    use_case = CreateUserUseCase(
        repo,
        deck_builder=AsyncMock(),
        candidate_repo=AsyncMock(),
        geo_filter=AsyncMock(),
        swipe_filter=AsyncMock(),
    )

    with pytest.raises(UserAlreadyExists):
        await use_case.execute(fake_user)

    repo.create.assert_awaited_once_with(fake_user)


# -------------------------------
# Tests for UpdateUserUseCase (NEW DECK LOGIC)
# -------------------------------

@pytest.mark.asyncio
async def test_update_user_success_builds_and_cleans(fake_user, candidate_user, fake_distance_candidate, monkeypatch):
    repo = AsyncMock()
    repo.update.return_value = fake_user

    deck_builder = AsyncMock()

    cache = AsyncMock()  
    candidate_repo = AsyncMock()
    candidates = [candidate_user]
    candidate_repo.find_by_preferences_and_bbox.return_value = candidates

    swipe_filter = AsyncMock()
    swipe_filter.filter.return_value = candidates

    geo_filter = AsyncMock()
    geo_filtered = [fake_distance_candidate]
    geo_filter.filter.return_value = geo_filtered

    bbx_sentinel = object()
    monkeypatch.setattr("app.application.use_cases.user.bounding_box", Mock(return_value=bbx_sentinel))
    monkeypatch.setattr(settings.deck, "radius_steps_km", [5, 10, 30])

    use_case = UpdateUserUseCase(repo, deck_builder, cache, candidate_repo, geo_filter, swipe_filter)

    user = await use_case.execute(fake_user.telegram_id, fake_user)

    assert user == fake_user
    repo.update.assert_awaited_once_with(fake_user.telegram_id, fake_user)

    candidate_repo.find_by_preferences_and_bbox.assert_awaited_once_with(fake_user, bbx_sentinel)
    swipe_filter.filter.assert_awaited_once_with(fake_user.telegram_id, candidates)
    geo_filter.filter.assert_awaited_once_with(fake_user, candidates)

    deck_builder.build.assert_awaited_once_with(fake_user, geo_filtered)
    deck_builder.clean_others.assert_awaited_once_with(fake_user, candidates)


@pytest.mark.asyncio
async def test_update_user_does_not_build_when_no_geo_candidates(fake_user, candidate_user, monkeypatch):
    repo = AsyncMock()
    repo.update.return_value = fake_user

    deck_builder = AsyncMock()
    cache = AsyncMock()

    candidate_repo = AsyncMock()
    candidate_repo.find_by_preferences_and_bbox.return_value = [candidate_user]

    swipe_filter = AsyncMock()
    swipe_filter.filter.return_value = [candidate_user]

    geo_filter = AsyncMock()
    geo_filter.filter.return_value = []

    monkeypatch.setattr("app.application.use_cases.user.bounding_box", Mock(return_value=object()))
    monkeypatch.setattr(settings.deck, "radius_steps_km", [5, 10, 30])

    use_case = UpdateUserUseCase(repo, deck_builder, cache, candidate_repo, geo_filter, swipe_filter)

    user = await use_case.execute(fake_user.telegram_id, fake_user)

    assert user == fake_user
    deck_builder.build.assert_not_awaited()
    deck_builder.clean_others.assert_not_awaited()


@pytest.mark.asyncio
async def test_update_user_not_found(fake_user):
    repo = AsyncMock()
    repo.update.return_value = None

    use_case = UpdateUserUseCase(
        repo,
        deck_builder=AsyncMock(),
        cache=AsyncMock(),
        candidate_repo=AsyncMock(),
        geo_filter=AsyncMock(),
        swipe_filter=AsyncMock(),
    )

    with pytest.raises(UserNotFoundById):
        await use_case.execute(fake_user.telegram_id, fake_user)

    repo.update.assert_awaited_once_with(fake_user.telegram_id, fake_user)


# -------------------------------
# Tests for UpdateUserDescriptionUseCase
# -------------------------------

@pytest.mark.asyncio
async def test_update_user_description_success(fake_user):
    repo = AsyncMock()
    repo.update_description.return_value = fake_user

    use_case = UpdateUserDescriptionUseCase(repo)

    user = await use_case.execute(fake_user.telegram_id, "New description")

    assert user == fake_user
    repo.update_description.assert_awaited_once_with(fake_user.telegram_id, "New description")


@pytest.mark.asyncio
async def test_update_user_description_not_found(fake_user):
    repo = AsyncMock()
    repo.update_description.return_value = None

    use_case = UpdateUserDescriptionUseCase(repo)

    with pytest.raises(UserNotFoundById):
        await use_case.execute(fake_user.telegram_id, "New description")

    repo.update_description.assert_awaited_once_with(fake_user.telegram_id, "New description")


# -------------------------------
# Tests for GetUserProfileViewUseCase (haversine)
# -------------------------------

@pytest.mark.asyncio
async def test_get_user_profile_view_success(fake_user, candidate_user, monkeypatch):
    repo = AsyncMock()
    repo.get_by_id.side_effect = [fake_user, candidate_user]

    haversine_mock = Mock(return_value=12.34)
    monkeypatch.setattr("app.application.use_cases.user.haversine", haversine_mock)

    use_case = GetUserProfileViewUseCase(repo)

    view = await use_case.execute(fake_user.telegram_id, candidate_user.telegram_id)

    assert isinstance(view, UserDistanceEntity)
    assert view.telegram_id == candidate_user.telegram_id
    assert view.name == candidate_user.name
    assert view.age == candidate_user.age
    assert view.distance == 12.34
    assert view.gender == candidate_user.gender
    assert view.prefer_gender == candidate_user.prefer_gender
    assert view.description == candidate_user.description

    assert repo.get_by_id.await_count == 2
    haversine_mock.assert_called_once_with(
        fake_user.latitude, fake_user.longitude, candidate_user.latitude, candidate_user.longitude
    )


@pytest.mark.asyncio
async def test_get_user_profile_view_not_found(fake_user, candidate_user):
    repo = AsyncMock()
    repo.get_by_id.side_effect = [fake_user, None] 

    use_case = GetUserProfileViewUseCase(repo)

    with pytest.raises(UserNotFoundById):
        await use_case.execute(fake_user.telegram_id, candidate_user.telegram_id)

    assert repo.get_by_id.await_count == 2
