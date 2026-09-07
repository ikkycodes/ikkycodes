import pathlib
p = pathlib.Path("README.md")
s = p.read_text(encoding="utf-8")
before = len(s)
s = "".join(ch for ch in s if not (0x200B <= ord(ch) <= 0x206F) and ch not in ("\ufeff",))
p.write_text(s, encoding="utf-8")
print("removed:", before - len(s))