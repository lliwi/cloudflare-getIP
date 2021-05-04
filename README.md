## Cloudflare getIP
cloudflare-getIP es un pequeño script en python3 que nos facilita la tarea de obtener la IP real de servicios web que usan el servicio de Cloudflare.

Busca la información en tres fuentes distintas:
.crimeflare.
.dnsdumpster.
.shodan

## Instalación
Para realizar la instalación descargamos el código e instalamos los requisitos:
```bash
$ git clone https://github.com/lliwi/cloudflare-getIP.git
$ pip3 install -r requierements.txt
```

## Uso
```bash
$ python3 cloudflare-getIP.py [url]
```

## Nota
Es necesario ser miembro de shodan o disponer de un plan para poder usar la búsqueda. Si no se dispone de la misma se puede copiar el hash proporcionado y buscarlo directamente en https://shodan.io
