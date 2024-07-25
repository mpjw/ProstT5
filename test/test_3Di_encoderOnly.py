#!/bin/python

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import pytest
from pathlib import Path
import subprocess


@pytest.fixture
def setup_fastas():
    long_sequence = 'MGDYGENMPISPDAVQLTFAQKAGASLFPSLTDGILLDENKLAEQRSASALEQTKISLSLRPETSIANLTAFCARHKCTLLGVLNVAWALVLSTYTDTELAQVLFVRYKDDTPYIGLSEIVIDGGETILQVLALVEQHLSTGMPVPSTTTITDLQNWTASDGHPVFNSVVLFSDSTTAERKEAGDYISLHARVAGDQLCINLQAPSHLLPAAQAQNCAATLSHVLGEIVQNPDLPLSDIGLMSPQGLDQISKWNHTAPAVVSRCVHELVDETAETQPDTIAIDGADGTMTYGELRSYSNQLAHYLTQQGVGPEFTVPLFFEKSKWAIVAMLGVVKAGGTIVNLDAKQPKERLRGLLAQLQASIVLTSVQNADLWKDERPVFVISEEFLHQLTTVAEAPKVAVTPQNALYIIFTSGSTGTPKGCVVEHESFLTAAAQHIKAGNILSSSRILQMTPYTFDVSMLEIFTTLTIGACICFCNDSEAARGVAHIINFLKISWTFMTPSLVRLVDPSSVPTLKTLALGGEGLARIDVTTWADKLHLINGYGPSECSVAATMHGPLSLNSDPANIGLGCGAICWVVDRNDHDRLVPIGAVGELVIQGPIVARGYLNEPGKTAAVFLDKVPAFAATLPRAPPAFRLYKTGDLVRQNSDGTLTFIGRKDRQVKLNGQRLELGEIEQRLSENSLVRHALVLLPKQGPCKGRLVAVLSLQDYPYSGEPDANVHQLSTEESRAARALLPAISAQLATHVPGYMVPTFWVVLAALPFTTSGKVHGVAMTQWLHAMSEETYNEIADVSEEIPTVDLSSEIELSLQKIFAEEMGIPITELKMNRSFIALGGDSLKAMKVVARCRQQELKLSVADVLRASSLIALAKCVEQASSGSNSVPEESKKEAFHSTPEQRIAALAESLLTAIGLAREQLEDAYGCSPMQDGILLSQVKFPGTYEIRRVLHVQSTHDVDTTVSRLQTAWQMVVDRHQALRTVFVEVEGRFQQLVLKKVSAYFQICKFSDLEDQEAVINRLKTLPPPSFKPSQPQHRLTICCAGVNEVFLKFEISHALVDGGSTEVILREISAAFDEHSLSGNPARFSDYMDYISNPEAAEISLGYWTEHLKGTQPTIMPMYPADATEKRICSVPVPFNDTAALIQFSEANGVTLANVLQAAWALVLRTYTDTSDICFGYIAAGRDVPVEGIDRAVGAFINMLVCRVRLEEQPTILDAILGMQEQYFDALPHQHTSLAQIQHRLDLSGMPLFNSIISVQNDVSDQPYAQSLAFKSVEEDDPTDFDLCVAIHVGNDNVRIDIGYWSSLLTKGDASNLAYTFSSAISAILRDASVPAVSVDLFSEYDRSQVFAWNQDEPTSKPGVVHDYVYAKVQEQPDAQAVCAWDGEYTYRELGGLSEKLAHHLAELGSGPEVLIPHCFSKSKLAAVVMLAIMKSGSACVGLSSSHPRTRVQDIIENCAATIAVVAKENIGVVDGLVNRVVVVDEAFLANLPEPSPGAQLPKALPHNPAFVSFTSGSTGKPKGIVLEHESLITSILAHGPEWGVDQSARVLQFSAYAFDASVSDTFTTLVGGGTVCIPHEKDRVDDLVGAINRLGVNWAFLTPRVLSLLTPELVPGLKTVVLGGEAISKEDIARWTDKICIRIVYGPTECTIYSMGSEPLNSQSDPLCLGHAVGTRLWITHPDDINKLMPVGCTGELIIEGPLVTRGYLNEPAKTEAAYFEDPVWLPKKESGEPRRFYKTSDLVRYYPDGQLRFIGRKDTQIKIRGQRVELGEIEHAILESMPGVSHVTVDSVVLPPQTLVAFLRIESLSTGIEPLFVPLDFGMADQLRTLEKNLVDKLPSYMIPSLFIPISHIPMTISGKVDRIALRRAVLSMNERQQKMYALADEVKEEPQTEQEHCLRDLWAVVLGKEPSSVGRQDSFFRLGGDSIGAMKLVAAARRAGYLLSVADIFRHPELIEMAVRLDLSNGAKAAAYAPFSLLQDEQNQRQATLEEAAQQCSVSQDAIEDIYHATPLQEGVFLMSTTHDGAYVAPTAFALPSEFDVRKFQESWQELVNAHPILRTRIVTINAISYQAVLTKNASVIEWETAASLNEYIDRVRASPVAAGRPLCRFALVPNEDSTVFVWTAHHALFDGWTMGLLFDQLAQLFKDGTRPAPATSFAEFVQFTRQMGQDTSRDFWASLCPQEPPAVFPRLPSSTYHPTANTTSYRTISTNLSKNTDFTMAILLRAAWSIVLARYTDAEDILYGLTLSGRDLPVSGIEKVMGPTITTVPMNVHLDGEMLIQDFLQRQHDENVEMMRHQHVGLQAIRRISKATAAATEFTNLFVVQPQATQVSGLTELTQVPTDMTRFDPYALVVECNLGDDQILLEARFDSSILSMDQANHLLGHFDHVLSQLTSFRPDCRLQDIDAFSLEDERQIWKWNAVPAKSEDFCIHDLIAAQADRHPQEIAVDAWDGSFTYKELDNLSTRLSNYLVTNIGIRPESLVPLCFDKSRWTIVVMLAVVKSGGGCVMLNPDHPVSRLEGVITDTGSSVVLASPERVGLFSSHAAKKVVITEALVHSLTLTEQDCLPLPPIQPTNPVFVIFTSGSSGKPKGIVVQHNSVCTVAIQHGEGLGFKGPGLRVLQFASFSFDVSMGEVFLTLAKGGTLCIPTEHDRLNNLADTINRMKITWTFMAPTVAALLDPREVPALKTLVLGGEAVSQSLVDQWATRVNLIDSYGPAECTIWASHAIASATVSPANIGRGVGCRYWIVDPLDYNRLTPIGCVGELLIEGPNVSRGYLNEPEKTKAVFVENPKWLQGKETPLYKFYCTGDLVRYNVDGSLNIAGRKDSQVKFNGQRIELSEIEFHLRAHSEIEAGMVVLPKEGPCKGKLVAVVALTGLQPAALEGDHIELVPRTLKNEAQLRVQQVQDRLGELLPPYMVPSIWVTLYSIPLTASRKINRLPISRWIQSMSDEIYHDVVDITVATVHQPTTQLEKELAQVWSHVLNVSIDAIGLDRSFLSLGGDSITAMQVVSRCRSLDIQVSVQDILQPKSLSGVVARALAAKPTAIHREEQYDTQFELSPIQQLYFEDVVRTNGEGMHHYNQSVLLRVLRPVTPAQLSEAMERVTANHAMLRARFRRDSDGKWTQMAKSPAQGLCSFDSCLVQDRPELFERLNASQRSINIENGPVFVAKYFQIANEDVRLLSLIAHHLVIDAVSWHIIIGQLEQVLQFPDTQLNPARMPFQSWLEEQRKLVESLSKSPIPLQDLPAANLEYWGLANLPLWGNGQEISFTLNEKTTALLLTAANTSLRTEPIDLLLAALQLSFADSFSDREMPSFFVEGHGREPWESSIDLSETIGWFTTFHPIHRRVRKNESIKTTIKRTKDARQSWNDNGFAYFARRHFDVETHEKLRSHRIMEICFNYLGQSQHAEREDAILQEEVLLPEESLENIGDSMGRLAVFDIVAAVSHGRLNVSFFFQNDILHQSKVCQWVKRCESTLQMAVDELTVSETEFCISDFPLLDINYQDLATLTTAVLPSIGISPDAIEDLYPCSPIQEGILISQARQPGTYEVRQLFKVVPREDQPAVDVSRLVAAWQQTVDRHALLRTVFIEAINGSGVFNQLVLRSYPAEVKRLSLDNVAGQEEVAVFVTSQMGPDYRQPAPAHRLTICETPDSVYCQLEVSHALIDGTSMALLVRDLVAAYEGTLLAVPGPLYSTYMKYLSQQSEADALSYWKSQLENVEACHFPALNTMPVSTTGFQSKVIEIDAGGELKKFCEANDLTMSNLFQVGWGLVLRAYTGSSDVCFGYMAAGRDIPVEGIYDAIGPFINLLVCRMHLDEKLSPNDLLQAMQTDYLESLPHQHVSLAAIQHALGQSDVALFNSIMSLQRKPSPGSPPEIELQVVAENDPTEYDVDLNITTGEESGVEIHITYRNSVLTDSQADRLLCNFSHILFALAACANQPLAQLDLSKASPMSLAQAVSREEPVSVQASIPKLISERTEASPTSIAVQCMVDDTILTYYDLDCLTCSLADHLLRLGVCQGDIVLLDFPRSKWALVALLAVLRAGATSLALSSTHDLKDIREALTAQKSAIVLGGERFTAKSVNDGFTHVTVDAAFMTSIKAVTLANTALRDISPSEVALAVKDGEDWALLAHHTISTAASHLGSKAGLTPGARVVQLSTIESTSYLVETLFTLIRGGTVIVPPTDVGVTQSLRLSRANWALLSKDEATSTNATQVPELQTLVVAGDRMPISLQLKWRDVNLIHPRQLNHIHVWVSLMIAPAGCDSLQPCPIPALARTWVRSPFSQTALAPTECKGEVLVDGPLVPRGYVGNSSQSLLRNPVWLPNAVLVCTGVQGRWSNNGVDLEEQSPSRATGNTADILGMEELVKTTLRPTENVLITAIQNEAEDRIVAYFTNSPEGEEPVKLLPLTDALQQRFLEIQAFLKGKVSDDLLPEFCFPVNRIPLAINRQFDRPGLNQLVSMLSDDTLASYRVQAPAIAPRLTSNENLIADLWSEVLHLPDRAKLDPSESFFRLGGDSIGAMRIIAAARSQGLVLTMNGIFQQPTLAGMAKEIRLLAPHEDRPVEPFSLLPPAVDSTTLISEAAAKCHVDASAVEDIYPCTPLQEGFMVLTSQDSAAYYVQEVFKMPESVDLARFREAWSTVVSRSTILRTRIISVLDGFFQVLLREPVYWQSGVDLETYLRDDMKKAMSYGQPLSRFAVVEAPRQRYFIWTAHHAVYDGLTMATLAKQVSAEYNQEMALPEIPYNRFIDYIQGVSPAAATEFWAAQCAVPATTFPMLPSRDQQPFPDQFMSHSIPVKIKPSTITLSTVLRAAWAMVLAQLTDSEHVNFGVTLSGRNASMVGINQVLGPTIATVPVQIHVPQNLAPQKFLQAVHKQAIDMIPFEHTGLQNIRKMGEQCREAVNFQNLLIIQPGTSPVDDSDFLGLTPVQQDGDQRDPYPLTIECNLLDDSIELKAQFDSRFIPSGEMSRILKQYARTVERFQTLDEAVSEDDGEETFDASNGLSDDDVEQILAWNSDRPVLIEKCLHEVFEEQARLRPDAPAVSSYDVQLTYRELKDLIDRLAMQLQSMGIKPEMKIPLCFSKSSWTIVAMFAVFKVGGVACMLNPEHPSNRIHLLLRDLDAEYALCDQASLSMMASLLSPANVLSVDGTYLRSLPPSSTLSYQVQPGNAALVVYTSGSTGKPKGSILEHRSIVTGLTAHCTAMGIGPESRVFQFAAYTFDVCFEEIFGALMLGGCVCVPSEDERMNSLADAMARYRVTWTELTPTVASLLLPSSIPTLKSLALSGESVTKEVVQRWGDAVQLINTYGPSECCVSSTCNVETAIVRDPSNIGRGLGCTTWIVNPDDVNVLAPIGATGELLIEGPIVARGYLNEPEKTAAAFISAPAWWPESWSCGRIYRTGDLVKYNADGTIKFIGRRDTQVKLHGQRIELGEIEHRIRGAFTDSSHQVAVEVLAPNTRGGLKILTAFICESSQVSEESDGLLLDLDDGMSHRFLELQARLMGELPRHMIPQLFIPIKHMPLSPSRKIERKVLRALGNALQADQLSAYALTQTARTAPSTATEKALSDIWTEVLGTSPSGTEDHFFHLGGDSIAAMKAVAAATKIGLSLSVAEIMQFPTLRAMAAAIDSAVDNEDVDEEVLECFSLIPPSQLSDVVAEAVAQCAVPAEDIEDIYPCTPSQEALMALTARDEAAYVSRAVYRLPLNLDVARYREAFEQLTQRQAIMRTRIIYSSVAARSYQVVVQGSLIWHTDESLAAYVAADKLTPMRHGDALMRFALLEGSTEDPRPCLVYTAHHAVYDGWSEASMFEEAETIYRQGLNALPAVAPYKKFIHYLSTIDSAASEEFWRSHLEGDLPAPFPPGSPDATTSLLTSRPNRSQFHSIRLPSLHSLPYTLPTVLKAAWALLLSRYTTSDDVIFGHVLSGRTVPLRGVSDMMGPTISTVPVRVRLNPDESVEALLRRIQTQAQDMTAFEQIGMQNIRRLLASPEAVDVGHLFFIQPPMEAGTTDLALEPVADADFDFDTYPLIVECQLDSDNGATLSVKYNDARISQTSMTWLLQHFENLVGQLYQSPRTAAISTLELTGSSDIQTLRGWIGAPVTPVQNTVHDEFRSRAFAHPERCAVQAWDGTLSYRELDVLSSQYARKLCSLGLSVGQAVGLIFDKSCWAAVAMLAVLKAGGCCVQLDAKHPSTRLVEIVEDTSLHHILAASSHVSLAKSLPVDHAIEVNHLSNSALQTSLDKASRLPVVDVMSPAYMTFTSGSTGKPKSVVINHQAIHTSISAFSSALCMNFKSRVLQFAAYTFDISYAETFAPLTLGATLCVLSEQDRLNDLAGAISRLGANWACLTPTVASLVEPASIKGLLKTLVLSGEAPTEENLRIWSGKVPNLINAYGPSEASVWCAAGSFKRPDDSCTNIGRPVGCHLVIAEPSDINRLTPVGCVGELIVCGPILSSGYLNNEKANSAAFHQNIAWREKLGIHAGCSRVYRTGDLARFLPDGSIEYLGRADTQVKIYGRRIEPREIEHHIHLELGDYLNMVDSVTLANRKNQKMLVAFIYQESAFVPNLDLATLARDLNPEIQSTLASLQAALRSRLPHWMIPTLFIPLRFMPTNAAGKTDRKLLARAVNLLTDDQLRDFALSGRTEKKPLTTYLQQQLADLWADVLTLDVQSIGADDTFFTLGGDSILAMKMASRARSAQISLSVADIFNYPVLADLASHLQALMPLTPGSETPTSDFHSKMALAPATDLVLLEALAQKAGVDAAAVEAVEHTTDFQDLALVGHLSKSRWMLNWFFFDGPGSGDAERLRKGCHDLVQQFDILRTVFVAHEGRFWQVVLNKLKPSFRVESTADFAGFTQSLYEDGLAQELNLSKPLVEFVLAVHPGGHSHRLLMRLSHAQYDGVSLPTLWDCLQRACHGEALPRISSFTQFLRATKPANLDATRSYWRSLLNGATETRFVAHSKPALRDEAHDRVVHVTRRQVPVVSLRQHGITPATVLRSAWAILLARLSASSDVTFGQTTANRSATTLPDIENVVGPCLNVVPVRASLKPGQTVLEFLLAQQAQQVSGLAHESLGFRQIIRDCTNWPSWTHFSSVVQHQNIEPDRDVPLGPNDADMYKPGFLGADLDLTDVSVLSTPTIDGYVDLDLLTSCKVMSPFAAELLVDQLSELLQLWAVVPLERFKVNERSMTTAMIPLVPADIGVPPVVKNSRRADIQDAWQTCLSKANSVVSLEDGDADFFRLGGDLVQMAQLASELHAKGIGRGVALETLVQHSTLDAMVQILS'
    max_seq_len = 1000
    t_seq = [long_sequence[i*max_seq_len:(i+1)*max_seq_len] for i in range(int(len(long_sequence)/max_seq_len))]
    t_id = ['test_seq_' + str(i) for i in range(len(t_seq))]
    short_fasta_records = [SeqRecord(Seq(t_seq[i]), t_id[i]) for i in range(len(t_seq))]
    long_fasta_record = SeqRecord(Seq(long_sequence), 'test_seq')
    
    test_dir = Path('test')
    if not test_dir.exists():
        test_dir.mkdir()

    short_AA_file = test_dir / 'short_AA.fasta'
    short_3Di_file = test_dir/ short_AA_file.name.replace('_AA.fasta', '_3Di.fasta')
    long_AA_file = test_dir / 'long_AA.fasta'
    long_3Di_file = test_dir / long_AA_file.replace('_AA.fasta', '_3Di.fasta')

    with open(short_AA_file, 'w') as out_file_short:
        SeqIO.write(short_fasta_records, out_file_short, 'fasta')

    with open(long_AA_file, 'w') as out_file_long:
        SeqIO.write(long_fasta_record, out_file_long, 'fasta')

    
    yield short_AA_file, long_AA_file, short_3Di_file, long_3Di_file

    # clean up
    short_AA_file.unlink()
    long_AA_file.unlink()
    if short_3Di_file.exists():
        short_3Di_file.unlink()
    if long_3Di_file.exists():
        long_3Di_file.unlink()

def test_predict_3Di_encoderOnly(setup_fastas):
    fasta_files = setup_fastas
    # f_short_AA, f_long_AA, f_short_3Di, f_long_3Di = *fasta_files

    # ProstT5 predict previously split sequences 
    command = [
        'python', 'predict_3Di_encoderOnly.py',
        '--fasta', fasta_files[0],
        '--output', fasta_files[2],
        '--half', '1'
        '--model', '/home/mpjw/eggNOG-3Di/data/prostt5/model/'
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    
    # ProstT5 predict long sequence with auto splitting
    command = [
        'python', 'predict_3Di_encoderOnly.py',
        '--fasta', fasta_files[1],
        '--output', fasta_files[3],
        '--half', '1'
        '--model', '/home/mpjw/eggNOG-3Di/data/prostt5/model/',
        '--split_long_seqs', '1'
    ]
    result = subprocess.run(command, capture_output=True, text=True)


    assert result.returncode == 0, "Script failed with error: {}".format(result.stderr)

    short_3Di_records = SeqIO.parse(fasta_files[2], "fasta")
    long_3Di_record = SeqIO.parse(fasta_files[3], "fasta")

    assert sum([len(r) for r in short_3Di_records]) == len(long_3Di_record), "3Di sequences did not match in length"
    assert ''.join([str(r.seq) for r in short_3Di_records]) == str(long_3Di_record.seq), '3Di sequences did not match in sequence identity'
