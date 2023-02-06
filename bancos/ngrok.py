#! ngrok authtoken 2KEMjIdLEFH0xJV0B6RmLb0vit7_6qxoWSZ9B8KPYbj64SwwG
from pyngrok import ngrok

public_url = ngrok.connect('8050')
print(public_url)