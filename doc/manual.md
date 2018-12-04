docker odoo environment manual
------------------------------

**Generalidades**

oe (odoo environment) es una utilidad para manejar ambientes dockerizados 
de odoo. Permite crear una instalacion de cero en un VPS virgen, con 
extrema facilidad, ademas maneja ambientes de desarrollo y staging
las unicas dependencias necesarias son python 2.7 y git.

**oe sh[ow]** Muestra o modifica las opciones almacenadas
oe mantiene un archivo yaml con la configuracion, de manera que cuando
se invoca una orden por ejemplo update no hay que reiterar cual es el 
cliente, el nombre de la base de datos o si estamos en produccion,
desarrollo o staging.

Si se invoca sin parametros muestra las variables almacenadas y con cada
uno de los siguientes parametros permite setear las variables, aqui hay
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
            DEFAULT nombre-cliente_default

**oe upd[ate]**  Instala o actualiza una instalación

Las siguientes opciones son requeridas o deben estar almacenadas

    --cli[ent]
    
Las siguientes opciones no se almacenan

    --quick evita ciertos pasos que demoran sobre todo cuando estamos en
        desarrollo y no queremos que baje todo de nuevo.

Cuando se invoca la opcion oe update, sin parametros se buscan las opciones
almacenadas, si falta alguna/s se requiere/n y si estan todas se procede
con lo siguiente:

3. hace un backup de la base de datos activa (si se puede)
4. baja todas las imagenes docker (si estan activas)
5. verifica las dependencias en el servidor y las instala (apt-get update y docker)
6. hace pull de todos los repos y las imagenes
7. levanta image postgres y aeroo (a veces aeroo no es requerido)
8. hace un update all dos veces (filtrando mensajes info)
9. instala la aplicacion por defecto
10. levanta todas las imagenes requeridas

**backup** generates a backup in the backup_dir folder
    -d database name

**restore** restores a database from backcup_dir
> -z backup to restore, if empty oe will search en backup_folder and get the last one
> -d database_name

- Pensar como garantizar que los ambientes de stagging y produccion tengan las mismas imagenes
- Pensar como hacer un ambiente desarrollo donde se pueda poner imagenes nuevas y probarlas.
- Al arrancar postgres seria bueno experimentar con volume en lugar de -v

**opcion deploy** que deberia hacer:

1. bajar los fuentes y las imagenes
2. arrancar la base de datos
3. crear el config file con las opciones que saca del manifiesto
4. correr un update all filtrando los mensajes info
5. instalar el modulo de la aplicacion filtrando los mensajes info

**wishes**
modo desarrollo y modo produccion

Importante ver como INSTALAR modulos no solo actualizar.

oe develop -u -m product_autoload -c iomaq -d iomaq_prod (ejecuta el update y almacena las variables en un json local)

oe develop -l (lista las variables que quedaron almacenadas en un json)

oe develop -r (arranca mostrando el log) en develop siempre muestra el log

en modo desarrollo se activan los sink de mails y demas yerbas para que no mandemos mails a los clientes. ver tecnativa.
