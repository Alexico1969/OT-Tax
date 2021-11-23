def extract_username(data):
    output = ""
    record = False
    for c in data:
        if record == True and c !="&":
            output += c
        if c == "=":
            record = True
        if c == "&":
            break

    return output

def extract_password(data):
    temp = ""
    output = ""
    record = False
    for c in data:
        if c == "&":
            record = True
        if record == True:
            temp += c
    record = False
    for c in temp:
        if record == True:
            output += c
        if c == "=":
            record = True

    return output