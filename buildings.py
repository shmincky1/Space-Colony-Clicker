import game

PER_SECOND=0.1

class PROffice(game.Building):
	name="PR Office"
	desc="PR Offices turn the public opinion twoard space exploration!"
	buy_costs={"usd":100}
	produces={
		"opinion": 1*PER_SECOND
	}

get=lambda game:{
	"proffice":PROffice(game)
}