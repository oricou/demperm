# Mock server

## Dépendance

Depuis le dossier `src.client/web/`, lancer:

```sh
npm i
```

## Pour lancer le serveur:

Depuis le dossier `src.client/web/`, lancer:

```sh
npx msw init public/
```

## Test depuis le naviguateur:

Lancer l'application avec:
```sh
npm run dev
```
et ouvrir l'application dans le naviguateur.

Dans la console du naviguateur, lancer:

```js
// Script de test complet
async function testMockServer() {
  console.log('🚀 Début des tests...\n');
  
  try {
    // 1. Login
    console.log('1️⃣ Test Login...');
    const loginRes = await fetch('/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'alice', password: 'test123' })
    });
    const loginData = await loginRes.json();
    console.log('✅ Login:', loginData.user.pseudo);
    localStorage.setItem('token', loginData.token);
    
    const token = loginData.token;
    
    // 2. Profil
    console.log('\n2️⃣ Test Profil...');
    const profileRes = await fetch('/users/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const profileData = await profileRes.json();
    console.log('✅ Profil:', profileData.pseudo);
    
    // 3. Domaines
    console.log('\n3️⃣ Test Domaines...');
    const domainsRes = await fetch('/api/domains', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const domainsData = await domainsRes.json();
    console.log('✅ Domaines:', domainsData.length, 'domaines');
    
    // 4. Mes votes
    console.log('\n4️⃣ Test Mes votes...');
    const votesRes = await fetch('/api/votes/by-voter/me', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const votesData = await votesRes.json();
    console.log('✅ Mes votes:', votesData.length, 'votes');
    
    // 5. Dashboard
    console.log('\n5️⃣ Test Dashboard...');
    const dashboardRes = await fetch('/api/dashboard/vote', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const dashboardData = await dashboardRes.json();
    console.log('✅ Dashboard:', {
      totalVoix: dashboardData.mesVoix.totalVotesUser,
      nbDomaines: dashboardData.mesVoix.parDomaine.length
    });
    
    // 6. Résultats
    console.log('\n6️⃣ Test Résultats...');
    const resultsRes = await fetch('/api/results?top=5', {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    const resultsData = await resultsRes.json();
    console.log('✅ Résultats:', resultsData.length, 'résultats');
    
    console.log('\n🎉 Tous les tests ont réussi !');
    
  } catch (error) {
    console.error('❌ Erreur:', error);
  }
}

// Lancer les tests
testMockServer();
```