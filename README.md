# Python tools for building the *On Java* book

> This is hacky, often embarrassing, but working code. I make no apologies and
> promise no explanations.

- This is what I'm currently using, and updating. I'm not looking for pull
  requests. Unless you need me to add something like shell scripts to match the
  Windows batch scripts, to make it more convenient. But nothing that changes
  the current behavior of `OnJava-Tools`.

- Thanks for your help, those who requested this!

## How to set up to successfully generate the example files and Gradle build for *On Java*

1. Install Python 3.5

2. Add this directory (`OnJava-Tools`) to your execution path.

3. You'll need to install [my tools](https://github.com/BruceEckel/betools/),
   and probably a number of other things that I'll post here when someone gives
   me a list (this whole thing is an experiment so I'm only doing what's
   absolutely necessary right now).

4. To extract the Example files from the book source (you must have permission
   and a clone of the book source -- if you don't, this isn't for you), run: `e
   all`. After that you should be able to successfully run `gradlew run` on the
   result.

## To Automatically Insert Generated Output Back Into Source Files

1. After extraction (`e all`), run `gradlew run`. This generates the `*.out`
   files which live in the same directories as the source files.

2. Run `_update_extracted_example_output format-and-include-new-output`. This
   generates the `*.p1` (phase one) files *and* reformats the output to the
   proper width. The `p1` files are also in the same directories as the source
   files. The `p1` files are inserted into the Java files as `/* Output:` and
   then the Java files are placed into the book.

3. At this point if you run `_verify_output -a`, everything should show up as
   `exact_match`.
