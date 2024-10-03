from Ascle_interface import AscleInterface
import warnings

# Suppress any warnings
warnings.filterwarnings("ignore")

# Create an instance of AscleInterface
med = AscleInterface()

# Define the prompt

prompt = ("summarize this text: The patient presents with symptoms of acute bronchitis, "
          "including cough, chest congestion, and mild fever. Auscultation reveals coarse breath sounds "
          "and occasional wheezing. Based on the clinical examination, a diagnosis of acute bronchitis is made, "
          "and the patient is prescribed a short course of bronchodilators and advised to rest and stay hydrated.")


# Define the model

#model = "ireneli1024/bart-large-elife-finetuned"
# Choose the model
#med.choose_model("ascle", model_ascle=model)
med.choose_model("ascle")


# Process the prompt and print the output
output = med.process_prompt(prompt)
print("Output:", output)
