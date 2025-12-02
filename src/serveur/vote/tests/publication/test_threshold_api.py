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


def test_get_threshold_setting_unauthorized():
    """
    Test que GET /threshold/{userId} retourne 403 sans authentification.
    """
    client = APIClient()
    user_id = "test-user-threshold-get-unauth"

    response = client.get(f"/threshold/{user_id}")

    assert response.status_code == 403


def test_get_threshold_setting_default_value():
    """
    Test que GET /threshold/{userId} retourne threshold=100 par défaut
    pour un nouvel utilisateur.
    """
    client = APIClient()
    user_id = "test-user-threshold-get-default"
    
    # Nettoyage préalable
    _cleanup_neo4j_user(user_id)

    auth_header = f"Bearer {user_id}"
    response = client.get(
        f"/threshold/{user_id}",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200
    data = response.json()
    
    assert "userId" in data
    assert "threshold" in data
    assert data["userId"] == user_id
    assert data["threshold"] == 100  # Valeur par défaut


def test_put_threshold_setting_unauthorized():
    """
    Test que PUT /threshold/{userId} retourne 403 sans authentification.
    """
    client = APIClient()
    user_id = "test-user-threshold-put-unauth"

    payload = {"threshold": 50}
    response = client.put(f"/threshold/{user_id}", payload, format="json")

    assert response.status_code == 403


def test_put_threshold_setting_forbidden_other_user():
    """
    Test qu'un utilisateur ne peut pas modifier le seuil d'un autre utilisateur.
    """
    client = APIClient()
    user_id = "test-user-threshold-put-other"
    other_user_id = "test-user-threshold-put-other-target"

    # L'utilisateur user_id tente de modifier le seuil de other_user_id
    auth_header = f"Bearer {user_id}"
    payload = {"threshold": 50}
    
    response = client.put(
        f"/threshold/{other_user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 403
    assert "Forbidden" in response.json()["error"]


def test_put_threshold_setting_invalid_data():
    """
    Test que PUT /threshold/{userId} retourne 400 si les données sont invalides.
    """
    client = APIClient()
    user_id = "test-user-threshold-put-invalid"

    auth_header = f"Bearer {user_id}"
    
    # Test 1: threshold manquant
    payload = {}
    response = client.put(
        f"/threshold/{user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert response.status_code == 400

    # Test 2: threshold négatif
    payload = {"threshold": -10}
    response = client.put(
        f"/threshold/{user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert response.status_code == 400


def test_put_threshold_setting_success_and_persisted():
    """
    Test que PUT /threshold/{userId} met à jour correctement le seuil
    et le persiste dans Neo4j.
    """
    client = APIClient()
    user_id = "test-user-threshold-put-success"
    
    # Nettoyage préalable
    _cleanup_neo4j_user(user_id)

    auth_header = f"Bearer {user_id}"

    # 1. Mise à jour à 50
    payload = {"threshold": 50}
    response = client.put(
        f"/threshold/{user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["userId"] == user_id
    assert data["threshold"] == 50

    # 2. Vérification dans Neo4j
    driver = get_driver()
    with driver.session() as session:
        record = session.run(
            """
            MATCH (u:User {id: $userId})
            RETURN u.threshold AS threshold
            """,
            userId=user_id,
        ).single()

        assert record is not None
        assert record["threshold"] == 50

    # 3. Mise à jour à 200
    payload = {"threshold": 200}
    response = client.put(
        f"/threshold/{user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["threshold"] == 200

    # 4. Vérification dans Neo4j
    with driver.session() as session:
        record = session.run(
            """
            MATCH (u:User {id: $userId})
            RETURN u.threshold AS threshold
            """,
            userId=user_id,
        ).single()

        assert record is not None
        assert record["threshold"] == 200


def test_get_threshold_setting_after_update():
    """
    Test du workflow complet: PUT puis GET pour vérifier la cohérence.
    """
    client = APIClient()
    user_id = "test-user-threshold-workflow"
    
    # Nettoyage préalable
    _cleanup_neo4j_user(user_id)

    auth_header = f"Bearer {user_id}"

    # 1. Mise à jour à 75
    payload = {"threshold": 75}
    put_response = client.put(
        f"/threshold/{user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert put_response.status_code == 200

    # 2. Récupération via GET
    get_response = client.get(
        f"/threshold/{user_id}",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert get_response.status_code == 200
    
    data = get_response.json()
    assert data["userId"] == user_id
    assert data["threshold"] == 75


def test_put_threshold_setting_zero_is_valid():
    """
    Test que threshold=0 est une valeur valide.
    """
    client = APIClient()
    user_id = "test-user-threshold-zero"
    
    # Nettoyage préalable
    _cleanup_neo4j_user(user_id)

    auth_header = f"Bearer {user_id}"

    # Mise à jour à 0
    payload = {"threshold": 0}
    response = client.put(
        f"/threshold/{user_id}",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["threshold"] == 0
