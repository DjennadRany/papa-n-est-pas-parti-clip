# AI motion production — no slideshow

## Source
Wan 2.2 I2V (open source): https://github.com/Wan-Video/Wan2.2
Free shared inference: https://huggingface.co/spaces/zerogpu-aoti/wan2-2-fp8da-aoti-faster

## Test
GitHub Actions → Generate AI motion shot (free public GPU) → Run workflow → scene 1.

This generates an actual video with character motion, not camera zoom. The free shared Hugging Face GPU may reject requests because of quota, queuing, or API changes. A GitHub runner does not have the GPU to run Wan locally. Never store Hugging Face tokens in source files.

## Output
Download the artifact ai-shot-1 from the Actions run. When approved, upload 01.mp4 to public/assets/video/ in this repository. Other shots follow the same pattern.

The final Remotion timeline must be adapted to video assets after a successful test. A complete 178-second movie cannot be guaranteed for free: public GPU limits and image consistency are real constraints. The 25-48 source images are low resolution and must be replaced for high-quality output.
