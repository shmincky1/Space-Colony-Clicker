import game
from browser import html

class BuildingsRenderer(game.Renderer):
	pass
	# def setup(self, container):
	# 	for key, value in self.game.buildings.items():
	# 		container["building-holder-holder"]<=html.DIV(id="building-holder_"+key, Class="building-holder")

	# def update(self, container):
	# 	for key, value in self.game.buildings.items():
	# 		container["building-holder_"+key].text=value.name+": "+str(value.built)

class CurrenciesRenderer(game.Renderer):
	def setup(self, container):
		for key, value in self.game.currencies.items():
			for container in container.get(selector=".currency-holder-holder"):
				container<=html.DIV(id="currency-holder_"+key, Class="currency-holder")

	def update(self, container):
		for key, value in self.game.currencies.items():
			for container in container.get(selector="#currency-holder_"+key):
				container.text=value.format_amount()

class WorldsRenderer(game.Renderer):
	def setup(self, container):
		def _make_handler(worldname):
			def _handler(e):
				print("Handling %s for %s"%(e, worldname))
				for ele in container.get(selector=".world-container"):
					ele.class_name="world-container world-container-hidden"
				container["world-container_"+worldname].class_name="world-container world-container-enabled"
				for ele in container.get(selector=".world-button"):
					ele.class_name="world-button"
				container["world_"+worldname].class_name+=" world-button-enabled"
			return _handler

		for key, value in sorted(self.game.worlds.items(), key=lambda e:e[1].sortorder):
			image=html.IMG(src=value.image, title=value.name, id="world_"+key, Class="world-button"+(" world-button-enabled" if value.sortorder==0 else ""))
			image.bind("click", _make_handler(key))
			container["colonies"]<=image

class FramingRenderer(game.Renderer):
	def setup(self, container):
		first=True
		for key, value in sorted(self.game.worlds.items(), key=lambda e:e[1].sortorder):
			world_container=html.DIV(Class="world-container"+(" world-container-enabled" if first else " world-container-hidden"), id="world-container_"+key)
			first=False
			resources=html.DIV(id="rescourses")
			resources<=html.DIV(Class="currency-holder-holder")
			resources<=key
			world_container<=resources
			buildings=html.DIV(id="buildings")
			buildings<=html.DIV(Class="building-holder-holder")
			world_container<=buildings
			world_container<=html.DIV(id="upgrades")
			vis=html.DIV(id="visualize")
			vis<=html.H1(key)
			vis<=html.IMG(src=value.image)
			world_container<=vis
			container["world-container-container"]<=world_container


get=lambda game:[
	FramingRenderer(game),
	CurrenciesRenderer(game),
	BuildingsRenderer(game),
	WorldsRenderer(game)
]