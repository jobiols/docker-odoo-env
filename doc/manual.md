docker odoo environment manual
------------------------------

**Generalidades**

oe (odoo environment) es una utilidad para manejar ambientes dockerizados 
de odoo. Permite crear una instalacion de cero en un VPS virgen, con 
extrema facilidad, ademas maneja ambientes de desarrollo y staging
las unicas dependencias necesarias son python (v2 o v3) y git.

**oe config** Muestra o modifica las opciones almacenadas
oe mantiene un archivo yaml con la configuracion, de manera que cuando
se invoca una orden por ejemplo update no hay que reiterar cual es el 
cliente, el nombre de la base de datos o si estamos en produccion,
desarrollo o staging.

Si se invoca sin parametros muestra las variables almacenadas y con cada
uno de los siguientes parametros permite setear las variables. Aqui hay 
una descripcion de cada una.

    --client client-name El nombre del cliente es util en ambiente de 
            desarrollo para poder tener multiples instalaciones (una por
            cliente) en la misma maquina. Es requerido en produccion 
            aunque habra un solo cliente solo por compatibilidad con 
            el ambiente de desarrollo.
            DEFAULT None (se requiere un valor)
    --environment[development|production|stagging] 
            Si esta en development produce lo siguiente:
                1. Abre el puerto 5432 en el container de postgres
                   para que se pueda acceder mediante pgadmin.
                2. Saca el log de odoo por consola.
                3. Al crear la instalacion por primera vez copia los 
                   fuentes de la imagen de odoo al host creando repositorios.
                4. Si la instalacion ya esta creada monta los directorios
                   copiados de la imagen en la imagen, de manera que odoo
                   corre sobre los fuentes que estan en el host.
                5. Al clonar repositorios pone --depth 50
                6. Se activan los servicios DUMMY de SMTP FETCHMAIL ETC.
            Si esta en stagging produce lo siguiente
                1. Se activan los servicios DUMMY de SMTP FETCHMAIL ETC.
            Si esta en production 
            DEFAULT production
    --nginx[on|off] instala nginx para acceder a odoo por los puertos 80
            y 8072 
            DEFAULT off
    --verbose[on|off] enciende el modo verborragico mostrando los comandos
            que envia a docker con pretty print.
            DEFAULT off
    --database base-de-datos base de datos activa
            DEFAULT nombre-cliente_prod
    --defapp git-path-to-client-app
            es la url al repo del cliente por defecto
    --odoo-image user/image:tag
            Esta opcion sobreescribe la imagen que viene en el manifiesto
            se considera solo cuando estoy en desarrollo
            DEFAULT None

**oe update**  Instala o actualiza una instalación

Las siguientes opciones son requeridas o deben estar almacenadas

    --client
    
Las siguientes opciones no se almacenan

    --quick evita ciertos pasos que demoran sobre todo cuando estamos en
        desarrollo y no queremos que baje todo de nuevo.

Cuando se invoca la opcion oe update, sin parametros se buscan las opciones
almacenadas, si falta alguna/s se requiere/n y si estan todas se procede
con lo siguiente:

**Si estoy en produccion o staging**

1. hace un backup de la base de datos activa (si se puede)
2. verifica las dependencias en el servidor y las instala o actualiza (apt-get update y docker)
3. baja todas las imagenes docker (si estan activas)
4. hace pull de todos los repos y las imagenes
5. levanta image postgres y aeroo (a veces aeroo no es requerido)
6. Si no esta creado, crea el odoo.conf poniendo workers = 3
7. hace un update all dos veces (filtrando mensajes info)
8. instala o si esta instalada, actualiza la aplicacion por defecto
9. levanta todas las demas imagenes requeridas 

**Si estoy en desarrollo**

-p hace pull de todos los repos y las imagenes, recrea los volumenes addons y librerias en sendos repositorios (agregar .gitignore)
-R levanta image postgres y aeroo (a veces aeroo no es requerido)
-r Si no esta creado, crea el odoo.conf poniendo workers = 0; levanta odoo y saca log por consola
-u -m [modulo|all] hace update all

**backup** generates a backup in the backup_dir folder
    -d database name

**restore** restores a database from backcup_dir
> -z backup to restore, if empty oe will search en backup_folder and get the last one
> -d database_name

- Pensar como garantizar que los ambientes de stagging y produccion tengan las mismas imagenes
- Pensar como hacer un ambiente desarrollo donde se pueda poner imagenes nuevas y probarlas.
- Al arrancar postgres seria bueno experimentar con volume en lugar de -v

**qa**

-d crear base de datos de test con el modulo default instalado. 
    


**wishes**

Importante ver como INSTALAR modulos no solo actualizar.

oe develop -u -m product_autoload -c iomaq -d iomaq_prod (ejecuta el update y almacena las variables en un json local)

oe develop -l (lista las variables que quedaron almacenadas en un json)

oe develop -r (arranca mostrando el log) en develop siempre muestra el log

en modo desarrollo se activan los sink de mails y demas yerbas para que no mandemos mails a los clientes. ver tecnativa.

crear bases de datos de test 