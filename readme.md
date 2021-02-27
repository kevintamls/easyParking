# streetParkingSafe: A concept for smart street parking in Hong Kong

## A submission from Team Degenerate

A proof of concept for smart parking (as a web app, ultimately as a mobile app) for Hong Kong where number of on street parking far outweighs demand. The application would be able to leverage IOT enabled devices such as pressure sensors physically installed on the ground and in the future image recognition technology using neural networks to detect the occupancy of on street parking in any particular street and offer a 3 colour model (red, amber, green) to show likelihood of space availability both in real time and in the future.

## How To Install

1. Clone the repository into your respective directory.
2. Change directory into repository.
3. Confirm that python version 3.8.5 and pip3 has been installed.
4. Using your desired terminal, install required dependencies by typing

    ```(bash)
    pip3 install -r requirements.txt
    ```

5. Run by typing

```(bash)
python3 app.py
```

## Sections of implementation

### Backend: Flask and Python

Pre-processing of data and the backend of the application has been designed and coded in Python and the use of Flask, a web based UWSGI web framework. Due to the size of the competition and the scope of the project, a full production based Flask project structure was not used. Instead, all backend assets are placed into 2 main python files, convertCoordinates.py and app.py. Flask is located in app.py, where the initialisation of the Flask app and demo data is processed. convertCoordinates.py was written to convert the HK 1980 grid coordinate system that the HK Transport Depart parking spots CSV had into longitude/latitude coordinates that is compatible with our frontend technology stack. Implementation of an web API from the Survey and Mapping Office of the Land's Department in Hong Kong was completed.

### Frontend: JavaScript, Mapbox, JQuery, AJAX, HTML, CSS

The frontend generation and visualisation of the page has been designed in JavaScript, JQuery and AJAX. MapBox was the choice for the map functionality of the page and layout has been modified minimally with CSS. The flexibility and common deployment of JavaScript in modern day websites made it an easy choice, whilst the use of MapBox was based on its API and the use of OpenStreetMap, a open source free for all alternative to other solutions such as Google Maps.