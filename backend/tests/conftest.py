import pytest

# Configuration for Pytest

@pytest.fixture(scope="session")
def sample_fixture():
    # Setup code for the fixture
    yield 42  # Sample return value for the test
    # Teardown code for the fixture, if needed

# Additional fixtures can be added here
