# NXOpen Python-Integration

Dieses Repository enthält Skripte, die die NXOpen API für die Automatisierung von Designaufgaben in Siemens NX verwenden. Der Code ermöglicht es, verschiedene Eigenschaften von Körpern, Skizzen und Features in einer NX-Sitzung zu analysieren und zu drucken.

## Übersicht

Das Skript setzt voraus, dass Siemens NX installiert und korrekt konfiguriert ist, um Python-Skripte auszuführen. Es verwendet die NXOpen Python-API, um Zugriff auf die Modellierungskomponenten zu erhalten und Details zu diesen Komponenten systematisch auszugeben.

### Hauptfunktionen

- **Körperdetails**: Listet Informationen zu allen Körpern in einem Teil auf, einschließlich ihrer Flächen und der Kanten jeder Fläche.
- **Skizzendetails**: Analysiert alle Skizzen, um spezifische Kantenlängen und Muster zu überprüfen.
- **Feature-Analyse**: Gibt Details zu bestimmten Features wie Extrusionen, Bohrungen und Rotationen aus.
  
### Besondere Merkmale

- **Fehlerprüfung**: Der Code handhabt Fehler und unerwartete Werte während des Zugriffs auf die Eigenschaften der Modellelemente.
- **Detaillierte Ausgabe**: Für jedes Feature und jede geometrische Komponente werden detaillierte technische Daten bereitgestellt, die für die Überprüfung und Analyse nützlich sind.

### Anwendungsszenarien

- **Automatisierte Qualitätssicherung**: Automatische Überprüfung von Maßen und Geometrien gegen vorgegebene Spezifikationen.
- **Dokumentationserstellung**: Generieren von Berichten über die verwendeten Features und Komponenten in einem Modell.

### Nutzung

Um das Skript auszuführen, starten Sie Ihre NX-Sitzung und laden Sie das Python-Skript in die NX-Umgebung. Das Skript beginnt mit der Analyse der aktuellen Arbeitssitzung und gibt seine Ergebnisse in das NX Listing Window aus.
