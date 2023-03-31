# Python
import openai
import gradio as gr
import requests
from PIL import Image

key = 'your key'

openai.api_key = key

# My ChatbotGPT

def openai_create(prompt):
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=prompt,
      temperature=0.9,
      max_tokens=1020,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0.6,
      stop=[" Human:", " AI:"]
    )
    
    return response.choices[0].text

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input + '\n')
    inp = ' \n'.join(s)
    output = openai_create(inp)
    history.append((input, output))
    
    return history, history

text_block = gr.Blocks()

with text_block:
    gr.Markdown("""<h1><center>My ChatbotGPT<center></h1>
    """)
    chatbot = gr.Chatbot()
    message = gr.Textbox(placeholder="Type:")
    state = gr.State()
    submit = gr.Button("SEND")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])
    
    
# My DALL·E

def openai_create_img(prompt):
    response = openai.Image.create(
      prompt=prompt,
      n=1,
      size="1024x1024"
    )
    
    image_url = response['data'][0]['url']
    r = requests.get(image_url, stream=True)
    img = Image.open(r.raw)
    
    return img


img_block = gr.Blocks()

with img_block:
    gr.Markdown("""<h1><center>My DALL·E<center></h1>
    """)
    new_image = gr.Image()
    message = gr.Textbox(placeholder="Type:")
    submit = gr.Button("SEND")
    submit.click(openai_create_img, inputs=[message], outputs=[new_image])
    

# DALL·E img Variator

def openai_var_img(im):
    img = Image.fromarray(im)
    img = img.resize((1024,1024))
    img.save("img1.png","PNG")
    
    response = openai.Image.create_variation(
      image=open("img1.png", "rb"),
      n=1,
      size="1024x1024"
    )
    
    image_url = response['data'][0]['url']
    r = requests.get(image_url, stream=True)
    img = Image.open(r.raw)
    
    return img

img_var_block = gr.Blocks()

with img_var_block:
    gr.Markdown("""<h1><center>DALL·E img Variator<center></h1>
    """)
    
    with gr.Row():
        im = gr.Image()
        im_2 = gr.Image()
        
    submit = gr.Button("SEND")
    submit.click(openai_var_img, inputs=[im], outputs=[im_2])
    

# Tabs
    
demo = gr.TabbedInterface([text_block, img_block,img_var_block], ["My ChatbotGPT", "My DALL·E","DALL·E img Variator"])

if __name__ == "__main__":
    demo.launch()
