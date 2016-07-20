import config
import collections
base = "/* Output:"

if __name__ == '__main__':
    all = collections.defaultdict(list)
    for md in config.example_dir.glob("**/*.java"):
        text = md.read_text()
        for line in text.splitlines():
            if(line.startswith(base)):
                all[line.strip()].append((md, text))

    for k in sorted(all.keys()):
        if(k != base):
            print(k)
            for tup in all[k]:
                rel = tup[0].relative_to(config.example_dir)
                print("\t" + str(rel))

    vbh = [tup for tup in all[k] for k in all.keys() if "{ValidateByHand}" in tup[1]]
    if vbh:
        print("=" * 50)
        print("{ValidateByHand} + /* Output:")
        for tup in vbh:
            rel = tup[0].relative_to(config.example_dir)
            print(str(rel))
