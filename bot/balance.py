
def convert_str_to_money(s):
    fractional = str(int(s) % 100)
    integer = str(int(s) // 100)
    res = integer + "," + (fractional if len(fractional) == 2 else "0" + fractional)
    return res