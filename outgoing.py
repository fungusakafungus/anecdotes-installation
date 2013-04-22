#!/usr/bin/env python
new_contents = """
outgoing
"""
f = open("/tmp/trigger", "w")
f.write(new_contents)
f.close()
