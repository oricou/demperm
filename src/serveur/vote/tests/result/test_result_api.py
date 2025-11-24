from rest_framework.test import APIClient
from app.neo4j_config import get_driver
from datetime import datetime, timedelta
from django.utils import timezone


def _cleanup_neo4j():
    """
    Nettoie toutes les données de test de Neo4j.
    """
    driver = get_driver()
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")


def _create_test_votes():
    """
    Crée des données de test dans Neo4j :
    - 3 utilisateurs dans le domaine "tech"
    - 2 utilisateurs dans le domaine "design"
    - Votes avec différents counts et dates
    """
    driver = get_driver()
    with driver.session() as session:
        # Votes pour le domaine "tech"
        # User1 reçoit 100 votes
        session.run(
            """
            MERGE (v1:User {id: 'voter-1'})
            MERGE (t1:User {id: 'user-tech-1'})
            MERGE (v1)-[r:VOTED {domain: 'tech'}]->(t1)
            SET r.id = 'vote-1',
                r.count = 100,
                r.createdAt = datetime($date)
            """,
            date=(datetime.now() - timedelta(days=10)).isoformat()
        )
        
        # User2 reçoit 50 votes
        session.run(
            """
            MERGE (v2:User {id: 'voter-2'})
            MERGE (t2:User {id: 'user-tech-2'})
            MERGE (v2)-[r:VOTED {domain: 'tech'}]->(t2)
            SET r.id = 'vote-2',
                r.count = 50,
                r.createdAt = datetime($date)
            """,
            date=(datetime.now() - timedelta(days=5)).isoformat()
        )
        
        # User3 reçoit 25 votes
        session.run(
            """
            MERGE (v3:User {id: 'voter-3'})
            MERGE (t3:User {id: 'user-tech-3'})
            MERGE (v3)-[r:VOTED {domain: 'tech'}]->(t3)
            SET r.id = 'vote-3',
                r.count = 25,
                r.createdAt = datetime($date)
            """,
            date=(datetime.now() - timedelta(days=15)).isoformat()
        )
        
        # Votes pour le domaine "design"
        # User4 reçoit 80 votes
        session.run(
            """
            MERGE (v4:User {id: 'voter-4'})
            MERGE (t4:User {id: 'user-design-1'})
            MERGE (v4)-[r:VOTED {domain: 'design'}]->(t4)
            SET r.id = 'vote-4',
                r.count = 80,
                r.createdAt = datetime($date)
            """,
            date=(datetime.now() - timedelta(days=8)).isoformat()
        )
        
        # User5 reçoit 30 votes
        session.run(
            """
            MERGE (v5:User {id: 'voter-5'})
            MERGE (t5:User {id: 'user-design-2'})
            MERGE (v5)-[r:VOTED {domain: 'design'}]->(t5)
            SET r.id = 'vote-5',
                r.count = 30,
                r.createdAt = datetime($date)
            """,
            date=(datetime.now() - timedelta(days=3)).isoformat()
        )


def test_get_results_unauthorized():
    """
    Test que GET /results retourne 403 sans authentification.
    """
    client = APIClient()
    response = client.get("/results")
    assert response.status_code == 403


def test_get_results_all_domains():
    """
    Test que GET /results retourne tous les résultats sans filtre.
    Vérifie aussi la logique d'élection (≥20% des voix du domaine).
    """
    _cleanup_neo4j()
    _create_test_votes()
    
    client = APIClient()
    auth_header = "Bearer test-user"
    
    response = client.get(
        "/results",
        HTTP_AUTHORIZATION=auth_header,
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # On doit avoir 5 résultats au total
    assert len(data) == 5
    
    # Vérifier que les résultats sont triés par count décroissant
    counts = [result["count"] for result in data]
    assert counts == sorted(counts, reverse=True)
    
    # Vérifier que le premier a 100 votes (user-tech-1)
    assert data[0]["count"] == 100
    assert data[0]["userId"] == "user-tech-1"
    assert data[0]["domain"] == "tech"
    
    # Vérifier la logique d'élection
    # Domaine "tech" : 100 + 50 + 25 = 175 votes total
    # - user-tech-1 : 100/175 = 57% ✓ élu (≥20%)
    # - user-tech-2 : 50/175 = 29% ✓ élu (≥20%)
    # - user-tech-3 : 25/175 = 14% ✗ non élu (<20%)
    # Domaine "design" : 80 + 30 = 110 votes total
    # - user-design-1 : 80/110 = 73% ✓ élu (≥20%)
    # - user-design-2 : 30/110 = 27% ✓ élu (≥20%)
    
    for result in data:
        if result["userId"] == "user-tech-1":
            assert result["elected"] is True, "user-tech-1 devrait être élu (57%)"
        elif result["userId"] == "user-tech-2":
            assert result["elected"] is True, "user-tech-2 devrait être élu (29%)"
        elif result["userId"] == "user-tech-3":
            assert result["elected"] is False, "user-tech-3 ne devrait PAS être élu (14%)"
        elif result["userId"] == "user-design-1":
            assert result["elected"] is True, "user-design-1 devrait être élu (73%)"
        elif result["userId"] == "user-design-2":
            assert result["elected"] is True, "user-design-2 devrait être élu (27%)"


def test_get_results_filter_by_domain():
    """
    Test que GET /results?domain=tech filtre correctement par domaine.
    """
    _cleanup_neo4j()
    _create_test_votes()
    
    client = APIClient()
    auth_header = "Bearer test-user"
    
    response = client.get(
        "/results?domain=tech",
        HTTP_AUTHORIZATION=auth_header,
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # On doit avoir 3 résultats pour le domaine "tech"
    assert len(data) == 3
    
    # Tous les résultats doivent être du domaine "tech"
    for result in data:
        assert result["domain"] == "tech"
    
    # Vérifier l'ordre (100, 50, 25)
    assert data[0]["count"] == 100
    assert data[1]["count"] == 50
    assert data[2]["count"] == 25
    
    # Vérifier la logique d'élection pour le domaine "tech"
    # Total : 175 votes (100 + 50 + 25)
    # Seuil 20% : 35 votes
    assert data[0]["elected"] is True  # 100 votes (57%)
    assert data[1]["elected"] is True  # 50 votes (29%)
    assert data[2]["elected"] is False  # 25 votes (14%, < 20%)


def test_get_results_with_top_limit():
    """
    Test que GET /results?top=2 limite le nombre de résultats.
    """
    _cleanup_neo4j()
    _create_test_votes()
    
    client = APIClient()
    auth_header = "Bearer test-user"
    
    response = client.get(
        "/results?top=2",
        HTTP_AUTHORIZATION=auth_header,
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # On doit avoir seulement 2 résultats
    assert len(data) == 2
    
    # Les 2 premiers doivent être user-tech-1 (100) et user-design-1 (80)
    assert data[0]["count"] == 100
    assert data[1]["count"] == 80
    
    # Note : avec top=2, on a seulement 2 résultats mais de domaines différents
    # Le calcul des 20% se fait quand même sur TOUS les votes du domaine
    # user-tech-1 : 100/175 (tech total) = 57% ✓ élu
    # user-design-1 : 80/110 (design total) = 73% ✓ élu
    assert data[0]["elected"] is True
    assert data[1]["elected"] is True


def test_get_results_with_since_filter():
    """
    Test que GET /results?since=YYYY-MM-DD filtre par date.
    """
    _cleanup_neo4j()
    _create_test_votes()
    
    client = APIClient()
    auth_header = "Bearer test-user"
    
    # Filtrer les votes des 12 derniers jours pour inclure 10, 8, 5 et 3 jours
    since_date = (datetime.now() - timedelta(days=12)).strftime("%Y-%m-%d")
    
    response = client.get(
        f"/results?since={since_date}",
        HTTP_AUTHORIZATION=auth_header,
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # On doit avoir 4 résultats (votes des 10, 8, 5, et 3 derniers jours)
    # user-tech-3 (15 jours) ne doit pas apparaître
    assert len(data) == 4
    
    user_ids = [result["userId"] for result in data]
    assert "user-tech-3" not in user_ids


def test_get_results_combined_filters():
    """
    Test avec plusieurs filtres combinés : domain + top.
    """
    _cleanup_neo4j()
    _create_test_votes()
    
    client = APIClient()
    auth_header = "Bearer test-user"
    
    response = client.get(
        "/results?domain=tech&top=2",
        HTTP_AUTHORIZATION=auth_header,
    )
    
    assert response.status_code == 200
    data = response.json()
    
    # On doit avoir 2 résultats du domaine "tech"
    assert len(data) == 2
    
    for result in data:
        assert result["domain"] == "tech"
    
    # Les 2 premiers tech : 100 et 50
    assert data[0]["count"] == 100
    assert data[1]["count"] == 50


def test_get_results_invalid_top_parameter():
    """
    Test que GET /results?top=invalid retourne 400.
    """
    client = APIClient()
    auth_header = "Bearer test-user"
    
    response = client.get(
        "/results?top=invalid",
        HTTP_AUTHORIZATION=auth_header,
    )
    
    assert response.status_code == 400
    assert "error" in response.json()


def test_get_results_invalid_since_parameter():
    """
    Test que GET /results?since=invalid retourne 400.
    """
    client = APIClient()
    auth_header = "Bearer test-user"
    
    response = client.get(
        "/results?since=invalid-date",
        HTTP_AUTHORIZATION=auth_header,
    )
    
    assert response.status_code == 400
    assert "error" in response.json()


def test_get_results_empty_database():
    """
    Test que GET /results retourne une liste vide si aucun vote n'existe.
    """
    _cleanup_neo4j()
    
    client = APIClient()
    auth_header = "Bearer test-user"
    
    response = client.get(
        "/results",
        HTTP_AUTHORIZATION=auth_header,
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 0
    assert isinstance(data, list)


def test_election_threshold_20_percent():
    """
    Test spécifique de la logique d'élection : 
    Élu si ≥ 20% des voix du domaine (membre du Conseil municipal).
    
    Scénario :
    - Domaine A : 4 personnes avec 100, 30, 20, 10 votes (total: 160)
      * 100/160 = 62.5% ✓ élu
      * 30/160 = 18.75% ✗ non élu (< 20%)
      * 20/160 = 12.5% ✗ non élu
      * 10/160 = 6.25% ✗ non élu
    """
    _cleanup_neo4j()
    
    driver = get_driver()
    with driver.session() as session:
        # Créer 4 personnes dans le domaine "test"
        session.run("""
            MERGE (v1:User {id: 'voter-1'})
            MERGE (t1:User {id: 'candidate-1'})
            MERGE (v1)-[r:VOTED {domain: 'test'}]->(t1)
            SET r.id = 'vote-1', r.count = 100, r.createdAt = datetime()
        """)
        
        session.run("""
            MERGE (v2:User {id: 'voter-2'})
            MERGE (t2:User {id: 'candidate-2'})
            MERGE (v2)-[r:VOTED {domain: 'test'}]->(t2)
            SET r.id = 'vote-2', r.count = 30, r.createdAt = datetime()
        """)
        
        session.run("""
            MERGE (v3:User {id: 'voter-3'})
            MERGE (t3:User {id: 'candidate-3'})
            MERGE (v3)-[r:VOTED {domain: 'test'}]->(t3)
            SET r.id = 'vote-3', r.count = 20, r.createdAt = datetime()
        """)
        
        session.run("""
            MERGE (v4:User {id: 'voter-4'})
            MERGE (t4:User {id: 'candidate-4'})
            MERGE (v4)-[r:VOTED {domain: 'test'}]->(t4)
            SET r.id = 'vote-4', r.count = 10, r.createdAt = datetime()
        """)
    
    client = APIClient()
    auth_header = "Bearer test-user"
    
    response = client.get("/results?domain=test", HTTP_AUTHORIZATION=auth_header)
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 4
    
    # Total : 160 votes
    # Seuil 20% : 32 votes
    
    # candidate-1 : 100 votes (62.5%) ✓ élu
    assert data[0]["userId"] == "candidate-1"
    assert data[0]["count"] == 100
    assert data[0]["elected"] is True
    
    # candidate-2 : 30 votes (18.75%) ✗ non élu
    assert data[1]["userId"] == "candidate-2"
    assert data[1]["count"] == 30
    assert data[1]["elected"] is False
    
    # candidate-3 : 20 votes (12.5%) ✗ non élu
    assert data[2]["userId"] == "candidate-3"
    assert data[2]["count"] == 20
    assert data[2]["elected"] is False
    
    # candidate-4 : 10 votes (6.25%) ✗ non élu
    assert data[3]["userId"] == "candidate-4"
    assert data[3]["count"] == 10
    assert data[3]["elected"] is False