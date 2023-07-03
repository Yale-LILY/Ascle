import itertools

import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from transformers import AutoModel, BertTokenizerFast
import numpy as np
from sklearn.metrics import classification_report



MAX_SEQ_LEN=500

def run_BERT(mimic_path, bert_fast_dev_run=False):
    "credit to https://colab.research.google.com/github/prateekjoshi565/Fine-Tuning-BERT/blob/master/Fine_Tuning_BERT_for_Spam_Classification.ipynb"
    # -*- coding: utf-8 -*-

    #%%
    # specify GPU
    device = torch.device("cuda")

    """# Load Dataset"""

    #%%

    train = pd.read_csv(mimic_path + 'train.csv', converters={'TARGET': eval})
    test = pd.read_csv(mimic_path + 'test.csv', converters={'TARGET': eval})


    if bert_fast_dev_run:
        train = train.head(10)
        test = test.head(10)

    #%%
    train.columns = ['text', 'label', 'HADM_ID']
    test.columns = ['text', 'label', 'HADM_ID']

    train_labels = set(itertools.chain.from_iterable(train.label))
    test_labels = set(itertools.chain.from_iterable(test.label))
    all_labels = train_labels.union(test_labels)

    #%%
    from sklearn.preprocessing import MultiLabelBinarizer

    mlb = MultiLabelBinarizer()
    mlb.fit([list(all_labels)])

    train_text = train['text']
    temp_text = test['text']
    train_labels = train['label']
    temp_labels = test['label']
    # train_labels = train['text']
    # temp_labels = test['label']


    """# Split train dataset into train, validation and test sets"""

    # we will use temp_text and temp_labels to create validation and test set
    val_text, test_text, val_labels, test_labels = train_test_split(temp_text, temp_labels, 
                                                                    random_state=123, 
                                                                    test_size=0.5)

    #%%
    temp_labels = mlb.transform(temp_labels)
    val_labels = mlb.transform(val_labels)
    test_labels = mlb.transform(test_labels)
    train_labels = mlb.transform(train_labels)
    #%%
    """# Import BERT Model and BERT Tokenizer"""
    # import BERT-base pretrained model
    bert = AutoModel.from_pretrained('bert-base-uncased')

    # Load the BERT tokenizer
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')
    #%%
    """# Tokenization"""

    # get length of all the messages in the train set
    seq_len = [len(i.split()) for i in train_text]

    pd.Series(seq_len).hist(bins = 30)

    max_seq_len = MAX_SEQ_LEN

    # tokenize and encode sequences in the training set
    tokens_train = tokenizer.batch_encode_plus(
        train_text.tolist(),
        max_length = max_seq_len,
        pad_to_max_length=True,
        truncation=True,
        return_token_type_ids=False
    )

    # tokenize and encode sequences in the validation set
    tokens_val = tokenizer.batch_encode_plus(
        val_text.tolist(),
        max_length = max_seq_len,
        pad_to_max_length=True,
        truncation=True,
        return_token_type_ids=False
    )

    # tokenize and encode sequences in the test set
    tokens_test = tokenizer.batch_encode_plus(
        test_text.tolist(),
        max_length = max_seq_len,
        pad_to_max_length=True,
        truncation=True,
        return_token_type_ids=False
    )
    #%%
    """# Convert Integer Sequences to Tensors"""

    # for train set
    train_seq = torch.tensor(tokens_train['input_ids'])
    train_mask = torch.tensor(tokens_train['attention_mask'])
    train_y = torch.tensor(train_labels.tolist())

    # for validation set
    val_seq = torch.tensor(tokens_val['input_ids'])
    val_mask = torch.tensor(tokens_val['attention_mask'])
    val_y = torch.tensor(val_labels.tolist())

    # for test set
    test_seq = torch.tensor(tokens_test['input_ids'])
    test_mask = torch.tensor(tokens_test['attention_mask'])
    test_y = torch.tensor(test_labels.tolist())
    #%%
    """# Create DataLoaders"""

    from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

    #define a batch size
    batch_size = 32

    # wrap tensors
    train_data = TensorDataset(train_seq, train_mask, train_y)

    # sampler for sampling the data during training
    train_sampler = RandomSampler(train_data)

    # dataLoader for train set
    train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

    # wrap tensors
    val_data = TensorDataset(val_seq, val_mask, val_y)

    # sampler for sampling the data during training
    val_sampler = SequentialSampler(val_data)

    # dataLoader for validation set
    val_dataloader = DataLoader(val_data, sampler = val_sampler, batch_size=batch_size)
    #%%
    """# Freeze BERT Parameters"""

    # freeze all the parameters
    for param in bert.parameters():
        param.requires_grad = False
    #%%
    """# Define Model Architecture"""

    class BERT_Arch(nn.Module):

        def __init__(self, bert):
        
            super(BERT_Arch, self).__init__()

            self.bert = bert 
            # self.bert = nn.DataParallel(self.bert)
            
            # dropout layer
            self.dropout = nn.Dropout(0.1)
            
            # relu activation function
            self.relu =  nn.ReLU()

            # dense layer 1
            self.fc1 = nn.Linear(768,512)
            
            # dense layer 2 (Output layer)
            self.fc2 = nn.Linear(512,len(all_labels))

            #softmax activation function
            self.softmax = nn.LogSoftmax(dim=1)

        #define the forward pass
        def forward(self, sent_id, mask):

            #pass the inputs to the model  
            _, cls_hs = self.bert(sent_id, attention_mask=mask, return_dict=False)
            
            x = self.fc1(cls_hs)

            x = self.relu(x)

            x = self.dropout(x)

            # output layer
            x = self.fc2(x)
            
            # apply softmax activation
            x = self.softmax(x)

            return x

    # pass the pre-trained BERT to our define architecture
    model = BERT_Arch(bert)

    # push the model to GPU
    model = model.to(device)

    # optimizer from hugging face transformers
    from transformers import AdamW

    # define the optimizer
    optimizer = AdamW(model.parameters(), lr = 2e-3)
    #%%
    """# Find Class Weights"""

    # from sklearn.utils.class_weight import compute_class_weight

    # #compute the class weights
    # class_wts = compute_class_weight('balanced', np.unique(train_labels), train_labels)

    # print(class_wts)

    # # convert class weights to tensor
    # weights= torch.tensor(class_wts,dtype=torch.float)
    # weights = weights.to(device)

    # loss function
    # cross_entropy  = nn.NLLLoss(weight=weights) 
    # cross_entropy  = nn.NLLLoss() 
    cross_entropy=nn.BCEWithLogitsLoss()

    # number of training epochs
    epochs = 3
    #%%
    """# Fine-Tune BERT"""

    # function to train the model
    def train():
        
        model.train()

        total_loss, total_accuracy = 0, 0
        
        # empty list to save model predictions
        total_preds=[]
        
        # iterate over batches
        for step,batch in enumerate(train_dataloader):
            
            # progress update after every 50 batches.
            if step % 50 == 0 and not step == 0:
                print('  Batch {:>5,}  of  {:>5,}.'.format(step, len(train_dataloader)))

            # push the batch to gpu
            batch = [r.to(device) for r in batch]
        
            sent_id, mask, labels = batch

            # clear previously calculated gradients 
            model.zero_grad()        

            # get model predictions for the current batch
            preds = model(sent_id, mask)

            # compute the loss between actual and predicted values
            # I"M WORRIED THIS COPIES MAKE SURE #TODO 
            loss = cross_entropy(preds, labels.type_as(preds))

            # add on to the total loss
            total_loss = total_loss + loss.item()

            # backward pass to calculate the gradients
            loss.backward()

            # clip the the gradients to 1.0. It helps in preventing the exploding gradient problem
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

            # update parameters
            optimizer.step()

            # model predictions are stored on GPU. So, push it to CPU
            preds=preds.detach().cpu().numpy()

            # append the model predictions
            total_preds.append(preds)

        # compute the training loss of the epoch
        avg_loss = total_loss / len(train_dataloader)
        
        # predictions are in the form of (no. of batches, size of batch, no. of classes).
        # reshape the predictions in form of (number of samples, no. of classes)
        total_preds  = np.concatenate(total_preds, axis=0)

        #returns the loss and predictions
        return avg_loss, total_preds

    # function for evaluating the model
    def evaluate():
    
        print("\nEvaluating...")
        
        # deactivate dropout layers
        model.eval()

        total_loss, total_accuracy = 0, 0
        
        # empty list to save the model predictions
        total_preds = []

        # iterate over batches
        for step,batch in enumerate(val_dataloader):
            
            # Progress update every 50 batches.
            if step % 50 == 0 and not step == 0:
                
                # Calculate elapsed time in minutes.
                # elapsed = format_time(time.time() - t0)
                        
                # Report progress.
                print('  Batch {:>5,}  of  {:>5,}.'.format(step, len(val_dataloader)))

            # push the batch to gpu
            batch = [t.to(device) for t in batch]

            sent_id, mask, labels = batch

            # deactivate autograd
            with torch.no_grad():
                
                # model predictions
                preds = model(sent_id, mask)

            # compute the validation loss between actual and predicted values
            loss = cross_entropy(preds,labels.type_as(preds))

            total_loss = total_loss + loss.item()

            preds = preds.detach().cpu().numpy()

            total_preds.append(preds)

        # compute the validation loss of the epoch
        avg_loss = total_loss / len(val_dataloader) 

        # reshape the predictions in form of (number of samples, no. of classes)
        total_preds  = np.concatenate(total_preds, axis=0)

        return avg_loss, total_preds
    #%%
    """# Start Model Training"""

    # set initial loss to infinite
    best_valid_loss = float('inf')

    # empty lists to store training and validation loss of each epoch
    train_losses=[]
    valid_losses=[]

    #for each epoch
    for epoch in range(epochs):
        
        print('\n Epoch {:} / {:}'.format(epoch + 1, epochs))
        
        #train model
        train_loss, _ = train()
        
        #evaluate model
        valid_loss, _ = evaluate()
        
        #save the best model
        if valid_loss < best_valid_loss:
            best_valid_loss = valid_loss
            torch.save(model.state_dict(), 'saved_weights.pt')
        
        # append training and validation loss
        train_losses.append(train_loss)
        valid_losses.append(valid_loss)
        
        print(f'\nTraining Loss: {train_loss:.3f}')
        print(f'Validation Loss: {valid_loss:.3f}')
    #%%
    """# Load Saved Model"""

    #load weights of best model
    path = 'saved_weights.pt'
    model.load_state_dict(torch.load(path))

    with torch.no_grad():
        preds = model(test_seq.to(device), test_mask.to(device))
        preds = preds.detach().cpu().numpy()

    preds = np.argmax(preds, axis = 1) 
    test_y = np.argmax(test_y, axis=1)
    print(classification_report(test_y, preds))



    return model
    #%%


def convertBERT(item):

    tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased')

    max_seq_len = MAX_SEQ_LEN

    encoded_toks = tokenizer.batch_encode_plus(
            [item],
            max_length = max_seq_len,
            pad_to_max_length=True,
            truncation=True,
            return_token_type_ids=False
        )
    tokens = torch.tensor(encoded_toks['input_ids'])
    masked_item = torch.tensor(encoded_toks['attention_mask'])
    return tokens, masked_item

