import os
from aiohttp import web
from jinja2 import Template

CDN_URL = "https://media.madliar.com"


def render_to_response(template, context=None):
    try:
        with open(template, encoding="utf-8") as f:
            template_context = f.read()
    except IOError:
        template_context = "<center><h3>Template Does Not Existed!</h3></center>"

    template = Template(template_context)
    return web.Response(text=template.render(context or {}), content_type="text/html")


async def index(request):
    image_files = os.listdir("./img")
    music_files = os.listdir("./mp3")
    context = {
        "title": "grafana",
        "CDN_URL": CDN_URL,
        "background_images": ["/img/" + img for img in image_files],
        "background_musics": ["/mp3/" + mp3 for mp3 in music_files],
    }
    return render_to_response("index.html", context=context)


app = web.Application()
app.router.add_get('/', index)
app.router.add_static("/mp3", "./mp3")
app.router.add_static("/img", "./img")
web.run_app(app, port=1024)
