import game
from browser import html

class BuildingsRenderer(game.Renderer):
	def setup(self, container):
		self.divs={}
		for key, value in self.game.buildings.items():
			self.divs[key]=[]
			for ele in container.get(selector=".building-holder-holder"):
				if value.in_world(ele.parent.parent.id.split("_")[1]):
					div=html.DIV(Class="building-holder building-holder_"+key)
					self.divs[key].append(div)
					ele<=div

	def update(self, container):
		for key, value in self.game.buildings.items():
			for ele in self.divs[key]:
				ele.text=value.name+": "+str(value.built)

class CurrenciesRenderer(game.Renderer):
	def setup(self, container):
		self.divs={}
		
		currency_holders=container.get(selector=".currency-holder-holder")
		for key, value in list(self.game.currencies.items()):
			self.divs[key]=[]
			for container in currency_holders:
				if value.in_world(container.parent.parent.id.split("_")[1]):
					div=html.DIV("asd", Class="currency-holder currency-holder_"+key)
					self.divs[key].append(div)
					container<=div
		print(self.divs)

	def update(self, container):
		for key, value in self.game.currencies.items():
			for container in self.divs[key]:
				container.text=value.format()

class WorldsRenderer(game.Renderer):
	def setup(self, container):
		def _make_handler(worldname):
			def _handler(e):
				print("Handling %s for %s"%(e, worldname))
				for ele in container.get(selector=".world-container"):
					ele.class_name="world-container world-container-hidden"
				container["world-container_"+worldname].class_name="world-container world-container-enabled"
				for ele in container.get(selector=".world-bar-item"):
					ele.class_name="world-bar-item"
				container["world_"+worldname].class_name+=" world-button-enabled"
			return _handler

		for key, value in sorted(self.game.worlds.items(), key=lambda e:e[1].sortorder):
			baritem=html.DIV(id="world_"+key, Class="world-bar-item"+(" world-button-enabled" if value.sortorder==0 else ""))
			
			baritem<=html.IMG(src=value.image, title=value.name)
			baritem<=html.P(value.name, Class="world-text")
			baritem.bind("click", _make_handler(key))
			container["colonies"]<=baritem

class FramingRenderer(game.Renderer):
	def setup(self, container):
		first=True
		for key, value in sorted(self.game.worlds.items(), key=lambda e:e[1].sortorder):
			world_container=html.DIV(Class="world-container"+(" world-container-enabled" if first else " world-container-hidden"), id="world-container_"+key)
			first=False
			resources=html.DIV(id="resources")
			
			resources<=html.B("Resources availible on "+value.name)
			resources<=html.HR()
			resources<=html.DIV(Class="currency-holder-holder")
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