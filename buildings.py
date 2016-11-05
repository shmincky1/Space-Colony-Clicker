import game

PER_SECOND=0.1

class PROffice(game.Building):
	name="PR Office"
	desc="PR Offices turn the public opinion twoard space exploration!"
	buy_costs={"usd":100}
	produces={
		"opinion": 1*PER_SECOND
	}
	worlds=["earth"]

class RnDOffice(game.Building):
	name="R&D Office"
	buy_costs={"usd":500}
	produces={
		"science": 1*PER_SECOND
	}
	worlds=["earth"]

class EarthLaunchPad(game.Building):
	name="Launch Pad"
	buy_costs={"usd":10000}
	worlds=["earth"]

class StationModule(game.Building):
	name="Space Station Module"
	buy_costs={"lifter":1, "usd":10000}
	produces={"science":0.1*PER_SECOND}
	worlds=["spacestation"]

class MoonBase(game.Building):
	name="Moonbase"

class AldrinCycler(game.Building):
	name="Aldrin Cycler Ship"
	worlds=["earth", "mars"]

get=lambda game:{
	"proffice":PROffice(game),
	"rndoffice":RnDOffice(game),
	"earthlaunchpad":EarthLaunchPad(game),
	"stationmodule":StationModule(game),
	"aldrincycler":AldrinCycler(game)
}