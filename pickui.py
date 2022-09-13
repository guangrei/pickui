# -*-coding:utf8;-*-
"""
The MIT License (MIT)

Copyright (c) 2022 pickui https://github.com/guangrei/pickui

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

from androidhelper import Android
import os

droid = Android()
class PickUI(object):
	
	title = "PickUI v1.0"
	
	def __init__(self, base_dir='/storage', private=False):
		self.base_dir = base_dir
		self.private = private
		self.path = False
		
	def set_title(self, title):
		self.title = title
		
	def __getListFiles(self, lis, filter):
		res = []
		for i in filter:
			ret = [f for f in lis if f.endswith(i)]
			res = res + ret
		return res
		
	def _listFiles(self,filter=None):
		ret = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
		if filter is not None:
			ret = self.__getListFiles(ret, filter)
		if self.private:
			if ".nomedia" in ret:
				return []
			ret = [f for f in ret if not f.startswith(".")]
		ret = ["💾 %s"%f for f in sorted(ret)]
		return ret
	
	def _listFolders(self):
		koleksi = os.listdir(self.path)
		ret = [f for f in koleksi if os.path.isdir(os.path.join(self.path, f))]
		if self.private:
			if ".nomedia" in koleksi:
				return []
			ret = [f for f in ret if not f.startswith(".")]
		ret = ["📁 %s"%f for f in sorted(ret)]
		return ret
	
	def _listAll(self, filter=None):
		file = self._listFiles(filter)
		folder = self._listFolders()
		return folder+file
			
	def filePicker(self,filter=None):
		if not self.path:
			self.path = self.base_dir
		nodes = self._listAll(filter)
		title = "ℹ %s"%os.path.basename(self.path).title()
		if self.path != self.base_dir:
			nodes.insert(0, '📂 ..')
		droid.dialogCreateAlert(title if self.path != self.base_dir else self.title)
		droid.dialogSetItems(nodes)
		droid.dialogShow()
		result = droid.dialogGetResponse().result
		droid.dialogDismiss()
		if 'item' not in result:
			self.path = False
			return False
		target = nodes[result['item']]
		target = target.replace("📁 ","")
		target = target.replace("💾 ","")
		target = target.replace("📂 ","")
		target_path = os.path.join(self.path, target)
		if target == '..':
			target_path = os.path.dirname(self.path)
		if os.path.isdir(target_path):
			self.path = target_path
			return self.filePicker(filter)
		else:
			self.path = False
			return target_path
			
	def folderPicker(self):
		if not self.path:
			self.path = self.base_dir
		nodes = self._listFolders()
		title = "ℹ %s"%os.path.basename(self.path).title()
		if self.path != self.base_dir:
			nodes.insert(0, '📂 ..')
		droid.dialogCreateAlert(title if self.path != self.base_dir else self.title)
		droid.dialogSetItems(nodes)
		droid.dialogShow()
		result = droid.dialogGetResponse().result
		droid.dialogDismiss()
		if 'item' not in result:
			self.path = False
			return False
		target = nodes[result['item']]
		target = target.replace("📁 ","")
		target = target.replace("📂 ","")
		target_path = os.path.join(self.path, target)
		if target == '..':
			target_path = os.path.dirname(self.path)
		title = '📌 select this directory or open?'
		message = target_path
		droid.dialogCreateAlert(title, message)
		droid.dialogSetPositiveButtonText('✔')
		droid.dialogSetNegativeButtonText('open')
		droid.dialogShow()
		response = droid.dialogGetResponse().result
		if response['which'] != 'positive':
			self.path = target_path
			return self.folderPicker()
		else:
			self.path = False
			return target_path

if __name__ == '__main__':
	pass