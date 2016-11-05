import game

get=lambda:{
	"usd":game.Currency("Money", amount=1000000, postfix="$"),
	"opinion":game.Currency("Public Opinion", ["earth"]),
	"science":game.Currency("Science")
}