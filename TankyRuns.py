import numpy as np
import colorsys
from PIL import Image, ImageDraw, ImageFont

# Using Cheat Engine I stopped multiple runs on the same Kill count
# Armor is increasing linearly, so I didn't bother recording it

ElectricDagger = {
  "x": [
    0,      10385,  20449,  42502,  53708,  70969,  89784,
    139674, 154459, 164547, 175623, 190101, 204918, 220687,
    230970, 243029, 259254, 270567, 285297, 295909, 311036,
    327526, 341531, 349748,
  ], "group": [
    {
      "name": "E1",
      "y": [
        19,      734886,  1337440, 2471358, 2912385, 3437785, 3822049,
        3723418, 3354929, 2993557, 2529435, 1915774, 928412,  0,
      ],
    }, {
      "name": "E2",
      "y": [
        19,      636946,  1167708, 2283821, 2779327, 3458574, 4075186,
        5098251, 5279535, 5378395, 5400547, 5363539, 5215591, 5076452,
        4847467, 4606030, 4141005, 3747025, 3275162, 2875227, 2122653,
        1257472, 606498,  0,
      ],
    }, {
      "name": "E3",
      "y": [
        19,      210815,  412606,  786512,  943492,  1185985, 1387291,
        1773496, 1817497, 1824519, 1827295, 1793691, 1760631, 1695471,
        1662253, 1623968, 1391359, 1204014, 979955,  925142,  728578,
        289289,  0,
      ],
    }, {
      "name": "E4",
      "y": [
        19,      113957,  217272,  403758,  510669,  644001,  725550,
        783828,  737076,  694741,  636787,  513428,  333433,  140042,
        0,
      ],
    },
  ],
}
BattleKnife = {
  "x": [
    0,      22461,  45531,  67398,  87569,  107683,
    128406, 149423, 179176, 200895, 221791, 241865,
    262177, 283344, 303943, 332629, 356484, 379115,
    406138, 428983, 454559,
  ],
  "group": [
    {
      "name": "B1",
      "y": [
        19,       3996409,  7743781,  10939418, 13580196, 15819966,
        17823799, 19432716, 21167993, 22015582, 22201607, 22578272,
        22704594, 22373662, 21564919, 20037313, 18110858, 15881624,
        12574936, 9457177,  5855394,
      ],
    }, {
      "name": "B2",
      "y": [
        19,       3404910,  6744712,  9712325,  12270146, 14709053,
        17028008, 19319205, 22109807, 23859410, 25294860, 26727099,
        27672447, 28820775, 29533650, 30736103, 31197820, 31498253,
        31713481, 31840773, 31427867,
      ],
    }, {
      "name": "B3",
      "y": [
        19,       1153217,  2291617,  3278712,  4165483,  5007037,
        5812104,  6585383,  7548720,  8146648,  8658494,  9109038,
        9461376,  9675828,  10118052, 10539159, 10580075, 10606491,
        10416807, 10591608, 10307343,
      ],
    }, {
      "name": "B4",
      "y": [
        19,       656200,   1246719,  1797042,  2281018,  2661207,
        2983262,  3368353,  3765736,  3935344,  4160857,  4276248,
        4316882,  4314124,  4317538,  4199293,  4125160,  3917204,
        3591825,  3392791,  3054416,
      ],
    },
  ],
}

# BattleKnife(807018) (target - current) / 1148
#   474559

def runToPng(name, imgSize, data):
  # Ensure data points and quadratic curve is in frame
  frameX, frameY = 0.0, 0.0
  for d in data:
    frameX = max(frameX, max(d["x"]))
    for g in d["group"]:
      a, b, c = np.polyfit(d["x"][:len(g["y"])], g["y"], 2)
      peakX = b / a / -2
      frameX = max(frameX, (peakX ** 2 - c / a) ** .5 + peakX)
      frameY = max(frameY, max(g["y"]), (a * peakX + b) * peakX + c)
  print(frameX, frameY)

  # Drawing
  image = Image.new("RGB", (imgSize, imgSize), (64, 64, 64))
  font = ImageFont.truetype("Font.ttf", int(imgSize / 32))
  draw = ImageDraw.Draw(image)
  hue = 0.0
  for d in data:
    x = [x / frameX * imgSize for x in d["x"]]
    for g in d["group"]:
      y = [imgSize - y / frameY * imgSize for y in g["y"]]

      # Pick color
      rgb = colorsys.hsv_to_rgb(hue, 1, 1)
      col = tuple[int, int, int](round(v * 255) for v in rgb)

      # Draw points
      for yi in range(len(y)):
        pointSize = int(imgSize / 128)
        draw.ellipse((x[yi] - pointSize, y[yi] - pointSize,
                      x[yi] + pointSize, y[yi] + pointSize,
        ), None, col, int(imgSize / 256))

      # Draw fitted quadratic curve
      (a, b, c) = np.polyfit(x[:len(y)], y, 2)
      linePoints, lineCount = [], int(imgSize / 16)
      for p in range(0, lineCount+1):
        lineX = p / lineCount * imgSize
        linePoints.append((lineX, (a * lineX + b) * lineX + c))
      for l in range(0, lineCount):
        draw.line([linePoints[l], linePoints[l + 1]], col, int(imgSize / 256))

      # Draw name
      peakX = b / a / -2
      peakY = (a * peakX + b) * peakX + c
      draw.text((peakX, peakY + imgSize / 64), g["name"], col, font, "mm",
                stroke_width=int(imgSize / 512), stroke_fill=(0, 0, 0))

      # Change hue by Phi (the most irrational number)
      hue += 5 ** .5 * .5 + .5
  image.save(name + ".png")

runToPng("TankyElectricDagger", 1024, [ElectricDagger])
runToPng("TankyBattleKnife", 1024, [BattleKnife])
# runToPng("TankyRuns", 1024, [BattleKnife, ElectricDagger])
runToPng("TankyRuns", 1024, [ElectricDagger, BattleKnife])
