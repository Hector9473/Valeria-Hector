import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import urlencode
import base64
import html


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

LUGAR = "Parroquia Nuestra Señora del Café"
DIRECCION = "Calle 23 A Norte #14-74"
CIUDAD = "Armenia, Quindío"

MAPS_URL = "https://maps.app.goo.gl/zgLv9FpbRy9U6T177"
FORMS_URL = "https://forms.gle/4cGepJCuvvtpjZpq6"

MENSAJE = """
Queremos que seas testigo de la unión de dos corazones,
de dos almas, de dos seres que decidieron amarse
y juntar sus vidas como uno solo en el camino de Dios.
"""

# Invitados de prueba
INVITADOS = {
    f"invitado-{i}": f"Invitado {i}"
    for i in range(1, 26)
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

st.markdown(
    f"""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700'
        '&family=Montserrat:wght@300;400;500;600'
        '&display=swap'
    );

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

    header {{
        visibility: hidden;
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

    .dress-title {{
        font-family: 'Cormorant Garamond', serif;
        font-size: 50px;
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
    """,
    unsafe_allow_html=True
)


# =========================================================
# PANEL DE CONFIGURACIÓN
# =========================================================

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

    st.markdown("### 📸 Fotografías")

    fotos = st.file_uploader(
        "Sube entre 6 y 10 fotografías",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )

    st.divider()

    st.markdown("### 👗 Código de vestuario")

    imagen_vestuario = st.file_uploader(
        "Imagen de referencia",
        type=["jpg", "jpeg", "png", "webp"]
    )

    st.divider()

    st.markdown("### 🎵 Música")

    musica = st.file_uploader(
        "Archivo de audio",
        type=["mp3", "wav", "m4a"]
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

    st.info(
        "En esta V1 los archivos cargados funcionan durante "
        "la sesión. En la siguiente etapa podemos hacerlos "
        "permanentes."
    )


# =========================================================
# PORTADA
# =========================================================

st.markdown(
    f"""
    <section class="hero">

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
    """,
    unsafe_allow_html=True
)


# =========================================================
# PERSONALIZACIÓN
# =========================================================

st.markdown(
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

        <div class="branch">
            ❧
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
    """,
    unsafe_allow_html=True
)


# =========================================================
# FECHA Y CEREMONIA
# =========================================================

st.markdown(
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
    """,
    unsafe_allow_html=True
)


# =========================================================
# MAPA
# =========================================================

st.markdown(
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
    """,
    unsafe_allow_html=True
)


# =========================================================
# GALERÍA
# =========================================================

st.markdown(
    """
    <section class="section section-beige">

        <div class="section-label">
            Nosotros
        </div>

        <div class="gallery-title">
            Algunos momentos
        </div>

    </section>
    """,
    unsafe_allow_html=True
)

if fotos:

    columnas = st.columns(2)

    for i, foto in enumerate(fotos):

        with columnas[i % 2]:
            st.image(
                foto,
                use_container_width=True
            )

else:

    st.markdown(
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
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CÓDIGO DE VESTUARIO
# =========================================================

st.markdown(
    f"""
    <section class="section section-olive">

        <div class="section-label">
            Código de vestuario
        </div>

        <div class="dress-title">
            Verde claro
        </div>

        <div class="dress-warning">
            🚫 El blanco es exclusivo de la novia.
        </div>

        <div class="separator"></div>

        <div class="dress-warning">
            Te esperamos a las {HORA_LLEGADA}
        </div>

    </section>
    """,
    unsafe_allow_html=True
)

if imagen_vestuario:

    st.image(
        imagen_vestuario,
        caption="Imagen de referencia",
        use_container_width=True
    )

else:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:50px 20px;
            background:#F2EBDD;
            font-family:'Montserrat',sans-serif;
        ">
            👗<br><br>
            Aquí aparecerá la imagen de referencia
            del código de vestuario.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# CONFIRMACIÓN
# =========================================================

st.markdown(
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
            padding:20px;
            background:#FFFDFC;
        ">
            <div style="
                font-family:'Montserrat',sans-serif;
                font-size:11px;
                letter-spacing:2px;
                color:#667052;
                margin-bottom:10px;
            ">
                NUESTRA CANCIÓN
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.audio(
        musica,
        format="audio/mp3",
        autoplay=False
    )

else:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:30px;
            background:#FFFDFC;
            font-family:'Montserrat',sans-serif;
            font-size:11px;
            letter-spacing:2px;
            color:#667052;
        ">
            ♫ &nbsp; 1+1=1 · Nanpa Básico
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
    """,
    unsafe_allow_html=True
)


# =========================================================
# INFORMACIÓN PARA PRUEBAS
# =========================================================

with st.expander("🔧 Información de prueba"):

    st.write(
        f"Invitado identificado: **{nombre_invitado}**"
    )

    st.code(
        f"https://TU-DOMINIO.streamlit.app/?invitado={codigo_invitado}"
    )

    st.caption(
        "Esta sección podrá ocultarse cuando publiquemos la versión final."
    )