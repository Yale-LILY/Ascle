from langchain.prompts import PromptTemplate
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory
from typing import List, Dict, Any
from umls_rerank import get_umls_keys
from tqdm import tqdm
import pandas as pd

llm = ChatOpenAI(model_name="gpt-4-0125-preview",
                 temperature=0,
                 openai_api_key="API-KEY")

class ExtendedConversationBufferWindowMemory(ConversationBufferWindowMemory):
    extra_variables:List[str] = []

    @property
    def memory_variables(self) -> List[str]:
        """Will always return list of memory variables."""
        return [self.memory_key] + self.extra_variables

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Return buffer with history and extra variables"""
        d = super().load_memory_variables(inputs)
        d.update({k:inputs.get(k) for k in self.extra_variables})
        return d

memory = ExtendedConversationBufferWindowMemory(k=0,
                                                ai_prefix="Physician",
                                                human_prefix="Patient",
                                                extra_variables=["context"])

template = """
Answer the question in conjunction with the following content.

Context:
{context}
Current conversation:
{history}
Patient: {input}
Physician:
"""

PROMPT = PromptTemplate(
    input_variables=["context", "history", "input"], template=template
)

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=PROMPT,
    verbose=True,
)

PROMPT = """
Question: {question}

You are interacting with a knowledge graph that contains definitions and relational information of medical terminologies. To provide a precise and relevant answer to this question, you are expected to:

1. Understand the Question Thoroughly: Analyze the question deeply to identify which specific medical terminologies and their interrelations, as extracted from the knowledge graph, are crucial for formulating an accurate response.

2. Extract Key Terminologies: Return the 3-5 most relevant medical terminologies based on their significance to the question.

3. Format the Output : Return in a structured JSON format with the key as "medical terminologies". For example:

{"medical terminologies": ["term1", "term2", ...]}
"""

context = get_umls_keys(i, PROMPT, llm)
answer = conversation.predict(context=context, input=i)
