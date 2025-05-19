import gradio as gr
import requests as rq

def generate_image_for_user(prompt: str):
    res = rq.post("http://0.0.0.0:8000/agent", json={"prompt": prompt})
    if res.status_code > 400:
        return "404.png", "An error has occurred while generating the image", f"Error: {res.text}"
    else:
        return "output.png", res.json()["process"], res.json()["response"]

with gr.Blocks(theme=gr.themes.Citrus(primary_hue="indigo", secondary_hue="teal")) as frontend:
    gr.HTML("<h1 align='center'>Image Generation Agent🎨</h1>")
    gr.HTML("<h2 align='center'>Get stunning AI-generated images!</h2>")
    with gr.Row():
        usr_txt = gr.Textbox(label="Prompt", placeholder="Describe the image you want here...")
        with gr.Column():
            gen_img = gr.Image(label="Generated Image")
            with gr.Accordion(label="Agent Output", open=False):
                resp = gr.Markdown(label="Agent Response", container=True)
                proc = gr.Markdown(label="Agent Process", container=True)
    with gr.Row():
        btn = gr.Button("Generate🖌️").click(fn=generate_image_for_user, inputs=[usr_txt], outputs=[gen_img, proc, resp])
