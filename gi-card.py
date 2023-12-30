import hashlib
import json
import locale
import os
import random
import time
from urllib.request import urlopen, Request
from PIL import Image, ImageDraw, ImageFilter, ImageFont

salt = "6s25p5ox5y14umn1p61aqyyvbvvl3lrt"
locale.setlocale(locale.LC_ALL, 'zh-cn')

# Reference: https://github.com/Scighost/Starward/blob/2df96823d634c67da9cf561decbee6643070c6b5/src/Starward.Core/GameRecord/GameRecordClient.cs#L72-L117
def generate_secret():
  t = int(time.time())
  r = "".join(random.choice('ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678') for _ in range(6))
  data = f"salt={salt}&t={t}&r={r}"
  #if body or query:
  #  query_parts = query.split("&")
  #  query_parts.sort()
  #  query_sorted = "&".join(query_parts)
  #  data += f"&b={body}&q={query_sorted}"
  check = hashlib.md5(data.encode("UTF-8")).hexdigest()
  return f"{t},{r},{check}"

# https://bbs-api-os.hoyolab.com/game_record/genshin/api/index?server=os_asia&role_id=857179228
server = os.environ["GI_SERVER"]
uid = os.environ["GI_UID"]
cookie = os.environ["GI_COOKIE"]

req = Request(
  f"https://bbs-api-os.hoyolab.com/game_record/genshin/api/index?server={server}&role_id={uid}",
  headers={
    "cookie": cookie,
    "ds": generate_secret(),
    "x-rpc-app_version": "1.5.0",
    "x-rpc-client_type": "5",
    "x-rpc-language": "zh-cn",
  }
)
with urlopen(req) as resp:
  response_bytes: bytes = resp.read()
resp_obj = json.loads(response_bytes.decode())
if resp_obj["retcode"] != 0:
  raise RuntimeError("API error %r: %r" % (resp_obj["retcode"], resp_obj["message"]))
data = resp_obj["data"]

text_color = (255, 255, 255, 255)
shadow_color = (13, 13, 13 ,128)
font_path = "assets/zh-cn.ttf"

nickname: str = data["role"]["nickname"]
level: int = data["role"]["level"]
active_days: int = data["stats"]["active_day_number"]
character_count: int = data["stats"]["avatar_number"]
achievement_count: int = data["stats"]["achievement_number"]
spiral_abyss: int = data["stats"]["spiral_abyss"]

img = Image.new("RGBA", (1000, 330), (255, 255, 255, 255))
img.paste(Image.open("assets/bg.png"), (0, 0, *img.size))

text_layer = Image.new("RGBA", img.size)
text_draw = ImageDraw.Draw(text_layer)
text_font_12 = ImageFont.truetype(font_path, 24)
text_font_14 = ImageFont.truetype(font_path, 28)
text_font_24 = ImageFont.truetype(font_path, 48)

nickname_anchor = (20, 36)
text_draw.text(nickname_anchor, nickname, text_color, text_font_24, "lm")
level_anchor = (nickname_anchor[0] + text_font_24.getbbox(nickname, anchor="lm")[2] + 16, 36)
text_draw.text(level_anchor, f"Lv.{level}", text_color, text_font_12, "lm")

text_draw.text((20, 80), f"UID: {uid}", text_color, text_font_14, "lm")

for i, (label, value) in enumerate([
  ("活跃天数", active_days),
  ("角色数量", character_count),
  ("成就数量", achievement_count),
  ("深境螺旋", spiral_abyss),
]):
  x = 72 + i * 144
  text_draw.text((x, 270), str(value), text_color, text_font_24, "mm")
  text_draw.text((x, 306), label, text_color, text_font_12, "mm")

text_draw.text((980, 24), f"{time.strftime('%Y/%m/%d %H时（%Z）')}更新", text_color, text_font_12, "rm")

text_draw.text((980, 254), "DGCK81LNN", text_color, text_font_12, "rm")
text_draw.text((980, 280), "基于 GitHub Actions", text_color, text_font_12, "rm")
text_draw.text((980, 306), "参考 Genshin-card", text_color, text_font_12, "rm")

text_shadow = text_layer.getchannel("A").filter(ImageFilter.GaussianBlur(10))

img.paste(Image.new("RGBA", text_layer.size, shadow_color), mask=text_shadow)
img.alpha_composite(text_layer)
img = img.convert("RGB")

out_dir = "output"
os.makedirs(out_dir, exist_ok=True)
img.save(os.path.join(out_dir, f"{uid}.jpg"), quality=95, progressive=True)
