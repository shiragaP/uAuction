
class Thumbnail:
    xPos = list()
    yPos = list()
    width = 160
    height = 240

    for i in range(2):
        xPos += list(j for j in range(210, 931, 180))

    for i in range(5):
        yPos += (60,)

    for i in range(5):
        yPos += (320,)

print(Thumbnail.xPos)
