Crear un entorno virtual

```
python -m venv myenv
```

Instalar las dependencias

```
pip install -r requirements.txt
```

Crear un archivo '.env' con el siguiente contenido:
```
FLASK_APP='todo'
FLASK_DEBUG=1

FLASK_DATABASE_HOST='localhost'
FLASK_DATABASE_PASSWORD='password'
FLASK_DATABASE_USER='user'
FLASK_DATABASE='todoer'
```

Modificar los valores de las variables que sean necesarios

Por ultimo para correr la app debemos ejecutar el siguiente comando
```
python app.py
```