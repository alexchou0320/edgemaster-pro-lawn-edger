
import urllib.request, json, time, os

API = "http://127.0.0.1:8188"
OUT = "C:\\site\\images"

os.makedirs(OUT, exist_ok=True)

def make_wf(prompt, neg, seed, w, h):
    return {
        "3": {"class_type": "KSampler", "inputs": {"seed": seed, "steps": 28, "cfg": 7.0,
            "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0,
            "model": ["4", 0], "positive": ["6", 0], "negative": ["7", 0], "latent_image": ["5", 0]}},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": "sd_xl_base_1.0.safetensors"}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"text": prompt, "clip": ["4", 1]}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["4", 1]}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "v2_", "images": ["8", 0]}}
    }

def gen(prompt, neg, seed, w, h, label):
    wf = make_wf(prompt, neg, seed, w, h)
    body = json.dumps({"prompt": wf}).encode()
    req = urllib.request.Request(f"{API}/prompt", data=body, headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req, timeout=60).read())
    pid = resp["prompt_id"]
    print(f"[{label}] queued", flush=True)
    for i in range(60):
        time.sleep(2)
        try:
            status = json.loads(urllib.request.urlopen(f"{API}/history/{pid}", timeout=10).read())
            if pid in status:
                for nid, no in status[pid].get("outputs",{}).items():
                    if "images" in no:
                        img = no["images"][0]
                        url = f"{API}/view?filename={img['filename']}&subfolder={img.get('subfolder','')}&type={img.get('type','output')}"
                        data = urllib.request.urlopen(url, timeout=30).read()
                        path = f"{OUT}\\{label}.png"
                        with open(path, "wb") as f:
                            f.write(data)
                        print(f"  -> {label}.png ({len(data)//1024}KB)", flush=True)
                        return
                break
        except:
            if i > 10: pass

neg = "blurry, low quality, distorted, watermark, text, signature, ugly, deformed, bad anatomy, amateur"
neg_h = neg + ", malformed hands, extra fingers"

images = [
    ("hero-cinematic", "cinematic product shot of premium manual lawn edger, dramatic golden hour lighting, wheel rotary edger with titanium blade, commercial photography, moody atmosphere", neg, 42, 1024, 1024),
    ("hero-angle2", "professional product photo manual lawn edger, rear 3/4 angle view, titanium blade, studio lighting white background, commercial photography", neg, 88, 1024, 1024),
    ("lifestyle-sunset", "sunset garden, using manual lawn edger to create clean edge, warm sunlight, bokeh, professional gardening lifestyle photography", neg_h, 156, 1344, 832),
    ("lifestyle-modern", "modern garden, person edging lawn, clean background, daylight, professional landscaping, editorial photography", neg_h, 222, 1344, 832),
    ("blade-premium", "extreme macro titanium alloy cutting blade, metallic texture, razor edge, shallow depth of field, luxury product detail", neg, 333, 1024, 1024),
    ("pedal-premium", "close-up wide foot pedal, textured non-slip surface, brushed metal, luxury tool macro photography", neg, 555, 1024, 1024),
    ("handle-premium", "ergonomic handle grip close-up, soft rubber texture, comfort grip, luxury tool macro photography, studio lighting", neg, 666, 1024, 1024),
    ("flatlay-wood", "flat lay premium lawn edger on weathered wood, garden tools, natural lighting, editorial style, top down view", neg, 888, 1408, 1024),
    ("action-dynamic", "dynamic action lawn edger in use, grass clippings flying, dramatic sunlight, landscaping action", neg_h, 999, 1344, 832),
    ("before-after", "split comparison lawn edge, left overgrown messy grass, right perfectly manicured edge, side by side, natural lighting", neg, 777, 1408, 768),
]

for label, prompt, neg_p, seed, w, h in images:
    print(f"=== {label} ===", flush=True)
    try:
        gen(prompt, neg_p, seed, w, h, label)
    except Exception as e:
        print(f"FAILED: {e}", flush=True)
        time.sleep(3)

print("ALL DONE")
