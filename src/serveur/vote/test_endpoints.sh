#!/bin/bash

BASE_URL="http://localhost:8000/api"

echo "=============================================================="
echo "   🔵 TEST GLOBAL DE L'API - VOTES / PUBLICATION / STATS / RESULTS"
echo "=============================================================="

########################################
# 📌 Identifiants de test
########################################
U1="11111111-1111-1111-1111-111111111111"
U2="22222222-2222-2222-2222-222222222222"
U3="33333333-3333-3333-3333-333333333333"
U4="44444444-4444-4444-4444-444444444444"

DOMAIN_TECH="tech"
DOMAIN_SPORT="sport"

echo
echo "=============================================================="
echo "   1️⃣  TEST ENDPOINTS PUBLICATION : GET & PUT "
echo "=============================================================="

echo "---- GET /api/publication (U1) ----"
curl -X GET "$BASE_URL/publication" \
    -H "Authorization: Bearer $U1"
echo -e "\n"

echo "---- PUT /api/publication (U1) -> publishVotes=true, threshold=50 ----"
curl -X PUT "$BASE_URL/publication" \
    -H "Authorization: Bearer $U1" \
    -H "Content-Type: application/json" \
    -d '{"publishVotes": true, "threshold": 50}'
echo -e "\n"


echo
echo "=============================================================="
echo "   2️⃣  TEST ENDPOINTS VOTES : POST / DELETE / LISTING"
echo "=============================================================="

echo "---- U1 -> U3 (tech) ----"
curl -X POST "$BASE_URL/votes" \
    -H "Authorization: Bearer $U1" \
    -H "Content-Type: application/json" \
    -d "{\"targetUserId\": \"$U3\", \"domain\": \"$DOMAIN_TECH\"}"
echo -e "\n"

echo "---- U2 -> U3 (sport) ----"
curl -X POST "$BASE_URL/votes" \
    -H "Authorization: Bearer $U2" \
    -H "Content-Type: application/json" \
    -d "{\"targetUserId\": \"$U3\", \"domain\": \"$DOMAIN_SPORT\"}"
echo -e "\n"

echo "---- U3 -> U4 (tech) ----"
curl -X POST "$BASE_URL/votes" \
    -H "Authorization: Bearer $U3" \
    -H "Content-Type: application/json" \
    -d "{\"targetUserId\": \"$U4\", \"domain\": \"$DOMAIN_TECH\"}"
echo -e "\n"



echo "---- GET /api/votes/by-user/U3 ----"
curl -X GET "$BASE_URL/votes/by-user/$U3" \
    -H "Authorization: Bearer $U3"
echo -e "\n"


echo "---- GET /api/votes/by-voter/me (U1) ----"
curl -X GET "$BASE_URL/votes/by-voter/me" \
    -H "Authorization: Bearer $U1"
echo -e "\n"


echo "---- DELETE /api/votes/{domain} : suppression de U1->U3 (tech) ----"
curl -X DELETE "$BASE_URL/votes/$DOMAIN_TECH" \
    -H "Authorization: Bearer $U1"
echo -e "\n"

echo
echo "=============================================================="
echo "   3️⃣  TEST ENDPOINT RESULTS : /api/results"
echo "=============================================================="

echo "---- GET /api/results ----"
curl -X GET "$BASE_URL/results" \
    -H "Authorization: Bearer $U1"
echo -e "\n"

echo "---- GET /api/results?domain=tech ----"
curl -X GET "$BASE_URL/results?domain=tech" \
    -H "Authorization: Bearer $U1"
echo -e "\n"

echo "---- GET /api/results?top=5 ----"
curl -X GET "$BASE_URL/results?top=5" \
    -H "Authorization: Bearer $U1"
echo -e "\n"

echo "---- GET /api/results?since=2024-01-01 ----"
curl -X GET "$BASE_URL/results?since=2024-01-01" \
    -H "Authorization: Bearer $U1"
echo -e "\n"


echo
echo "=============================================================="
echo "   4️⃣  TEST ENDPOINT STATS : DAILY / MONTHLY / CHART"
echo "=============================================================="

echo "---- GET /stats/votes/daily/{U3} ----"
curl -X GET "$BASE_URL/stats/votes/daily/$U3" \
    -H "Authorization: Bearer $U3"
echo -e "\n"

echo "---- GET /stats/chart ----"
curl -X GET "$BASE_URL/stats/chart" \
    -H "Authorization: Bearer $U1"
echo -e "\n"


echo
echo "=============================================================="
echo "  🎉 FIN DU TEST – TOUS LES ENDPOINTS ONT ÉTÉ APPELÉS "
echo "=============================================================="
