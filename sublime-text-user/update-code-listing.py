import sublime
import sublime_plugin
import os.path
import textwrap
import User.config


def package_name(lines):
    for line in lines:
        if line.startswith("package "):
            pname = line.split(';')[0]
            return pname.split(' ')[1].strip() + "."
    return ""


def fill_to_width(text):
    result = ""
    for line in text.splitlines():
        result += textwrap.fill(line, width=User.config.maxlinewidth) + "\n"
    return result.strip()


def substitute_output_into_this_code_listing(self, edit):
    output = self.view.find("(?s)/\* Output:.*?\*/", 0)
    clines = self.view.substr(output).splitlines()
    len_0 = len(clines[0]) + 1
    output_code = sublime.Region(output.a + len_0, output.b - 3)
    self.view.sel().clear()
    self.view.sel().add(output_code)
    self.view.show(sublime.Region(output_code.a, output_code.a))

    lines = self.view.substr(sublime.Region(0, self.view.size())).splitlines()
    slug = lines[0][3:]
    pathparts = slug.split("/")

    outfilename = package_name(lines) + pathparts[-1].replace(".java", ".out")
    outfile = os.path.join(User.config.basepath, pathparts[0], outfilename)
    print(outfile)
    if not os.path.isfile(outfile):
        sublime.message_dialog("File doesn't exist:\n" + slug)
        return
    output_text = open(outfile).read().strip()
    self.view.replace(edit, output_code, fill_to_width(output_text))
    print("successfully inserted output")
    self.view.run_command("save")
    # A terrible hack to refresh the buffer and clear the dirty flag:
    sublime.set_timeout(lambda: self.view.run_command("revert"), 10)
    # sublime.set_timeout(lambda: self.view.window().focus_view(self.view), 10)


class update_code_listing(sublime_plugin.TextCommand):

    def run(self, edit):
        if self.view.file_name().endswith(".java"):
            return substitute_output_into_this_code_listing(self, edit)
        sel = self.view.sel()[0]
        javacode = self.view.find("(?s)```java\n(.*?)```", sel.a - 10)
        code_body = sublime.Region(javacode.a + 8, javacode.b - 4)
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
        java_source = open(java_path).read().strip()
        self.view.replace(edit, code_body, java_source)
        print("successfully updated:", slug)

        sel = self.view.sel()[0]
        output = self.view.find("(?s)/\* Output:.*?\*/", sel.a)
        clines = self.view.substr(output).splitlines()
        len_0 = len(clines[0]) + 1
        output_code = sublime.Region(output.a + len_0, output.b - 3)
        self.view.sel().clear()
        self.view.sel().add(output_code)
        self.view.show(sublime.Region(output_code.a, output_code.a))

        outfilename = package_name(
            lines) + pathparts[-1].replace(".java", ".out")
        outfile = os.path.join(User.config.basepath, pathparts[0], outfilename)
        print(outfile)
        if not os.path.isfile(outfile):
            sublime.message_dialog("File doesn't exist:\n" + slug)
            return
        output_text = open(outfile).read().strip()
        self.view.replace(edit, output_code, fill_to_width(output_text))
        print("successfully inserted output")
