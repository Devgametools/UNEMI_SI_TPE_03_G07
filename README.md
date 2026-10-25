# Demo de criptografía: simétrica, asimétrica, firma digital y cifrado híbrido

Script en Python que demuestra:

1. Cifrado y descifrado con **AES-256-GCM** y detección de alteraciones.
2. **Firma digital RSA-2048 + SHA-256 (PSS)** y su verificación.
3. **Cifrado híbrido**: una clave AES protegida con RSA-OAEP.
4. **Rendimiento comparativo** entre RSA, AES-GCM y ChaCha20-Poly1305.
5. Tamaño de firmas **ECDSA P-256** frente a RSA-2048.

## Requisitos

- **Python 3.9 o superior** ([python.org/downloads](https://www.python.org/downloads/))
  - En Windows, marca la casilla **"Add Python to PATH"** al instalar.
- Archivos del proyecto:

```
UNEMI_SI_TPE_03_G07/
├── script/
├────  crypto.py
├── requirements.txt
└── README.md
```

Abre una terminal **dentro de la carpeta `UNEMI_SI_TPE_03_G07`** antes de seguir.

---

## 1. Crear el entorno virtual (venv)

**Windows (PowerShell o CMD)**

```powershell
python -m venv venv
```

**Linux / macOS**

```bash
python3 -m venv venv
```

> En Ubuntu/Debian, si aparece un error sobre `ensurepip`, instala primero:
> `sudo apt install python3-venv`

## 2. Activar el entorno virtual

**Windows – PowerShell**

```powershell
.\venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea el script, ejecuta una vez:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y vuelve a intentarlo.

**Windows – CMD**

```cmd
venv\Scripts\activate.bat
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Cuando el entorno está activo, el prompt muestra `(venv)` al inicio.

## 3. Instalar las dependencias

Con el entorno activado (igual en los tres sistemas):

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Ejecutar el script

**Windows**

```powershell
python script/crypto.py
```

**Linux / macOS**

```bash
python3 script/crypto.py
```

Salida esperada (los valores hexadecimales y los tiempos cambian en cada equipo y ejecución):

```
== 1. Cifrado simetrico AES-256-GCM ==
Texto claro : Transferencia: $1500 a la cuenta 001-UNEMI
...
Alteracion de 1 bit detectada -> InvalidTag (integridad)

== 2. Firma digital RSA-2048 + SHA-256 (PSS) ==
Verificacion con mensaje original: VALIDA
Verificacion con mensaje alterado: INVALIDA
...
```

> La prueba de rendimiento cifra 50 MiB en memoria; puede tardar unos segundos.

## 5. Desactivar el entorno

```bash
deactivate
```

---

## Resumen rápido

| Paso       | Windows                           | Linux / macOS                     |
| ---------- | --------------------------------- | --------------------------------- |
| Crear venv | `python -m venv venv`             | `python3 -m venv venv`            |
| Activar    | `.\venv\Scripts\Activate.ps1`     | `source venv/bin/activate`        |
| Instalar   | `pip install -r requirements.txt` | `pip install -r requirements.txt` |
| Ejecutar   | `python script/crypto.py`         | `python3 script/crypto.py`        |
| Salir      | `deactivate`                      | `deactivate`                      |
