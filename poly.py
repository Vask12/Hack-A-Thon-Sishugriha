import re

__all__ = ["P"]


class P:
    def __init__(self, val):
        if type(val) == type([]):
            self.plist = val
        elif type(val) == type(""):
            self.plist = parse_string(val)
        else:
            raise "Unknown argument to Polynomial: %s" % val
        return

    def __add__(self, other):
        return P(add(self.plist, plist(other)))

    def __radd__(self, other):
        return P(add(self.plist, plist(other)))

    def __sub__(self, other):
        return P(sub(self.plist, plist(other)))

    def __rsub__(self, other):
        return -P(sub(self.plist, plist(other)))

    def __mul__(self, other):
        return P(multiply(self.plist, plist(other)))

    def __rmul__(self, other):
        return P(multiply(self.plist, plist(other)))

    def __neg__(self):
        return -1 * self

    def __pow__(self, e):
        return P(power(self.plist, e))

    def __str__(self):
        p = strip_leading_zeros(self.plist)
        if p == [0]:
            return "0"
        str = []
        for i in range(len(p) - 1, -1, -1):
            if p[i]:
                if i < len(p) - 1:
                    if p[i] >= 0:
                        str.append("+")
                    else:
                        str.append("-")
                    str.append(tostring_term(abs(p[i]), i))
                else:
                    str.append(tostring_term(p[i], i))
        return " ".join(str)

    def __call__(self, x1, x2=None):
        return peval(self.plist, x1, x2)


def strip_leading_zeros(p):
    "Remove the leading (in terms of high orders of x) zeros in the polynomial"
    # compute the highest nonzero element of the list
    for i in range(len(p) - 1, -1, -1):
        if p[i]:
            break
    return p[: i + 1]


superscripts = {
    "1": "",
    "2": "\u00B2",
    "3": "\u00B3",
    "4": "\u2074",
    "5": "\u2075",
    "6": "\u2076",
    "7": "\u2077",
    "8": "\u2078",
    "9": "\u2079",
}


def superscript(x: int):
    return "".join(superscripts[j] for j in str(x))


def tostring_term(c, i):
    "Convert a single coefficient c and power e to a string cx^i"
    if i == 1:
        if c == 1:
            return "x"
        elif c == -1:
            return "-x"
        return "%sx" % c
    elif i:
        if c == 1:
            return "x" + superscript(i)
        elif c == -1:
            return "-x^" + superscript(i)
        return f"{c}x{superscript(i)}"
    return "%s" % c


def tostring(p):
    """\
    Convert a plist into a string. This looks overly complex at first,
    but most of the complexity is caused by special cases.
    """
    p = strip_leading_zeros(p)
    if p == [0]:
        return "0"
    str = []
    for i in range(len(p) - 1, -1, -1):
        if p[i]:
            if i < len(p) - 1:
                if p[i] >= 0:
                    str.append("+")
                else:
                    str.append("-")
                str.append(tostring_term(abs(p[i]), i))
            else:
                str.append(tostring_term(p[i], i))
    return " ".join(str)


def add(p1, p2):
    "Return a new plist corresponding to the sum of the two input plists."
    if len(p1) > len(p2):
        new = [i for i in p1]
        for i in range(len(p2)):
            new[i] += p2[i]
    else:
        new = [i for i in p2]
        for i in range(len(p1)):
            new[i] += p1[i]
    return new


def sub(p1, p2):
    return add(p1, mult_const(p2, -1))


def mult_const(p, c):
    "Return a new plist corresponding to the input plist multplied by a const"
    return [c * pi for pi in p]


def multiply(p1, p2):
    "Return a new plist corresponding to the product of the two input plists"
    if len(p1) > len(p2):
        short, long = p2, p1
    else:
        short, long = p1, p2
    new = []
    for i in range(len(short)):
        new = add(new, mult_one(long, short[i], i))
    return new


def mult_one(p, c, i):
    """\
    Return a new plist corresponding to the product of the input plist p
    with the single term c*x^i
    """
    new = [0] * i  # increment the list with i zeros
    for pi in p:
        new.append(pi * c)
    return new


def power(p, e):
    "Return a new plist corresponding to the e-th power of the input plist p"
    assert int(e) == e, "Can only take integral power of a plist"
    new = [1]
    for i in range(e):
        new = multiply(new, p)
    return new


def plist(term):
    "Force term to have the form of a polynomial list"
    # First see if this is already a Polynomial object
    try:
        pl = term.plist
        return pl
    except:
        pass

    if isinstance(term, int) or isinstance(term, float):
        return [term]
    elif type(term) == type(""):
        return parse_string(term)
    # We ultimately want to be able to parse a string here
    else:
        raise ValueError("Unsupported term can't be corced into a plist: %s" % term)


def peval(plist, x, x2=None):
    """\
    Eval the plist at value x. If two values are given, the
    difference between the second and the first is returned. This
    latter feature is included for the purpose of evaluating
    definite integrals.
    """
    val = 0
    if x2:
        for i in range(len(plist)):
            val += plist[i] * (pow(x2, i) - pow(x, i))
    else:
        for i in range(len(plist)):
            val += plist[i] * pow(x, i)
    return val


def parse_string(str=None):
    """\
    Do very, very primitive parsing of a string into a plist.
    'x' is the only term considered for the polynomial, and this
    routine can only handle terms of the form:
    7x^2 + 6x - 5
    and will choke on seemingly simple forms such as
    x^2*7 - 1
    or
    x**2 - 1
    """
    termpat = re.compile("([-+]?\s*\d*\.?\d*)(x?\^?\d?)")
    res_dict = {}
    for n, p in termpat.findall(str):
        n, p = n.strip(), p.strip()
        if not n and not p:
            continue
        n, p = parse_n(n), parse_p(p)
        if p in res_dict.keys():
            res_dict[p] += n
        else:
            res_dict[p] = n
    highest_order = max(res_dict.keys())
    res = [0] * (highest_order + 1)
    for key, value in res_dict.items():
        res[key] = value
    return res


def parse_n(str):
    "Parse the number part of a polynomial string term"
    if not str:
        return 1
    elif str == "-":
        return -1
    elif str == "+":
        return 1
    return eval(str)


def parse_p(str):
    "Parse the power part of a polynomial string term"
    pat = re.compile("x\^?(\d)?")
    if not str:
        return 0
    res = pat.findall(str)[0]
    if not res:
        return 1
    return int(res)


def main():
    a = P("x^2 + 2x - 15")
    b = P("x-2")
    print(a)
    print(b)
    print(a * b)


if __name__ == "__main__":
    main()
