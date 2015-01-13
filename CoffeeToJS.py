import subprocess
import sublime, sublime_plugin

from itertools import chain
from functools import wraps

PLUGIN_SETTINGS_FILE = 'coffeetojs.sublime_settings'
PROJECT_SETTINGS = 'coffeetojs'

def get_settings():
	settings = {
		'coffeeCommand': 'coffee',
		'inlineArgs': ['--no-header', '--bare'],
		'fileArgs': ['--no-header'],
		'debug': False,
	}
	ud_settings = sublime.load_settings(PLUGIN_SETTINGS_FILE) or {}
	project_settings = sublime.active_window().active_view().settings().get(PROJECT_SETTINGS) or {}

	return {
		'coffeeCommand': ud_settings.get(
			'coffeeCommand',
			project_settings.get(
				'coffeeCommand',
				settings.get('coffeeCommand')
			)
		),
		
		'inlineArgs': ud_settings.get(
			'inlineArgs',
			project_settings.get(
				'inlineArgs',
				settings.get('inlineArgs')
			)
		),
		
		'fileArgs': ud_settings.get(
			'fileArgs',
			project_settings.get(
				'fileArgs',
				settings.get('fileArgs')
			)
		),
		
		'debug': ud_settings.get(
			'debug',
			project_settings.get(
				'debug',
				settings.get('debug')
			)
		),
	}

def debug(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		response = func(*args, **kwargs)
		print('DEBUG COMMAND ::', response)
		return response
	return wrapper

class Command:
	@staticmethod
	@debug
	def selectCommand(code):
		settings = get_settings()
		#chain flattens the list
		command = chain.from_iterable(
			[[settings['coffeeCommand']], settings['inlineArgs'], ['-ec', code]]
		)
		return list(command)

	@staticmethod
	@debug
	def fileCommand(file):
		settings = get_settings()
		command = chain.from_iterable(
			[[settings['coffeeCommand']], settings['fileArgs'], ['-c', file]]
		)
		return list(command)

	@staticmethod
	@debug
	def clipboardCommand(code):
		return Command.selectCommand(code)


class CoffeeToJsSelectedCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		selects = self.view.sel()
		for select in selects:
			code = self.view.substr(select)
			if not code:
				continue
			process = subprocess.Popen(Command.selectCommand(code), stdout=subprocess.PIPE)
			out, err = process.communicate()
			self.view.insert(edit, select.begin(), out.decode())


	def is_enabled(self):
		return True

class CoffeeToJsFromFileCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		source = self.view.file_name()
		subprocess.call(Command.fileCommand(source))


	def is_enabled(self):
		return True

class CoffeeToJsFromClipboardCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		code = sublime.get_clipboard()
		process = subprocess.Popen(
			Command.clipboardCommand(code),
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		out, err = process.communicate()
		if err:
			self.write_to_console(err)
		self.view.replace(edit, self.view.sel()[0], out.decode())


	def is_enabled(self):
		return True