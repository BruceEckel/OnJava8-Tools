Python tools for building the *On Java* book
============================================

> This is hacky, often embarrassing, but working code. I make no apologies and
> promise no explanations.

- Published here for those interested in creating an alternate build system
that generates Gradle files instead of Ant Files.

- This is what I'm currently using, and updating. I'm not looking for pull
requests. Unless you need me to add something like shell scripts to match
the Windows batch scripts, to make it more convenient. But nothing that
changes the current behavior of `OnJava-Tools`.

- If you're interested in working on the gradle-build project, that will be in
a separate repo (linked here when it exists).

- I will continue to use this repository (generating Ant files) until such time
as a gradle-build system is working, at which time I'll experiment with that
and decide whether I can switch to it.

- Thanks for your help, those of you that requested this!

How to set up to successfully generate the "Ant" build files for *On Java*
--------------------------------------------------------------------------

1. Install Python 3.5

2. Create a directory `on-java` on the same level as this one (`OnJava-Tools`).

3. Under `on-java`, create a directory `ExtractedExamples`.

4. Unpack
[The Book Code](https://github.com/BruceEckel/OnJava-Examples/archive/master.zip)
into `ExtractedExamples`.

5. Add this directory (`OnJava-Tools`) to your execution path.

6. You'll need to install [my tools](https://github.com/BruceEckel/betools/),
and probably a number of other things that I'll post here when someone
gives me a list (this whole thing is an experiment so I'm only doing
what's absolutely necessary right now).

7. To build the Ant files, run: `e -a`. That might be the only command that
runs for you, but that's the one that you want to replace in the gradle-build
project. (Or perhaps, just add a new command to what's already there. Or
make a whole new Python file, probably).

**Note:** You're only really interested in the `Examples.py` file, for this
project, and only part of that.
