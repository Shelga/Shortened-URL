import shortuuid



z = "https://stackoverflow.com/questions/42703059/how-to-create-a-8-digit-unique-id-in-python"

y = shortuuid.uuid()[:8]
# x = y[:8]

print(y)



