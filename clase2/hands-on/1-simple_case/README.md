# Instalación de la imagen

Si queremos usar la linea de comando, los pasos a seguir es

1. Construimos la imagen

```Bash
docker build -t python-app:latest . 
```

2. Ahora podemos ejecutar la imagen. Le doy el commando run de ejecutar y el nombre del contenedor

```Bash
docker run python-app
```

Me va a devolver el Zen de Python