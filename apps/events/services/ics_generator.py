import requests
import re
from datetime import datetime, timedelta
from uuid import uuid4

from agendadosDjango.settings import GEMINI_API_KEY


def generate_event_ics(description):
    """
    Genera un archivo ICS completo basado en una descripción de horario usando Gemini.

    Args:
        description (str): Descripción del horario
        api_key (str): API key de Google Gemini (opcional)

    Returns:
        str: Contenido del archivo ICS
    """
    # URL de la API de Gemini
    api_key = GEMINI_API_KEY
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}'

    # Crear el prompt para generar ICS
    prompt = f"""Analiza esta descripción de horario: "{description}"

Instrucciones:
- Genera un archivo .ics COMPLETO y válido que represente este horario
- Incluye TODOS los componentes necesarios: VCALENDAR, VEVENT, VTIMEZONE si es necesario
- Usa RRULE cuando sea apropiado para horarios recurrentes
- Establece DTSTART apropiado (usa fecha actual como referencia: {datetime.now().strftime('%Y%m%d')})
- Incluye DTEND para cada evento
- Añade un SUMMARY descriptivo basado en la descripción
- Usa formato de fecha/hora correcto (YYYYMMDDTHHMMSS)
- El archivo debe ser completamente funcional e importable en cualquier calendario
- Usa zona horaria Europe/Madrid

RESPONDE ÚNICAMENTE con el contenido del archivo .ics, sin explicaciones adicionales.

Ejemplo de formato esperado:
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Generador Horarios//NONSGML v1.0//ES
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Europe/Madrid
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
DTSTART;TZID=Europe/Madrid:20250519T100000
DTEND;TZID=Europe/Madrid:20250519T140000
RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR
SUMMARY:Horario de trabajo
UID:horario-trabajo-1@example.com
DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}
END:VEVENT
END:VCALENDAR"""

    # Datos para la API
    data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': prompt
                    }
                ]
            }
        ]
    }

    try:
        # Realizar petición a Gemini
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            json=data,
            timeout=30
        )

        if not response.ok:
            raise Exception(f"Error HTTP: {response.status_code} - {response.text}")

        # Extraer respuesta
        json_response = response.json()
        raw_content = json_response.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '')

        if not raw_content:
            raise Exception("No se pudo obtener respuesta de Gemini")

        # Limpiar y validar contenido ICS
        ics_content = clean_ics_content(raw_content)

        # Validar que el contenido sea válido
        if not validate_ics_content(ics_content):
            # Si no es válido, intentar generar uno básico
            ics_content = generate_fallback_ics(description)

        return ics_content

    except Exception as e:
        print(f"Error al generar ICS con Gemini: {e}")
        # Generar ICS básico como fallback
        return generate_fallback_ics(description)


def clean_ics_content(raw_content):
    """
    Limpia el contenido ICS eliminando marcadores de código y texto innecesario.

    Args:
        raw_content (str): Contenido crudo de la respuesta

    Returns:
        str: Contenido ICS limpio
    """
    # Eliminar marcadores de código
    content = re.sub(r'```ics\n?|```\n?', '', raw_content).strip()

    # Si no empieza con BEGIN:VCALENDAR, buscar y extraer la parte válida
    if not content.startswith('BEGIN:VCALENDAR'):
        lines = content.split('\n')
        start_index = -1
        end_index = -1

        for i, line in enumerate(lines):
            if line.strip() == 'BEGIN:VCALENDAR':
                start_index = i
            elif line.strip() == 'END:VCALENDAR':
                end_index = i
                break

        if start_index != -1 and end_index != -1:
            content = '\n'.join(lines[start_index:end_index + 1])

    return content


def validate_ics_content(content):
    """
    Valida que el contenido ICS tenga la estructura básica correcta.

    Args:
        content (str): Contenido ICS a validar

    Returns:
        bool: True si es válido, False en caso contrario
    """
    required_elements = [
        'BEGIN:VCALENDAR',
        'END:VCALENDAR',
        'BEGIN:VEVENT',
        'END:VEVENT',
        'VERSION:',
        'DTSTART'
    ]

    return all(element in content for element in required_elements)


def generate_fallback_ics(description):
    """
    Genera un archivo ICS básico como fallback cuando Gemini falla.

    Args:
        description (str): Descripción del horario

    Returns:
        str: Contenido ICS básico
    """
    now = datetime.now()
    uid = str(uuid4())
    dtstamp = now.strftime('%Y%m%dT%H%M%SZ')

    # ICS básico con evento semanal
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Generador Horarios//NONSGML v1.0//ES
CALSCALE:GREGORIAN
BEGIN:VTIMEZONE
TZID:Europe/Madrid
BEGIN:DAYLIGHT
TZOFFSETFROM:+0100
TZOFFSETTO:+0200
TZNAME:CEST
DTSTART:19700329T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:+0200
TZOFFSETTO:+0100
TZNAME:CET
DTSTART:19701025T030000
RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
DTSTART;TZID=Europe/Madrid:{now.strftime('%Y%m%d')}T090000
DTEND;TZID=Europe/Madrid:{now.strftime('%Y%m%d')}T170000
RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR
SUMMARY:Horario: {description[:50]}...
DESCRIPTION:{description}
UID:{uid}@generador-horarios.com
DTSTAMP:{dtstamp}
END:VEVENT
END:VCALENDAR"""

    return ics_content


def save_ics_file(ics_content, description, filename=None):
    """
    Guarda el contenido ICS en un archivo.

    Args:
        ics_content (str): Contenido del archivo ICS
        description (str): Descripción del horario
        filename (str): Nombre del archivo (opcional)

    Returns:
        str: Nombre del archivo guardado
    """
    if filename is None:
        # Generar nombre único
        date_str = datetime.now().strftime('%Y%m%d_%H%M')
        clean_desc = re.sub(r'[^a-zA-Z0-9]', '_', description[:20])
        filename = f"horario_{date_str}_{clean_desc}.ics"

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(ics_content)
        print(f"✅ Archivo guardado como: {filename}")
        return filename
    except Exception as e:
        print(f"❌ Error al guardar archivo: {e}")
        return None


# Ejemplo de uso
if __name__ == "__main__":
    # Descripción de ejemplo
    descripcion_ejemplo = "De dilluns a divendres: de 10 a 14 h i de 17 a 20 h Dissabtes: d'11 a 14 h i de 17 a 20 h Diumenges i altres festius: d'11 a 14 h"

    # Generar archivo ICS
    print("Generando archivo ICS...")
    contenido_ics = generate_event_ics(descripcion_ejemplo)

    # Guardar archivo
    nombre_archivo = save_ics_file(contenido_ics, descripcion_ejemplo)

    # Mostrar contenido
    print("\n--- CONTENIDO ICS GENERADO ---")
    print(contenido_ics)