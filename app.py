import streamlit as st
from pathlib import Path
from urllib.parse import quote
import base64
import html


# =========================================================
# CONFIGURACIÓN
# =========================================================

st.set_page_config(
    page_title="Valeria & Hector | 08.01.2027",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# INFORMACIÓN DE LA BODA
# =========================================================

NOVIOS = "Valeria & Hector"

FECHA = "08 · 01 · 2027"
FECHA_CORTA = "08"
MES_ANO = "ENERO · 2027"

HORA = "05:00 PM"
HORA_LLEGADA = "04:30 PM"

LUGAR = "Parroquia Nuestra Señora del Café"
DIRECCION = "Calle 23 A Norte #14-74"
CIUDAD = "Armenia, Quindío"

MAPS_URL = (
    "https://maps.app.goo.gl/zgLv9FpbRy9U6T177"
)

FORMS_URL = (
    "https://forms.gle/4cGepJCuvvtpjZpq6"
)

MENSAJE = (
    "Queremos que seas testigo de la unión de dos corazones, "
    "de dos almas, de dos seres que decidieron amarse y "
    "juntar sus vidas como uno solo en el camino de Dios."
)


# =========================================================
# INVITADOS
# =========================================================

INVITADOS = {
    f"invitado-{i}": f"Invitado {i}"
    for i in range(1, 26)
}


# =========================================================
# RUTAS DE ARCHIVOS
# =========================================================

BASE_DIR = Path(__file__).parent

FOTOS_DIR = BASE_DIR / "mi-carpeta"
VESTUARIO_DIR = BASE_DIR / "assets" / "vestuario"
MUSICA_DIR = BASE_DIR / "assets" / "musica"


# =========================================================
# PALETA
# =========================================================

BLANCO = "#FFFDFC"
BEIGE = "#F2EBDD"
OLIVA = "#667052"
OLIVA_OSCURO = "#4F5941"
TERRACOTA = "#B96F57"
CARBON = "#30352C"


# =========================================================
# IDENTIFICAR INVITADO
# =========================================================

codigo_invitado = st.query_params.get(
    "invitado",
    "invitado-1"
)

if isinstance(codigo_invitado, list):
    codigo_invitado = codigo_invitado[0]

codigo_invitado = str(codigo_invitado).lower()

nombre_invitado = INVITADOS.get(
    codigo_invitado,
    "Invitado"
)


# =========================================================
# FUNCIONES
# =========================================================

def encontrar_fotos():
    """Busca automáticamente las fotografías."""

    extensiones = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.webp"
    ]

    archivos = []

    if FOTOS_DIR.exists():

        for extension in extensiones:
            archivos.extend(
                FOTOS_DIR.glob(extension)
            )

    return sorted(archivos)


def encontrar_imagen_vestuario():
    """Busca la imagen de referencia."""

    extensiones = [
        "*.jpg",
        "*.jpeg",
        "*.png",
        "*.webp"
    ]

    if VESTUARIO_DIR.exists():

        for extension in extensiones:

            archivos = list(
                VESTUARIO_DIR.glob(extension)
            )

            if archivos:
                return archivos[0]

    return None


def encontrar_musica():
    """Busca el archivo de música."""

    extensiones = [
        "*.mp3",
        "*.wav",
        "*.m4a"
    ]

    if MUSICA_DIR.exists():

        for extension in extensiones:

            archivos = list(
                MUSICA_DIR.glob(extension)
            )

            if archivos:
                return archivos[0]

    return None


def imagen_base64(path):
    """Convierte una imagen en base64."""

    if not path or not path.exists():
        return None

    extension = path.suffix.lower()

    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp"
    }.get(extension, "image/jpeg")

    data = base64.b64encode(
        path.read_bytes()
    ).decode()

    return f"data:{mime};base64,{data}"


# =========================================================
# ARCHIVOS
# =========================================================

fotos = encontrar_fotos()
imagen_vestuario = encontrar_imagen_vestuario()
musica = encontrar_musica()


# =========================================================
# CSS
# =========================================================

st.markdown(
    f"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700'
'&family=Montserrat:wght@300;400;500;600'
'&display=swap'
);


/* ================================
   GENERAL
================================ */

html {{
    scroll-behavior: smooth;
}}

.stApp {{
    background: {BLANCO};
    color: {CARBON};
}}

.block-container {{
    max-width: 1000px;
    padding: 0 !important;
}}

#MainMenu {{
    visibility: hidden;
}}

header {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}


/* ================================
   TIPOGRAFÍAS
================================ */

.serif {{
    font-family: 'Cormorant Garamond', serif;
}}

.sans {{
    font-family: 'Montserrat', sans-serif;
}}


/* ================================
   HERO
================================ */

.hero {{
    min-height: 100vh;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;

    background:
        linear-gradient(
            rgba(255,253,252,.20),
            rgba(255,253,252,.82)
        );

    padding: 50px 20px;
}}

.hero-inner {{
    width: 100%;
    max-width: 850px;
}}

.monogram {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 32px;
    letter-spacing: 6px;
    color: {OLIVA};
    margin-bottom: 30px;
}}

.names {{
    font-family: 'Cormorant Garamond', serif;
    font-size: clamp(60px, 9vw, 105px);
    line-height: .82;
    font-weight: 500;
}}

.amp {{
    color: {TERRACOTA};
    font-size: .60em;
}}

.hero-line {{
    width: 50px;
    height: 1px;
    background: {TERRACOTA};
    margin: 32px auto;
}}

.hero-text {{
    font-family: 'Montserrat', sans-serif;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
}}

.hero-date {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 32px;
    margin-top: 25px;
    color: {OLIVA};
}}


/* ================================
   SECCIONES
================================ */

.section {{
    padding: 100px 25px;
    text-align: center;
}}

.beige {{
    background: {BEIGE};
}}

.olive {{
    background: {OLIVA};
    color: white;
}}

.label {{
    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 20px;
}}

.title {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 52px;
    font-weight: 500;
    line-height: 1;
}}

.text {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 27px;
    line-height: 1.5;
    max-width: 700px;
    margin: 30px auto 0;
}}

.line {{
    width: 50px;
    height: 1px;
    background: {TERRACOTA};
    margin: 30px auto;
}}


/* ================================
   INVITADO
================================ */

.guest-name {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 65px;
    color: {OLIVA};
}}

.guest-small {{
    font-family: 'Montserrat', sans-serif;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
}}


/* ================================
   FECHA
================================ */

.day {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 125px;
    line-height: .75;
    color: {OLIVA};
}}

.month {{
    font-family: 'Montserrat', sans-serif;
    font-size: 13px;
    letter-spacing: 7px;
    margin-top: 20px;
}}

.time {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 34px;
    margin-top: 30px;
}}

.venue {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 30px;
    margin-top: 40px;
}}

.address {{
    font-family: 'Montserrat', sans-serif;
    font-size: 12px;
    line-height: 1.8;
    margin-top: 10px;
}}


/* ================================
   BOTONES
================================ */

.button {{
    display: inline-block;

    padding: 15px 32px;
    margin-top: 30px;

    background: {OLIVA};

    color: white !important;

    border-radius: 30px;

    text-decoration: none !important;

    font-family: 'Montserrat', sans-serif;
    font-size: 10px;
    letter-spacing: 2px;

    transition: .3s;
}}

.button:hover {{
    background: {TERRACOTA};
    transform: translateY(-2px);
}}


/* ================================
   VESTUARIO
================================ */

.dress-code {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 58px;
}}

.dress-note {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 26px;
    max-width: 550px;
    margin: 25px auto;
}}

.reference {{
    max-width: 500px;
    margin: 40px auto;
}}

.reference img {{
    width: 100%;
    border-radius: 3px;
}}


/* ================================
   MAPA
================================ */

.map-card {{
    max-width: 650px;
    margin: 40px auto;
    padding: 45px 25px;

    background: {BEIGE};

    border: 1px solid rgba(102,112,82,.20);
}}


/* ================================
   CIERRE
================================ */

.closing {{
    min-height: 70vh;

    display: flex;
    flex-direction: column;

    align-items: center;
    justify-content: center;

    text-align: center;

    background: {BEIGE};
}}

.closing-names {{
    font-family: 'Cormorant Garamond', serif;
    font-size: 62px;
}}

.closing-date {{
    font-family: 'Montserrat', sans-serif;
    font-size: 11px;
    letter-spacing: 4px;
    margin-top: 20px;
}}


/* ================================
   MÓVIL
================================ */

@media(max-width:700px) {{

    .section {{
        padding: 75px 20px;
    }}

    .names {{
        font-size: 65px;
    }}

    .title {{
        font-size: 43px;
    }}

    .text {{
        font-size: 23px;
    }}

    .guest-name {{
        font-size: 52px;
    }}

    .day {{
        font-size: 95px;
    }}

    .dress-code {{
        font-size: 48px;
    }}

    .closing-names {{
        font-size: 48px;
    }}
}}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# PORTADA
# =========================================================

foto_portada = None

if fotos:
    foto_portada = imagen_base64(fotos[0])


hero_background = ""

if foto_portada:

    hero_background = f"""
        background-image:
        linear-gradient(
            rgba(255,253,252,.10),
            rgba(255,253,252,.85)
        ),
        url('{foto_portada}');
        background-size: cover;
        background-position: center;
    """


st.markdown(
    f"""
<section class="hero"
style="{hero_background}">

    <div class="hero-inner">

        <div class="monogram">
            VH
        </div>

        <div class="names">
            Valeria
            <span class="amp">&</span>
            Hector
        </div>

        <div class="hero-line"></div>

        <div class="hero-text">
            Queremos compartir contigo
            este gran momento
        </div>

        <div class="hero-date">
            {FECHA}
        </div>

    </div>

</section>
""",
    unsafe_allow_html=True
)


# =========================================================
# PERSONALIZACIÓN
# =========================================================

st.markdown(
    f"""
<section class="section beige">

    <div class="guest-small">
        Esta invitación es para
    </div>

    <div class="guest-name">
        {html.escape(nombre_invitado)}
    </div>

    <div class="line"></div>

    <div class="text">
        Nos encantará compartir
        este día tan especial contigo.
    </div>

</section>
""",
    unsafe_allow_html=True
)


# =========================================================
# MENSAJE
# =========================================================

st.markdown(
    f"""
<section class="section">

    <div class="label">
        Nuestro día
    </div>

    <div class="title">
        Dos corazones,<br>
        un solo camino
    </div>

    <div class="text">
        {MENSAJE}
    </div>

    <div class="line"></div>

    <div class="monogram">
        VH
    </div>

</section>
""",
    unsafe_allow_html=True
)


# =========================================================
# CEREMONIA
# =========================================================

st.markdown(
    f"""
<section class="section beige">

    <div class="label">
        Ceremonia
    </div>

    <div class="day">
        {FECHA_CORTA}
    </div>

    <div class="month">
        {MES_ANO}
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

</section>
""",
    unsafe_allow_html=True
)


# =========================================================
# UBICACIÓN
# =========================================================

st.markdown(
    f"""
<section class="section">

    <div class="label">
        Ubicación
    </div>

    <div class="title">
        Te esperamos
    </div>

    <div class="map-card">

        <div class="venue">
            {LUGAR}
        </div>

        <div class="address">
            {DIRECCION}<br>
            {CIUDAD}
        </div>

        <a
            href="{MAPS_URL}"
            target="_blank"
            class="button"
        >
            📍 CÓMO LLEGAR
        </a>

    </div>

</section>
""",
    unsafe_allow_html=True
)


# =========================================================
# GALERÍA
# =========================================================

st.markdown(
    """
<section class="section beige">

    <div class="label">
        Valeria & Hector
    </div>

    <div class="title">
        Algunos momentos
    </div>

</section>
""",
    unsafe_allow_html=True
)


if len(fotos) > 1:

    fotos_galeria = fotos[1:]

    columnas = st.columns(2)

    for indice, foto in enumerate(fotos_galeria):

        with columnas[indice % 2]:

            st.image(
                str(foto),
                use_container_width=True
            )

else:

    st.markdown(
        """
        <div style="
            padding:80px 20px;
            text-align:center;
            background:#F2EBDD;
            font-family:'Montserrat';
            color:#667052;
        ">
            Las fotografías aparecerán aquí.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# VESTUARIO
# =========================================================

st.markdown(
    f"""
<section class="section olive">

    <div class="label">
        Código de vestuario
    </div>

    <div class="dress-code">
        Verde claro
    </div>

    <div class="dress-note">
        🤍 El blanco es exclusivo de la novia.
    </div>

    <div class="line"></div>

    <div class="dress-note">
        Hora recomendada de llegada<br>
        <strong>{HORA_LLEGADA}</strong>
    </div>

</section>
""",
    unsafe_allow_html=True
)


if imagen_vestuario:

    st.markdown(
        """
        <div class="reference">
        """,
        unsafe_allow_html=True
    )

    st.image(
        str(imagen_vestuario),
        use_container_width=True
    )

    st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CONFIRMACIÓN
# =========================================================

forms_url_personalizado = (
    f"{FORMS_URL}"
)

st.markdown(
    f"""
<section class="section">

    <div class="label">
        Confirmación
    </div>

    <div class="title">
        ¿Nos acompañas?
    </div>

    <div class="text">
        {html.escape(nombre_invitado)},
        nos haría muy felices compartir
        este momento contigo.
    </div>

    <a
        href="{forms_url_personalizado}"
        target="_blank"
        class="button"
    >
        ✉ CONFIRMAR ASISTENCIA
    </a>

</section>
""",
    unsafe_allow_html=True
)


# =========================================================
# MÚSICA
# =========================================================

if musica:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:35px 20px;
            background:#FFFDFC;
        ">

            <div style="
                font-family:'Montserrat';
                font-size:10px;
                letter-spacing:3px;
                color:#667052;
                margin-bottom:15px;
            ">
                NUESTRA CANCIÓN
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.audio(
        str(musica),
        format="audio/mp3",
        autoplay=True
    )

else:

    st.markdown(
        """
        <div style="
            padding:30px;
            text-align:center;
            background:#FFFDFC;
            font-family:'Montserrat';
            font-size:10px;
            letter-spacing:3px;
            color:#667052;
        ">
            ♫ 1+1=1 · NANPA BÁSICO
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CIERRE
# =========================================================

st.markdown(
    f"""
<section class="closing">

    <div class="monogram">
        VH
    </div>

    <div class="closing-names">
        Valeria
        <span style="color:{TERRACOTA}">
            &
        </span>
        Hector
    </div>

    <div class="closing-date">
        {FECHA}
    </div>

    <div class="line"></div>

    <div class="text">
        Con amor, esperamos compartir
        este día contigo.
    </div>

</section>
""",
    unsafe_allow_html=True
)
