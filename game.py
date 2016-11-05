import json, copy
from browser import html

class DotAccessibleDict(dict):
	def __getattr__(self, a): return self[a]
	def __setattr__(self, a, v): self[a]=v

ALL_WORLDS=object()

class Currency(object):
	def __init__(self, name, worlds=ALL_WORLDS, amount=0, clamp_to_zero=False, round_to=0, postfix=""):
		self.name=name
		self.worlds=worlds
		self.amount=amount
		self.clamp_to_zero=clamp_to_zero
		self.round_to=round_to
		self.postfix=postfix

	def in_world(self, w):
		return self.worlds==ALL_WORLDS or w in self.worlds

	def add(self, amt):
		self.amount+=amt
		return self.amount

	def __iadd__(self, amt):
		self.add(amt)
		return self

	def sub(self, amt):
		self.amount-=amt
		was_more_than_we_had = self.amount>=0
		if was_more_than_we_had and self.clamp_to_zero:
			self.amount=0
		return was_more_than_we_had

	def __isub__(self, amt):
		self.sub(amt)
		return self

	def __gt__(self, v): return self.amount>v
	def __lt__(self, v): return self.amount<v
	def __ge__(self, v): return self.amount>=v
	def __le__(self, v): return self.amount<=v
	def __eq__(self, v): return self.amount==v

	def format_amount(self):
		return str(int(self.amount) if self.round_to==0 else round(self.amount, self.round_to))

	def format(self):
		return self.name+": "+self.format_amount()+self.postfix

class Renderer(object):
	def __init__(self, game):
		self.game=game

	def setup(self, container):
		pass

	def update(self, container):
		pass

class Building(object):
	name=""
	desc=""
	required_upgrades=[]
	worlds=[]
	buy_costs={}
	produces={}
	def __init__(self, game):
		self.game=game
		self.built=0

	def in_world(self, w):
		return self.worlds==ALL_WORLDS or w in self.worlds

	def can_buy(self):
		return all(game.upgrades[name] for name in self.required_upgrades) and all(game.currencies[name]>=cost for name,cost in self.buy_costs.items())

	@property
	def buy_desc(self):
		ret="Required Upgrades: "
		for req in self.required_upgrades:
			ret+=", ".join(self.required_upgrades)
		ret+="\nCosts: "
		for name, amt in self.buy_costs.items():
			ret+=", ".join(name+": "+amt)
		return ret

	def on_buy(self):
		self.built+=1
		for k,v in self.buy_costs.items():
			self.game.currencies[k]-=v

	def tick(self):
		for k,v in self.produces.items():
			self.game.currencies[k]+=v*self.built

	def __nonzero__(self): return self.built>0

class World(object):
	def __init__(self, sortorder, name, image, enabled=False):
		self.name=name
		self.image=image
		self.enabled=enabled
		self.sortorder=sortorder

import currencies, worlds, buildings, upgrades, directives

class Game(object):
	def __init__(self, container):
		self.container=container
		print("...")
		self.currencies=DotAccessibleDict(currencies.get())
		print("...")
		self.buildings=DotAccessibleDict(buildings.get(self))
		print("...")
		self.directives=directives.get(self)
		print("...")
		self.worlds=worlds.get()
		print("...")
		self.setup()
		print("...!")

	def setup(self):
		[i.setup(self.container) for i in self.directives]
		self.update()

	def update(self):
		[i.update(self.container) for i in self.directives]

	def tick(self):
		[b.tick() for b in self.buildings.values()]
		self.update()

	def _save(self):
		return {
			"currency_amounts":{k:v.amount for k,v in self.currencies.items()},
			"buildings":{k:v.built for k,v in self.buildings.items()},
			"worlds":{k:v.enabled for k,v in self.worlds.items()},
			"upgrades":{k:v.bought for k,v in self.upgrades.items()}
		}

	def _load(self, data):
		for k,v in data["currency_amounts"].items():
			self.currencies[k].amount=v
		for k,v in data["buildings"].items():
			self.buildings[k].built=v
		for k,v in data["worlds"].items():
			self.worlds[k].enabled=v
		for k,v in data["upgrades"].items():
			self.upgrades[k].bought=v