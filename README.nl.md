# Hoe werkt het?

## snake.py
Het bestand snake.py (het bestand dat word gestart om de game te starten) bestaat uit 4 belangrijke functies. updateWindow(), home(), snake() en pause().

### updateWindow()
De functie updateWindow doet wat de naam suggereert en update de game window met `pygame.display.flip()`. Ook checkt het of de escape toets is ingedrukt of op het kruisje van het scherm is gedrukt en sluit daarna het scherm en stopt het programma met sys.exit(0). De nul is optioneel en staat voor ["successful termination"](https://docs.python.org/3/library/sys.html#sys.exit). Ook zorgt updateWindow ervoor dat de width en height variabele worden veranderd zodra het scherm word veranderd van grootte, omdat ik het scherm de [pygame.RESIZABLE](http://www.pygame.org/docs/ref/display.html#pygame.display.set_mode) flag mee heb gegeven bij het [initializeren van het scherm](https://github.com/Wouterr0/Snake/blob/master/snake.py#L35). Omdat ik de [pygame_gui](https://github.com/MyreMylar/pygame_gui) gebruik voor de slider moet ik de manager ook [updaten](https://github.com/Wouterr0/Snake/blob/master/snake.py#L60).