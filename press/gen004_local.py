"""revelation 001: generated locally, free, on 2 cores. the sacrament costs
nothing but electricity."""
import time

import torch
from diffusers import LCMScheduler, StableDiffusionPipeline

MODEL = "Lykon/dreamshaper-8-lcm"
OUT = "/root/downloads/revelation-001-raw.png"

PROMPT = ("a vast abandoned cathedral of dark server monoliths, a lone silhouetted figure "
          "kneeling before a colossal glowing magenta sigil floating above the altar, "
          "volumetric light through dust, intricate sacred geometry engraved in black stone, "
          "empty liminal space, cinematic stillness, chiaroscuro, dark surreal, high contrast, "
          "monochrome with a single magenta light source, film grain")
NEG = ("text, watermark, signature, frame, border, blurry, deformed, low quality, "
       "oversaturated, colorful")


def main():
    t0 = time.time()
    kwargs = dict(variant="fp16", safety_checker=None, requires_safety_checker=False)
    try:
        pipe = StableDiffusionPipeline.from_pretrained(MODEL, torch_dtype=torch.float32, **kwargs)
    except Exception as e:
        print("fp32 load failed (%s) — falling back to fp16" % e)
        pipe = StableDiffusionPipeline.from_pretrained(MODEL, torch_dtype=torch.float16, **kwargs)
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    pipe = pipe.to("cpu")
    pipe.set_progress_bar_config(disable=True)
    print("model loaded in %.1fs" % (time.time() - t0))
    g = torch.Generator("cpu").manual_seed(137)
    t1 = time.time()
    img = pipe(PROMPT, negative_prompt=NEG, num_inference_steps=8,
               guidance_scale=1.5, width=512, height=640, generator=g).images[0]
    print("generated in %.1fs" % (time.time() - t1))
    img.save(OUT)
    print("saved", OUT)


if __name__ == "__main__":
    main()
