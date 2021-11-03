import shortuuid


z = "https://pythonru.com/uroki/11-rabota-s-formami-vo-flask"

y = shortuuid.uuid(z)[:8]

print(y)



