from faker import Faker

from cmstest.data.generators import RUN_ID, fake, run_marker, unique_name


def test_run_marker_is_stable_within_a_process() -> None:
    assert run_marker() == f"autotest-{RUN_ID}"
    assert run_marker() == run_marker()


def test_unique_names_share_the_marker_but_differ() -> None:
    names = {unique_name() for _ in range(50)}

    assert len(names) == 50
    assert all(name.startswith(run_marker() + "-") for name in names)


def test_seed_makes_generation_reproducible() -> None:
    Faker.seed(12345)
    first = [fake.name(), fake.url(), fake.color()]
    Faker.seed(12345)
    second = [fake.name(), fake.url(), fake.color()]

    assert first == second
