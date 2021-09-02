import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ppscore as pps
from dython.nominal import compute_associations

file_path = './GRCh37_20210315_v1.4.0.KSE.clvrvAdded.tab'
output_path = './output'

dpi = 300
fontsize = 20
fig_height = 40
fig_width = 40

features = 'gerp_rs,phastCon46,phyloP46,SIFT_score,SIFT_median,SIFT_prediction,Polyphen-2.HumDiv,Polyphen-2.HumVar,MT_treevote,fathmm-mkl_C.score,fathmm-mkl_NC.score,fathmm-xf_C.score,fathmm-xf_NC.score,CADD,CADD_phred,PrimateAI,mcap_sensitivityv1.4,SpliceAI_DS_AG,SpliceAI_DS_AL,SpliceAI_DS_DG,SpliceAI_DS_DL,Ada_score,AF_HC'.split(',')
features.append('Clinsig_model')

def cm_to_inch(value):
    return value/2.54

def process(df):
    fill_columns = 'SpliceAI_DS_AG,SpliceAI_DS_AL,SpliceAI_DS_DG,SpliceAI_DS_DL,Ada_score,AF_HC'.split(',')
    values = {x:0 for x in fill_columns}
    df.fillna(values,inplace=True)
    df.columns = df.columns.str.replace(' ', '')


def calculate_ppscore_matrix(df,file_name):
    filename = os.path.join(output_path, file_name+'_'+'pps.png')
    if os.path.isfile(filename) == False:
        matrix_df = pps.matrix(df, sample=None)[['x', 'y', 'ppscore']].pivot(columns='x', index='y', values='ppscore')
        matrix_df = matrix_df[features].reindex(features)
        matrix_df.to_csv(os.path.join(output_path, file_name+'_'+'pps.csv'),index=False)

        plt.figure(figsize=(cm_to_inch(fig_height),cm_to_inch(fig_width))).set_facecolor("w")
        sns.set(font_scale=fontsize-18)
        sns.heatmap(matrix_df, vmin=0, vmax=1, cmap="Blues", linewidths=0.5)#, annot=True)
        plt.xticks(fontsize=fontsize)
        plt.xlabel("Feature",fontsize=fontsize+2)
        plt.yticks(fontsize=fontsize)
        plt.ylabel("Target",fontsize=fontsize+2)
        #plt.title(file_name  + " PPS")
        plt.savefig(filename,bbox_inches='tight',dpi=dpi)
        plt.clf()
        plt.close('all')


def calculate_associations(df,file_name):
    print("Calculate association")
    filename = os.path.join(output_path, file_name+'_'+'associations_theilu.png')
    if os.path.exists(filename)== False:
        try:
            corr = compute_associations(df,clustering=True,theil_u=True,nan_strategy="drop_samples")
            corr = corr[features].reindex(features)
            corr.to_csv(os.path.join(output_path, file_name+'_'+'associations_replacenan0_theilu.csv'),index=False)
            plt.figure(figsize=(cm_to_inch(fig_height),cm_to_inch(fig_width))).set_facecolor("w")
            sns.set(font_scale=fontsize-18)
            sns.heatmap(corr, vmin=-1, vmax=1, cmap="Blues", linewidths=0.5)
            plt.xticks(fontsize=fontsize)
            plt.yticks(fontsize=fontsize)
            plt.savefig(filename,bbox_inches='tight',dpi=dpi)
            plt.clf()
            plt.close('all')
        except Exception as e:
            print(e)

    filename = os.path.join(output_path, file_name+'_'+'associations_cramers_v.png')
    if os.path.exists(filename)== False:
        corr = compute_associations(df,clustering=True,theil_u=False, nan_strategy="drop_samples")
        corr = corr[features].reindex(features)
        corr.to_csv(os.path.join(output_path, file_name+'_'+'associations_replacenan0_cramers_v.csv'),index=False)
        plt.figure(figsize=(cm_to_inch(fig_height),cm_to_inch(fig_width))).set_facecolor("w")
        sns.set(font_scale=fontsize-18)
        sns.heatmap(corr, vmin=-1, vmax=1, cmap="Blues", linewidths=0.5)
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.savefig(filename,bbox_inches='tight',dpi=dpi)
        plt.clf()
        plt.close('all')



def main():
    df = pd.read_csv(file_path,delimiter='\t')
    process(df)
    df_snp = df[df['is_snp']==1]
    df_indel = df[df['is_snp']==0]
    df_indel.drop(['var','id','is_snp'],axis=1,inplace=True)
    df_snp.drop(['var','id','is_snp'],axis=1,inplace=True)
    calculate_ppscore_matrix(df_indel.drop(['clvrv.stars'],axis=1),'GRCh37_20210315_v1.4.0.KSE.clvrvAdded'+'_indel_authorfill')
    calculate_ppscore_matrix(df_snp.drop(['clvrv.stars'],axis=1),'GRCh37_20210315_v1.4.0.KSE.clvrvAdded'+'_snp_authorfill')
    calculate_associations(df_indel.drop(['clvrv.stars'],axis=1),'GRCh37_20210315_v1.4.0.KSE.clvrvAdded'+'_indel_authorfill')
    calculate_associations(df_snp.drop(['clvrv.stars'],axis=1),'GRCh37_20210315_v1.4.0.KSE.clvrvAdded'+'_snp_authorfill')

if __name__ =='__main__':
    main()