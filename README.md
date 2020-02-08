# Numerowany Kolaż

Program pozwalający na tworzenie kolaży zdjęć z możliwością numeracji oraz wstawienia znaku wodnego/logo. Kolaże tworzone są w grupach po 4 lub mniej, jeśli nie ma innej możliwości. Dodatkowo sortowane są wymiarami na portretowe i krajobrazowe.

Przydatne dla osób, które potrzebują mieć ponumerowane zdjęcia automatycznie i szybko. Przykładowe zastosowanie, to fotografia - ułatwienie klientowi wyboru zdjęć poprzez odniesienie się do nich przy pomocy numerów.

## Instalacja

Program do działania wymaga zainstalowanego [Python 3.7.0][pyth] wraz z modułem [Pillow][pil]. Moduł można zainstalować korzystając z managera [pip][pip], komendą

```
pip install Pillow
```

## Działanie aplikacji

### Obsługa

Aplikację otwiera się plikiem `numbered-collages.pyw`. Zbiór zdjęć, które mają być przekształcone na kolaż powinien znajdować się w jednym dowolnym katalogu. Po naciśnięciu `Wybierz folder` należy wskazać katalog ze zdjęciami. Obsługiwana jest grafika w formacie `jpg`. Po wyborze wystaczy nacisnąć `Utwórz kolaże` i poczekać na komunikat. Utworzony zostanie folder z przetworzonymi obrazami o nazwie `kolaże`, w wybranej wcześniej lokalizacji.

### Sposób tworzenia kolaży

Kolaże tworzone są w grupach po 4 lub mniej na jeden plik. Dodatkowo sortowane są wymiarami na portretowe (szerokość mniejsza niż wysokość) oraz krajobrazowe (szerokość większa niż wysokość). W lewym górnym rogu każdego zdjęcia kolażu, dostawiany jest numer zdjęcia, a w prawym dolnym znak wodny/logo z pliku `watermark.png`. Jeżeli w danym kolażu są tylko 3 zdjęcia, w utworzone puste miejsce wstawiona jest grafika z pliku `logo.png`.

### Dodatkowe uwagi

 * Wybrana lokalizacja folderu zostaje zapamiętana po zamknięciu aplikacji.
 * Zdjęcia przygotowane do kolażu powinny mieć wymiary co najmniej `900x600px` lub `600x900px`.
 * Aby zmienić znak wodny na własny, należy nadpisać plik z grafiką o nazwie `watermark.png`. Powinien mieć szerokość ok. `200px`.
 * Aby zmienić grafikę wstawianą przy kolażu złożonego z trzech zdjęć, należy nadpisać plik `logo.png`. Powinien mieć szerokość ok. `400px`.
 * Do zmiany grafiki w aplikacji należy nadpisać plik `logo.gif`. Powinien mieć szerokość ok. `200px`.
 * Jeżeli aplikacja nie działa prawidłowo, można przejżeć błędy w utworzonym pliku `log.txt`.

[pyth]: <https://www.python.org/downloads/release/python-370/>
[pip]: <https://pip.pypa.io/en/stable/>
[pil]: <https://pillow.readthedocs.io/en/stable/>
