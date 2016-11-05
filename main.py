from browser import document, timer
import browser
import game
print=browser.console.log

thegame=game.Game(document)
thegame.buildings.proffice.built+=1

timer.set_interval(thegame.tick, 100)