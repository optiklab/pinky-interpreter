import dis

def times50(n):
  return n * 50

print(times50.__code__.co_code)
print(dis.dis(times50))
