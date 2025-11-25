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

def test_delete_vote_unauthorized():
    client = APIClient()

    response = client.delete("/votes/tech", format="json")

    assert response.status_code == 403


def test_delete_vote_not_found():
    client = APIClient()

    voter_id = "44444444-4444-4444-4444-444444444444"
    target_user_id = "55555555-5555-5555-5555-555555555555"
    domain = "tech"

    _cleanup_neo4j_for_users(voter_id, target_user_id)

    auth_header = f"Bearer {voter_id}"

    response = client.delete(
        f"/votes/{domain}",
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 404


def test_delete_vote_success_removes_relationship_in_neo4j():
    client = APIClient()

    voter_id = "66666666-6666-6666-6666-666666666666"
    target_user_id = "77777777-7777-7777-7777-777777777777"
    domain = "tech"

    _cleanup_neo4j_for_users(voter_id, target_user_id)

    payload = {
        "targetUserId": target_user_id,
        "domain": domain,
    }
    auth_header = f"Bearer {voter_id}"

    response_create = client.post(
        "/votes",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert response_create.status_code == 201

    driver = get_driver()
    with driver.session() as session:
        record_before = session.run(
            """
            MATCH (v:User {id: $voterId})-[r:VOTED {domain: $domain}]->(t:User {id: $targetUserId})
            RETURN count(r) AS rel_count
            """,
            voterId=voter_id,
            targetUserId=target_user_id,
            domain=domain,
        ).single()
        assert record_before["rel_count"] == 1

    response_delete = client.delete(
        f"/votes/{domain}",
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response_delete.status_code == 204

    with driver.session() as session:
        record_after = session.run(
            """
            MATCH (v:User {id: $voterId})-[r:VOTED {domain: $domain}]->(t:User {id: $targetUserId})
            RETURN count(r) AS rel_count
            """,
            voterId=voter_id,
            targetUserId=target_user_id,
            domain=domain,
        ).single()
        assert record_after["rel_count"] == 0


def test_get_received_votes_for_user_me_simple():
    """
    Deux utilisateurs votent pour le même target.
    Le total doit être la somme des counts de toutes les relations entrantes.
    """
    client = APIClient()

    voter1_id = "11111111-1111-1111-1111-111111111111"
    voter2_id = "22222222-2222-2222-2222-222222222222"
    target_user_id = "99999999-9999-9999-9999-999999999999"
    domain = "tech"

    _cleanup_neo4j_for_users(voter1_id, target_user_id)
    _cleanup_neo4j_for_users(voter2_id, target_user_id)

    payload = {
        "targetUserId": target_user_id,
        "domain": domain,
    }

    response1 = client.post(
        "/votes",
        payload,
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter1_id}",
    )
    assert response1.status_code == 201

    response2 = client.post(
        "/votes",
        payload,
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter2_id}",
    )
    assert response2.status_code == 201

    response_get = client.get(
        "/votes/for-user/me",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {target_user_id}",
    )

    assert response_get.status_code == 200
    data = response_get.json()

    assert data["userId"] == target_user_id
    assert data["total"] == 2
    assert data["byDomain"]["tech"] == 2

    voters = data["usersByDomain"]["tech"]
    assert set(voters) == {voter1_id, voter2_id}


def test_get_received_votes_for_user_by_id():
    """
    Même scénario que précédent, mais via /votes/for-user/{userId}
    (et on peut appeler avec n'importe quel user authentifié).
    """
    client = APIClient()

    voter1_id = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    voter2_id = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    target_user_id = "cccccccc-cccc-cccc-cccc-cccccccccccc"
    caller_id = "dddddddd-dddd-dddd-dddd-dddddddddddd"
    domain = "tech"

    _cleanup_neo4j_for_users(voter1_id, target_user_id)
    _cleanup_neo4j_for_users(voter2_id, target_user_id)

    payload = {
        "targetUserId": target_user_id,
        "domain": domain,
    }

    client.post(
        "/votes",
        payload,
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter1_id}",
    )
    client.post(
        "/votes",
        payload,
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter2_id}",
    )

    response_get = client.get(
        f"/votes/for-user/{target_user_id}",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {caller_id}",
    )

    assert response_get.status_code == 200
    data = response_get.json()

    assert data["userId"] == target_user_id
    assert data["total"] == 2
    assert data["byDomain"]["tech"] == 2
    assert set(data["usersByDomain"]["tech"]) == {voter1_id, voter2_id}


def test_get_votes_by_voter_me_lists_all_votes():
    client = APIClient()

    voter_id = "12121212-1212-1212-1212-121212121212"
    target1_id = "13131313-1313-1313-1313-131313131313"
    target2_id = "14141414-1414-1414-1414-141414141414"
    domain = "tech"

    _cleanup_neo4j_for_users(voter_id, target1_id)
    _cleanup_neo4j_for_users(voter_id, target2_id)

    payload1 = {"targetUserId": target1_id, "domain": domain}
    payload2 = {"targetUserId": target2_id, "domain": domain}

    auth_header = f"Bearer {voter_id}"

    resp1 = client.post(
        "/votes",
        payload1,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert resp1.status_code == 201

    resp2 = client.post(
        "/votes",
        payload2,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert resp2.status_code == 201

    response_get = client.get(
        "/votes/by-voter/me",
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response_get.status_code == 200
    data = response_get.json()

    assert isinstance(data, list)
    assert len(data) == 2

    voter_ids = {item["voterId"] for item in data}
    target_ids = {item["targetUserId"] for item in data}

    assert voter_ids == {voter_id}
    assert target_ids == {target1_id, target2_id}


def test_get_votes_by_voter_with_domain_filter():
    client = APIClient()

    voter_id = "15151515-1515-1515-1515-151515151515"
    target1_id = "16161616-1616-1616-1616-161616161616"
    target2_id = "17171717-1717-1717-1717-171717171717"

    _cleanup_neo4j_for_users(voter_id, target1_id)
    _cleanup_neo4j_for_users(voter_id, target2_id)

    resp1 = client.post(
        "/votes",
        {"targetUserId": target1_id, "domain": "tech"},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter_id}",
    )
    assert resp1.status_code == 201

    resp2 = client.post(
        "/votes",
        {"targetUserId": target2_id, "domain": "design"},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter_id}",
    )
    assert resp2.status_code == 201

    response_get = client.get(
        "/votes/by-voter/me?domain=tech",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter_id}",
    )

    assert response_get.status_code == 200
    data = response_get.json()

    assert len(data) == 1
    assert data[0]["domain"] == "tech"
    assert data[0]["targetUserId"] == target1_id

def test_received_votes_chain_abc_d():
    """
    Scénario de chaîne :
      A -> C
      B -> C
      C -> D

    Selon la manière dont on calcule les weights, on vérifie que
    le total de D est la somme des counts des relations entrantes.
    """
    client = APIClient()

    voter_a = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
    voter_b = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
    voter_c = "cccccccc-cccc-cccc-cccc-cccccccccccc"
    user_d = "dddddddd-dddd-dddd-dddd-dddddddddddd"
    domain = "tech"

    _cleanup_neo4j_for_users(voter_a, voter_c)
    _cleanup_neo4j_for_users(voter_b, voter_c)
    _cleanup_neo4j_for_users(voter_c, user_d)

    client.post(
        "/votes",
        {"targetUserId": voter_c, "domain": domain},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter_a}",
    )
    client.post(
        "/votes",
        {"targetUserId": voter_c, "domain": domain},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter_b}",
    )
    client.post(
        "/votes",
        {"targetUserId": user_d, "domain": domain},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter_c}",
    )

    response_get = client.get(
        f"/votes/for-user/{user_d}",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {user_d}",
    )

    assert response_get.status_code == 200
    data = response_get.json()

    assert data["byDomain"]["tech"] == data["total"]
    assert data["total"] == 3

def test_received_votes_chain_cross_domain():
    """
    Scénario de chaîne avec domaines différents :
      A -> C (tech)
      B -> C (finance)
      C -> D (tech)

    Le poids de C en tech ne doit tenir compte que des votes tech qu'il a reçus.
    Donc D ne doit recevoir que A + C (2), pas B.

    Attendu :
      - D.total == 2
      - byDomain.tech == 2
      - usersByDomain.tech == {C} (votants directs seulement)
    """
    client = APIClient()

    voter_a = "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"
    voter_b = "ffffffff-ffff-ffff-ffff-ffffffffffff"
    voter_c = "99999999-9999-9999-9999-999999999999"
    user_d = "10101010-1010-1010-1010-101010101010"
    domain_tech = "tech"
    domain_finance = "finance"

    _cleanup_neo4j_for_users(voter_a, voter_c)
    _cleanup_neo4j_for_users(voter_b, voter_c)
    _cleanup_neo4j_for_users(voter_c, user_d)

    client.post(
        "/votes",
        {"targetUserId": voter_c, "domain": domain_tech},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter_a}",
    )

    client.post(
        "/votes",
        {"targetUserId": voter_c, "domain": domain_finance},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter_b}",
    )

    client.post(
        "/votes",
        {"targetUserId": user_d, "domain": domain_tech},
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {voter_c}",
    )

    response_get = client.get(
        f"/votes/for-user/{user_d}",
        format="json",
        HTTP_AUTHORIZATION=f"Bearer {user_d}",
    )

    assert response_get.status_code == 200
    data = response_get.json()

    assert data["userId"] == user_d

    assert data["byDomain"]["tech"] == data["total"] == 2

    voters_tech = set(data["usersByDomain"]["tech"])
    assert voters_tech == {voter_c}

    assert "finance" not in data["byDomain"]

