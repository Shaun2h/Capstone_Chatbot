# Capstone_Chatbot
Capstone Final Product, used in the showcase.<br>
Python 3.7++<br>
Required packages:<br>
1. Django<br>
2. Python-barcode<br>
3. Snips NLU library<br>
4. Snips NLU English language support library<br>
5. Microsoft Azure Cognitive services<br>
6. Python docx - for printing of picklist/labels<br>
7. Python Selenium Webdriver, for the chatbot to search relevant items.<br>

```
python -m pip install Django
python -m pip install python-barcode
python -m pip install snips-nlu
python -m pip install azure-cognitiveservices-speech
python -m pip install python-docx
python -m pip install selenium
```
OR 
for convenience:
```
python -m pip install --upgrade pip 
python -m pip install azure-cognitiveservices-speech snips-nlu-en snips-nlu python-barcode Django python-docx selenium
```
To start:<br>
```
python manage.py runserver
```
'http:127.0.0.1:8000' or 'http:/localhost:8000/'<br>
Admin is currently enabled on the server.<br>
http:127.0.0.1:8000/` brings you to the various templates available.<br>
http:127.0.0.1:8000/models` brings you to the models pages. These  are loaded from iframes in the actual pages to allow a visible model.<br>
For simplicity, Admin username is admin, password is adminpassword. This needs to be changed based off documentation.

Further Documentation can be granted upon request.
