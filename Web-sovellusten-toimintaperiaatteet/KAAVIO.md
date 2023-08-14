Käyttäjä luo uuden muistiinpanon:

```mermaid
graph TD;
    Käyttäjä-->muistiinpano lähetetään;
    muistiinpano lähetetään-->Serveri;
    Serveri-->käsittelyn jälkeen näytetään käyttäjälle;
    käsittelyn jälkeen näytetään käyttäjälle-->Käyttäjä
```
