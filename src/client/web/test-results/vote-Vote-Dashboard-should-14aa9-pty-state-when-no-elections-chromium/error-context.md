# Page snapshot

```yaml
- generic [ref=e5]:
  - heading "Connexion" [level=3] [ref=e7]
  - generic [ref=e9]:
    - generic [ref=e10]:
      - generic [ref=e11]: Email
      - textbox "Email" [ref=e12]:
        - /placeholder: vous@exemple.com
        - text: alice@example.com
    - generic [ref=e13]:
      - generic [ref=e14]:
        - generic [ref=e15]: Mot de passe
        - textbox "Mot de passe" [ref=e16]:
          - /placeholder: ••••••••
          - text: test123
      - button "Afficher le mot de passe" [ref=e17] [cursor=pointer]
    - generic [ref=e18]: Erreur de connexion
    - button "Se connecter" [active] [ref=e19] [cursor=pointer]
    - generic [ref=e20]: Mot de passe oublié ?
```