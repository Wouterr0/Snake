# Hoe werkt het?

## snake.py
Het bestand snake.py (het bestand dat wordt gestart om de game te starten) bestaat uit 4 belangrijke functies:
 - [updateWindow](README.nl.md#updateWindow) <sub>\[[in file](snake.py#L40)\]</sub>
 - [home](README.nl.md#home) <sub>\[[in file](snake.py#L71)\]</sub>
 - [snake](README.nl.md#snake) <sub>\[[in file](snake.py#L148)\]</sub>
 - [pause](README.nl.md#pause) <sub>\[[in file](snake.py#L224)\]</sub>

Als het bestand wordt uitgevoerd, komt het in een eindeloze lus van `snake(*home())`.

### updateWindow()
De functie `updateWindow` doet wat de naam suggereert en ververst het scherm met `pygame.display.flip()`. Ook controleert het of <kbd>Esc</kbd> is ingedrukt of op het kruisje van het scherm is gedrukt en sluit daarna het scherm en stopt het programma met sys.exit(0). De nul is optioneel en staat voor ["successful termination"](https://docs.python.org/3/library/sys.html#sys.exit). Ook zorgt `updateWindow` ervoor dat de variabelen `width` en `height` worden veranderd zodra het scherm wordt veranderd van grootte, omdat ik het scherm de [pygame.RESIZABLE](http://www.pygame.org/docs/ref/display.html#pygame.display.set_mode) flag mee heb gegeven bij het [initialiseren van het scherm](https://github.com/Wouterr0/Snake/blob/master/snake.py#L35). Omdat ik de [pygame_gui](https://github.com/MyreMylar/pygame_gui) gebruik voor de slider, moet ik de [manager](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.html#pygame_gui.ui_manager.UIManager) daarna ook [updaten](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.html#pygame_gui.ui_manager.UIManager.update).

### home()
De functie `home` is voor het beginscherm en begint met het renderen van de tekst "PLAY". Daarna wordt er gebruik gemaakt van de bibliotheek `pygame_ui` en aan de variabele `slider` een [`pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider`](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.elements.html#module-pygame_gui.elements.ui_horizontal_slider) toegekend. Dan wordt een `pygame.time.Clock` gemaakt om ervoor te zorgen dat het even snel gaat op elke computer.

De functie komt dan in een eindeloze lus met `while True`. Dan wordt de `repeatTileImage` functie uit [config.py](./config.py#L33) gebruikt (wat een plaatje herhaalt tot een bepaalde grootte) om het scherm te vullen met [achtergrondplaatje](assets/brick.png), nadat het is vergroot met [`startBgImage.resize`](https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#PIL.Image.Image.resize). Als de gebruiker op <kbd>b</kbd> drukt, gaat `berryMode` aan. Het maakt ook een [`obj.Button`](objects.py#L182) voor de startknop. Verder tekent het daarna dingen de achtergrond. Dan updatet het de [slider](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.elements.html#module-pygame_gui.elements.ui_horizontal_slider) en de [`pygame_gui manager`](https://pygame-gui.readthedocs.io/en/latest/pygame_gui.html#pygame_gui.ui_manager.UIManager). Het verandert daarna de kleur van de startknop afhankelijk van of de muispositie en positie van de startknop. Dan wordt de startknop, de tekst met de level en berrymode en de tekst met "PLAY" erop getekend op het scherm. Het roept daarna `updateWindow` aan om het scherm te verversen.

### snake()
De functie `snake` is voor het spel zelf en neemt als argumenten de moeilijkheidsgraad en of berryMode aan staat. Aan het begin genereert het een willekeurige kleur voor de vakjes en dezelfde kleur maar dan donkerder voor de randjes van de vakken. Het berekend de breedte en hoogte van het raster door de formule: `-2 * (moeilijkheidsgraad van 1-10) + 29 `. Daarna maakt het een [`obj.Grid`](objects.py#L31) met tijdelijke x, y, width, height van 0 maar die veranderen eronder weer naar de goede grootte. Het maakt dan een [`obj.Snake`](objects.py#L92) object aan met de goedde vorm en de goedde richtingen. Ook maakt het gebruik van de [`mapArrayToRainBow`](config.py#L54) om een lijst van getallen van 0-1 als hue van [HSV kleuren](https://en.wikipedia.org/wiki/HSL_and_HSV) naar [RGB kleuren](https://en.wikipedia.org/wiki/RGB_color_model) te converteren met de ingebouwde [`colorsys`](https://docs.python.org/3.8/library/colorsys.html) bibliotheek, omdat pygame werkt met de RGB colorspace. De variabele `newFacing` is de richting die het hoofd van de slang op moet gaan de volgende tick. Als de speler in de tick dood is gegaan returned de functie de score moeilijkheidsgraad en of berryMode aan staat. Als een toets word ingedrukt word een de nieuwe richting tijdelijk opgeslagen in de `newFacing` variabele en wordt toegewezen aan `snake.facing[0]` elke tick. De variabele `snake.facing[0]` word niet direct gemodificeerd, omdat de game dan niet meer de vorige richting weet waar de slang naartoe wees en dan niet weet of de speler de slang een 180 graden bocht laat maken (wat niet kan). De game veranderdde grootte van de grid dan naar 80% van de minimale waarde van hoogte en breedte van het scherm. Zo past het raster altijd op het scherm en als het scherm veranderd van grootte worden die veranderingen gelijk verbeterd. Dan worden het raster en de slang getekend en de score gerendered en getekend. Ten slotte wordt het scherm ververst met `updateWindow()`. En dan begint het weer opnieuw in de loop.

### pause()
De functie `pause` is voor als de speler op <kbd>p</kbd> van pause heeft gedrukt in de `snake` functie. De pause knop fade van heel klein naar groot en komt op als een pop-up op. Daarna worden de teksten voor heel groot gerenderd omdat als je de lettertypegrootte grootte animeerd het dan niet smooth gaat, want een lettertypegrootte zijn alleen gehele getallen. Voor de animatie word er gebruik gemaakt vab de [`combineSufacesVertical`](config.py#L25) functie uit [`config.py`](config.py) om de teksten `Paused, click to continue` en `Hit SPACE to return home` verticaal aan elkaar te plakken. Achter de knop komt de gepauseerde game met een lagere helderheid om het pepauseerde effect te geven. Daarbij word er gebruik gemaakt vab de functie [`changeBrightness`](config.py#L22) om het een helderheid te geven van 30%. De height van de pause knop gebaseerd op de [formule](https://www.desmos.com/calculator/xwd1igu7zd):

![equation](https://latex.codecogs.com/gif.latex?hoogte%3D50%5Csin%5Cleft%28%5Cfrac%7Bx%7D%7B10%7D%5Cright%29%5Ccdot1.03%5E%7B-x%7D&plus;%5Cleft%28100-1000%5Cfrac%7B1%7D%7B2x%7D%5Cright%29)

waar x is de frames sinds de speler op <kbd>p</kbd> heeft gedrukt. De width is `φ * height` zodat de rechthoek een golden ratio heeft. De tekst is 90% van de de pauseknop. Als de speler op spatie drukt returned de functie met waarde -1. Dat betekend dat de speler naar het beginscherm terug wil. Dan veranderd het de kleur van de pauseknop gebaseerd op of de muis boven de knop hangt. Daarna word de knop op het scherm getekend met [`pauseButton.draw(win)`](snake.py#L282), de framecount word opgehoogt en en [`updateWindow`](snake.py#L40) word opgeroept.

### coolste feature van het spel
Mijn persoonlijke coolste feature van het spel is dat de [debug print](snake.py#L32) dat het spel begonnen is altijd even groot is als het command line window en dat de tekst `BEGIN` altijd in het midden staat.
![example1](reference_images/example1.png)
![example2](reference_images/example2.png)

### tweede coolste feature van het spel
Mijn persoonlijke tweede coolste feature van het spel is dat de speler de window op elk moment in het spel kan resizen en dat de game mooi responsive reageert.
![2example1](reference_images/2example1.png)
![2example2](reference_images/2example2.png)
