/*
 * versuch_1_blinkende_led – USER-CODE-Abschnitte für Core/Src/main.c
 *
 * Projekt in STM32CubeIDE: File > New > STM32 Project > Board Selector
 * (NUCLEO-F767ZI bzw. euer Nucleo-144-Board), Name "versuch_1_blinkende_led",
 * "Initialize all peripherals with their default Mode" = Yes, Code generieren.
 *
 * Standard-Pinbelegung (Nucleo-144, aus UM1974):
 *   LD1 (grün)   -> PB0   (LD1_GPIO_Port / LD1_Pin)
 *   USER_Btn     -> PC13  (USER_Btn_GPIO_Port / USER_Btn_Pin), gedrückt = HIGH
 *   USART3 (VCP) -> PD8 TX / PD9 RX, 115200 Baud 8N1 über ST-LINK (huart3)
 *
 * Nur die Inhalte zwischen den passenden USER-CODE-Markern einfügen,
 * damit sie beim Neugenerieren erhalten bleiben.
 */

/* USER CODE BEGIN PV */
volatile uint8_t taster_zustand = 0;   /* 2.4: globaler Tasterzustand (0/1) */
volatile char    taster_char    = 0;   /* 2.5: Zustand als char für UART    */
/* USER CODE END PV */

/* ... in main(), Endlosschleife: */

  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* 2.3/2.4: Taster an PC13 einlesen */
    taster_zustand = (uint8_t)HAL_GPIO_ReadPin(USER_Btn_GPIO_Port, USER_Btn_Pin);

    /* 2.2/2.3: 2 Hz = 500 ms Periode -> alle 250 ms toggeln,
       solange der Taster NICHT gedrückt ist */
    if (taster_zustand == GPIO_PIN_RESET)
    {
      HAL_GPIO_TogglePin(LD1_GPIO_Port, LD1_Pin);
    }

    /* 2.5: Zustand als char per UART3 (ST-LINK Virtual COM Port) senden */
    taster_char = (char)taster_zustand;            /* Rohwert 0x00 / 0x01 */
    HAL_UART_Transmit(&huart3, (uint8_t *)&taster_char, 1, HAL_MAX_DELAY);

    HAL_Delay(250);
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
