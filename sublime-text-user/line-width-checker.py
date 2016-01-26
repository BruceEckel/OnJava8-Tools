import sublime, sublime_plugin, os

class line_width_checker(sublime_plugin.TextCommand):
  def run(self, edit):
    self.view.run_command("save")
    os.system("start l.bat")
