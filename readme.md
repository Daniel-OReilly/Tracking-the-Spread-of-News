#CPSC 473: Data Mining Project
This project has been completed in requirement of the CSPSC 473 syllabus

This project is titled "News Travels? - A Quantitative Approach to Understanding the Scope and Spread of Localized News Events"

##Team Members
* Daniel O'Reilly - 230096504
* Michael Lane - 230130236
* Cem Gumucineli - 230124214

##Installation
Use the package manager  [pip](https://pip.pypa.io/en/stable/) to install the following dependencies 
```bash
pip install folium
pip install geopy
pip install sklearn
pip install scipy
pip install nltk
pip install newspaper3k
pip install reverse_geocoder
pip install search-engine-parser
```
##Usage
The program takes three parameters:
* location: (e.g. Kitimat)
* search radius: (e.g. 100)
* headline limit: (e.g. 20)
```bash
python main.py Kitimat 100 20
```

##Output 
The output of this program will automatically open in an HTML window

##Questions
If there are any problems please email oreilly@unbc.ca immediately

##General Notes
To keep run time down we suggest implementations on small town areas, with greater search radiuses.
Running the program in densely  populated areas increases run time drastically. 

This program has been extensively tested on Windows, if using any other Operating System
Ensure that the data and key folder are created, if not recognized