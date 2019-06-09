import dominate
from dominate.tags import *

_html = html()
_body = _html.add(body())
header  = _body.add(div(id='header'))
content = _body.add(div(id='content'))
footer  = _body.add(div(id='footer'))

footer.add("thanks")

print(_html)

