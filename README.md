# CoDzisNaSobie app

Co Dziś na Sobie? to aplikacja desktopowa, która pomaga zaplanować dzień na podstawie aktualnej pogody. Użytkownik wpisuje nazwę miasta, a program pobiera dane pogodowe z API Open Meteo. Na ich podstawie aplikacja wyświetla temperaturę, wysokość opadów, siłę wiatru, jakość powietrza, rysuje wykres prognozy oraz generuje spersonalizowane porady, np. “weź parasol”, “załóż kurtkę”, czy nawet “najlepsze okno na bieganie to 17:00-18:30”. Porady będą uwzględniać profil użytkownika (np. Czy łatwo marznie, biega, jeździ rowerem), który zapisuje się w ustawieniach (plik json). Do pliku zapisywane będą również m.in ulubione miasta, w których pogodę śledzi użytkownik. Każde konto i podstawowe informacje o nim (w tym hashowane hasło) znajdują się w bazie danych, komunikującą się z kodem za pomocą SQLite3

## Run the app

### uv

Run as a desktop app:

```bash
uv run flet run
```

Run as a web app:

```bash
uv run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/).

## Build the app

### Android

```bash
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```bash
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```bash
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```bash
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```bash
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).

### Web

```bash
flet build web -v
```

For more details on building Web app, refer to the [Web Packaging Guide](https://flet.dev/docs/publish/web/).
