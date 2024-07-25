#!/bin/python

from Bio import SeqIO
import pytest
from pathlib import Path
import subprocess


@pytest.fixture
def setup_fastas():
    long_seq = 'MGDYGENMPISPDAVQLTFAQKAGASLFPSLTDGILLDENKLAEQRSASALEQTKISLSLRPETSIANLTAFCARHKCTLLGVLNVAWALVLSTYTDTELAQVLFVRYKDDTPYIGLSEIVIDGGETILQVLALVEQHLSTGMPVPSTTTITDLQNWTASDGHPVFNSVVLFSDSTTAERKEAGDYISLHARVAGDQLCINLQAPSHLLPAAQAQNCAATLSHVLGEIVQNPDLPLSDIGLMSPQGLDQISKWNHTAPAVVSRCVHELVDETAETQPDTIAIDGADGTMTYGELRSYSNQLAHYLTQQGVGPEFTVPLFFEKSKWAIVAMLGVVKAGGTIVNLDAKQPKERLRGLLAQLQASIVLTSVQNADLWKDERPVFVISEEFLHQLTTVAEAPKVAVTPQNALYIIFTSGSTGTPKGCVVEHESFLTAAAQHIKAGNILSSSRILQMTPYTFDVSMLEIFTTLTIGACICFCNDSEAARGVAHIINFLKISWTFMTPSLVRLVDPSSVPTLKTLALGGEGLARIDVTTWADKLHLINGYGPSECSVAATMHGPLSLNSDPANIGLGCGAICWVVDRNDHDRLVPIGAVGELVIQGPIVARGYLNEPGKTAAVFLDKVPAFAATLPRAPPAFRLYKTGDLVRQNSDGTLTFIGRKDRQVKLNGQRLELGEIEQRLSENSLVRHALVLLPKQGPCKGRLVAVLSLQDYPYSGEPDANVHQLSTEESRAARALLPAISAQLATHVPGYMVPTFWVVLAALPFTTSGKVHGVAMTQWLHAMSEETYNEIADVSEEIPTVDLSSEIELSLQKIFAEEMGIPITELKMNRSFIALGGDSLKAMKVVARCRQQELKLSVADVLRASSLIALAKCVEQASSGSNSVPEESKKEAFHSTPEQRIAALAESLLTAIGLAREQLEDAYGCSPMQDGILLSQVKFPGTYEIRRVLHVQSTHDVDTTVSRLQTAWQMVVDRHQALRTVFVEVEGRFQQLVLKKVSAYFQICKFSDLEDQEAVINRLKTLPPPSFKPSQPQHRLTICCAGVNEVFLKFEISHALVDGGSTEVILREISAAFDEHSLSGNPARFSDYMDYISNPEAAEISLGYWTEHLKGTQPTIMPMYPADATEKRICSVPVPFNDTAALIQFSEANGVTLANVLQAAWALVLRTYTDTSDICFGYIAAGRDVPVEGIDRAVGAFINMLVCRVRLEEQPTILDAILGMQEQYFDALPHQHTSLAQIQHRLDLSGMPLFNSIISVQNDVSDQPYAQSLAFKSVEEDDPTDFDLCVAIHVGNDNVRIDIGYWSSLLTKGDASNLAYTFSSAISAILRDASVPAVSVDLFSEYDRSQVFAWNQDEPTSKPGVVHDYVYAKVQEQPDAQAVCAWDGEYTYRELGGLSEKLAHHLAELGSGPEVLIPHCFSKSKLAAVVMLAIMKSGSACVGLSSSHPRTRVQDIIENCAATIAVVAKENIGVVDGLVNRVVVVDEAFLANLPEPSPGAQLPKALPHNPAFVSFTSGSTGKPKGIVLEHESLITSILAHGPEWGVDQSARVLQFSAYAFDASVSDTFTTLVGGGTVCIPHEKDRVDDLVGAINRLGVNWAFLTPRVLSLLTPELVPGLKTVVLGGEAISKEDIARWTDKICIRIVYGPTECTIYSMGSEPLNSQSDPLCLGHAVGTRLWITHPDDINKLMPVGCTGELIIEGPLVTRGYLNEPAKTEAAYFEDPVWLPKKESGEPRRFYKTSDLVRYYPDGQLRFIGRKDTQIKIRGQRVELGEIEHAILESMPGVSHVTVDSVVLPPQTLVAFLRIESLSTGIEPLFVPLDFGMADQLRTLEKNLVDKLPSYMIPSLFIPISHIPMTISGKVDRIALRRAVLSMNERQQKMYALADEVKEEPQTEQEHCLRDLWAVVLGKEPSSVGRQDSFFRLGGDSIGAMKLVAAARRAGYLLSVADIFRHPELIEMAVRLDLSNGAKAAAYAPFSLLQDEQNQRQATLEEAAQQCSVSQDAIEDIYHATPLQEGVFLMSTTHDGAYVAPTAFALPSEFDVRKFQESWQELVNAHPILRTRIVTINAISYQAVLTKNASVIEWETAASLNEYIDRVRASPVAAGRPLCRFALVPNEDSTVFVWTAHHALFDGWTMGLLFDQLAQLFKDGTRPAPATSFAEFVQFTRQMGQDTSRDFWASLCPQEPPAVFPRLPSSTYHPTANTTSYRTISTNLSKNTDFTMAILLRAAWSIVLARYTDAEDILYGLTLSGRDLPVSGIEKVMGPTITTVPMNVHLDGEMLIQDFLQRQHDENVEMMRHQHVGLQAIRRISKATAAATEFTNLFVVQPQATQVSGLTELTQVPTDMTRFDPYALVVECNLGDDQILLEARFDSSILSMDQANHLLGHFDHVLSQLTSFRPDCRLQDIDAFSLEDERQIWKWNAVPAKSEDFCIHDLIAAQADRHPQEIAVDAWDGSFTYKELDNLSTRLSNYLVTNIGIRPESLVPLCFDKSRWTIVVMLAVVKSGGGCVMLNPDHPVSRLEGVITDTGSSVVLASPERVGLFSSHAAKKVVITEALVHSLTLTEQDCLPLPPIQPTNPVFVIFTSGSSGKPKGIVVQHNSVCTVAIQHGEGLGFKGPGLRVLQFASFSFDVSMGEVFLTLAKGGTLCIPTEHDRLNNLADTINRMKITWTFMAPTVAALLDPREVPALKTLVLGGEAVSQSLVDQWATRVNLIDSYGPAECTIWASHAIASATVSPANIGRGVGCRYWIVDPLDYNRLTPIGCVGELLIEGPNVSRGYLNEPEKTKAVFVENPKWLQGKETPLYKFYCTGDLVRYNVDGSLNIAGRKDSQVKFNGQRIELSEIEFHLRAHSEIEAGMVVLPKEGPCKGKLVAVVALTGLQPAALEGDHIELVPRTLKNEAQLRVQQVQDRLGELLPPYMVPSIWVTLYSIPLTASRKINRLPISRWIQSMSDEIYHDVVDITVATVHQPTTQLEKELAQVWSHVLNVSIDAIGLDRSFLSLGGDSITAMQVVSRCRSLDIQVSVQDILQPKSLSGVVARALAAKPTAIHREEQYDTQFELSPIQQLYFEDVVRTNGEGMHHYNQSVLLRVLRPVTPAQLSEAMERVTANHAMLRARFRRDSDGKWTQMAKSPAQGLCSFDSCLVQDRPELFERLNASQRSINIENGPVFVAKYFQIANEDVRLLSLIAHHLVIDAVSWHIIIGQLEQVLQFPDTQLNPARMPFQSWLEEQRKLVESLSKSPIPLQDLPAANLEYWGLANLPLWGNGQEISFTLNEKTTALLLTAANTSLRTEPIDLLLAALQLSFADSFSDREMPSFFVEGHGREPWESSIDLSETIGWFTTFHPIHRRVRKNESIKTTIKRTKDARQSWNDNGFAYFARRHFDVETHEKLRSHRIMEICFNYLGQSQHAEREDAILQEEVLLPEESLENIGDSMGRLAVFDIVAAVSHGRLNVSFFFQNDILHQSKVCQWVKRCESTLQMAVDELTVSETEFCISDFPLLDINYQDLATLTTAVLPSIGISPDAIEDLYPCSPIQEGILISQARQPGTYEVRQLFKVVPREDQPAVDVSRLVAAWQQTVDRHALLRTVFIEAINGSGVFNQLVLRSYPAEVKRLSLDNVAGQEEVAVFVTSQMGPDYRQPAPAHRLTICETPDSVYCQLEVSHALIDGTSMALLVRDLVAAYEGTLLAVPGPLYSTYMKYLSQQSEADALSYWKSQLENVEACHFPALNTMPVSTTGFQSKVIEIDAGGELKKFCEANDLTMSNLFQVGWGLVLRAYTGSSDVCFGYMAAGRDIPVEGIYDAIGPFINLLVCRMHLDEKLSPNDLLQAMQTDYLESLPHQHVSLAAIQHALGQSDVALFNSIMSLQRKPSPGSPPEIELQVVAENDPTEYDVDLNITTGEESGVEIHITYRNSVLTDSQADRLLCNFSHILFALAACANQPLAQLDLSKASPMSLAQAVSREEPVSVQASIPKLISERTEASPTSIAVQCMVDDTILTYYDLDCLTCSLADHLLRLGVCQGDIVLLDFPRSKWALVALLAVLRAGATSLALSSTHDLKDIREALTAQKSAIVLGGERFTAKSVNDGFTHVTVDAAFMTSIKAVTLANTALRDISPSEVALAVKDGEDWALLAHHTISTAASHLGSKAGLTPGARVVQLSTIESTSYLVETLFTLIRGGTVIVPPTDVGVTQSLRLSRANWALLSKDEATSTNATQVPELQTLVVAGDRMPISLQLKWRDVNLIHPRQLNHIHVWVSLMIAPAGCDSLQPCPIPALARTWVRSPFSQTALAPTECKGEVLVDGPLVPRGYVGNSSQSLLRNPVWLPNAVLVCTGVQGRWSNNGVDLEEQSPSRATGNTADILGMEELVKTTLRPTENVLITAIQNEAEDRIVAYFTNSPEGEEPVKLLPLTDALQQRFLEIQAFLKGKVSDDLLPEFCFPVNRIPLAINRQFDRPGLNQLVSMLSDDTLASYRVQAPAIAPRLTSNENLIADLWSEVLHLPDRAKLDPSESFFRLGGDSIGAMRIIAAARSQGLVLTMNGIFQQPTLAGMAKEIRLLAPHEDRPVEPFSLLPPAVDSTTLISEAAAKCHVDASAVEDIYPCTPLQEGFMVLTSQDSAAYYVQEVFKMPESVDLARFREAWSTVVSRSTILRTRIISVLDGFFQVLLREPVYWQSGVDLETYLRDDMKKAMSYGQPLSRFAVVEAPRQRYFIWTAHHAVYDGLTMATLAKQVSAEYNQEMALPEIPYNRFIDYIQGVSPAAATEFWAAQCAVPATTFPMLPSRDQQPFPDQFMSHSIPVKIKPSTITLSTVLRAAWAMVLAQLTDSEHVNFGVTLSGRNASMVGINQVLGPTIATVPVQIHVPQNLAPQKFLQAVHKQAIDMIPFEHTGLQNIRKMGEQCREAVNFQNLLIIQPGTSPVDDSDFLGLTPVQQDGDQRDPYPLTIECNLLDDSIELKAQFDSRFIPSGEMSRILKQYARTVERFQTLDEAVSEDDGEETFDASNGLSDDDVEQILAWNSDRPVLIEKCLHEVFEEQARLRPDAPAVSSYDVQLTYRELKDLIDRLAMQLQSMGIKPEMKIPLCFSKSSWTIVAMFAVFKVGGVACMLNPEHPSNRIHLLLRDLDAEYALCDQASLSMMASLLSPANVLSVDGTYLRSLPPSSTLSYQVQPGNAALVVYTSGSTGKPKGSILEHRSIVTGLTAHCTAMGIGPESRVFQFAAYTFDVCFEEIFGALMLGGCVCVPSEDERMNSLADAMARYRVTWTELTPTVASLLLPSSIPTLKSLALSGESVTKEVVQRWGDAVQLINTYGPSECCVSSTCNVETAIVRDPSNIGRGLGCTTWIVNPDDVNVLAPIGATGELLIEGPIVARGYLNEPEKTAAAFISAPAWWPESWSCGRIYRTGDLVKYNADGTIKFIGRRDTQVKLHGQRIELGEIEHRIRGAFTDSSHQVAVEVLAPNTRGGLKILTAFICESSQVSEESDGLLLDLDDGMSHRFLELQARLMGELPRHMIPQLFIPIKHMPLSPSRKIERKVLRALGNALQADQLSAYALTQTARTAPSTATEKALSDIWTEVLGTSPSGTEDHFFHLGGDSIAAMKAVAAATKIGLSLSVAEIMQFPTLRAMAAAIDSAVDNEDVDEEVLECFSLIPPSQLSDVVAEAVAQCAVPAEDIEDIYPCTPSQEALMALTARDEAAYVSRAVYRLPLNLDVARYREAFEQLTQRQAIMRTRIIYSSVAARSYQVVVQGSLIWHTDESLAAYVAADKLTPMRHGDALMRFALLEGSTEDPRPCLVYTAHHAVYDGWSEASMFEEAETIYRQGLNALPAVAPYKKFIHYLSTIDSAASEEFWRSHLEGDLPAPFPPGSPDATTSLLTSRPNRSQFHSIRLPSLHSLPYTLPTVLKAAWALLLSRYTTSDDVIFGHVLSGRTVPLRGVSDMMGPTISTVPVRVRLNPDESVEALLRRIQTQAQDMTAFEQIGMQNIRRLLASPEAVDVGHLFFIQPPMEAGTTDLALEPVADADFDFDTYPLIVECQLDSDNGATLSVKYNDARISQTSMTWLLQHFENLVGQLYQSPRTAAISTLELTGSSDIQTLRGWIGAPVTPVQNTVHDEFRSRAFAHPERCAVQAWDGTLSYRELDVLSSQYARKLCSLGLSVGQAVGLIFDKSCWAAVAMLAVLKAGGCCVQLDAKHPSTRLVEIVEDTSLHHILAASSHVSLAKSLPVDHAIEVNHLSNSALQTSLDKASRLPVVDVMSPAYMTFTSGSTGKPKSVVINHQAIHTSISAFSSALCMNFKSRVLQFAAYTFDISYAETFAPLTLGATLCVLSEQDRLNDLAGAISRLGANWACLTPTVASLVEPASIKGLLKTLVLSGEAPTEENLRIWSGKVPNLINAYGPSEASVWCAAGSFKRPDDSCTNIGRPVGCHLVIAEPSDINRLTPVGCVGELIVCGPILSSGYLNNEKANSAAFHQNIAWREKLGIHAGCSRVYRTGDLARFLPDGSIEYLGRADTQVKIYGRRIEPREIEHHIHLELGDYLNMVDSVTLANRKNQKMLVAFIYQESAFVPNLDLATLARDLNPEIQSTLASLQAALRSRLPHWMIPTLFIPLRFMPTNAAGKTDRKLLARAVNLLTDDQLRDFALSGRTEKKPLTTYLQQQLADLWADVLTLDVQSIGADDTFFTLGGDSILAMKMASRARSAQISLSVADIFNYPVLADLASHLQALMPLTPGSETPTSDFHSKMALAPATDLVLLEALAQKAGVDAAAVEAVEHTTDFQDLALVGHLSKSRWMLNWFFFDGPGSGDAERLRKGCHDLVQQFDILRTVFVAHEGRFWQVVLNKLKPSFRVESTADFAGFTQSLYEDGLAQELNLSKPLVEFVLAVHPGGHSHRLLMRLSHAQYDGVSLPTLWDCLQRACHGEALPRISSFTQFLRATKPANLDATRSYWRSLLNGATETRFVAHSKPALRDEAHDRVVHVTRRQVPVVSLRQHGITPATVLRSAWAILLARLSASSDVTFGQTTANRSATTLPDIENVVGPCLNVVPVRASLKPGQTVLEFLLAQQAQQVSGLAHESLGFRQIIRDCTNWPSWTHFSSVVQHQNIEPDRDVPLGPNDADMYKPGFLGADLDLTDVSVLSTPTIDGYVDLDLLTSCKVMSPFAAELLVDQLSELLQLWAVVPLERFKVNERSMTTAMIPLVPADIGVPPVVKNSRRADIQDAWQTCLSKANSVVSLEDGDADFFRLGGDLVQMAQLASELHAKGIGRGVALETLVQHSTLDAMVQILS'
    max_seq_len = 1000
    short_seqs = [long_seq[i*max_seq_len:(i+1)*max_seq_len] for i in range(int(len(long_seq)/max_seq_len) + 1)]
    short_seq_ids = ['test_seq_' + str(i) for i in range(len(short_seqs))]
    #short_fasta_records = [SeqRecord(Seq(t_seq[i]), t_id[i]) for i in range(len(t_seq))]
    #long_fasta_record = SeqRecord(Seq(long_sequence), 'test_seq')
    
    test_dir = Path('test')
    if not test_dir.exists():
        test_dir.mkdir()

    short_AA_file = test_dir / 'short_AA.fasta'
    short_3Di_file = test_dir/ short_AA_file.name.replace('_AA.fasta', '_3Di.fasta')
    long_AA_file = test_dir / 'long_AA.fasta'
    long_3Di_file = test_dir / long_AA_file.name.replace('_AA.fasta', '_3Di.fasta')

    with open(short_AA_file, 'w') as out_file_short:
        for i in range(len(short_seqs)):
            out_file_short.write('>' + short_seq_ids[i] + '\n')
            out_file_short.write(short_seqs[i] + '\n')

        #SeqIO.write(short_fasta_records, out_file_short, 'fasta')

    with open(long_AA_file, 'w') as out_file_long:
        #SeqIO.write(long_fasta_record, out_file_long, 'fasta')
        out_file_long.write('>test_seq\n')
        out_file_short.write(long_seq + '\n')



    
    yield short_AA_file, long_AA_file, short_3Di_file, long_3Di_file

    # clean up
    #short_AA_file.unlink()
    #long_AA_file.unlink()
    #if short_3Di_file.exists():
    #    short_3Di_file.unlink()
    #if long_3Di_file.exists():
    #    long_3Di_file.unlink()

def test_predict_3Di_encoderOnly(setup_fastas):
    fasta_files = setup_fastas
    # f_short_AA, f_long_AA, f_short_3Di, f_long_3Di = *fasta_files

    # ProstT5 predict previously split sequences 
    command = [
        'python', 'scripts/predict_3Di_encoderOnly.py',
        '--input', str(fasta_files[0]),
        '--output', str(fasta_files[2]),
        '--half', '1',
        '--model', '/home/mpjw/eggNOG-3Di/data/prostt5/model/'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    
    # ProstT5 predict long sequence with auto splitting
    command = [
        'python', 'scripts/predict_3Di_encoderOnly.py',
        '--input', str(fasta_files[1]),
        '--output', str(fasta_files[3]),
        '--half', '1',
        '--model', '/home/mpjw/eggNOG-3Di/data/prostt5/model/',
        '--split_long_seqs', '1'
    ]
    result = subprocess.run(command, capture_output=True, text=True)


    assert result.returncode == 0, "Script failed with error: {}".format(result.stderr)

    short_3Di_records = list(SeqIO.parse(fasta_files[2], "fasta"))
    long_3Di_record = list(SeqIO.parse(fasta_files[3], "fasta"))[0]

    assert sum([len(r) for r in short_3Di_records]) == len(long_3Di_record), "3Di sequences did not match in length"
    
    print(str(long_3Di_record.seq))
    for rec in short_3Di_records:
        print(str(rec.seq))
    
    # compute sequence identity
    short_3Di_concat = ''.join([str(r.seq) for r in short_3Di_records])
    print("Sequence identity: {}".format(sum([str(long_3Di_record.seq)[i] == short_3Di_concat[i] for i in range(len(short_3Di_concat))])/len(short_3Di_concat)))
    assert short_3Di_concat == str(long_3Di_record.seq), '3Di sequences did not match in sequence identity'
