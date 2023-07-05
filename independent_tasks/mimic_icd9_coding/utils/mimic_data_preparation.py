
# %% [markdown]
# # Data preparation for automated text classification for ICD 9 diagnosis code assignment from MIMIC Database
#%%
# Data prep code from: https://github.com/IM-APHP/mimic_icd9_code_assignment
# %%
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# %% [markdown]
# Load MIMIC tables NOTEEVENTS and DIAGNOSES_ICD

def run_mimic_prep(train_split=False, mimic_data_path='../data/mimic_data', output_folder ='../data', output_name='mimic_full.csv', code_mincount=1000, return_df=False, verbose=False):
    if code_mincount != 1000:
        rewrite=True
    # %%
    NOTEEVENTS=pd.read_csv(mimic_data_path + 'NOTEEVENTS.csv',dtype={'ROW_ID':np.int32, 'SUBJECT_ID': np.int32,'HADM_ID': np.float64,
                                        'CHARTDATE':str,'STORETIME':str,'CHARTTIME':str,
                                        'STORETIME': str,'CATEGORY': str,'DESCRIPTION':str,'CGID':str,'ISERROR':str,
                                            'TEXT':str}, parse_dates=['CHARTDATE'])
    DIAGNOSES_ICD=pd.read_csv(mimic_data_path + 'DIAGNOSES_ICD.csv',dtype={'ROW_ID':np.int32, 'SUBJECT_ID': np.int32,'HADM_ID': np.int32,
                                                'SEQ_NUM': np.float64, 'ICD9_CODE':str})

    # %% [markdown]
    # ## Explore NOTEEVENTS
    # NOTEEVENTS.groupby('CATEGORY').count()

    # %% [markdown]
    # ## Explore DIAGNOSES_ICD

    # %%
    DIAGNOSES_ICD['ICD9_CODE']=DIAGNOSES_ICD['ICD9_CODE'].str.pad(4,'left','0')
    DIAGNOSES_ICD['ICD9_CHAP']=DIAGNOSES_ICD['ICD9_CODE'].str.slice(0,3)
    # DIAGNOSES_ICD.count()

    ##Explore by the first character
    # DIAGNOSES_ICD.groupby(DIAGNOSES_ICD['ICD9_CODE'].str.slice(0,1))['HADM_ID'].count()

    # %% [markdown]
    # Codes from V,E,U,8,9 can be exclude in a purpose of facturation as they are not take in count for the calculus of hospitalization fees.

    # %%
    # DIAGNOSES_ICD=DIAGNOSES_ICD[~DIAGNOSES_ICD['ICD9_CODE'].str.slice(0,1).isin(['V','E','U','8','9'])]

    # %% [markdown]
    # ## Exploration of diagnoses to choose the perfect y
    # ### Selection of the most frequent codes

    # %%
    a=DIAGNOSES_ICD.groupby('ICD9_CODE')['HADM_ID'].count().sort_values(ascending=False)
    # %% [markdown]
    # Due to dispersion of the distribution and the low frequency of some code, for the machine learning task a selection of the code and their chapter will be made

    # %%
    if verbose:
        print('Nb codes > 1000 occurences= '+str(len(a[a>1000]))+
            '  \nNb codes 1000-100 occurences = ' +str(len(a[(a<1000)&(a>100)]))
            +'  \nNb codes <100 occurences = ' +str(len(a[a<100])) )


    # %%
    a=DIAGNOSES_ICD.groupby('ICD9_CODE')[ 'HADM_ID'].count()
    DIAGNOSES_ICD_freq=DIAGNOSES_ICD[DIAGNOSES_ICD['ICD9_CODE'].isin(a[a>code_mincount].keys())]
    df=DIAGNOSES_ICD_freq.groupby('HADM_ID')['ICD9_CODE'].apply(lambda x: "['%s']" %"','".join(x))
    df=df.apply(lambda x : eval(x))
    DIAGNOSES_ICD_freq=pd.DataFrame(df)
    DIAGNOSES_ICD_freq['HADM_ID']=df.keys()
    # DIAGNOSES_ICD_freq.head()

    # %% [markdown]
    # Select the visits with the most frequent codes

    # %%
    if verbose:
        print('Nb of stays selected = '+str(DIAGNOSES_ICD_freq['HADM_ID'].nunique())+
            '  \nNb of different codes = ' +str(len(a[a>code_mincount])))

    # %% [markdown]
    # ### Selection of the most frequent chapters

    # %%
    a=DIAGNOSES_ICD.groupby('ICD9_CHAP')[ 'HADM_ID'].count().sort_values(ascending=False)


    # %%
    if verbose:
        print('Nb chapter codes > {} occurences= '.format(code_mincount)+str(len(a[a>code_mincount]))+
            '  \nNb chapter codes 1000-100 occurences = ' +str(len(a[(a<1000)&(a>100)]))
            +'  \nNb chapter codes <100 occurences = ' +str(len(a[a<100])) )


    # %%
    #a=DIAGNOSES_ICD[~DIAGNOSES_ICD['ICD9_CODE'].isin(DIAGNOSES_ICD_freq['ICD9_CODE'])].groupby('ICD9_CHAP')[ 'HADM_ID'].count()
    a=DIAGNOSES_ICD.groupby('ICD9_CHAP')['HADM_ID'].count()
    DIAGNOSES_ICD_chap_freq=DIAGNOSES_ICD[DIAGNOSES_ICD['ICD9_CHAP'].isin(a[a>code_mincount].keys())]

    # %% [markdown]
    # Selection of stays with the most frequent codes

    # %%
    if verbose:
        print('Number of stays selected = '+str(DIAGNOSES_ICD_chap_freq['HADM_ID'].nunique())+
            '  \nNb of different chapters = ' +str(DIAGNOSES_ICD_chap_freq['ICD9_CHAP'].nunique()))


    # %%
    # DIAGNOSES_ICD_chap_freq.groupby('ICD9_CHAP')['HADM_ID'].count().sort_values(ascending=False).plot(kind='bar',figsize= (17, 10))


    # %%
    df=DIAGNOSES_ICD_chap_freq.groupby('HADM_ID')['ICD9_CHAP'].apply(lambda x: "['%s']" %"','".join(x))
    df=df.apply(lambda x : eval(x))
    DIAGNOSES_ICD_chap_freq=pd.DataFrame(df)
    DIAGNOSES_ICD_chap_freq['HADM_ID']=df.keys()
    # DIAGNOSES_ICD_chap_freq.head()

    # %% [markdown]
    # ### Conclusion : we will focus on ICD chapters.
    # %% [markdown]
    # ## Build the final X and y
    # %% [markdown]
    # Merge of the most important notes to make a single text by hospitalisation.
    # 
    # In the first place we will focus on discharge summaries.

    # %%
    selected_doc=['Discharge summary']
    df=NOTEEVENTS[NOTEEVENTS['CATEGORY'].isin(selected_doc)].groupby('HADM_ID')['TEXT'].apply(lambda x: "{%s}" % ', '.join(x))
    df2=pd.DataFrame(df)
    df2.index.names = ['HADM_ID_INDEX']
    df2['HADM_ID']=df.keys()


    # %%
    DIAGNOSES_ICD_chap_freq.index.names = ['HADM_ID_INDEX']
    DIAGNOSES_ICD_chap_freq.head()

    # %% [markdown]
    # Create one dataframe for selected diagnoses with merge with texts on HADM_ID, and the other one for selected chapters, and concatenate them to have the final dataframe that will be use for prediction

    # %%
    NOTE_DIAGNOSES=pd.merge(df2,DIAGNOSES_ICD_chap_freq[['HADM_ID','ICD9_CHAP']],on='HADM_ID')
    # NOTE_DIAGNOSES=pd.merge(df2,DIAGNOSES_ICD_chap_freq[['HADM_ID','ICD9_CHAP']], left_index=True, right_on='HADM_ID')
    # new = pd.join(df2)

    # %%
    from sklearn import model_selection
    import os
    NOTE_DIAGNOSES.rename(columns={"ICD9_CHAP": "TARGET"}, inplace=True)
    # if not os.path.exists(output_folder):
        # os.mkdir(output_folder)
    if train_split:
        train, test = model_selection.train_test_split(NOTE_DIAGNOSES[['TEXT','TARGET', 'HADM_ID']],test_size=0.2, random_state=123)
        print('Size of train: '+ str(train.shape[0])+' \nSize of test: '+str(test.shape[0]) )
        train.to_csv(output_folder + 'train.csv',index=False)
        test.to_csv(output_folder + 'test.csv',index=False)
        if return_df:
            return train, test
    else:
        out_df = NOTE_DIAGNOSES[['TEXT', 'TARGET', 'HADM_ID']]

        out_df.to_csv(output_folder + output_name,index=False)
        if return_df:
            return out_df
