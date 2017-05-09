import re, sys
import textwrap

class JavaMain:
    max_output_length = 32  # lines beyond which we flag this
    maxlinewidth = 59
    maindef = re.compile("public\s+static\s+void\s+main")
    leader = "_" * 8
    ellipses = [leader + leader.join(["..."] * 4) + leader]
    # ellipses = ["[...]".center(14, '_') * 4]

    class JFile:
        @staticmethod
        def with_main(javaFilePath):
            code = javaFilePath.read_text()
            if JavaMain.maindef.search(code) or "{Exec:" in code:
                # print(javaFilePath)
                return JavaMain.JFile(javaFilePath, code)
            return None

        def __init__(self, javaFilePath, code):
            self.javaFilePath = javaFilePath
            self.code = code
            self.lines = self.code.splitlines()
            self.output_line = None
            for line in self.lines:
                if "/* Output:" in line:
                    self.output_line = line
            self.newcode = ""

    @staticmethod
    def create(javaFilePath):
        j_file = JavaMain.JFile.with_main(javaFilePath)
        if j_file is None:
            return None
        if "{ValidateByHand}" in j_file.code:
            return None
        if "/* Output: (None) */" in j_file.code:
            return None
        if "/* Output: (Execute to see)" in j_file.code:
            return None
        outfile = javaFilePath.with_name(javaFilePath.stem + "-output.txt")
        errfile = javaFilePath.with_name(javaFilePath.stem + "-erroroutput.txt")
        if outfile.exists() or errfile.exists():
            return JavaMain(javaFilePath, j_file, outfile, errfile)
        return None

    def __init__(self, javaFilePath, j_file, outfile, errfile):
        self.javaFilePath = javaFilePath
        self.j_file = j_file
        self.outfile = outfile
        self.errfile = errfile
        self.first_and_last = None
        self.first_lines = None
        self.long_output = False

        self.output_line = self.j_file.output_line
        if self.output_line:
            if "(First and last" in self.output_line:
                self.first_and_last = \
                    int(self.output_line.partition("(First and last")[2].split()[0])
            elif "(First" in self.output_line:
                self.first_lines = \
                    int(self.output_line.partition("(First")[2].split()[0])

        result = ""
        if outfile.exists():
            with outfile.open() as f:
                out = f.read().strip()
                if out:
                    if self.first_and_last:
                        lines = out.splitlines()
                        out = "\n".join(lines[:self.first_and_last] +
                                        JavaMain.ellipses +
                                        lines[-self.first_and_last:])
                    elif self.first_lines:
                        lines = out.splitlines()
                        out = "\n".join(lines[:self.first_lines] +
                                        [" " * 18 + "..."])
                    result += out + "\n"
        if errfile.exists():  # Always include all of errfile
            with errfile.open() as f:
                err = f.read().strip()
                if err:
                    result += "___[ Error Output ]___\n"
                    result += err
        self.result = JavaMain.wrapOutput(result) + "\n"

        if len(self.result.splitlines()) > JavaMain.max_output_length:
            self.long_output = True

        for line in self.j_file.lines:
            if line.strip() == self.output_line.strip():
                self.j_file.newcode += self.output_line + "\n"
                self.j_file.newcode += self.result + "*/\n"
                break
            # if line.startswith("/* Output:"):
            #     line = line.partition("*/")[0]
            #     self.j_file.newcode += line + "\n"
            #     self.j_file.newcode += self.result + "*/\n"
            #     break
            else:
                self.j_file.newcode += line + "\n"

    def new_code(self):
        return self.j_file.newcode

    @staticmethod
    def wrapOutput(output):
        """
        Wrap to line limit and perform other fixups for display and comparison
        """
        output = output.replace('\0', "NUL")
        lines = output.splitlines()
        result = []
        for line in lines:
            result += textwrap.wrap(line.rstrip(), width=JavaMain.maxlinewidth)
        return "\n".join(result)

    def write_modified_file(self):
        with self.j_file.javaFilePath.open('w') as modified:
            modified.write(self.j_file.newcode)
