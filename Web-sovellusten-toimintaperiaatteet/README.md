Käyttäjä luo uuden muistiinpanon:

```mermaid
graph TD;
    Käyttäjä-->muistiinpano_lähetetään;
    muistiinpano_lähetetään-->Serveri;
    Serveri-->muistiinpano_näytetään;
    muistiinpano_näytetään-->Käyttäjä;
```


```mermaid
graph TD;
    browser->>server: GET https://studies.cs.helsinki.fi/exampleapp/notes
    activate server
    server-->>browser: HTML document
    deactivate server
    
    browser->>server: GET https://studies.cs.helsinki.fi/exampleapp/main.css
    activate server
    server-->>browser: the css file
    deactivate server
    
    browser->>server: GET https://studies.cs.helsinki.fi/exampleapp/main.js
    activate server
    server-->>browser: the JavaScript file
    deactivate server
    
    Note right of browser: The browser starts executing the JavaScript code that fetches the JSON from the server
    
    browser->>server: GET https://studies.cs.helsinki.fi/exampleapp/data.json
    activate server
    server-->>browser: [{ "content": "HTML is easy", "date": "2023-1-1" }, ... ]
    deactivate server

```
