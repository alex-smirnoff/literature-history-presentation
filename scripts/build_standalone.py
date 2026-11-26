import base64
import mimetypes
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT
def data_uri(file):
    mime={'.webp':'image/webp','.woff2':'font/woff2'}.get(file.suffix) or mimetypes.guess_type(file.name)[0] or 'application/octet-stream'
    return 'data:'+mime+';base64,'+base64.b64encode(file.read_bytes()).decode('ascii')
def css_resource(match):
    resource=match.group(1).strip().strip('"\'')
    if resource.startswith('data:'):
        return match.group(0)
    path=DIST/resource
    return 'url("'+data_uri(path)+'")' if path.is_file() else match.group(0)

html=(DIST/'index.html').read_text(encoding='utf-8')
for name in ['styles.css','research.css']:
    css=re.sub(r'url\(([^)]+)\)',css_resource,(DIST/name).read_text(encoding='utf-8'))
    html=html.replace('<link rel="stylesheet" href="'+name+'">','<style>\n'+css+'\n</style>')
js=(DIST/'script.js').read_text(encoding='utf-8')
for file in (DIST/'assets/scene').glob('*.webp'):
    js=js.replace('assets/scene/'+file.name,data_uri(file))
html=html.replace('<script src="script.js"></script>','<script>\n'+js+'\n</script>')
output=ROOT/'Presentation.html'
output.write_text(html,encoding='utf-8')
print('Built:', output.name, output.stat().st_size, 'bytes')
