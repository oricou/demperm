from rest_framework.test import APIClient
from app.neo4j_config import get_driver


def _cleanup_neo4j_user(user_id: str):
    """
    Supprime un utilisateur de Neo4j pour rendre les tests déterministes.
    """
    driver = get_driver()
    with driver.session() as session:
        session.run(
            """
            MATCH (u:User {id: $userId})
            DETACH DELETE u
            """,
            userId=user_id,
        )


def test_get_publication_setting_unauthorized():
    """
    Test que GET /publication/{userId} retourne 403 sans authentification.
    """
    client = APIClient()
    user_id = "test-user-get-unauth"

    response = client.get(f"/publication/{user_id}")

    assert response.status_code == 403


def test_get_publication_setting_default_value():
    """
    Test que GET /publication/{userId} retourne publishVotes=True par défaut
    pour un nouvel utilisateur.
    """
    client = APIClient()
    user_id = "test-user-get-default"
    
    # Nettoyage préalable
    _cleanup_neo4j_user(user_id)

    auth_header = f"Bearer {user_id}"
    response = client.get(
        f"/publication/{user_id}",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200
    data = response.json()
    
    assert "userId" in data
    assert "publishVotes" in data
    assert data["userId"] == user_id
    assert data["publishVotes"] is True  # Valeur par défaut


def test_put_publication_setting_unauthorized():
    """
    Test que PUT /publication/{userId} retourne 403 sans authentification.
    """
    client = APIClient()
    user_id = "test-user-put-unauth"

    payload = {"publishVotes": False}
    response = client.put(f"/publication/{user_id}", payload, format="json")

    assert response.status_code == 403


def test_put_publication_setting_forbidden_other_user():
    """
    Test qu'un utilisateur ne peut pas modifier les paramètres d'un autre utilisateur.
    """
    client = APIClient()
    user_id = "test-user-put-other"
    other_user_id = "test-user-put-other-target"

    # L'utilisateur user_id tente de modifier les paramètres de other_user_id
    auth_header = f"Bearer {user_id}"
    payload = {"publishVotes": False}
    
    response = client.put(
        f"/publication/{other_user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 403
    assert "Forbidden" in response.json()["error"]


def test_put_publication_setting_invalid_data():
    """
    Test que PUT /publication/{userId} retourne 400 si les données sont invalides.
    """
    client = APIClient()
    user_id = "test-user-put-invalid"

    auth_header = f"Bearer {user_id}"
    
    # Payload invalide (publishVotes manquant)
    payload = {}
    response = client.put(
        f"/publication/{user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 400


def test_put_publication_setting_success_and_persisted():
    """
    Test que PUT /publication/{userId} met à jour correctement le paramètre
    et le persiste dans Neo4j.
    """
    client = APIClient()
    user_id = "test-user-put-success"
    
    # Nettoyage préalable
    _cleanup_neo4j_user(user_id)

    auth_header = f"Bearer {user_id}"

    # 1. Mise à jour à False
    payload = {"publishVotes": False}
    response = client.put(
        f"/publication/{user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["userId"] == user_id
    assert data["publishVotes"] is False

    # 2. Vérification dans Neo4j
    driver = get_driver()
    with driver.session() as session:
        record = session.run(
            """
            MATCH (u:User {id: $userId})
            RETURN u.publishVotes AS publishVotes
            """,
            userId=user_id,
        ).single()

        assert record is not None
        assert record["publishVotes"] is False

    # 3. Mise à jour à True
    payload = {"publishVotes": True}
    response = client.put(
        f"/publication/{user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["publishVotes"] is True

    # 4. Vérification dans Neo4j
    with driver.session() as session:
        record = session.run(
            """
            MATCH (u:User {id: $userId})
            RETURN u.publishVotes AS publishVotes
            """,
            userId=user_id,
        ).single()

        assert record is not None
        assert record["publishVotes"] is True


def test_get_publication_setting_after_update():
    """
    Test du workflow complet: PUT puis GET pour vérifier la cohérence.
    """
    client = APIClient()
    user_id = "test-user-workflow"
    
    # Nettoyage préalable
    _cleanup_neo4j_user(user_id)

    auth_header = f"Bearer {user_id}"

    # 1. Mise à jour à False
    payload = {"publishVotes": False}
    put_response = client.put(
        f"/publication/{user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert put_response.status_code == 200

    # 2. Récupération via GET
    get_response = client.get(
        f"/publication/{user_id}",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert get_response.status_code == 200
    
    data = get_response.json()
    assert data["userId"] == user_id
    assert data["publishVotes"] is False
