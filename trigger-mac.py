f = open("/tmp/trigger", "r")
contents = f.read()
if "incoming" in contents:
    new_contents = """
    outgoing
    """

else:
    new_contents = """
    incoming
    """
    
f.close()
f = open("/tmp/trigger", "w")
f.write(new_contents)
f.close()
