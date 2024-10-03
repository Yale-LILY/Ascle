from Ascle_interface import AscleInterface
import warnings
import os

warnings.filterwarnings("ignore")
# Crear instancia de AscleInterface
med = AscleInterface()
#prompt = "extract abbreviations in: Rift Valley Fever Virus (RVFV) is an emerging zoonotic pathogen transmitted to humans and livestock through mosquito bites, which was first isolated in Kenya in 1930."

prompt = "Extract abbreviations from the following text: Spinal and bulbar muscular atrophy (SBMA) is an \
inherited motor neuron disease caused by the expansion \
of a polyglutamine tract within the androgen receptor (AR). \
SBMA can be caused by this easily."

'''
prompt =    """
            resume:
            The patient presents with symptoms of acute bronchitis,
            including cough, chest congestion, and mild fever.
            Auscultation reveals coarse breath sounds and occasional 
            wheezing. Based on the clinical examination, a diagnosis
            of acute bronchitis is made, and the patient is prescribed 
            a short course of bronchodilators and advised to rest and
            stay hydrated.
            """


'''

model = "meta-llama/Llama-2-7b-chat-hf"
med.choose_model("llama",model_llama=model)

output = med.process_prompt(prompt)
print("Output: ", output)