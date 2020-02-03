import cgi, cgitb

import Cookie

form=cgi.FieldStorage
username=form["username"].value
email=form["emailaddress"].value
print("Content-type:text/html\r\n\r\n")
print("<html>")
print("<head>")
print("<title>my first CGI app</title>")
print("</head>")
print("<body>")
print("<h3>this is html body Section</h3>")
print(username)
print(email)
print("</body>")
print("</html>")