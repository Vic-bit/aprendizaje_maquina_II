# Ejecución de los contenedores

Si queremos usar la línea de comando, los pasos a seguir es

1. Construimos las imágenes y levantamos todo. Va a constuir la imagen y levanta en un solo comando

```Bash
docker-compose up -d 
```

Tenemos levantado el wordpress y la base de datos, pero no están comunicados.

2. Para bajar todo lo que hemos hecho:
También se puede ingresar a docker desktop y borrarlos desde ahí.

```Bash
docker compose down 
```

3. Si queremos eliminar las imágenes y los volúmenes, hacemos

```Bash
docker compose down --rmi all --volumes
```