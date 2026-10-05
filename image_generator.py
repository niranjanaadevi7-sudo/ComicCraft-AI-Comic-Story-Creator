import os
import torch
from dotenv import load_dotenv
from diffusers import StableDiffusionPipeline

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

MODEL_ID = "stable-diffusion-v1-5/stable-diffusion-v1-5"

pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    token=HF_TOKEN
)

pipe = pipe.to("cpu")


def generate_image(prompt, output_path):
    image = pipe(
        prompt,
        num_inference_steps=10,
        height=512,
        width=512
    ).images[0]

    image.save(output_path)

    return output_path