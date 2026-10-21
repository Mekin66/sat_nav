# Versuch 1 – Blinkende LED

Code: [`main_user_code.c`](main_user_code.c) (USER-CODE-Abschnitte für `Core/Src/main.c`).

## 2.1 Projekt
STM32CubeIDE → neues STM32-Projekt über *Board Selector* (Nucleo-144, z. B. NUCLEO-F767ZI), Name `versuch_1_blinkende_led`, Peripherie im Default-Modus initialisieren, Code generieren.

## 2.2 Blinken mit 2 Hz
2 Hz → Periode 500 ms → LED alle **250 ms** toggeln (`HAL_GPIO_TogglePin` + `HAL_Delay(250)`). LD1 liegt auf **PB0**.

## 2.3 Blinken per Taster unterbrechen
USER_Btn (blau) liegt auf **PC13**, Eingang, gedrückt = `GPIO_PIN_SET`. Solange gedrückt, wird nicht getoggelt – die LED bleibt im letzten Zustand (an oder aus).

## 2.4 Tasterzustand in STM32CubeMonitor
Globale Variable `taster_zustand` (`volatile`, sonst ggf. wegoptimiert). In CubeMonitor die `.elf` laden, Variable auswählen, Template-Flow deployen, *Start Acquisition*.

**Beobachtung:**
- Der Wert springt zwischen 0 (losgelassen) und 1 (gedrückt) – Rechtecksignal im Plot.
- Die Variable wird nur alle 250 ms aktualisiert, CubeMonitor tastet zusätzlich mit eigener Rate ab → Flanken erscheinen verzögert, sehr kurze Tastendrücke (< 250 ms) können fehlen.
- Das Auslesen erfolgt über SWD im laufenden Betrieb, ohne das Programm anzuhalten.

## 2.5 Ausgabe über UART / hterm
`taster_char` (Typ `char`) wird per `HAL_UART_Transmit(&huart3, …)` gesendet. USART3 ist mit dem ST-LINK verbunden (Virtual COM Port). hterm: COM-Port des ST-LINK, **115200 Baud, 8N1**.

**Beobachtung:**
- Es kommt alle 250 ms ein Byte an.
- In der **ASCII-Ansicht** ist nichts Sinnvolles lesbar: gesendet werden die Rohwerte `0x00`/`0x01`, das sind nicht druckbare Steuerzeichen (NUL, SOH).
- In der **Hex-/Dez-Ansicht** von hterm sieht man korrekt `00` bzw. `01`.
- Für lesbare Ausgabe muss in ASCII gewandelt werden, z. B. `taster_char = '0' + taster_zustand;` → `'0'` (0x30) / `'1'` (0x31).
- Falsche Baudrate in hterm → Zeichensalat.
