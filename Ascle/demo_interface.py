from Ascle_interface import AscleInterface
import warnings
import os

warnings.filterwarnings("ignore")
# Crear instancia de AscleInterface
med = AscleInterface()
#prompt = "extract abbreviations in: Rift Valley Fever Virus (RVFV) is an emerging zoonotic pathogen transmitted to humans and livestock through mosquito bites, which was first isolated in Kenya in 1930."
'''
prompt = "Get abbreviations: Spinal and bulbar muscular atrophy (SBMA) is an \
inherited motor neuron disease caused by the expansion \
of a polyglutamine tract within the androgen receptor (AR). \
SBMA can be caused by this easily."
'''
prompt =    """
            The patient presents with symptoms of acute bronchitis,
            including cough, chest congestion, and mild fever.
            Auscultation reveals coarse breath sounds and occasional 
            wheezing. Based on the clinical examination, a diagnosis
            of acute bronchitis is made, and the patient is prescribed 
            a short course of bronchodilators and advised to rest and
            stay hydrated.
            """
# Elegir modelo específico (chatgpt, claude, gemini o local)
med.choose_model('chatgpt')  # Usar modelo ChatGPT
# Procesar un prompt con el modelo seleccionado
output = med.process_prompt(prompt)
print("**********")
print("chatgpt:\n", output)
print("**********")
med.choose_model('claude')  # Usar modelo Claude
output = med.process_prompt(prompt)
print("claude:\n", output)

print("**********")
med.choose_model('gemini')  # Usar modelo Gemini
output = med.process_prompt(prompt)
print("gemini:\n", output)

print("**********")
# Cambiar a modelo local
med.choose_model('Ascle')
# Procesar un prompt con un modelo local (analiza el tipo de acción)
output = med.process_prompt(prompt)
print("Ascle:\n", output)
