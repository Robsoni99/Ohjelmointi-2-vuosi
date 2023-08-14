Käyttäjä luo uuden muistiinpanon:

```mermaid
graph TD;
    Käyttäjä-->muistiinpano_lähetetään;
    muistiinpano_lähetetään-->Serveri;
    Serveri-->muistiinpano_näytetään;
    muistiinpano_näytetään-->Käyttäjä;
```
