# docs/images

Both images are real renders of `demo/index.html` in headless Chrome — not mockups, not retouched. If the panel changes, regenerate rather than editing the pixels.

| File | What it is | Used by |
|---|---|---|
| `demo.png` | two crops stacked: the request card (scenario detected) above the generated prompt card | top of both READMEs, `GETTING_STARTED.md` §3 |
| `demo.gif` | 4 frames of the full page: empty → typing → detected → generated | "What's inside" section of both READMEs |

## Why the hero is a composite, not one screenshot

A single full-page shot at readable size is ~1130 px tall, which pushes the first paragraph below the fold. The composite is 776 × 661 and still shows the actual transformation: one line in, a constrained prompt out. Both halves are crops of the same render — neither is a redraw.

## How they were made

The panel accepts URL presets (`?lang`, `q`, `go`, `scroll`, `sy`) so any state can be reproduced from a string instead of by clicking around.

**GIF — four frames, no scrolling, identical crop box**

```bash
CHROME="/c/Program Files/Google/Chrome/Application/chrome.exe"
BASE="file:///<repo>/demo/index.html"

for u in "?lang=en" \
         "?lang=en&q=Design%20a%20travel%20boo" \
         "?lang=en&q=Design%20a%20travel%20booking%20site%20for%20me" \
         "?lang=en&q=Design%20a%20travel%20booking%20site%20for%20me&go=1"; do
  "$CHROME" --headless=new --hide-scrollbars --window-size=880,1450 \
    --virtual-time-budget=4000 --screenshot="frame_$RANDOM.png" "$BASE$u"
done
# Pillow: identical crop box across frames, 128-colour palette,
# durations 900 / 700 / 1000 / 2600 ms, loop forever
```

**Hero — two bands clipped out of the same page**

`scroll=req` and `scroll=out` put a specific card at the top of the viewport. Wrap the panel in an iframe offset by `-52px` horizontally inside an `overflow:hidden` box 760 px wide, screenshot that at `--force-device-scale-factor=2`, then stack the two bands with a 26 px gap on the `#fafafa` background.

```html
<div style="width:760px;height:300px;overflow:hidden;position:relative;background:#fafafa">
  <iframe src="index.html?lang=en&q=...&go=1&scroll=req"
          style="position:absolute;left:-52px;top:12px;width:880px;height:1600px;border:0"></iframe>
</div>
```

## Rules

- **Do not edit the pixels.** If a label is wrong, fix the panel and re-render — otherwise the image and the product drift apart, and this repo's whole argument is that claims should be reproducible.
- Keep the GIF under 8 MB (this one is ~0.16 MB). Above ~10 MB GitHub still renders it but mobile clients stall.
- Never put a real account name, bookmark bar, or another browser tab in the frame.
- Check the crops for stray slivers of the neighbouring card — the 12 px gap between cards is enough for the next card's top border to leak into a band.
