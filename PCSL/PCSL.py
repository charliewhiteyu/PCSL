import pickle




PCSL_Output="PCSL_Output/"
MD_chat_MD_res_file="MD_chat_MD_res.db"
homo_chat_homo_res_file="homo_chat_homo_res.db"
MD_chat_homo_res_file="MD_chat_homo_res.db"
MD_chat_Xray_res_file="MD_chat_Xray_res.db"




# Load spring constant kij
MD_MD_db = pickle.load(open(PCSL_Output+MD_chat_MD_res_file,'rb'))
MD_MD_rec = MD_MD_db['BF_rec']
MD_MD_kij = MD_MD_rec['ForceConsMat']

homo_homo_db = pickle.load(open(PCSL_Output+homo_chat_homo_res_file,'rb'))
homo_homo_rec = homo_homo_db['BF_rec']
homo_homo_kij = homo_homo_rec['ForceConsMat']

MD_homo_db = pickle.load(open(PCSL_Output+MD_chat_homo_res_file,'rb'))
MD_homo_rec = MD_homo_db['BF_rec']
MD_homo_kij = MD_homo_rec['ForceConsMat']

MD_Xray_db = pickle.load(open(PCSL_Output+MD_chat_Xray_res_file,'rb'))
MD_Xray_rec = MD_Xray_db['BF_rec']
MD_Xray_kij = MD_Xray_rec['ForceConsMat']





