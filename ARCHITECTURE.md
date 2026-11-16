# Studio Clip IA — architecture

## Production
1. Upload images, soundtrack, and storyboard to the existing repository.
2. Keep a scene manifest in scenes.json with explicit start/end timecodes.
3. Generate each numbered MP4 with Wan or any other image-to-video engine.
4. Preserve approved footage as public/assets/video/NN.mp4, or as GitHub Actions checkpoint artifacts until approval.
5. Validate all required clips. No automatic substitution with still images.
6. Assemble on the original song with Remotion, export MP4.

## Multiple engines
Providers are interchangeable at the **file** boundary: every provider must output an MP4 named NN.mp4. Free Hugging Face ZeroGPU availability is not guaranteed. No automatic paid-provider failover is configured. Provider credentials must be held in GitHub Actions secrets, never committed.

## Dashboard
The GitHub Pages site under docs/ provides a local project manifest editor and production progress. It cannot directly upload to a private repository or launch Actions without authenticated GitHub integration. Anonymous GitHub API calls cannot inspect a private repository. GitHub Pages availability for private repos depends on GitHub plan/settings. The current dashboard is a functional frontend, not a fully autonomous upload-and-render application.

## Limits and next milestones
- Provide an authenticated GitHub App/OAuth backend or a user-controlled GitHub token flow to support uploads, workflow dispatch, and progress on private repos.
- Add a durable video asset store beyond temporary Actions artifacts; GitHub Git is not optimized for many large MP4s, and Git LFS may have limits.
- Add true multi-provider adapters and scene-level quality checks.
- Align exact musical cut points, verify duration and render with audio.
- Existing low-resolution 25–48 images need high-resolution replacements.
