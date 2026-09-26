import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import urlencode
import base64
import html
from io import BytesIO
from pathlib import Path
from pprint import pformat

from PIL import Image, ImageOps


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

st.set_page_config(
    page_title="Valeria & Hector | 08.01.2027",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# DATOS FIJOS DE LA BODA
# =========================================================

NOVIOS = "Valeria & Hector"
FECHA = "08 · 01 · 2027"
FECHA_COMPLETA = "08 de enero de 2027"
HORA = "05:00 PM"
HORA_LLEGADA = "04:30 PM"

# Colores/prendas sugeridas para el código de vestuario
VESTUARIO_MUJER = "Verde Oliva, Verde Claro"
VESTUARIO_HOMBRE = "Camisa café, pantalón beige"

LUGAR = "Parroquia Nuestra Señora del Café"
DIRECCION = "Calle 23 A Norte #14-74"
CIUDAD = "Armenia, Quindío"

MAPS_URL = "https://maps.app.goo.gl/zgLv9FpbRy9U6T177"
FORMS_URL = "https://forms.gle/4cGepJCuvvtpjZpq6"

# Texto que aparece debajo del reproductor
CANCION = "1+1=1 · Nanpa Básico"

MENSAJE = """
Queremos que seas testigo de la unión de dos corazones,
de dos almas, de dos seres que decidieron amarse
y juntar sus vidas como uno solo en el camino de Dios.
"""

# Lista de invitados: código (va en el enlace) -> nombre que se muestra
INVITADOS = {
    "maria-jose": "Maria Jose",
    "sandra-liliana": "Sandra Liliana",
    "hector-fabio": "Hector Fabio",
    "liliana": "Liliana",
    "valeria-ramos": "Valeria Ramos",
    "hector-salazar": "Hector Salazar",
}


# =========================================================
# PALETA
# =========================================================

BLANCO = "#FFFDFC"
BEIGE = "#F2EBDD"
OLIVA = "#667052"
TERRACOTA = "#B96F57"
CARBON = "#30352C"

# =========================================================
# FOTOGRAFÍAS: CONFIGURACIÓN
# =========================================================

# True  -> muestra el panel lateral para subir fotos y elegir dónde va cada una.
# False -> versión final para los invitados (sin panel ni datos de prueba).
MODO_EDICION = True

# Fotos definitivas (las que verán los invitados).
# 1) Sube tus imágenes a una carpeta del repositorio (ver NOMBRES_CARPETA_FOTOS).
# 2) Escribe aquí sus nombres. El panel lateral te genera este bloque
#    ya armado en la sección "3. Dejarlo fijo".
FOTOS_FIJAS = {
    "portada": None,      # fondo de la portada
    "historia": [],       # 1 foto = arco; 2 a 6 fotos = collage
    "galeria": [],        # lista de fotos, en el orden en que se mostrarán
    "vestuario": [],      # 1 foto = ancho completo; 2 fotos = una junto a otra
    "cierre": None,       # fondo de la sección final
}

# Encuadre vertical de las fotos de fondo:
# 0 = se ve la parte de arriba, 50 = centro, 100 = la parte de abajo.
POSICION_FIJA = {"portada": 50, "cierre": 50}

# Carpetas del repositorio donde se buscan las fotos (junto a app.py).
# Si tus fotos están en otra carpeta, agrega su nombre a esta lista.
NOMBRES_CARPETA_FOTOS = ("fotos", "mi-carpeta")
EXTENSIONES = {".jpg", ".jpeg", ".png", ".webp"}
NINGUNA = "— Ninguna —"

# Velo claro sobre las fotos de fondo para que el texto siga leyéndose.
# Sube el segundo número (0 a 1) si necesitas más contraste.
HERO_DEGRADADO = "linear-gradient(rgba(255,253,250,0.35), rgba(255,253,250,0.85))"
CIERRE_DEGRADADO = "linear-gradient(rgba(242,235,221,0.80), rgba(242,235,221,0.92))"


# =========================================================
# FOTOGRAFÍAS: FUNCIONES
# =========================================================

def html_block(codigo):
    """Muestra HTML en Streamlit.

    Quita las sangrías y las líneas en blanco para que Markdown no
    interprete partes del HTML como un bloque de código.
    """
    limpio = "\n".join(
        linea.strip() for linea in codigo.splitlines() if linea.strip()
    )
    st.markdown(limpio, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def optimizar(datos, max_lado=1600, calidad=82):
    """Reduce el tamaño de la foto para que la invitación cargue rápido."""
    img = Image.open(BytesIO(datos))
    img = ImageOps.exif_transpose(img)  # respeta la rotación del celular
    img.thumbnail((max_lado, max_lado))

    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        fondo = Image.new("RGB", img.size, (255, 253, 252))
        fondo.paste(img, mask=img.split()[-1])
        img = fondo
    else:
        img = img.convert("RGB")

    salida = BytesIO()
    img.save(salida, "JPEG", quality=calidad, optimize=True)
    return salida.getvalue()


def a_data_uri(datos, max_lado=1600):
    b64 = base64.b64encode(optimizar(datos, max_lado)).decode()
    return f"data:image/jpeg;base64,{b64}"


def carpetas_de_fotos():
    """Carpetas existentes donde buscar fotos (junto a app.py y en la raíz)."""
    bases = [Path(__file__).resolve().parent, Path.cwd()]
    encontradas = []

    for base in bases:
        for nombre in NOMBRES_CARPETA_FOTOS:
            carpeta = base / nombre
            if carpeta.is_dir() and carpeta not in encontradas:
                encontradas.append(carpeta)

    return encontradas


def cargar_banco(subidas):
    """Junta las fotos de las carpetas del repositorio y las subidas desde el panel."""
    banco = {}

    for carpeta in carpetas_de_fotos():
        for ruta in sorted(carpeta.iterdir()):
            if ruta.suffix.lower() in EXTENSIONES:
                banco[ruta.name] = ruta.read_bytes()

    for archivo in subidas or []:
        banco[archivo.name] = archivo.getvalue()

    return banco


FORMATOS_AUDIO = {
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".m4a": "audio/mp4",
    ".ogg": "audio/ogg",
}


def buscar_audio_en_carpeta():
    """Primer archivo de audio que haya en las carpetas del repositorio."""
    for carpeta in carpetas_de_fotos():
        for ruta in sorted(carpeta.iterdir()):
            if ruta.suffix.lower() in FORMATOS_AUDIO:
                return ruta

    return None


def cargar_musica(subida):
    """Devuelve (datos, formato) de la canción.

    Usa el archivo subido desde el panel si existe; si no, el que esté
    en la carpeta del repositorio. Sin canción devuelve (None, None).
    """
    if subida is not None:
        extension = Path(subida.name).suffix.lower()
        return subida.getvalue(), FORMATOS_AUDIO.get(extension, "audio/mpeg")

    ruta = buscar_audio_en_carpeta()

    if ruta is not None:
        return ruta.read_bytes(), FORMATOS_AUDIO[ruta.suffix.lower()]

    return None, None


def elegir(etiqueta, clave, nombres):
    """Lista desplegable para escoger qué foto va en un lugar."""
    opciones = [NINGUNA] + nombres
    fija = FOTOS_FIJAS.get(clave)
    indice = opciones.index(fija) if fija in opciones else 0

    elegido = st.selectbox(
        etiqueta,
        opciones,
        index=indice,
        key=f"foto_{clave}"
    )

    return None if elegido == NINGUNA else elegido


def elegir_fondo(etiqueta, clave, nombres):
    """Igual que elegir(), pero añade el encuadre vertical de la foto."""
    nombre = elegir(etiqueta, clave, nombres)
    posicion = POSICION_FIJA.get(clave, 50)

    if nombre:
        posicion = st.slider(
            "Encuadre vertical",
            0, 100, posicion,
            key=f"pos_{clave}",
            help="0 = se ve la parte de arriba de la foto, 100 = la de abajo."
        )

    return nombre, posicion


def estilo_fondo(datos, degradado, posicion, max_lado):
    """Devuelve el atributo style con la foto de fondo (o vacío si no hay)."""
    if not datos:
        return ""

    uri = a_data_uri(datos, max_lado)

    return (
        f'style="background-image: {degradado}, url(\'{uri}\'); '
        f'background-size: cover; '
        f'background-position: center {posicion}%;"'
    )


def html_reproductor(datos, formato):
    """Reproductor HTML con la canción incluida en la propia página."""
    if not datos:
        return ""

    b64 = base64.b64encode(datos).decode()

    return (
        f'<audio class="player" controls preload="metadata" '
        f'src="data:{formato};base64,{b64}"></audio>'
    )


def html_foto_historia(lista_datos):
    """Foto(s) de la sección de historia.

    Con una sola foto se muestra en arco, como antes.
    Con 2 a 4 fotos se arman en un pequeño collage.
    """
    imagenes = [d for d in lista_datos if d]

    if not imagenes:
        return ""

    if len(imagenes) == 1:
        uri = a_data_uri(imagenes[0], 900)
        return (
            f'<img class="story-photo" src="{uri}" '
            f'alt="{html.escape(NOVIOS)}">'
        )

    tarjetas = "".join(
        f'<img src="{a_data_uri(datos, 700)}" alt="{html.escape(NOVIOS)}">'
        for datos in imagenes[:6]
    )

    return f'<div class="story-collage">{tarjetas}</div>'


def html_fotos_vestuario(lista_datos):
    """Foto(s) de referencia del código de vestuario.

    Con 1 foto ocupa todo el ancho, como antes.
    Con 2 fotos se muestran una junto a la otra.
    """
    imagenes = [d for d in lista_datos if d]

    if not imagenes:
        return ""

    if len(imagenes) == 1:
        uri = a_data_uri(imagenes[0], 1400)
        return f'<img src="{uri}" style="width:100%; display:block;">'

    tarjetas = "".join(
        f'<img src="{a_data_uri(datos, 1000)}">'
        for datos in imagenes[:2]
    )

    return f'<div class="dress-photos">{tarjetas}</div>'



# =========================================================
# IDENTIFICAR INVITADO
# =========================================================

params = st.query_params

codigo_invitado = params.get("invitado", "invitado-1")

if isinstance(codigo_invitado, list):
    codigo_invitado = codigo_invitado[0]

nombre_invitado = INVITADOS.get(
    codigo_invitado.lower(),
    "Invitado"
)


# =========================================================
# CSS
# =========================================================

html_block(
    f"""
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Montserrat:wght@300;400;500;600&display=swap');

    html {{
        scroll-behavior: smooth;
    }}

    .stApp {{
        background: {BLANCO};
        color: {CARBON};
    }}

    .block-container {{
        max-width: 1100px;
        padding-top: 0;
        padding-bottom: 0;
    }}

    /* Ocultar elementos innecesarios de Streamlit */

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    /* Se oculta la barra de herramientas pero NO el botón que abre
       el panel lateral (si no, no se podría abrir la configuración) */

    header {{
        background: transparent !important;
    }}

    [data-testid="stToolbar"] {{
        visibility: hidden;
    }}

    [data-testid="stDecoration"] {{
        display: none;
    }}

    /* Tipografías */

    .serif {{
        font-family: 'Cormorant Garamond', serif;
    }}

    .sans {{
        font-family: 'Montserrat', sans-serif;
    }}

    /* Separador */

    .separator {{
        width: 55px;
        height: 1px;
        background: {TERRACOTA};
        margin: 25px auto;
    }}

    /* Ramas */

    .branch {{
        color: {OLIVA};
        font-size: 28px;
        text-align: center;
        margin: 12px 0;
    }}

    /* PORTADA */

    .hero {{
        min-height: 90vh;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        background:
            linear-gradient(
                rgba(255,253,250,0.20),
                rgba(255,253,250,0.82)
            );
        padding: 70px 25px;
    }}

    .hero-content {{
        max-width: 800px;
    }}

    .monogram {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 32px;
        color: {OLIVA};
        margin-bottom: 25px;
        letter-spacing: 3px;
    }}

    .names {{
        font-family: 'Cormorant Garamond', serif;
        font-size: clamp(60px, 9vw, 110px);
        line-height: 0.85;
        color: {CARBON};
        font-weight: 500;
    }}

    .amp {{
        color: {TERRACOTA};
        font-size: 0.65em;
    }}

    .hero-subtitle {{
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        letter-spacing: 2px;
        margin-top: 35px;
        text-transform: uppercase;
    }}

    .date {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 30px;
        margin-top: 25px;
    }}

    /* SECCIONES */

    .section {{
        padding: 90px 30px;
        text-align: center;
    }}

    .section-beige {{
        background: {BEIGE};
    }}

    .section-olive {{
        background: {OLIVA};
        color: white;
    }}

    .section-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 48px;
        font-weight: 500;
        margin-bottom: 25px;
    }}

    .section-label {{
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        letter-spacing: 3px;
        text-transform: uppercase;
        color: {OLIVA};
        margin-bottom: 15px;
    }}

    .section-olive .section-label {{
        color: white;
    }}

    .body-text {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 27px;
        line-height: 1.5;
        max-width: 700px;
        margin: auto;
    }}

    /* PERSONALIZACIÓN */

    .guest-name {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 58px;
        color: {OLIVA};
        margin-top: 15px;
    }}

    .guest-message {{
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        letter-spacing: 1px;
    }}

    /* FECHA */

    .big-day {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 110px;
        line-height: 0.8;
        color: {OLIVA};
    }}

    .month {{
        font-family: 'Montserrat', sans-serif;
        font-size: 17px;
        letter-spacing: 7px;
        margin-top: 15px;
    }}

    .time {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 32px;
        margin-top: 25px;
    }}

    .venue {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 27px;
        margin-top: 35px;
    }}

    .address {{
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        line-height: 1.8;
    }}

    /* BOTONES */

    .button {{
        display: inline-block;
        padding: 16px 34px;
        margin-top: 25px;
        border-radius: 30px;
        background: {OLIVA};
        color: white !important;
        text-decoration: none !important;
        font-family: 'Montserrat', sans-serif;
        font-size: 12px;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }}

    .button:hover {{
        background: {TERRACOTA};
        transform: translateY(-2px);
    }}

    /* VESTUARIO */

    .dress-label {{
        font-size: 13px !important;
        letter-spacing: 5px !important;
        font-weight: 600;
        padding-bottom: 14px;
        margin-bottom: 20px !important;
        border-bottom: 1px solid rgba(255,255,255,0.35);
        display: inline-block;
    }}

    .dress-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 42px;
        line-height: 1.3;
        max-width: 480px;
        margin: 0 auto;
    }}

    .dress-code {{
        font-family: 'Montserrat', sans-serif;
        font-size: 17px;
        letter-spacing: 4px;
        margin: 20px 0;
    }}

    .dress-warning {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 25px;
        margin: 25px auto;
        max-width: 500px;
    }}

    .dress-arrow {{
        font-size: 34px;
        margin-top: 28px;
        animation: dress-bounce 1.8s ease-in-out infinite;
    }}

    @keyframes dress-bounce {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(10px); }}
    }}

    .dress-photo-wrap {{
        max-width: 480px;
        margin: 0 auto;
        padding: 45px 20px 20px 20px;
    }}

    .dress-photo-wrap img {{
        border-radius: 18px;
        box-shadow: 0 18px 40px rgba(48, 53, 44, 0.18);
    }}

    .dress-photos {{
        display: flex;
        gap: 14px;
        justify-content: center;
    }}

    .dress-photos img {{
        width: 50%;
        aspect-ratio: 3 / 4;
        object-fit: cover;
        display: block;
    }}

    @media (max-width: 480px) {{
        .dress-photos {{
            gap: 10px;
        }}
    }}

    .dress-signs {{
        display: flex;
        flex-wrap: wrap;
        gap: 14px;
        justify-content: center;
        max-width: 480px;
        margin: 0 auto 45px auto;
        padding: 0 20px;
    }}

    .dress-sign {{
        flex: 1;
        min-width: 200px;
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 14px;
        padding: 18px 16px;
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        letter-spacing: 0.5px;
        line-height: 1.5;
    }}

    .dress-sign-label {{
        display: block;
        font-family: 'Cormorant Garamond', serif;
        font-size: 22px;
        letter-spacing: 2px;
        margin-bottom: 6px;
    }}

    /* REPRODUCTOR DE MÚSICA */

    .player {{
        display: block;
        width: min(420px, 100%);
        margin: 28px auto 0 auto;
    }}

    .song-credit {{
        font-family: 'Montserrat', sans-serif;
        font-size: 11px;
        letter-spacing: 2px;
        color: {OLIVA};
        margin-top: 14px;
    }}

    /* FOTO EN ARCO (historia) */

    .story-photo {{
        display: block;
        width: min(340px, 80%);
        aspect-ratio: 4 / 5;
        object-fit: cover;
        border-radius: 999px 999px 14px 14px;
        margin: 0 auto 45px auto;
    }}

    /* COLLAGE (historia, 2 a 6 fotos) */

    .story-collage {{
        display: flex;
        justify-content: center;
        align-items: center;
        flex-wrap: wrap;
        max-width: 560px;
        margin: 10px auto 55px auto;
    }}

    .story-collage img {{
        width: 135px;
        height: 170px;
        object-fit: cover;
        border: 6px solid white;
        border-radius: 6px;
        background: white;
        box-shadow: 0 14px 26px rgba(48, 53, 44, 0.18);
        margin: 10px -12px;
    }}

    .story-collage img:nth-child(1) {{ transform: rotate(-7deg); z-index: 3; }}
    .story-collage img:nth-child(2) {{ transform: rotate(5deg) translateY(-16px); z-index: 4; }}
    .story-collage img:nth-child(3) {{ transform: rotate(-4deg) translateY(10px); z-index: 2; }}
    .story-collage img:nth-child(4) {{ transform: rotate(8deg) translateY(-8px); z-index: 1; }}
    .story-collage img:nth-child(5) {{ transform: rotate(-6deg) translateY(6px); z-index: 0; }}
    .story-collage img:nth-child(6) {{ transform: rotate(4deg) translateY(-10px); z-index: 5; }}

    @media (max-width: 480px) {{
        .story-collage img {{
            width: 100px;
            height: 128px;
            margin: 7px -9px;
        }}
    }}

    /* GALERÍA */

    .gallery-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 50px;
    }}

    /* CIERRE */

    .closing {{
        padding: 100px 25px;
        text-align: center;
        background: {BEIGE};
    }}

    .closing-names {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 55px;
    }}

    .closing-date {{
        font-family: 'Montserrat', sans-serif;
        letter-spacing: 3px;
        margin-top: 15px;
    }}

    /* MOBILE */

    @media (max-width: 700px) {{

        .hero {{
            min-height: 85vh;
            padding: 40px 20px;
        }}

        .names {{
            font-size: 62px;
        }}

        .section {{
            padding: 65px 20px;
        }}

        .section-title {{
            font-size: 40px;
        }}

        .body-text {{
            font-size: 23px;
        }}

        .big-day {{
            font-size: 85px;
        }}

        .guest-name {{
            font-size: 48px;
        }}

        .closing-names {{
            font-size: 45px;
        }}
    }}

    </style>
    """
)


# =========================================================
# PANEL DE CONFIGURACIÓN (solo con MODO_EDICION = True)
# =========================================================

seleccion = {}
posicion = {}

if MODO_EDICION:

    with st.sidebar:

        st.markdown(
            """
            ## 🌿 Configuración
            ### Invitación Valeria & Hector
            """
        )

        st.caption(
            "Esta sección es temporal para la primera versión."
        )

        st.divider()

        st.markdown("### 📸 1. Sube tus fotografías")

        subidas = st.file_uploader(
            "Sube todas las fotos que quieras usar",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True
        )

        banco = cargar_banco(subidas)
        nombres = list(banco)

        # Diagnóstico: dónde se están buscando las fotos del repositorio
        carpetas = carpetas_de_fotos()

        if carpetas:
            st.success(
                f"📁 {len(nombres)} foto(s) disponibles. "
                f"Carpeta(s) del repositorio: "
                + ", ".join(f"`{c.name}`" for c in carpetas)
            )
        else:
            st.warning(
                "No encontré ninguna carpeta de fotos junto a `app.py`. "
                f"Busqué: {', '.join(NOMBRES_CARPETA_FOTOS)}. "
                f"Ruta de app.py: `{Path(__file__).resolve().parent}`"
            )

        st.caption(
            "Sube primero todas las fotos y después asígnalas: "
            "si agregas más fotos más tarde, las selecciones "
            "pueden reiniciarse."
        )

        st.divider()

        st.markdown("### 🖼️ 2. Elige dónde va cada una")

        if not nombres:
            st.info("Sube al menos una fotografía para poder asignarla.")

        st.caption(
            "Cada foto solo puede usarse en un lugar: al elegirla aquí, "
            "deja de aparecer en las demás listas."
        )

        # Portada, historia, vestuario y cierre se reparten cada una su
        # propia foto: a medida que se elige una, se quita de las
        # opciones de las siguientes para que ninguna se repita.
        usadas = []

        disponibles = [n for n in nombres if n not in usadas]
        seleccion["portada"], posicion["portada"] = elegir_fondo(
            "Portada (fondo del inicio)", "portada", disponibles
        )
        if seleccion["portada"]:
            usadas.append(seleccion["portada"])

        disponibles = [n for n in nombres if n not in usadas]
        historia_defecto = [
            n for n in FOTOS_FIJAS["historia"] if n in disponibles
        ][:6]

        historia_sel = st.multiselect(
            "Historia (1 foto = en arco · 2 a 6 = collage)",
            disponibles,
            default=historia_defecto,
            key="foto_historia"
        )

        if len(historia_sel) > 6:
            st.warning("Se usarán solo las primeras 6 fotos elegidas.")
            historia_sel = historia_sel[:6]

        usadas.extend(historia_sel)

        disponibles = [n for n in nombres if n not in usadas]
        vestuario_defecto = [
            n for n in FOTOS_FIJAS["vestuario"] if n in disponibles
        ][:2]

        vestuario_sel = st.multiselect(
            "Código de vestuario (1 o 2 fotos de referencia)",
            disponibles,
            default=vestuario_defecto,
            key="foto_vestuario"
        )

        if len(vestuario_sel) > 2:
            st.warning("Se usarán solo las primeras 2 fotos elegidas.")
            vestuario_sel = vestuario_sel[:2]

        usadas.extend(vestuario_sel)

        disponibles = [n for n in nombres if n not in usadas]
        seleccion["cierre"], posicion["cierre"] = elegir_fondo(
            "Cierre (fondo de la sección final)", "cierre", disponibles
        )
        if seleccion["cierre"]:
            usadas.append(seleccion["cierre"])

        # La galería solo ofrece las fotos que sobraron, para que no se
        # repita ninguna foto ya asignada a portada, historia,
        # vestuario o cierre.
        disponibles_galeria = [n for n in nombres if n not in usadas]

        galeria_defecto = [
            n for n in FOTOS_FIJAS["galeria"]
            if n in disponibles_galeria
        ] or disponibles_galeria

        galeria_sel = st.multiselect(
            "Galería (en el orden que las elijas)",
            disponibles_galeria,
            default=galeria_defecto,
            key="foto_galeria"
        )

        st.divider()

        st.markdown("### 🎵 Música")

        musica = st.file_uploader(
            "Archivo de audio",
            type=["mp3", "wav", "m4a", "ogg"]
        )

        audio_carpeta = buscar_audio_en_carpeta()

        if audio_carpeta is not None:
            st.success(f"🎵 Canción en el repositorio: `{audio_carpeta.name}`")
        else:
            st.warning(
                "No encontré ninguna canción (.mp3, .wav, .m4a u .ogg) "
                "en la carpeta de fotos del repositorio."
            )

        st.divider()

        st.markdown("### 🔗 Enlaces")

        st.link_button(
            "Abrir Google Maps",
            MAPS_URL,
            use_container_width=True
        )

        st.link_button(
            "Abrir Google Forms",
            FORMS_URL,
            use_container_width=True
        )

        st.divider()

        st.markdown("### 💾 3. Dejarlo fijo")

        st.caption(
            "Las fotos subidas desde este panel se pierden al cerrar "
            "la página y los invitados no las ven. Para dejarlas "
            "definitivas: sube las fotos a una carpeta del repositorio "
            "(como `mi-carpeta`) junto a `app.py` y pega este bloque "
            "en la sección FOTOS_FIJAS del código."
        )

        configuracion = {
            "portada": seleccion["portada"],
            "historia": historia_sel,
            "galeria": galeria_sel,
            "vestuario": vestuario_sel,
            "cierre": seleccion["cierre"],
        }

        st.code(
            "FOTOS_FIJAS = "
            + pformat(configuracion, sort_dicts=False)
            + "\n\nPOSICION_FIJA = "
            + pformat(posicion, sort_dicts=False),
            language="python"
        )

        st.divider()

        st.info(
            "En esta V1 los archivos cargados funcionan durante "
            "la sesión. En la siguiente etapa podemos hacerlos "
            "permanentes."
        )

else:

    banco = cargar_banco([])

    seleccion = {
        clave: FOTOS_FIJAS.get(clave)
        for clave in ("portada", "cierre")
    }

    historia_sel = [n for n in FOTOS_FIJAS["historia"] if n in banco][:6]
    vestuario_sel = [n for n in FOTOS_FIJAS["vestuario"] if n in banco][:2]

    posicion = {
        "portada": POSICION_FIJA.get("portada", 50),
        "cierre": POSICION_FIJA.get("cierre", 50),
    }

    usadas_fijas = (
        {v for v in seleccion.values() if v}
        | set(historia_sel)
        | set(vestuario_sel)
    )

    galeria_sel = [
        n for n in FOTOS_FIJAS["galeria"] if n in banco
    ] or [n for n in banco if n not in usadas_fijas]
    musica = None


# Canción: la subida desde el panel o la de la carpeta del repositorio
musica_datos, musica_formato = cargar_musica(musica)


# Piezas HTML que dependen de las fotos elegidas

fondo_portada = estilo_fondo(
    banco.get(seleccion["portada"]),
    HERO_DEGRADADO,
    posicion["portada"],
    1600
)

fondo_cierre = estilo_fondo(
    banco.get(seleccion["cierre"]),
    CIERRE_DEGRADADO,
    posicion["cierre"],
    1400
)

foto_historia = html_foto_historia(
    [banco.get(n) for n in historia_sel]
)

fotos_vestuario = html_fotos_vestuario(
    [banco.get(n) for n in vestuario_sel]
)

reproductor = html_reproductor(musica_datos, musica_formato)


# =========================================================
# PORTADA
# =========================================================

html_block(
    f"""
    <section class="hero" {fondo_portada}>

        <div class="hero-content">

            <div class="monogram">
                VH
            </div>

            <div class="names">
                Valeria
                <span class="amp">&</span>
                Hector
            </div>

            <div class="hero-subtitle">
                Queremos compartir contigo este gran momento
            </div>

            <div class="date">
                {FECHA}
            </div>

            <div class="branch">
                ❧
            </div>

        </div>

    </section>
    """
)


# =========================================================
# PERSONALIZACIÓN
# =========================================================

html_block(
    f"""
    <section class="section section-beige">

        <div class="section-label">
            Una invitación para ti
        </div>

        <div class="guest-name">
            {html.escape(nombre_invitado)}
        </div>

        <div class="separator"></div>

        <div class="guest-message">
            Nos encantará compartir contigo este momento.
        </div>

        <div class="music">
            {reproductor}
            <div class="song-credit">
                ♫ &nbsp; {html.escape(CANCION)}
            </div>
        </div>

        <div class="branch">
            ❧
        </div>

    </section>
    """
)


# =========================================================
# MENSAJE
# =========================================================

html_block(
    f"""
    <section class="section">

        {foto_historia}

        <div class="section-label">
            Nuestro día
        </div>

        <div class="section-title">
            Una historia de amor
        </div>

        <div class="body-text">
            {MENSAJE}
        </div>

        <div class="separator"></div>

        <div class="monogram">
            VH
        </div>

    </section>
    """
)


# =========================================================
# FECHA Y CEREMONIA
# =========================================================

html_block(
    f"""
    <section class="section section-beige">

        <div class="section-label">
            Ceremonia
        </div>

        <div class="big-day">
            08
        </div>

        <div class="month">
            ENERO · 2027
        </div>

        <div class="time">
            {HORA}
        </div>

        <div class="venue">
            {LUGAR}
        </div>

        <div class="address">
            {DIRECCION}<br>
            {CIUDAD}
        </div>

        <div class="branch">
            ❧
        </div>

    </section>
    """
)


# =========================================================
# MAPA
# =========================================================

html_block(
    f"""
    <section class="section">

        <div class="section-label">
            Ubicación
        </div>

        <div class="section-title">
            ¿Cómo llegar?
        </div>

        <div class="body-text">
            {LUGAR}<br>
            <span style="font-size:18px;">
                {DIRECCION}, {CIUDAD}
            </span>
        </div>

        <a
            class="button"
            href="{MAPS_URL}"
            target="_blank"
        >
            📍 &nbsp; CÓMO LLEGAR
        </a>

    </section>
    """
)


# =========================================================
# GALERÍA
# =========================================================

html_block(
    """
    <section class="section section-beige">

        <div class="section-label">
            Nosotros
        </div>

        <div class="gallery-title">
            Algunos momentos
        </div>

    </section>
    """
)

fotos_galeria = [banco[n] for n in galeria_sel if n in banco]

if fotos_galeria:

    columnas = st.columns(2)

    for i, foto in enumerate(fotos_galeria):

        with columnas[i % 2]:
            st.image(
                optimizar(foto, 1400),
                use_container_width=True
            )

else:

    html_block(
        """
        <div style="
            text-align:center;
            padding:60px 20px;
            background:#F2EBDD;
            font-family:'Montserrat',sans-serif;
            color:#667052;
        ">
            📷<br><br>
            Las fotografías de Valeria & Hector
            aparecerán aquí.
        </div>
        """
    )


# =========================================================
# CÓDIGO DE VESTUARIO
# =========================================================

html_block(
    f"""
    <section class="section section-olive">

        <div class="section-label dress-label">
            👗 &nbsp; Código de vestuario
        </div>

        <div class="dress-title">
            Que te parezcas a los modelos
        </div>

        <div class="dress-warning">
            🚫 El blanco es exclusivo de la novia.
        </div>

        <div class="separator"></div>

        <div class="dress-warning">
            Te esperamos a las {HORA_LLEGADA}
        </div>

        <div class="dress-arrow">
            ↓
        </div>

    </section>
    """
)

if fotos_vestuario:

    html_block(
        f"""
        <section class="section section-olive" style="padding-top:0; padding-bottom:0;">
            <div class="dress-photo-wrap">
                {fotos_vestuario}
            </div>
        </section>
        """
    )

else:

    html_block(
        """
        <section class="section section-olive" style="padding-top:0; padding-bottom:0;">
            <div class="dress-photo-wrap" style="
                background: rgba(255,255,255,0.12);
                border-radius: 18px;
                color: white;
                font-family:'Montserrat',sans-serif;
            ">
                👗<br><br>
                Aquí aparecerá la imagen de referencia
                del código de vestuario.
            </div>
        </section>
        """
    )

html_block(
    f"""
    <section class="section section-olive" style="padding-top:0;">
        <div class="dress-signs">
            <div class="dress-sign">
                <span class="dress-sign-label">Mujer</span>
                {html.escape(VESTUARIO_MUJER)}
            </div>
            <div class="dress-sign">
                <span class="dress-sign-label">Hombre</span>
                {html.escape(VESTUARIO_HOMBRE)}
            </div>
        </div>
    </section>
    """
)


# Se conserva la hora de llegada en la sección de la ceremonia; si
# quieres mostrarla también aquí, agrega un bloque .dress-warning
# como el de más abajo.



# =========================================================
# CONFIRMACIÓN
# =========================================================

html_block(
    f"""
    <section class="section">

        <div class="section-label">
            Confirmación
        </div>

        <div class="section-title">
            ¿Nos acompañas?
        </div>

        <div class="body-text">
            {html.escape(nombre_invitado)}, nos haría muy felices
            compartir este momento contigo.
        </div>

        <a
            class="button"
            href="{FORMS_URL}"
            target="_blank"
        >
            ✉ &nbsp; CONFIRMAR ASISTENCIA
        </a>

    </section>
    """
)


# =========================================================
# CIERRE
# =========================================================

html_block(
    f"""
    <section class="closing" {fondo_cierre}>

        <div class="monogram">
            VH
        </div>

        <div class="closing-names">
            Valeria <span style="color:{TERRACOTA}">&</span> Hector
        </div>

        <div class="closing-date">
            {FECHA}
        </div>

        <div class="separator"></div>

        <div class="body-text"
             style="font-size:22px;">
            Con amor, esperamos compartir
            este día contigo.
        </div>

        <div class="branch">
            ❧
        </div>

    </section>
    """
)


# =========================================================
# INFORMACIÓN PARA PRUEBAS
# =========================================================

if MODO_EDICION:

    with st.expander("🔧 Información de prueba"):

        st.write(
            f"Invitado identificado: **{nombre_invitado}**"
        )

        st.code(
            f"https://TU-DOMINIO.streamlit.app/?invitado={codigo_invitado}"
        )

        st.caption(
            "Esta sección se oculta al poner MODO_EDICION = False."
        )
