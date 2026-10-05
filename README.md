El cifrado en sobre consiste en conectarse a AWS KMS especificando una clave maestra para solicitar una clave de datos temporal. KMS nos devuelve esta clave en dos versiones: una en texto plano para operar localmente y otra cifrada que servirá como candado.

Con la clave en texto plano ciframos el mensaje original y armamos el sobre digital, que es la estructura donde guardamos juntos el mensaje cifrado y la clave cifrada. Justo después de guardar el sobre, eliminamos inmediatamente la clave en texto plano de la memoria RAM por seguridad.

Para el proceso de descifrado, tomamos la clave cifrada que estaba dentro del sobre y se la enviamos a KMS. KMS la valida con la clave maestra y nos devuelve la clave plana; con ella abrimos el sobre, recuperamos el mensaje original y mostramos en pantalla tanto el texto como la clave utilizada.
