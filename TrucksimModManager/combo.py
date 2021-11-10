#  Copyright 2021 Illia Boiko (selplacei)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#      http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from pathlib import Path
from typing import List
from .combo_info import (
	OrderEntryInfo, SingleEntryInfo, FilenameEntryInfo, OptionalEntryInfo,
	EquivalentEntryInfo, ComboInfo
)


class OrderEntry:
	def __init__(self, display_name, description=None):
		self.display_name = display_name
		self.description = description

	def as_filenames(self) -> List[Path]:
		raise NotImplemented


class SingleEntry(OrderEntry):
	def __init__(self, display_name, filename, link=None, description=None):
		super().__init__(display_name, description)
		self.filename = filename
		self.link = link

	def as_filenames(self) -> List[Path]:
		return [self.filename]


class EquivalentEntry(OrderEntry):
	def __init__(self, display_name, options: List[List[SingleEntry]], description=None):
		super().__init__(display_name, description)
		self.options = options
		self.selected_index = 0

	def as_filenames(self) -> List[Path]:
		return [entry.as_filenames()[0] for entry in self.options[self.selected_index]]


class OptionalEntry(OrderEntry):
	def __init__(self, display_name, feature, enable_mod, disable_mod=None, description=None):
		super().__init__(display_name, description)
		self.enabled = False
		self.feature = feature
		self.enable_mod = enable_mod
		self.disable_mod = disable_mod

	def as_filenames(self) -> List[Path]:
		if self.enabled:
			return self.enable_mod.as_filenames()
		elif self.disable_mod:
			return self.disable_mod.as_filenames()
		return []


class Combo:
	def __init__(self, combo_info):
		self.name = combo_info.name
		self.version = combo_info.version
		self.game = combo_info.game
		self.game_version = combo_info.game_version
		self.author = combo_info.author
		self.description = combo_info.description
		self.source = combo_info.source
		self.version_check = combo_info.version_check
		self.order = []
		self._raw_order = combo_info.order

	def create_entries(self, downloads_path, temp_path):
		...

	def set_feature(self, feature, enabled: bool):
		for entry in self.order:
			if isinstance(entry, OptionalEntry) and entry.feature == feature:
				entry.enabled = enabled

	def requested_features(self):
		return set(entry.feature for entry in self.order if isinstance(entry, OptionalEntry))

	def install(self, *args):  # Need to research installation process first
		...
