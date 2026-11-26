from google import genai
from google.genai import types
SYSTEM_PROMPT = """Jesteś pomocnym asystentem pogodowym. Na podstawie pogody i profilu użytkownika doradź naturalnie i konkretnie, jak się ubrać.
Zasady:
- Pisz po polsku, płynnie i normalnym, ludzkim językiem — bez sztywnych szablonów, wstępów, wypunktowań i emotikon.
- Długość: 3–4 sensowne zdania.
- Nie wspominaj o ubraniach przeciwdeszczowych przy śladowych opadach (poniżej 0.5 mm deszczu), chyba że prawdopodobieństwo opadów jest wysokie (powyżej 60%). Podobnie przy śladowym śniegu nie przesadzaj z alarmowaniem.
- Jeśli użytkownik ma aktywności (np. bieganie, rower, siłownia, spacery), wskaż najlepszą porę dnia na nie na podstawie prognozy; przy bieganiu uwzględnij krótko strój na trening, ale przed tym ZAWSZE uwzględnij ubiór na zwykłe wyjście z domu (np. na spacer/spontaniczne wyjście).
- Jeśli ciśnienie jest wyraźnie wysokie (> 1020 hPa) lub niskie (< 1000 hPa), naturalnie wspomnij o możliwym wpływie na samopoczucie."""

ACTIVITY_HINTS = {
    "running": "użytkownik biega, więc ubranie ma być oddychające i warstwowe, bo podczas wysiłku robi się cieplej. W swojej odpowiedzi uwzględnij zasugerowany ubiór na trening biegowy, jak i drugi wariant ubioru na normalne wyjście z domu, np. na spacer, zakupy",
    "cold": "użytkownik jest wrażliwy na zimno, więc dobieraj cieplejsze ubrania, "
            "niż wynikałoby z samej temperatury",
    "cold_resistance": "użytkownik jest odporny na zimno, więc możesz dobierać lżejsze ubrania, niż wynikałoby z samej temperatury i komfortu dla przeciętnego człowieka",
    "often_walking": "użytkownik często spaceruje, wychodzi na powietrze",
    "gym": "użytkownik trenuje siłowo. Biorąc pod uwagę temperaturę i ciśnienie, zaproponuj najlepszą porę na siłownię i ciężary.",
    "rarely_outside": "użytkownik rzadko wychodzi z domu",
    "pressure_sensitive": "użytkownik jest wrażliwy na wysokie ciśnienie, miewa bóle głowy",
    "cycling": "użytkownik jeździ na rowerze",
    "wind_sensitive": "użytkownik jest wrażliwy na wiatr",
    "often_sick": "użytkownik zgłasza częste przeziębienia"
}
'''
"Bieganie": "running",
            "Wrażliwość na zimno": "cold",
            "Odporność na zimno": "cold_resistance",
            "Częste spacery": "often_walking",
            "Trening siłowy": "gym",
            "Rzadkie wyjścia z domu": "rarely_outside",
            "Wrażliwość na wysokie ciśnienie": "pressure_sensitive",
            "Jazda na rowerze": "cycling",
            "Wrażliwość na wiatr": "wind_sensitive",
            "Częste przeziębienia": "often_sick"
'''

def build_prompt(weather, active_activities):
    current_hour = weather.current_hour
    lines =[
        f"Temperatura: {weather.temperature}°C",
        f"Wiatr: {weather.wind} km/h",
        f"Aktualne cisnienie: {weather.pressure} hPa",
        f"Maksymalne prawdopodobienstwo opadow do konca dnia: {max(weather.precipitation_probability[current_hour:])}",
        f"Suma opadów śniegu do konca dnia (cm): {sum(weather.snowfall[current_hour:])} ",
        f"Suma opadów deszczu do konca dnia (mm): {sum(weather.rain[current_hour:])}",
    ]

    if weather.hourly_temp is not None:
        lines.append(f"Prognoza temperatur: {weather.hourly_temp}")

    hints = []

    for activity in active_activities:
        if activity in ACTIVITY_HINTS:
            hints.append(ACTIVITY_HINTS[activity])

    if hints:
       lines.extend(hints)
    else:
        lines.append("Brak szczegolnych preferencji uzytkownika")

    return lines

def generate_suggestions(weather, active_activities):
    client = genai.Client()

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=build_prompt(weather, active_activities),
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            ),
        )
        return response.text
    except Exception as e:
        print(f"błąd AI: {e}")
        return f"Nie udało się teraz wygenerować rekomendacji (asystent AI jest przeciążony). Spróbuj ponownie później."

