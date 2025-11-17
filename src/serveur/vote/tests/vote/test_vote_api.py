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


def _cleanup_neo4j_for_users(voter_id: str, target_user_id: str):
    """
    Supprime les noeuds et relations pour ces IDs,
    pour rendre les tests déterministes.
    """
    driver = get_driver()
    with driver.session() as session:
        session.run(
            """
            MATCH (u:User)
            WHERE u.id IN [$voterId, $targetUserId]
            DETACH DELETE u
            """,
            voterId=voter_id,
            targetUserId=target_user_id,
        )


def test_create_vote_success_and_persisted_in_neo4j():
    client = APIClient()

    voter_id = "11111111-1111-1111-1111-111111111111"
    target_user_id = "22222222-2222-2222-2222-222222222222"
    domain = "tech"

    _cleanup_neo4j_for_users(voter_id, target_user_id)

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
            MATCH (v:User {id: $voterId})-[r:VOTED {domain: $domain}]->(t:User {id: $targetUserId})
            RETURN r.id AS rel_id, r.count AS rel_count
            """,
            voterId=voter_id,
            targetUserId=target_user_id,
            domain=domain,
        ).single()

        assert record is not None
        assert record["rel_id"] == data["id"]
        assert record["rel_count"] == 1


def test_create_vote_twice_increments_count():
    """
    Même voter, même target, même domain → une seule relation mais count qui s'incrémente.
    """
    client = APIClient()

    voter_id = "11111111-1111-1111-1111-111111111111"
    target_user_id = "33333333-3333-3333-3333-333333333333"
    domain = "tech"

    _cleanup_neo4j_for_users(voter_id, target_user_id)

    payload = {
        "targetUserId": target_user_id,
        "domain": domain,
    }

    auth_header = f"Bearer {voter_id}"

    response1 = client.post(
        "/votes",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert response1.status_code == 201

    response2 = client.post(
        "/votes",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert response2.status_code == 201

    driver = get_driver()
    with driver.session() as session:
        record = session.run(
            """
            MATCH (v:User {id: $voterId})-[r:VOTED {domain: $domain}]->(t:User {id: $targetUserId})
            RETURN r.count AS rel_count
            """,
            voterId=voter_id,
            targetUserId=target_user_id,
            domain=domain,
        ).single()

        assert record is not None
        assert record["rel_count"] == 2
