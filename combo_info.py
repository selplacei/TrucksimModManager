from typing import List, Union


class OrderEntryInfo:
	def __init__(self, name, display_name=None, description=None):
		self.name = name
		self.display_name = display_name or name.replace('_', ' ')
		self.description = description


class SingleEntryInfo(OrderEntryInfo):
	def __init__(self, name, display_name=None, description=None):
		super().__init__(name, display_name, description)


class FilenameEntryInfo(OrderEntryInfo):
	def __init__(self, mod_name, filename, display_name=None, description=None):
		super().__init__(mod_name, display_name, description)
		self.filename = filename


class OptionalEntryInfo(OrderEntryInfo):
	def __init__(
		self, feature, enable_mod: OrderEntryInfo,
		disable_mod: OrderEntryInfo = None, display_name=None, description=None
	):
		super().__init__(enable_mod.name, display_name or f'[Optional] {enable_mod.display_name}', description)
		self.feature = feature
		self.enable_mod = enable_mod
		self.disable_mod = disable_mod


class EquivalentEntryInfo(OrderEntryInfo):
	def __init__(
		self, name, options: List[Union[OrderEntryInfo, List[OrderEntryInfo]]],
		display_name=None, description=None
	):
		super().__init__(name, display_name, description)
		self.options = options


class ComboInfo:
	def __init__(
		self, order: List[OrderEntryInfo], name, version, game, game_version,
		author=None, description=None, source=None, version_check=None
	):
		self.order = order
		self.name = name
		self.version = version
		self.game = game
		self.game_version = game_version
		self.author = author
		self.description = description
		self.source = source
		self.version_check = version_check
