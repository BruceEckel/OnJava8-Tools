import sublime, sublime_plugin
import os.path
import textwrap
import User.config


def package_name(lines):
  for line in lines:
    if line.startswith("package "):
      pname = line.split(';')[0]
      return pname.split(' ')[1].strip() + "."
  return ""

class edit_code_listing(sublime_plugin.TextCommand):
  def run(self, edit):
    sel = self.view.sel()[0]
    javacode = self.view.find("(?s)```java\n(.*?)```", sel.a - 10)
    code_body = sublime.Region(javacode.a + 8, javacode.b -4)
    self.view.sel().clear()
    self.view.sel().add(code_body)
    self.view.show(sublime.Region(javacode.a, javacode.a))

    lines = self.view.substr(code_body).splitlines()
    if not lines[0].startswith("// "):
      sublime.error_message("Listing doesn't start with //")
      return
    slug = lines[0][3:]
    pathparts = slug.split("/")
    java_path = os.path.join(User.config.basepath, *pathparts)
    if not os.path.isfile(java_path):
      sublime.error_message("File doesn't exist:\n" + slug)
      return
    self.view.window().open_file(java_path)