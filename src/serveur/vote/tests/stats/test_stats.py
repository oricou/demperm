from rest_framework.test import APIClient
from app.neo4j_config import get_driver
import pytest

@pytest.fixture(scope="session")
def driver():
    driver = get_driver()  # ta fonction d'application
    yield driver
    driver.close()

@pytest.fixture(autouse=True, scope="module")
def clean_db(driver):
    yield
    with driver.session(database="neo4j") as session:
        session.run("MATCH (n) DETACH DELETE n")

@pytest.fixture(scope="module")
def sample_data(driver):
    with driver.session(database="neo4j") as session:
        session.run("""
            CREATE (u:User {id: '1' , domain: 'france'})
            CREATE (u2:User {id: '2', domain: 'france'})
            CREATE (u3:User {id: '3', domain: 'france'})
            CREATE (u4:User {id: '4', domain: 'france'})
            CREATE (u5:User {id: '5', domain: 'france'})
            CREATE (u)-[:VOTED {created_at: datetime(), count: 1}]->(u2)
            CREATE (u2)-[:VOTED {created_at: datetime("2025-02-14T15:30:00Z"), count: 2}]->(u4)
            CREATE (u3)-[:VOTED {created_at: datetime("2025-11-15T15:30:00Z"), count:1}]->(u4)
            CREATE (u5)-[:VOTED {created_at: datetime(), count: 3}]->(u4)
        """)

def test_get_daily_unauth(driver):
    """
    Test que GET /api/stats/vote/daily/{userId} retourne 403 sans authentification.
    """
    client = APIClient()
    user_id = "test-user-get-unauth"

    response = client.get(f"/api/stats/votes/daily/{user_id}")

    assert response.status_code == 403


def test_get_daily(sample_data, driver):
    client = APIClient()
    user_id = "4"

    auth_header = f"Bearer {user_id}"
    response = client.get(
        f"/api/stats/votes/daily/{user_id}",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200

    data = response.json()
    print(data)
    assert data['userId'] == user_id
    assert len(data['daily']) == 3
    assert data['daily'][0]['count'] == 3
    assert data['delta'] == 3

def test_get_monthly_unauth(driver):
    """
    Test que GET /api/stats/vote/monthly/{userId} retourne 403 sans authentification.
    """
    client = APIClient()
    user_id = "test-user-get-unauth"

    response = client.get(f"/api/stats/votes/monthly/{user_id}")

    assert response.status_code == 403


def test_get_monthly(sample_data, driver):
    client = APIClient()
    user_id = "4"

    auth_header = f"Bearer {user_id}"
    response = client.get(
        f"/api/stats/votes/monthly/{user_id}",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200

    data = response.json()
    print(data)
    assert data['userId'] == user_id
    assert len(data['monthly']) == 3
    assert data['monthly'][0]['count'] == 3
    assert data['delta'] == 3

def test_chart_unauth(driver):
    """
    Test que GET /api/stats/chart retourne 403 sans authentification.
    """
    client = APIClient()

    response = client.get(f"/api/stats/chart")

    assert response.status_code == 403


def test_chart(sample_data, driver):
    client = APIClient()

    auth_header = f"Bearer 4"
    response = client.get(
        f"/api/stats/chart",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200

    data = response.json()
    print(data)
    assert len(data) == 1
    first_chart = data[0]
    assert first_chart['domain'] == 'france'
    assert len(first_chart['users']) == 1
    first_user = first_chart['users'][0]
    assert first_user['userId'] == '4'
    assert len(first_user['votes']) == 2
    first_vote = first_user['votes'][0]
    assert first_vote['count'] == 3
