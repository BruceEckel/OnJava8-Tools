import sublime
import sublime_plugin
import os.path
import textwrap
import glob
import codecs
import User.config


class insert_current_code_listing(sublime_plugin.TextCommand):

    def run(self, edit):
        whole_file = sublime.Region(0, self.view.size())
        lines = self.view.substr(whole_file).splitlines()
        if not lines[0].startswith("// "):
            sublime.error_message("Listing doesn't start with //")
            return
        slug = lines[0]
        containing_file = None
        for f in glob.glob(User.config.markdownpath):
            text = codecs.open(f, encoding="utf-8").read()
            if slug in text:
                containing_file = f
                print("found {}\nin\n{}".format(slug, f))
                break
        if not containing_file:
            sublime.error_message(
                "Containing markdown file for {} not found".format(slug))
            return
        cfview = self.view.window().open_file(containing_file)
        sublime.set_timeout(lambda: find_listing_start(cfview, slug), 10)


def find_listing_start(cfview, slug):
    if not cfview.is_loading():
        listing_start = cfview.find(slug, 0)
        pre_listing_start = sublime.Region(listing_start.a - 8, listing_start.a - 8)
        cfview.sel().clear()
        cfview.sel().add(pre_listing_start)
        cfview.show(pre_listing_start)
    else:
        sublime.set_timeout(lambda: find_listing_start(cfview, slug), 10)