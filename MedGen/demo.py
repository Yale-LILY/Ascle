from MedGen import MedGen
import pprint

if __name__ == '__main__':
    print("Welcome to LILY-MedGen. Here's a complete run-through of all MedGen text processing functions.")

    # initialize MedGen object
    med = MedGen()

    print("========== Start of SciSpacy Functions ==========")

    print('\n\n')
    print('Abbreviations')

    record =  "Rift Valley Fever Virus (RVFV) is an emerging zoonotic pathogen transmitted to humans and livestock through mosquito bites, which was first isolated in Kenya in 1930. The virus is classified by the WHO among the pathogens for which there is an urgent need to develop research, diagnostics, and therapies. However, the efforts developed to control the virus remain limited, and the virus is not well characterized. In this article, we will introduce RVFV and then focus on its virulence factor, the nonstructural protein NSs. We will mainly discuss the ability of this viral protein to form amyloid-like fibrils and its implication in the neurotoxicity associated with RVFV infection."

    med.update_and_delete_main_record(record)
    print(med.get_abbreviations())


    print('\n\n')
    print('Hyponyms')

    record = "Keystone plant species such as fig trees are good for the soil."

    med.update_and_delete_main_record(record)
    print(med.get_hyponyms())

   
    print('\n\n')
    print('Linked entities')

    record = "Spinal and bulbar muscular atrophy (SBMA) is an " \
             "inherited motor neuron disease caused by the expansion" \
             "of a polyglutamine tract within the androgen receptor (AR)." \
             "SBMA can be caused by this easily."

    med.update_and_delete_main_record(record)
    print(med.get_linked_entities())

    print('\n\n')
    print('Named entities')

    record = """
             Myeloid derived suppressor cells (MDSC) are immature
             myeloid cells with immunosuppressive activity.
             They accumulate in tumor-bearing mice and humans
             with different types of cancer, including hepatocellular
             carcinoma (HCC).
             """

    med.update_and_delete_main_record(record)
    print(med.get_named_entities())

    print('\n\n')
    print('POS Tagging')

    record = """
             Myeloid derived suppressor cells (MDSC) are immature
             myeloid cells with immunosuppressive activity.
             They accumulate in tumor-bearing mice and humans
             with different types of cancer, including hepatocellular
             carcinoma (HCC).
             """

    med.update_and_delete_main_record(record)
    print(med.get_pos_tagging(model_name="en_core_sci_sm")) 

    print("========== End of SciSpacy Functions ==========")
    print('\n\n')

    # translation
    print("========== Start of Translation ==========")

    # reference: https://qbi.uq.edu.au/brain/brain-anatomy/what-neuron
    record = "Neurons (also called neurones or nerve cells) are the fundamental units of the brain and nervous system, " \
             "the cells responsible for receiving sensory input from the external world, for sending motor commands to " \
             "our muscles, and for transforming and relaying the electrical signals at every step in between. More than " \
             "that, their interactions define who we are as people. Having said that, our roughly 100 billion neurons do" \
             " interact closely with other cell types, broadly classified as glia (these may actually outnumber neurons, " \
             "although it’s not really known)."


    med.update_and_delete_main_record(record)
    print(med.get_translation('French'))

    print("========== End of Translation ==========")

    # segmentation
    print("========== Start of Sentencizer ==========")

    record = "Neurons (also called neurones or nerve cells) are the fundamental units of the brain and nervous system, " \
             "the cells responsible for receiving sensory input from the external world, for sending motor commands to " \
             "our muscles, and for transforming and relaying the electrical signals at every step in between. More than " \
             "that, their interactions define who we are as people. Having said that, our roughly 100 billion neurons do" \
             " interact closely with other cell types, broadly classified as glia (these may actually outnumber neurons, " \
             "although it’s not really known)."

    med.update_and_delete_main_record(record)

    print('Using stanza')
    print(med.get_sentences('stanza'))

    # print('Using PyRush')
    # print(med.get_sentences('pyrush'))

    print('Using SciSpacy')
    print(med.get_sentences('scispacy'))

    print("========== End of Sentencizer ==========")

    # clustering
    print("========== Start of Clustering ==========")

    record = "Neurons (also called neurones or nerve cells) are the fundamental units of the brain and nervous system, " \
             "the cells responsible for receiving sensory input from the external world, for sending motor commands to " \
             "our muscles, and for transforming and relaying the electrical signals at every step in between. More than " \
             "that, their interactions define who we are as people. Having said that, our roughly 100 billion neurons do" \
             " interact closely with other cell types, broadly classified as glia (these may actually outnumber neurons, " \
             "although it’s not really known)."

    # reference: https://www.investopedia.com/terms/n/neuralnetwork.asp
    cand1 = "A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of " \
            "data through a process that mimics the way the human brain operates. In this sense, neural networks refer to " \
            "systems of neurons, either organic or artificial in nature."

    # reference: https://medlineplus.gov/druginfo/meds/a682878.html
    cand2 = "Prescription aspirin is used to relieve the symptoms of rheumatoid arthritis (arthritis caused by swelling " \
            "of the lining of the joints), osteoarthritis (arthritis caused by breakdown of the lining of the joints), " \
            "systemic lupus erythematosus (condition in which the immune system attacks the joints and organs and causes " \
            "pain and swelling) and certain other rheumatologic conditions (conditions in which the immune system " \
            "attacks parts of the body)."

    # reference: https://www.medicalnewstoday.com/articles/161255
    cand3 = "People can buy aspirin over the counter without a prescription. Everyday uses include relieving headache, " \
            "reducing swelling, and reducing a fever. Taken daily, aspirin can lower the risk of cardiovascular events, " \
            "such as a heart attack or stroke, in people with a high risk. Doctors may administer aspirin immediately" \
            " after a heart attack to prevent further clots and heart tissue death."

    med.update_and_delete_main_record(record)
    med.replace_supporting_records([cand1, cand2, cand3])
    print(med.get_clusters())

    print("========== End of Clustering ==========")

    # similar documents
    print("========== Start of Similar Documents ==========")

    record = "Neurons (also called neurones or nerve cells) are the fundamental units of the brain and nervous system, " \
             "the cells responsible for receiving sensory input from the external world, for sending motor commands to " \
             "our muscles, and for transforming and relaying the electrical signals at every step in between. More than " \
             "that, their interactions define who we are as people. Having said that, our roughly 100 billion neurons do" \
             " interact closely with other cell types, broadly classified as glia (these may actually outnumber neurons, " \
             "although it’s not really known)."

    # reference: https://www.investopedia.com/terms/n/neuralnetwork.asp
    cand1 = "A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of " \
            "data through a process that mimics the way the human brain operates. In this sense, neural networks refer to " \
            "systems of neurons, either organic or artificial in nature."

    # reference: https://medlineplus.gov/druginfo/meds/a682878.html
    cand2 = "Prescription aspirin is used to relieve the symptoms of rheumatoid arthritis (arthritis caused by swelling " \
            "of the lining of the joints), osteoarthritis (arthritis caused by breakdown of the lining of the joints), " \
            "systemic lupus erythematosus (condition in which the immune system attacks the joints and organs and causes " \
            "pain and swelling) and certain other rheumatologic conditions (conditions in which the immune system " \
            "attacks parts of the body)."

    # reference: https://www.medicalnewstoday.com/articles/161255
    cand3 = "People can buy aspirin over the counter without a prescription. Everyday uses include relieving headache, " \
            "reducing swelling, and reducing a fever. Taken daily, aspirin can lower the risk of cardiovascular events, " \
            "such as a heart attack or stroke, in people with a high risk. Doctors may administer aspirin immediately" \
            " after a heart attack to prevent further clots and heart tissue death."

    med.update_and_delete_main_record(record)
    med.replace_supporting_records([cand1, cand2, cand3])
    print(med.get_similar_documents(3))

    print("========== End of Similar Documents ==========")

    """ UNDER CONSTRUCTION """
    """ stanza functions """
    # print dependencies
    record = "A neural network is a series of algorithms that endeavors to recognize underlying relationships in a set of " \
             "data through a process that mimics the way the human brain operates. In this sense, neural networks refer to " \
             "systems of neurons, either organic or artificial in nature."

    med.update_and_delete_main_record(record)
    med.get_dependency()

    print("========== Start of Pretrained Model Functions ==========")
    print('')
    
    print('\n\n')
    print('POS Tagging with Huggingface')
    import pprint
    record = 'The patient presented with a persistent cough and shortness of breath.'
    med.update_and_delete_main_record(record)
    pprint.pprint(med.get_pos_tagging_hf())

    
    
    print('\n\n')
    print('Question Generation')

    record = """
             Myeloid derived suppressor cells (MDSC) are immature
             myeloid cells with immunosuppressive activity.
             They accumulate in tumor-bearing mice and humans
             with different types of cancer, including hepatocellular
             carcinoma (HCC).
             """
    med.update_and_delete_main_record(record)
    print(med.get_question())


    print('\n\n')
    print("Translations")
    print(med.get_translation_mt5('French'))

    print('\n\n')
    print("Question and Answering: choose from 5 candidates")
    text = ""
    question = "The excitatory postsynaptic potentials:"
    choices = ["They are all or nothing." ,
               "They are hyperpolarizing.",
               "They can be added.",
               "They spread long distances.",
               "They present a refractory period."]
    num_labels = 5
    med.update_and_delete_main_record(question)
    print("The answer is: ", med.get_choice(text, question, choices, num_labels))

    print('\n\n')
    print("Question and Answering: ")
    question = 'Question: What are the common symptoms of the flu?'
    content = 'Content: Influenza, commonly known as the flu, is a viral respiratory illness. It is characterized by symptoms such as fever, cough, sore throat, runny or stuffy nose, body aches, fatigue, and headaches.'
    med.update_and_delete_main_record(question)
    print(med.get_span_answer(content))

    print('\n\n')
    print("Translate to Layman language: ")
    content = 'The patient presents with symptoms of acute bronchitis, including cough, chest congestion, and mild fever. Auscultation reveals coarse breath sounds and occasional wheezing. Based on the clinical examination, a diagnosis of acute bronchitis is made, and the patient is prescribed a short course of bronchodilators and advised to rest and stay hydrated.'
    layman_model = "ireneli1024/bart-large-elife-finetuned"
    med.update_and_delete_main_record(content)
    print(med.get_layman_text(layman_model, min_length=20, max_length=70))


    print('\n\n')
    print("Interactive chat, by default, this will last 5 rounds: ")
    med.get_dialogpt()








