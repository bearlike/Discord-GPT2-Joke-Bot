#!/usr/bin/env python3
import warnings
import discord
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import os
import numpy as np
import logging

logging.getLogger().setLevel(logging.CRITICAL)
warnings.filterwarnings('ignore')

class Utils:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2-medium')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2-medium')
        self.device = 'cpu'
        if torch.cuda.is_available():
            self.device = 'cuda'
        self.model = self.model.to(self.device)

    def say_joke(self, keyword: str) -> str:
        status, joke = self.generate_joke(begin=keyword, epoch=4)
        return joke.capitalize()

    def choose_from_top(self, probs, n=5):
        ind = np.argpartition(probs, -n)[-n:]
        top_prob = probs[ind]
        top_prob = top_prob / np.sum(top_prob)  # Normalize
        choice = np.random.choice(n, 1, p=top_prob)
        token_id = ind[choice][0]
        return int(token_id)

    def generate_joke(self, begin="", epoch=2):
        MODEL_EPOCH = epoch
        models_folder = "trained_models"
        model_path = os.path.join(
            models_folder, f"gpt2_medium_joker_{MODEL_EPOCH}.pt")
        self.model.load_state_dict(torch.load(model_path))
        self.model.eval()

        with torch.no_grad():
            joke_finished = False
            cur_ids = torch.tensor(self.tokenizer.encode(
                f"JOKE:{begin}")).unsqueeze(0).to(self.device)
            for i in range(100):
                outputs = self.model(cur_ids, labels=cur_ids)
                loss, logits = outputs[:2]
                # Take the first(from only one in this case) batch and the last predicted embedding
                softmax_logits = torch.softmax(logits[0, -1], dim=0)
                if i < 3:
                    n = 20
                else:
                    n = 3
                # Randomly(from the topN probability distribution) select the next word
                next_token_id = self.choose_from_top(
                    softmax_logits.to('cpu').numpy(), n=n)
                cur_ids = torch.cat([cur_ids, torch.ones((1, 1)).long().to(
                    self.device) * next_token_id], dim=1)  # Add the last word to the running sequence

                if next_token_id in self.tokenizer.encode('<|endoftext|>'):
                    joke_finished = True
                    break

            if joke_finished:
                output_list = list(cur_ids.squeeze().to('cpu').numpy())
                output_text = self.tokenizer.decode(output_list)
                output_text = output_text.replace(
                    "JOKE:", "").replace('<|endoftext|>', "")
                return (True, output_text)
        return (False, "I don't know a joke with that")
