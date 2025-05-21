# Image Generation Agent

**Image Generation Agent** is an open source project aimed at helping you produce stunning images aligned with your prompts, through the automation of the prompt refinement-generation-visual feedback loop.

## Installation

This is a **uv project**, thus you have to make sure uv is installed on your machine - if not, you can get it with:

```bash
pip install uv
```

Or follow the [installation guidelines](https://docs.astral.sh/uv/getting-started/installation/) on uv docs.

Once uv is on your machine, you can clone this repository:

```bash
git clone https://github.com/run-llama/image-generation-agent
cd image-generation-agent
```

And run:

```bash
uv sync
source .venv/bin/activate
```

Congrats, you successfully installed this project and its dependencies!

## Setting up

Access the `scripts` sub-folder, and modify the [`.env.example`](./scripts/.env.example) file so that it contains a valid `GOOGLE_API_KEY` and `OPENAI_API_KEY`. After that, make sure to rename it to `.env`:

```bash
cd scripts/
mv .env.example .env
```

Alternatively, you can export the keys as environmental variables from your terminal:

```bash
export GOOGLE_API_KEY="***"
export OPENAI_API_KEY="sk-***"
```

## Launching

While still being in the `scripts` sub-folder, you can launch the backend of the project with:

```bash
python3 server.py
```

You will se a log message telling you that the websocket server has been started on port 8765.

After the websocket has connected, launch the frontend from another terminal window (remaining in the `scripts` sub-folder and with the virtual environment active), using:

```bash
python3 client.py
```

With this command, you'll have the application running on http://localhost:7860 and you will be able to interact with it!

## How does it work?

The agent uses two tools under the hood:

- `generate_image`: this exploits OpenAI image generation API to create images starting from textual prompts.
- `evaluate_generated_image`: this uses the advanced vision capabilities of Gemini, employing the model as a judge of the faithfulness and quality of the image

Whenever you submit a request, the agent first activates the `generate_image` tool, then it assess the fit of the image with your prompt using the `evaluate_generated_image` tool. If the image is deemed suitable, it is returned to the user, whereas otherwise the prompt is refined and the generate-evaluate loop is resumed.

## Contributing

Contributions are more than welcome! Follow the [contribution guidelines](CONTRIBUTING.md) to make sure your contribution is compliant with the repo's requirements :)

## License and rights of usage

This is an open-source project distributed under an [MIT License](LICENSE).
