<!--
*** Thanks for checking out LLM-Vision-Capabilities. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again!
-->
# LLM-Vision-Capabilities

This Python script allows you to identify crops in an image using a local [Ollama](https://ollama.com/) server with vision-capable large language models (LLMs) such as `llama3.2-vision` or `qwen2.5vl`.

It sends an image and a predefined JSON-format prompt to a selected vision model running locally via Ollama, and returns structured information about the crop detected in the image.

## Features

- Uses models like `llama3.2-vision` and `qwen2.5vl` via the Ollama API
- Accepts a local image and outputs structured JSON including:
  - Crop name
  - Alternate crop names
  - Color details
  - Confidence score
  - Metadata like inference time

## Requirements

- Python 3.6+
- [Ollama](https://ollama.com) installed and running locally
- Required Python packages:
  - `requests`
  - `Pillow`
  - `ollama` (Ollama Python SDK)

## Installation

```bash
pip install requests pillow ollama
```

Ensure Ollama is installed and running:

```bash
ollama serve
```

Then pull the desired vision model(s):

```bash
ollama pull llama3.2-vision
ollama pull qwen2.5vl
```

## Usage

```bash
python3 LLM-Vision-Capabilities.py <model_name> <image_path>
```

### Examples

```bash
python3 LLM-Vision-Capabilities.py llama3.2-vision:latest /home/user/image.jpg
python3 LLM-Vision-Capabilities.py qwen2.5vl:latest /home/user/image.jpg
```

If no arguments are passed, defaults will be used:
- Model: `qwen2.5vl:latest`
- Image: `/home/anantharajuc/Desktop/ng.jpg`

## Output

The result is a structured JSON response, like:

```json
{
  "crop": "wheat",
  "alternate_names": ["triticum"],
  "color": ["golden", "brown"],
  "confidence": 0.92,
  "metadata": {
    "startDateTime": "2025-05-17T12:00:00",
    "endDateTime": "2025-05-17T12:00:03",
    "duration": 3.0
  }
}
```

## Notes

- Ensure that the Ollama server is running on `http://localhost:11434`
- The script encodes the image in base64 before sending it to the model
- The output strictly follows the expected JSON schema

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Kindly refer to [CONTRIBUTING.md](/CONTRIBUTING.md) for important **Pull Request Process** details

1. In the top-right corner of this page, click **Fork**.

2. Clone a copy of your fork on your local, replacing *YOUR-USERNAME* with your Github username.

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
**style**   : Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)  
**test**    : Adding missing tests or correcting existing tests  

## Reporting Issues/Suggest Improvements

This Project uses GitHub's integrated issue tracking system to record bugs and feature requests. If you want to raise an issue, please follow the recommendations below:

* 	Before you log a bug, please [search the issue tracker](https://github.com/AnanthaRajuC/LLM-Vision-Capabilities/search?type=Issues) to see if someone has already reported the problem.
* 	If the issue doesn't already exist, [create a new issue](https://github.com/AnanthaRajuC/LLM-Vision-Capabilities/issues/new)
* 	Please provide as much information as possible with the issue report.
* 	If you need to paste code, or include a stack trace use Markdown +++```+++ escapes before and after your text.  

## License

Distributed under the MIT License. See [LICENSE.md](/LICENSE.md) for more information.

## Author

Anantha Raju C - [@anantharajuc](https://twitter.com/anantharajuc) - arcswdev@gmail.com
