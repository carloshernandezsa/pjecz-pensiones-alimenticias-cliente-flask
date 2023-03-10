"""
Solicitudes, formularios
"""
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
import requests
from wtforms import BooleanField, EmailField, HiddenField, SelectField, StringField, SubmitField, FileField
from wtforms.validators import DataRequired, Length

from config.settings import API_BASE_URL, API_TIMEOUT
from lib.hashids import descifrar_id


class IngresarForm(FlaskForm):
    """Formulario para ingresar datos personales"""

    try:
        respuesta = requests.get(
            f"{API_BASE_URL}/distritos",
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        abort(500, "No se pudo conectar con la API Distritos. " + str(error))
    except requests.exceptions.Timeout as error:
        abort(500, "Tiempo de espera agotado al conectar con la API Distritos. " + str(error))
    except requests.exceptions.HTTPError as error:
        abort(500, "Error HTTP porque la API Distritos arrojó un problema: " + str(error))
    except requests.exceptions.RequestException as error:
        abort(500, "Error desconocido con la API Distritos. " + str(error))
    datos = respuesta.json()

    # Seleccionar unicamente Distritos de la respuesta de la API
    items_distritos = datos["result"]["items"]
    catalogo = []
    for item in items_distritos:
        if not item["nombre"].find("DISTRITO"):
            catalogo.append({"id_hasheado": item["id_hasheado"], "nombre": item["nombre"]})

    nombres = StringField(
        "Nombres",
        default="Carlos Gabriel",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    apellido_primero = StringField(
        "Primer apellido",
        default="Hernandez",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    apellido_segundo = StringField(
        "Segundo apellido",
        default="Salas",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    curp = StringField(
        "CURP",
        default="HESC741104HCLRLR09",
        validators=[DataRequired(), Length(min=18, max=18)],
        render_kw={"placeholder": "18 caracteres"},
    )
    email = EmailField(
        "Email",
        default="carlos.hernandez@coahuila.gob.mx",
        validators=[DataRequired(), Length(min=3, max=128)],
    )
    telefono = StringField(
        "Telefono celular",
        default="8442180123",
        validators=[DataRequired(), Length(min=10, max=10)],
        render_kw={"placeholder": "10 dígitos sin espacios ni guiones"},
    )
    colonia = StringField(
        "Colonia",
        default="Lomas de Lourdes",
        validators=[DataRequired(), Length(min=10, max=50)],
    )
    calle = StringField(
        "Calle",
        default="Correcaminos",
        validators=[DataRequired(), Length(min=10, max=50)],
    )
    numero = StringField(
        "Numero",
        default="1290",
        validators=[DataRequired(), Length(min=2, max=15)],
    )
    codigo = StringField(
        "Numero",
        default="25290",
        validators=[DataRequired(), Length(min=5, max=5)],
    )
    compania = SelectField(
        "Compañia telefónica",
        validators=[DataRequired()],
        choices=[("", "Selecciona una compañia"), ("Telcel", "Telcel"), ("Movistar", "Movistar"), ("UNEFON", "UNEFON"), ("IUSACELL", "IUSACELL"), ("AT&T", "AT&T")],
    )
    distrito = SelectField(
        "Distrito Judicial",
        validators=[DataRequired()],
        choices=[("", "Selecciona un Distrito")] + [(descifrar_id(key["id_hasheado"]), key["nombre"]) for key in catalogo],
        render_kw={"onchange": "obtenerJuzgados()"},
        validate_choice=False,
    )
    juzgado = SelectField(
        "Juzgado",
        validators=[DataRequired()],
        choices=[("", "Selecciona un Juzgado")],
        validate_choice=False,
    )
    expediente = StringField(
        "Número de Expediente",
        validators=[DataRequired()],
        render_kw={"placeholder": "Expediente"},
    )
    ine = FileField(
        "Credencial de elector",
        validators=[DataRequired()],
        render_kw={"placeholder": "Seleccione un archivo PDF con la INE por ambos lados", "accept": "application/pdf"},
    )
    comprobante = FileField(
        "Comprobante de domicilio",
        validators=[DataRequired()],
        render_kw={"placeholder": "Seleccione un archivo PDF del comprobante de domicilio", "accept": "application/pdf"},
    )
    autorizacion = FileField(
        "Autorización firmada",
        validators=[DataRequired()],
        render_kw={"placeholder": "Autorización firmada en archivo PDF", "accept": "application/pdf"},
    )
    # recaptcha = RecaptchaField()
    aceptar = BooleanField(
        "He leído y acepto el <a href='/aviso' class='nav-link link-aviso'>Aviso de Privacidad</a>",
        validators=[DataRequired()],
        default="checked",
    )
    registrar = SubmitField("Registrar")
