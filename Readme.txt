This application allows users to browse and select a PDF template containing tokens like [[name]].
Once the template is selected the system will detect all tokens present in the PDF and generate a
form for the user to fill out. After the users submits the form, the system will search and replace
the tokens with the users data and generate new document. THe user will br presented with a link
to the document so they can view it in thier browser or download it.


This is a python 3 flask app.

You will need python 3 installed to use it.

Change directory into the top level folder...
 'cd dynamic-document-generation'

Run flask
 'flask --app app run'

Open in a web browser. It will create a server and return a url that looks something like this...
 'http://127.0.0.1:5000'

