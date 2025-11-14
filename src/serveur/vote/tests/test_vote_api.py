import uuid

from rest_framework.test import APIClient
from app.neo4j_config import get_driver


def test_create_vote_unauthorized():
    client = APIClient()

    payload = {
        "targetUserId": "22222222-2222-2222-2222-222222222222",
        "domain": "tech",
    }

    response = client.post("/votes", payload, format="json")

    assert response.status_code == 403


def test_create_vote_success_and_persisted_in_neo4j():
    client = APIClient()

    voter_id = "11111111-1111-1111-1111-111111111111"
    target_user_id = "22222222-2222-2222-2222-222222222222"
    domain = "tech"

    payload = {
        "targetUserId": target_user_id,
        "domain": domain,
    }

    auth_header = f"Bearer {voter_id}"

    response = client.post(
        "/votes",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 201

    data = response.json()

    for field in ["id", "voterId", "targetUserId", "domain", "createdAt"]:
        assert field in data

    assert data["voterId"] == voter_id
    assert data["targetUserId"] == target_user_id
    assert data["domain"] == domain

    uuid.UUID(data["id"])

    driver = get_driver()
    with driver.session() as session:
        record = session.run(
            """
            MATCH (v:User {id: $voterId})-[r:VOTED {id: $voteId}]->(t:User {id: $targetUserId})
            RETURN count(r) AS rel_count
            """,
            voterId=voter_id,
            targetUserId=target_user_id,
            voteId=data["id"],
        ).single()

        assert record is not None
        assert record["rel_count"] == 1
