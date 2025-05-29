import requests
import re
from datetime import datetime
import json
from icalendar import Calendar

from agendadosDjango.settings import GEMINI_API_KEY


def generate_event_ics(description, start_date=None, end_date=None):
    """
    Genera un archivo ICS completo basado en una descripción de horario usando Gemini.

    Args:
        description (str): Descripción del horario
        start_date (str, optional): Fecha de inicio en formato 'YYYY-MM-DD'
        end_date (str, optional): Fecha de fin en formato 'YYYY-MM-DD'
        api_key (str): API key de Google Gemini (opcional)

    Returns:
        str: Contenido del archivo ICS
    """
    # URL de la API de Gemini
    api_key = GEMINI_API_KEY
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}'

    # Formatear fechas para el prompt
    current_date = datetime.now().strftime('%Y%m%d')
    start_date_info = f"Fecha de inicio: {start_date}" if start_date else f"Usa fecha actual como referencia: {current_date}"
    end_date_info = f"Fecha de fin: {end_date}" if end_date else ""

    # Crear el prompt para generar ICS
    prompt = f"""Analiza esta descripción de horario: "{description}"

Instrucciones:
- Genera un archivo .ics COMPLETO y válido que represente este horario
- Incluye TODOS los componentes necesarios: VCALENDAR, VEVENT, VTIMEZONE si es necesario
- Usa RRULE cuando sea apropiado para horarios recurrentes
- {start_date_info}
- {end_date_info}
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

        ics_content = clean_ics_content(raw_content)

        return ics_content

    except Exception as e:
        print(f"Error al generar ICS con Gemini: {e}")
        # Generar ICS básico como fallback

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
    required_elements = [
        'BEGIN:VCALENDAR',
        'END:VCALENDAR',
        'BEGIN:VEVENT',
        'END:VEVENT',
        'VERSION:',
        'DTSTART'
    ]

    return all(element in content for element in required_elements)

def parse_ics_string_to_json(ics_string):
    cal = Calendar.from_ical(ics_string.encode("utf-8"))

    events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            event = {
                "summary": str(component.get("summary")),
                "description": str(component.get("description", "")),
                "location": str(component.get("location", "")),
                "start": component.get("dtstart").dt.isoformat() if isinstance(component.get("dtstart").dt, datetime) else str(component.get("dtstart").dt),
                "end": component.get("dtend").dt.isoformat() if isinstance(component.get("dtend").dt, datetime) else str(component.get("dtend").dt),
                "uid": str(component.get("uid")),
            }
            events.append(event)

    return json.dumps(events, indent=4, ensure_ascii=False)
