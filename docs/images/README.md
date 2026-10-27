# docs/images

Both images are real renders of `demo/index.html` in headless Chrome — not mockups, not retouched. If the panel changes, regenerate rather than editing the pixels.

| File | What it is | Used by |
|---|---|---|
| `demo.gif` | 4 frames: empty → typing → scenario detected → prompt generated | top of both READMEs |
| `demo.png` | the same panel, static, English, full height | `GETTING_STARTED.md` §3 |

## How they were made

The panel accepts URL presets (`?lang`, `q`, `go`, `scroll`, `sy`) so a state can be reproduced from a string rather than by clicking around.

```bash
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
BASE="file:///<repo>/demo/index.html"

# static hero: English UI, request pre-filled, prompt generated
"$CHROME" --headless=new --hide-scrollbars --force-device-scale-factor=2 \
  --window-size=880,1700 --virtual-time-budget=4000 \
  --screenshot=demo_raw.png \
  "$BASE?lang=en&q=Design%20a%20travel%20booking%20site%20for%20me&go=1&scroll=out"
# then crop the background-coloured tail and downscale to 1280 wide

# gif: four frames, no scrolling, identical crop box
for u in "?lang=en" \
         "?lang=en&q=Design%20a%20travel%20boo" \
         "?lang=en&q=Design%20a%20travel%20booking%20site%20for%20me" \
         "?lang=en&q=Design%20a%20travel%20booking%20site%20for%20me&go=1"; do
  "$CHROME" --headless=new --hide-scrollbars --window-size=880,1450 \
    --virtual-time-budget=4000 --screenshot="f_$RANDOM.png" "$BASE$u"
done
# assemble with Pillow: identical crop box across frames, 128-colour palette,
# durations 900 / 700 / 1000 / 2600 ms, loop forever
```

## Rules

- **Do not edit the pixels.** If a label is wrong, fix the panel and re-render — otherwise the image and the product drift apart, and this repo's whole argument is that claims should be reproducible.
- Keep the GIF under 8 MB (this one is ~0.16 MB). Above ~10 MB GitHub still renders it but mobile clients stall.
- Never put a real account name, bookmark bar, or another browser tab in the frame.
