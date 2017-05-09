import config
import collections

if __name__ == '__main__':
    all = collections.defaultdict(list)
    for md in config.example_dir.glob("**/*.java"):
        all[md.name].append(md)
    for k in sorted(all.keys()):
        if(len(all[k]) > 1):
            print(k)
            for path in all[k]:
                rel = path.relative_to(config.example_dir)
                print("\t" + str(rel))
