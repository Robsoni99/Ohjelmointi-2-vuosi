```mermaid
sequenceDiagram
    participant selain
    participant serveri
    
    selain->>serveri: https://studies.cs.helsinki.fi/exampleapp/notes
    serveri-->>selain: HTML
    
    selain->>serveri: https://studies.cs.helsinki.fi/exampleapp/main.css
    serveri-->>sealin: CSS
    
    selain->>serveri: GET https://studies.cs.helsinki.fi/exampleapp/main.js
    serveri-->>selain: JS
        
    selain->>serveri: https://studies.cs.helsinki.fi/exampleapp/data.json
    serveri-->>selain: Muistiinpanot
```
