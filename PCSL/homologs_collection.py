#-*-coding:utf-8 -*-


from prody import parsePDB
from prody import blastPDB
from prody import writePDB
import requests
import os
import glob



seqid = 40 # seqid for the minimum sequence identity for including sequences 
hitlist_size=3000 # Number of maximum sequences to be collected
expect=1e-3 # E-value for BLAST
ref_pdb_id="3TGI"
ref_chain="E"
ref_sequence='''IVGGYTCQENSVPYQVSLNSGYHFCGGSLINDQWVVSAAHCYK
             SRIQVRLGEHNINVLEGNEQFVNAAKIIKHPNFDRKTLNNDIMLIK
             LSSPVKLNARVATVALPSSCAPAGTQCLISGWGNTLSSGVNEPDLL
             QCLDAPLLPQADCEASYPGKITDNMVCVGFLEGGKDSCQGDSGGPV
             VCNGELQGIVSWGYGCALPDNPGVYTKVCNYVDWIQDTIAAN'''
             
str_folder="pdb_store/"
log="str_collection_log.txt"
fasta_ref_file="ref.fasta"
fasta_file="homo.fasta"


isExist = os.path.exists(str_folder)
if not isExist:
    os.makedirs(str_folder)

ref_sequence_2=ref_sequence.replace(" ","").replace("\n","")



print("Obtaining the reference structure")
print("-----------------------------------------")
pdb_chain_tmp=parsePDB(ref_pdb_id, chain=ref_chain)
pdb_chain=pdb_chain_tmp.select('not hetero')
writePDB(str_folder+ref_pdb_id.lower()+"_"+ref_chain+".pdb", pdb_chain)
os.system("rm "+ref_pdb_id.lower()+"*")




print("Do BLAST searching against the PDB")
print("-----------------------------------------")
blast_record = blastPDB(ref_sequence, hitlist_size=hitlist_size, expect=expect)
print(blast_record.isSuccess)
while not blast_record.isSuccess:
    blast_record.fetch()


print("Write out all collected sequences from PDB database:")
print("-----------------------------------------")
pdb_hits = []
for key, item in blast_record.getHits(percent_identity=seqid).items():
    pdb_hits.append( key+"_"+item['chain_id'] )




print("Start to filter structures that are not from Xray...")
print("Number of %i structures is being scanned:" %len(pdb_hits) )
print("-----------------------------------------")
pdb_hits_xray=[]
for pdb_hit in pdb_hits:    

    print(pdb_hit)

    pdb_hit_sp=pdb_hit.split("_")

    pdb_id = pdb_hit_sp[0]
    pdb_ch = pdb_hit_sp[1]    
    all_info = get_info(pdb_id)

    if "X-RAY" in all_info['exptl'][0]['method']:
        pdb_hits_xray.append(pdb_id+"_"+pdb_ch)    
    elif "NMR" in all_info['exptl'][0]['method']:
        continue 




print("Obtain strucures and extract the sequnece from the download PDB file")
print("-----------------------------------------")
sequence_store=dict()
dumped_store=[]
for pdb_hit_id, pdb_hit in enumerate(pdb_hits_xray):

    print( "%i/%i is being processed" %( (pdb_hit_id+1), len(pdb_hits_xray) ) )

    pdb_hit_sp=pdb_hit.split("_")

    pdb_id = pdb_hit_sp[0]
    pdb_ch = pdb_hit_sp[1]      


    ref_prot_tmp = parsePDB(pdb_id, chain=pdb_ch)
    if not (not ref_prot_tmp) :
        ref_prot=ref_prot_tmp.select('not hetero')
        ref_hv = ref_prot.getHierView()[pdb_ch]
        sequence = ref_hv.getSequence()
    elif not ref_prot_tmp:
        os.system("rm "+pdb_id+"*")
        dumped_store.append(pdb_id+"_"+pdb_ch)
        continue

    
    store_flag=True
    for aa in sequence: 
        if aa not in 'ACDEFGHIKLMNPQRSTVWY':
            store_flag=False
            break
    r_up=1.2; r_bot=0.8;
    if ( len(sequence) > r_up*len(ref_sequence_2)  ) or \
       ( r_bot*len(ref_sequence_2) > len(sequence) ):
        store_flag=False
    text_files = glob.glob(pdb_id+"*")[0];
    if "pdb.gz" not in text_files:
        store_flag=False
     
     
    if store_flag==True:
        str_name=pdb_id+"_"+pdb_ch
        sequence_store[str_name]=sequence
        writePDB(str_folder+str_name+".pdb", ref_prot)
        os.system("rm "+pdb_id+"*")            
    elif store_flag==False:
        os.system("rm "+text_files)
        dumped_store.append(pdb_id+"_"+pdb_ch)




print("Check consistency")
print("-----------------------------------------")
files_and_directories = os.listdir(str_folder)
if (len(sequence_store)+1) != len(files_and_directories):
    print("The something wrong!!")




print("Output results")
print("-----------------------------------------")
with open(log, 'a') as f:
    f.write("Number of sequences used to do further analysis:" )
    f.write(str(len(sequence_store)+1)+"\n")
    f.write("-----------------\n")


with open(log, 'a') as f:
    f.write("PDB ID (Chain):\n")
with open(log, 'a') as f:
    f.write(ref_pdb_id.lower()+" ("+ref_chain+")\n")
for item in sequence_store.keys():
    item_sp = item.split("_")
    with open(log, 'a') as f:
        f.write(item_sp[0]+" ("+item_sp[1]+")\n")




with open(fasta_ref_file, 'a') as f:
    f.write(">"+ref_pdb_id.lower()+"_"+ref_chain+".pdb\n")
    f.write(ref_sequence_2+"\n")
for key in sequence_store.keys():
    with open(fasta_file, 'a') as f:
        f.write(">"+key+".pdb\n")
        f.write(sequence_store[key]+"\n")


#------------------------------------------------------------------------------------------------
# End of this code
#------------------------------------------------------------------------------------------------

