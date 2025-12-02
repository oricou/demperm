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
    Test que GET /api/publication retourne 401 sans authentification.
    """
    client = APIClient()

    response = client.get(f"/api/publication")

    assert response.status_code == 403


def test_get_publication_setting_default_value():
    """
    Test que GET /api/publication retourne publishVotes=True et threshold=-1 par défaut
    pour un nouvel utilisateur.
    """
    client = APIClient()
    user_id = "test-user-get-default"
    
    # Nettoyage préalable
    _cleanup_neo4j_user(user_id)

    auth_header = f"Bearer {user_id}"
    response = client.get(
        f"/api/publication",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200
    data = response.json()
    
    assert "publishVotes" in data
    assert "threshold" in data
    assert data["publishVotes"] is True  # Valeur par défaut
    assert data["threshold"] == -1  # Valeur par défaut


def test_put_publication_setting_unauthorized():
    """
    Test que PUT /api/publication retourne 401 sans authentification.
    """
    client = APIClient()

    payload = {"publishVotes": False, "threshold": 10}
    response = client.put(f"/api/publication", payload, format="json")

    assert response.status_code == 403

def test_put_publication_setting_invalid_data():
    """
    Test que PUT /api/publication retourne 400 si les données sont invalides.
    """
    client = APIClient()
    user_id = "test-user-put-invalid"

    auth_header = f"Bearer {user_id}"
    
    # Payload invalide (publishVotes manquant)
    payload = {}
    response = client.put(
        f"/api/publication",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 400


def test_put_publication_setting_success_and_persisted():
    """
    Test que PUT /api/publication met à jour correctement le paramètre
    et le persiste dans Neo4j.
    """
    client = APIClient()
    user_id = "test-user-put-success"
    
    # Nettoyage préalable
    _cleanup_neo4j_user(user_id)

    auth_header = f"Bearer {user_id}"

    # 1. Mise à jour à False et 10
    payload = {"publishVotes": False, "threshold": 10}
    response = client.put(
        f"/api/publication",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["publishVotes"] is False
    assert data["threshold"] == 10

    # 2. Vérification dans Neo4j
    driver = get_driver()
    with driver.session() as session:
        record = session.run(
            """
            MATCH (u:User {id: $userId})
            RETURN u.publishVotes AS publishVotes, u.threshold AS threshold
            """,
            userId=user_id,
        ).single()

        assert record is not None
        assert record["publishVotes"] is False
        assert record["threshold"] == 10

    # 3. Mise à jour à True et 100
    payload = {"publishVotes": True, "threshold": 100}
    response = client.put(
        f"/api/publication",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["publishVotes"] is True
    assert data["threshold"] == 100

    # 4. Vérification dans Neo4j
    with driver.session() as session:
        record = session.run(
            """
            MATCH (u:User {id: $userId})
            RETURN u.publishVotes AS publishVotes, u.threshold AS threshold
            """,
            userId=user_id,
        ).single()

        assert record is not None
        assert record["publishVotes"] is True
        assert record["threshold"] == 100


def test_get_publication_setting_after_update():
    """
    Test du workflow complet: PUT puis GET pour vérifier la cohérence.
    """
    client = APIClient()
    user_id = "test-user-workflow"
    
    # Nettoyage préalable
    _cleanup_neo4j_user(user_id)

    auth_header = f"Bearer {user_id}"

    # 1. Mise à jour à False et 10
    payload = {"publishVotes": False, "threshold": 10}
    put_response = client.put(
        f"/api/publication",
        payload,
        format="json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert put_response.status_code == 200

    # 2. Récupération via GET
    get_response = client.get(
        f"/api/publication",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert get_response.status_code == 200
    
    data = get_response.json()
    assert data["publishVotes"] is False
    assert data["threshold"] == 10
