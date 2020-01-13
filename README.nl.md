# Hoe werkt het?

## snake.py
Het bestand snake.py (het bestand dat wordt gestart om de game te starten) bestaat uit 4 belangrijke functies: `updateWindow()`, `home()`, `snake()` en `pause()`.

Als het bestand wordt uitgevoerd, komt het in een eindeloze lus van `snake(*home())`.

### updateWindow()
De functie `updateWindow` doet wat de naam suggereert en ververst het scherm met `pygame.display.flip()`. Ook controleert het of <kbd>Esc</kbd> is ingedrukt of op het kruisje van het scherm is gedrukt en sluit daarna het scherm en stopt het programma met sys.exit(0). De nul is optioneel en staat voor ["successful termination"](https://docs.python.org/3/library/sys.html#sys.exit). Ook zorgt `updateWindow` ervoor dat de variabelen `width` en `height` worden veranderd zodra het scherm wordt veranderd van grootte, omdat ik het scherm de [pygame.RESIZABLE](http://www.pygame.org/docs/ref/display.html#pygame.display.set_mode) flag mee heb gegeven bij het [initialiseren van het scherm](https://github.com/Wouterr0/Snake/blob/master/snake.py#L35). Omdat ik de [pygame_gui](https://github.com/MyreMylar/pygame_gui) gebruik voor de slider, moet ik de [manager](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.html#pygame_gui.ui_manager.UIManager) daarna ook [updaten](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.html#pygame_gui.ui_manager.UIManager.update).

### home()
De functie `home` is voor het beginscherm en begint met het renderen van de tekst "PLAY". Daarna wordt er gebruik gemaakt van de bibliotheek `pygame_ui` en aan de variabele `slider` een [`pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider`](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.elements.html#module-pygame_gui.elements.ui_horizontal_slider) toegekend. Dan wordt een `pygame.time.Clock` gemaakt om ervoor te zorgen dat het even snel gaat op elke computer.

De functie komt dan in een eindeloze lus met `while True`. Dan wordt de `repeatTileImage` functie uit [config.py](./config.py#L33) gebruikt (wat een plaatje herhaalt tot een bepaalde grootte) om het scherm te vullen met [achtergrondplaatje](assets/brick.png), nadat het is vergroot met [`startBgImage.resize`](https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#PIL.Image.Image.resize). Als de gebruiker op <kbd>b</kbd> drukt, gaat `berryMode` aan. Het maakt ook een [obj.Button](objects.py#L182) voor de startknop. Verder tekent het daarna dingen de achtergrond. Dan updatet het de [slider](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.elements.html#module-pygame_gui.elements.ui_horizontal_slider) en de [`pygame_gui manager`](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.html#pygame_gui.ui_manager.UIManager). Het verandert daarna de kleur van de startknop afhankelijk van of de muispositie en positie van de startknop. Dan wordt de startknop, de tekst met de level en berrymode en de tekst met "PLAY" erop getekend op het scherm. Het roept daarna `updateWindow` aan om het scherm te verversen.

### snake()
De functie `snake` is voor het spel zelf en neemt als argumenten de moeilijkheidsgraad en of berryMode aan staat. Aan het begin genereert het een willekeurige kleur voor de vakjes en dezelfde kleur maar dan donkerder voor de randjes van de vakken. Het berekend de breedte en hoogte van het raster door de formule: `-2 * (moeilijkheidsgraad van 1-10) + 29 `. 
