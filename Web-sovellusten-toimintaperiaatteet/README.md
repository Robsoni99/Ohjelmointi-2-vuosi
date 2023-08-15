```mermaid
sequenceDiagram
    participant selain
    participant serveri
    
    selain->>serveri: pyytää https://studies.cs.helsinki.fi/exampleapp/notes
    serveri-->>selain: HTML
    
    selain->>serveri: pyytää https://studies.cs.helsinki.fi/exampleapp/main.css
    serveri-->>selain: CSS
    
    selain->>serveri: pyytää https://studies.cs.helsinki.fi/exampleapp/main.js
    serveri-->>selain: JS
        
    selain->>serveri: pyytää https://studies.cs.helsinki.fi/exampleapp/data.json
    serveri-->>selain: Muistiinpanot
```
