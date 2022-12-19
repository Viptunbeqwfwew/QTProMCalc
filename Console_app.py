import sys


class HelpArg:
    def __init__(self, args):
        args = list(args)
        self.call = args.pop(0)
        self.kwargs = {}
        self.args = []
        cou = False
        last = ""
        c = 0
        for i in args:
            i = str(i)
            if cou:
                self.kwargs[last[2:]] = i
                last, cou = "", False
                c += 1
                continue
            if i.startswith("--"):
                if len(args) == c + 1 or args[c + 1].startswith("--"):
                    self.kwargs[i[2:]] = ""
                    c += 1
                    continue
                cou = True
                last = i
                c += 1
                continue
            self.args.append(i)
            c += 1


def connects(*args, **kwargs):
    Connects = {}
    if "ports" in kwargs:
        ports = kwargs.get("ports").split(",")
    else:
        ports = "6066,".split(",")
    if "ips" in kwargs:
        ips = kwargs.get("ips").split(",")
    else:
        ips = "localhost,".split(",")
    for i in zip(ips, ports):
        Connects[i[0]] = int(i[1])
        print(f"connected {i[0]}:{i[1]}")
    return Connects


def main():
    arg = sys.argv[1:]
    helper = HelpArg(arg)
    globals()[helper.call](*helper.args, **helper.kwargs)


if __name__ == "__main__":
    while True:
        break
    main()
