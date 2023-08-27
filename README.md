## Anleitung zum Starten von Server und Client

Folgen Sie diesen Schritten, um Server und Client korrekt zu starten:

1. **config.txt anpassen:**
   - Auf dem Server: Tragen Sie nur Ihre eigene IP-Adresse ein.
   - Auf dem Client: Tragen Sie die IP-Adresse des Servers und die MAC des Controllers ein.

2. **Server starten:**
   - Im Terminal:
     ```bash
     $env:PYTHONPATH += ";[Your_Path]\4x4_gewinnt"
     py .\py_server\src\ConnectCollect.py
     ```
   - Alternativ in PyCharm:
     - Öffnen Sie `ConnectCollect.py`.
     - Wählen Sie `Run CurrentFile`.

3. **Controller in Pairing-Mode bringen.**

4. **Client starten:**
   - Navigieren Sie in den `cpp_client` Ordner:
     ```bash
     bash run.sh
     ```

Vergewissern Sie sich, dass Sie vor dem Start alle erforderlichen Abhängigkeiten und Einstellungen vorgenommen haben.

## Server Keybinds

Taste: `1` - Keyboard Spieler hinzufügen (sofern noch keiner existiert)
Taste: `2` - Keyboard Spieler entfernen (sofern bereits einer existiert)

Pfeiltasten liks, rechts, unten - Steuerung des Spiel-Chips analog zur Controller-Steuerung
