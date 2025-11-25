#!/bin/bash

BASE_URL="http://localhost:8000"

########################################
# Scénario 1 : A->C (tech), B->C (tech), C->D (tech)
########################################

A="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
B="bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
C="cccccccc-cccc-cccc-cccc-cccccccccccc"
D="dddddddd-dddd-dddd-dddd-dddddddddddd"
DOMAIN="tech"

echo "========== SCENARIO 1 : A,B (tech) -> C, puis C (tech) -> D =========="

echo "---------- A -> C (tech) ----------"
curl -X POST "$BASE_URL/votes" \
    -H "Authorization: Bearer $A" \
    -H "Content-Type: application/json" \
    -d "{\"targetUserId\": \"$C\", \"domain\": \"$DOMAIN\"}"
echo -e "\n"


echo "---------- B -> C (tech) ----------"
curl -X POST "$BASE_URL/votes" \
    -H "Authorization: Bearer $B" \
    -H "Content-Type: application/json" \
    -d "{\"targetUserId\": \"$C\", \"domain\": \"$DOMAIN\"}"
echo -e "\n"


echo "---------- C -> D (tech) ----------"
curl -X POST "$BASE_URL/votes" \
    -H "Authorization: Bearer $C" \
    -H "Content-Type: application/json" \
    -d "{\"targetUserId\": \"$D\", \"domain\": \"$DOMAIN\"}"
echo -e "\n"


echo "---------- GET votes for D (scenario 1) ----------"
curl -X GET "$BASE_URL/votes/for-user/$D" \
    -H "Authorization: Bearer $D" \
    -H "Content-Type: application/json"
echo -e "\n\n"

echo "Manuellement, vérifie (SCENARIO 1) que:"
echo "  - total == 3"
echo "  - byDomain.tech == 3"
echo


########################################
# Scénario 2 : A2 (tech) -> C2, B2 (finance) -> C2, C2 (tech) -> D2
########################################

A2="eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee"
B2="ffffffff-ffff-ffff-ffff-ffffffffffff"
C2="99999999-9999-9999-9999-999999999999"
D2="10101010-1010-1010-1010-101010101010"
DOMAIN_TECH="tech"
DOMAIN_FINANCE="finance"

echo "========== SCENARIO 2 :"
echo " A2 (tech) -> C2,"
echo " B2 (finance) -> C2,"
echo " C2 (tech) -> D2 =========="

echo "---------- A2 -> C2 (tech) ----------"
curl -X POST "$BASE_URL/votes" \
    -H "Authorization: Bearer $A2" \
    -H "Content-Type: application/json" \
    -d "{\"targetUserId\": \"$C2\", \"domain\": \"$DOMAIN_TECH\"}"
echo -e "\n"


echo "---------- B2 -> C2 (finance) ----------"
curl -X POST "$BASE_URL/votes" \
    -H "Authorization: Bearer $B2" \
    -H "Content-Type: application/json" \
    -d "{\"targetUserId\": \"$C2\", \"domain\": \"$DOMAIN_FINANCE\"}"
echo -e "\n"


echo "---------- C2 -> D2 (tech) ----------"
curl -X POST "$BASE_URL/votes" \
    -H "Authorization: Bearer $C2" \
    -H "Content-Type: application/json" \
    -d "{\"targetUserId\": \"$D2\", \"domain\": \"$DOMAIN_TECH\"}"
echo -e "\n"


echo "---------- GET votes for C2 (scenario 2) ----------"
curl -X GET "$BASE_URL/votes/for-user/$C2" \
    -H "Authorization: Bearer $C2" \
    -H "Content-Type: application/json"
echo -e "\n\n"

echo "Pour C2, tu dois voir quelque chose du genre :"
echo "  - total == 2"
echo "  - byDomain.tech == 1"
echo "  - byDomain.finance == 1"
echo


echo "---------- GET votes for D2 (scenario 2) ----------"
curl -X GET "$BASE_URL/votes/for-user/$D2" \
    -H "Authorization: Bearer $D2" \
    -H "Content-Type: application/json"
echo -e "\n\n"

echo "Pour D2 (SCENARIO 2), vérifie que :"
echo "  - total == 3"
echo "  - byDomain.tech == 3"
echo " (le vote finance sur C2 contribue quand même au poids de C2 quand il vote pour D2)"
