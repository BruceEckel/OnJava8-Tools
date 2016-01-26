import os, sys
from pathlib import Path

# import java.util.*;
# import java.util.stream.*;
# import java.util.function.*;



standard = """\
// %s/%s.java
import java.nio.file.*;

public class %s {
  public static void main(String[] args) {

  }
}
/* Output:

*/
"""

gofile = """\
javac %s.java
java %s
java %s | clip
"""

def create_java_file():
    # print("classname: %s" % sys.argv[1])
    # print(Path.cwd().stem)
    java_file = standard % (Path.cwd().stem, sys.argv[1], sys.argv[1])
    file_name = sys.argv[1] + ".java"
    if Path(file_name).exists():
        print(file_name + " already exists!")
        sys.exit()
    Path(file_name).write_text(java_file)
    Path("go.bat").write_text(gofile % (sys.argv[1], sys.argv[1], sys.argv[1]))
    os.system("subl " + file_name)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: makejava PublicClassName")
        sys.exit()
    create_java_file()