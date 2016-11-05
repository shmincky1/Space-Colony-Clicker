import game

get=lambda:{
	"earth": game.World(0, "Earth", "img/earth-icon.png", enabled=True),
	"spacestation": game.World(1, "Station", "img/space-station-icon.png", enabled=True),
	"moon": game.World(2, "Moon", "img/moon-icon.png", enabled=True),
	"mars": game.World(3, "Mars", "img/mars-icon.png", enabled=True)
}