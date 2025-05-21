import websockets
import gradio as gr

async def websocket_chat(prompt):
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(prompt)
            full_response = ""

            while True:
                message = await websocket.recv()
                if message == "[END]":
                    break
                full_response += message
                yield full_response, "blurry.jpg"
            yield full_response, "output.png"

    except Exception as e:
        yield f"❌ Error: {e}"

def launch_interface():
    with gr.Blocks(theme=gr.themes.Citrus(primary_hue="indigo", secondary_hue="teal")) as frontend:
        gr.HTML("<h1 align='center'>Image Generation Agent🎨</h1>")
        gr.HTML("<h2 align='center'>Get stunning AI-generated images!</h2>")
        with gr.Row():
            usr_txt = gr.Textbox(label="Prompt", placeholder="Describe the image you want here...")
            with gr.Column():
                resp = gr.Markdown(label="Agent Output", container=True, show_label=True, show_copy_button=True)
                gen_img = gr.Image(label="Generated Image")


        with gr.Row():
            btn = gr.Button("Generate🖌️").click(fn=websocket_chat, inputs=[usr_txt], outputs=[resp, gen_img])

    frontend.launch()

if __name__ == "__main__":
    launch_interface()
