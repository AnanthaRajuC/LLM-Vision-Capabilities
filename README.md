<!--
*** Thanks for checking out LLM-Vision-Capabilities. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again!
-->

<div align="center">

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen?logo=github)](CODE_OF_CONDUCT.md) [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Checkout+this+recipe+for+LLM+Vision&url=https://github.com/AnanthaRajuC/LLM-Vision-Capabilities&hashtags=LLM) [![Twitter Follow](https://img.shields.io/twitter/follow/anantharajuc?label=follow%20me&style=social)](https://twitter.com/anantharajuc)
</div>

<div align="center">
  <sub>Built with ❤︎ by <a href="https://twitter.com/anantharajuc">Anantha Raju C</a> and <a href="https://github.com/AnanthaRajuC/LLM-Vision-Capabilities/graphs/contributors">contributors</a>
</div>

</br>

<p align="center">
	<a href="https://github.com/AnanthaRajuC/LLM-Vision-Capabilities/blob/master/README.md#llm-vision-capabilities"><strong>Explore the docs »</strong></a>
	<br />
	<br />
	<a href="https://github.com/AnanthaRajuC/LLM-Vision-Capabilities/issues">Report Bug</a>
	·
	<a href="https://github.com/AnanthaRajuC/LLM-Vision-Capabilities/issues">Request Feature</a>
</p>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
-->

|     Service     | Badge | Badge | Badge | Badge | Badge |
|-----------------|-------|-------|-------|-------|-------|
|  **GitHub**     |[![GitHub last commit](https://img.shields.io/github/last-commit/anantharajuc/LLM-Vision-Capabilities)](https://github.com/anantharajuc/LLM-Vision-Capabilities/commits/master)|[![GitHub pull requests](https://img.shields.io/github/issues-pr-raw/anantharajuc/LLM-Vision-Capabilities)](https://github.com/anantharajuc/LLM-Vision-Capabilities/pulls)|[![GitHub issues](https://img.shields.io/github/issues/anantharajuc/LLM-Vision-Capabilities)](https://github.com/anantharajuc/LLM-Vision-Capabilities/issues)|[![GitHub forks](https://img.shields.io/github/forks/anantharajuc/LLM-Vision-Capabilities)](https://github.com/anantharajuc/LLM-Vision-Capabilities/network)|[![GitHub stars](https://img.shields.io/github/stars/anantharajuc/LLM-Vision-Capabilities)](https://github.com/anantharajuc/LLM-Vision-Capabilities/stargazers)|
|  **GitHub**     |![GitHub top language](https://img.shields.io/github/languages/top/anantharajuc/LLM-Vision-Capabilities.svg)|

# LLM-Vision-Capabilities

This Python script allows you to identify crops in an image using [Ollama](https://ollama.com/) server to run vision-enabled LLMs locally, such as `llama3.2-vision` or `qwen2.5vl`, without relying on the Hugging Face Transformers library or cloud-based APIs.

It sends an image and a predefined JSON-format prompt to a selected vision model running locally via Ollama, and returns structured information about the crop detected in the image.

```text
Identify the crop in this image and respond ONLY in the following JSON format:

{
  "crop": "<primary crop name>",
  "alternate_names": ["<alternate name 1>", "<alternate name 2>"],
  "color": ["<color 1>", "<color 2>"],
  "confidence": <confidence score from 0 to 1>
}

If any field is not known, return an empty list or null value as appropriate. Do not include any other text.
```

## Model Recommendation

While the script has been briefly tested with `qwen2.5vl:latest` and `llama3.2-vision:latest`, `qwen2.5vl:latest` is recommended based on local testing due to:

- Reasonable inference times
- Reliable structured JSON responses
- Decent resource usage on a typical commodity laptop

⚠️ **Note:** These observations are based on running the models locally on a standard laptop. Performance and accuracy may vary depending on your system's hardware (CPU, GPU, RAM, etc.).

## Details
  
- [Getting Started](GETTING_STARTED.MD)

## Features

- Uses models like `llama3.2-vision` and `qwen2.5vl` via the Ollama API
- Accepts a local image and outputs structured JSON including:
  - Crop name
  - Alternate crop names
  - Color details
  - Confidence score
  - Metadata like inference time

## Demo Image

![Demo Image](crop_detector/assets/demo.jpg)

## Output

The result is a structured JSON response, like:

```json
{
  "crop": "peanut",
  "alternate_names": [
    "groundnut",
    "earthnut"
  ],
  "color": [
    "brown",
    "green"
  ],
  "confidence": 0.95,
  "metadata": {
    "startDateTime": "2025-05-17T11:05:47.702582",
    "endDateTime": "2025-05-17T11:09:09.020386",
    "duration": 201.32
  }
}
```
<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Kindly refer to [CONTRIBUTING.md](/CONTRIBUTING.md) for important **Pull Request Process** details

1. In the top-right corner of this page, click **Fork**.

2. Clone a copy of your fork on your local, replacing *YOUR-USERNAME* with your GitHub username.

   `git clone https://github.com/YOUR-USERNAME/LLM-Vision-Capabilities.git`

3. **Create a branch**: 

   `git checkout -b <my-new-feature-or-fix>`

4. **Make necessary changes and commit those changes**:

   `git add .`

   `git commit -m "new feature or fix"`

5. **Push changes**, replacing `<add-your-branch-name>` with the name of the branch you created earlier at step #3. :

   `git push origin <add-your-branch-name>`

6. Submit your changes for review. Go to your repository on GitHub, you'll see a **Compare & pull request** button. Click on that button. Now submit the pull request.

That's it! Soon I'll be merging your changes into the master branch of this project. You will get a notification email once the changes have been merged. Thank you for your contribution.

Kindly follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) to create an explicit commit history. Kindly prefix the commit message with one of the following type's.

**build**   : Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)  
**ci**      : Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)  
**docs**    : Documentation only changes  
**feat**    : A new feature  
**fix**     : A bug fix  
**perf**    : A code change that improves performance  
**refactor**: A code change that neither fixes a bug nor adds a feature  
**style**   : Changes that do not affect the meaning of the code (white-space, formatting, missing semicolons, etc.)  
**test**    : Adding missing tests or correcting existing tests  

## Reporting Issues/Suggest Improvements

This Project uses GitHub's integrated issue tracking system to record bugs and feature requests. If you want to raise an issue, please follow the recommendations below:

* 	Before you log a bug, please [search the issue tracker](https://github.com/AnanthaRajuC/LLM-Vision-Capabilities/search?type=Issues) to see if someone has already reported the problem.
* 	If the issue doesn't already exist, [create a new issue](https://github.com/AnanthaRajuC/LLM-Vision-Capabilities/issues/new)
* 	Please provide as much information as possible with the issue report.
* 	If you need to paste code, or include a stack trace use Markdown +++```+++ escapes before and after your text.  

## License

Distributed under the MIT License. See [LICENSE.md](/LICENSE) for more information.

## Author

Anantha Raju C - [@anantharajuc](https://twitter.com/anantharajuc) - arcswdev@gmail.com
