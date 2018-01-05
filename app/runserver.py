from app import app
import sys

from core.views import core

app.register_blueprint(core, url_prefix='/core')

# Sets the port, or defaults to 80
if (len(sys.argv) > 1):
    port = int(sys.argv[1])
else:
    port=80

app.run(debug=True, host='127.0.0.1', port=port)
