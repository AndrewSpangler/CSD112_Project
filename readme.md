## Project Proposal

### <center>Modular Portfolio site</center>

#### Tools and technologies:

Frontend:
    
    - HTML
    - CSS
    - JS

Backend:

    - Python 
    - Flask
    - Jinja Templating
    
#### Goals:
Develop a modular portfolio site using dynamically loaded self-contained modules.


#### File Structure:
```
src/Site/
├─app.py             <- Application entry point
├─static/            <- shared static files folder
│ └─css/
│   └─core.css       <- CSS shared by all pages
├─templates/         <- shared static files folder
│ └─core.html        <- HTML shared by all pages
├─modules/           <- Dynamic modules folder
│ ├─index/           <- Index page module
│ │ ├─module.py      <- Module load point
│ │ ├─static/        <- Module's static folder
│ │ │ └─css/
│ │ │   └─index.css  <- Index page CSS
│ │ └─templates/     <- Module's static folder
│ │   └─index.html   <- Index page HTML
│ ├─module1/         <- Other module
│ │ ├─module.py      <- Load point
│ │ ├─static/        <- Module's static folder
│ │ │ └─css/
│ │ │   └─module1.css <- Module CSS
│ │ └─templates/      <- module's static folder
│ │   └─ module1.html <- Index page HTML
etc...
```
