#!/bin/python

from Bio import SeqIO
import pytest
from pathlib import Path
import subprocess
from math import ceil

MAX_SEQENCE_LENGTH = 1000
MIN_SPLIT_LEN = 2

@pytest.fixture
def setup_fastas():
    long_seq = "MGDYGENMPISPDAVQLTFAQKAGASLFPSLTDGILLDENKLAEQRSASALEQTKISLSLRPETSIANLTAFCARHKCTLLGVLNVAWALVLSTYTDTELAQVLFVRYKDDTPYIGLSEIVIDGGETILQVLALVEQHLSTGMPVPSTTTITDLQNWTASDGHPVFNSVVLFSDSTTAERKEAGDYISLHARVAGDQLCINLQAPSHLLPAAQAQNCAATLSHVLGEIVQNPDLPLSDIGLMSPQGLDQISKWNHTAPAVVSRCVHELVDETAETQPDTIAIDGADGTMTYGELRSYSNQLAHYLTQQGVGPEFTVPLFFEKSKWAIVAMLGVVKAGGTIVNLDAKQPKERLRGLLAQLQASIVLTSVQNADLWKDERPVFVISEEFLHQLTTVAEAPKVAVTPQNALYIIFTSGSTGTPKGCVVEHESFLTAAAQHIKAGNILSSSRILQMTPYTFDVSMLEIFTTLTIGACICFCNDSEAARGVAHIINFLKISWTFMTPSLVRLVDPSSVPTLKTLALGGEGLARIDVTTWADKLHLINGYGPSECSVAATMHGPLSLNSDPANIGLGCGAICWVVDRNDHDRLVPIGAVGELVIQGPIVARGYLNEPGKTAAVFLDKVPAFAATLPRAPPAFRLYKTGDLVRQNSDGTLTFIGRKDRQVKLNGQRLELGEIEQRLSENSLVRHALVLLPKQGPCKGRLVAVLSLQDYPYSGEPDANVHQLSTEESRAARALLPAISAQLATHVPGYMVPTFWVVLAALPFTTSGKVHGVAMTQWLHAMSEETYNEIADVSEEIPTVDLSSEIELSLQKIFAEEMGIPITELKMNRSFIALGGDSLKAMKVVARCRQQELKLSVADVLRASSLIALAKCVEQASSGSNSVPEESKKEAFHSTPEQRIAALAESLLTAIGLAREQLEDAYGCSPMQDGILLSQVKFPGTYEIRRVLHVQSTHDVDTTVSRLQTAWQMVVDRHQALRTVFVEVEGRFQQLVLKKVSAYFQICKFSDLEDQEAVINRLKTLPPPSFKPSQPQHRLTICCAGVNEVFLKFEISHALVDGGSTEVILREISAAFDEHSLSGNPARFSDYMDYISNPEAAEISLGYWTEHLKGTQPTIMPMYPADATEKRICSVPVPFNDTAALIQFSEANGVTLANVLQAAWALVLRTYTDTSDICFGYIAAGRDVPVEGIDRAVGAFINMLVCRVRLEEQPTILDAILGMQEQYFDALPHQHTSLAQIQHRLDLSGMPLFNSIISVQNDVSDQPYAQSLAFKSVEEDDPTDFDLCVAIHVGNDNVRIDIGYWSSLLTKGDASNLAYTFSSAISAILRDASVPAVSVDLFSEYDRSQVFAWNQDEPTSKPGVVHDYVYAKVQEQPDAQAVCAWDGEYTYRELGGLSEKLAHHLAELGSGPEVLIPHCFSKSKLAAVVMLAIMKSGSACVGLSSSHPRTRVQDIIENCAATIAVVAKENIGVVDGLVNRVVVVDEAFLANLPEPSPGAQLPKALPHNPAFVSFTSGSTGKPKGIVLEHESLITSILAHGPEWGVDQSARVLQFSAYAFDASVSDTFTTLVGGGTVCIPHEKDRVDDLVGAINRLGVNWAFLTPRVLSLLTPELVPGLKTVVLGGEAISKEDIARWTDKICIRIVYGPTECTIYSMGSEPLNSQSDPLCLGHAVGTRLWITHPDDINKLMPVGCTGELIIEGPLVTRGYLNEPAKTEAAYFEDPVWLPKKESGEPRRFYKTSDLVRYYPDGQLRFIGRKDTQIKIRGQRVELGEIEHAILESMPGVSHVTVDSVVLPPQTLVAFLRIESLSTGIEPLFVPLDFGMADQLRTLEKNLVDKLPSYMIPSLFIPISHIPMTISGKVDRIALRRAVLSMNERQQKMYALADEVKEEPQTEQEHCLRDLWAVVLGKEPSSVGRQDSFFRLGGDSIGAMKLVAAARRAGYLLSVADIFRHPELIEMAVRLDLSNGAKAAAYAPFSLLQDEQNQRQATLEEAAQQCSVSQDAIEDIYHATPLQEGVFLMSTTHDGAYVAPTAFALPSEFDVRKFQESWQELVNAHPILRTRIVTINAISYQAVLTKNASVIEWETAASLNEYIDRVRASPVAAGRPLCRFALVPNEDSTVFVWTAHHALFDGWTMGLLFDQLAQLFKDGTRPAPATSFAEFVQFTRQMGQDTSRDFWASLCPQEPPAVFPRLPSSTYHPTANTTSYRTISTNLSKNTDFTMAILLRAAWSIVLARYTDAEDILYGLTLSGRDLPVSGIEKVMGPTITTVPMNVHLDGEMLIQDFLQRQHDENVEMMRHQHVGLQAIRRISKATAAATEFTNLFVVQPQATQVSGLTELTQVPTDMTRFDPYALVVECNLGDDQILLEARFDSSILSMDQANHLLGHFDHVLSQLTSFRPDCRLQDIDAFSLEDERQIWKWNAVPAKSEDFCIHDLIAAQADRHPQEIAVDAWDGSFTYKELDNLSTRLSNYLVTNIGIRPESLVPLCFDKSRWTIVVMLAVVKSGGGCVMLNPDHPVSRLEGVITDTGSSVVLASPERVGLFSSHAAKKVVITEALVHSLTLTEQDCLPLPPIQPTNPVFVIFTSGSSGKPKGIVVQHNSVCTVAIQHGEGLGFKGPGLRVLQFASFSFDVSMGEVFLTLAKGGTLCIPTEHDRLNNLADTINRMKITWTFMAPTVAALLDPREVPALKTLVLGGEAVSQSLVDQWATRVNLIDSYGPAECTIWASHAIASATVSPANIGRGVGCRYWIVDPLDYNRLTPIGCVGELLIEGPNVSRGYLNEPEKTKAVFVENPKWLQGKETPLYKFYCTGDLVRYNVDGSLNIAGRKDSQVKFNGQRIELSEIEFHLRAHSEIEAGMVVLPKEGPCKGKLVAVVALTGLQPAALEGDHIELVPRTLKNEAQLRVQQVQDRLGELLPPYMVPSIWVTLYSIPLTASRKINRLPISRWIQSMSDEIYHDVVDITVATVHQPTTQLEKELAQVWSHVLNVSIDAIGLDRSFLSLGGDSITAMQVVSRCRSLDIQVSVQDILQPKSLSGVVARALAAKPTAIHREEQYDTQFELSPIQQLYFEDVVRTNGEGMHHYNQSVLLRVLRPVTPAQLSEAMERVTANHAMLRARFRRDSDGKWTQMAKSPAQGLCSFDSCLVQDRPELFERLNASQRSINIENGPVFVAKYFQIANEDVRLLSLIAHHLVIDAVSWHIIIGQLEQVLQFPDTQLNPARMPFQSWLEEQRKLVESLSKSPIPLQDLPAANLEYWGLANLPLWGNGQEISFTLNEKTTALLLTAANTSLRTEPIDLLLAALQLSFADSFSDREMPSFFVEGHGREPWESSIDLSETIGWFTTFHPIHRRVRKNESIKTTIKRTKDARQSWNDNGFAYFARRHFDVETHEKLRSHRIMEICFNYLGQSQHAEREDAILQEEVLLPEESLENIGDSMGRLAVFDIVAAVSHGRLNVSFFFQNDILHQSKVCQWVKRCESTLQMAVDELTVSETEFCISDFPLLDINYQDLATLTTAVLPSIGISPDAIEDLYPCSPIQEGILISQARQPGTYEVRQLFKVVPREDQPAVDVSRLVAAWQQTVDRHALLRTVFIEAINGSGVFNQLVLRSYPAEVKRLSLDNVAGQEEVAVFVTSQMGPDYRQPAPAHRLTICETPDSVYCQLEVSHALIDGTSMALLVRDLVAAYEGTLLAVPGPLYSTYMKYLSQQSEADALSYWKSQLENVEACHFPALNTMPVSTTGFQSKVIEIDAGGELKKFCEANDLTMSNLFQVGWGLVLRAYTGSSDVCFGYMAAGRDIPVEGIYDAIGPFINLLVCRMHLDEKLSPNDLLQAMQTDYLESLPHQHVSLAAIQHALGQSDVALFNSIMSLQRKPSPGSPPEIELQVVAENDPTEYDVDLNITTGEESGVEIHITYRNSVLTDSQADRLLCNFSHILFALAACANQPLAQLDLSKASPMSLAQAVSREEPVSVQASIPKLISERTEASPTSIAVQCMVDDTILTYYDLDCLTCSLADHLLRLGVCQGDIVLLDFPRSKWALVALLAVLRAGATSLALSSTHDLKDIREALTAQKSAIVLGGERFTAKSVNDGFTHVTVDAAFMTSIKAVTLANTALRDISPSEVALAVKDGEDWALLAHHTISTAASHLGSKAGLTPGARVVQLSTIESTSYLVETLFTLIRGGTVIVPPTDVGVTQSLRLSRANWALLSKDEATSTNATQVPELQTLVVAGDRMPISLQLKWRDVNLIHPRQLNHIHVWVSLMIAPAGCDSLQPCPIPALARTWVRSPFSQTALAPTECKGEVLVDGPLVPRGYVGNSSQSLLRNPVWLPNAVLVCTGVQGRWSNNGVDLEEQSPSRATGNTADILGMEELVKTTLRPTENVLITAIQNEAEDRIVAYFTNSPEGEEPVKLLPLTDALQQRFLEIQAFLKGKVSDDLLPEFCFPVNRIPLAINRQFDRPGLNQLVSMLSDDTLASYRVQAPAIAPRLTSNENLIADLWSEVLHLPDRAKLDPSESFFRLGGDSIGAMRIIAAARSQGLVLTMNGIFQQPTLAGMAKEIRLLAPHEDRPVEPFSLLPPAVDSTTLISEAAAKCHVDASAVEDIYPCTPLQEGFMVLTSQDSAAYYVQEVFKMPESVDLARFREAWSTVVSRSTILRTRIISVLDGFFQVLLREPVYWQSGVDLETYLRDDMKKAMSYGQPLSRFAVVEAPRQRYFIWTAHHAVYDGLTMATLAKQVSAEYNQEMALPEIPYNRFIDYIQGVSPAAATEFWAAQCAVPATTFPMLPSRDQQPFPDQFMSHSIPVKIKPSTITLSTVLRAAWAMVLAQLTDSEHVNFGVTLSGRNASMVGINQVLGPTIATVPVQIHVPQNLAPQKFLQAVHKQAIDMIPFEHTGLQNIRKMGEQCREAVNFQNLLIIQPGTSPVDDSDFLGLTPVQQDGDQRDPYPLTIECNLLDDSIELKAQFDSRFIPSGEMSRILKQYARTVERFQTLDEAVSEDDGEETFDASNGLSDDDVEQILAWNSDRPVLIEKCLHEVFEEQARLRPDAPAVSSYDVQLTYRELKDLIDRLAMQLQSMGIKPEMKIPLCFSKSSWTIVAMFAVFKVGGVACMLNPEHPSNRIHLLLRDLDAEYALCDQASLSMMASLLSPANVLSVDGTYLRSLPPSSTLSYQVQPGNAALVVYTSGSTGKPKGSILEHRSIVTGLTAHCTAMGIGPESRVFQFAAYTFDVCFEEIFGALMLGGCVCVPSEDERMNSLADAMARYRVTWTELTPTVASLLLPSSIPTLKSLALSGESVTKEVVQRWGDAVQLINTYGPSECCVSSTCNVETAIVRDPSNIGRGLGCTTWIVNPDDVNVLAPIGATGELLIEGPIVARGYLNEPEKTAAAFISAPAWWPESWSCGRIYRTGDLVKYNADGTIKFIGRRDTQVKLHGQRIELGEIEHRIRGAFTDSSHQVAVEVLAPNTRGGLKILTAFICESSQVSEESDGLLLDLDDGMSHRFLELQARLMGELPRHMIPQLFIPIKHMPLSPSRKIERKVLRALGNALQADQLSAYALTQTARTAPSTATEKALSDIWTEVLGTSPSGTEDHFFHLGGDSIAAMKAVAAATKIGLSLSVAEIMQFPTLRAMAAAIDSAVDNEDVDEEVLECFSLIPPSQLSDVVAEAVAQCAVPAEDIEDIYPCTPSQEALMALTARDEAAYVSRAVYRLPLNLDVARYREAFEQLTQRQAIMRTRIIYSSVAARSYQVVVQGSLIWHTDESLAAYVAADKLTPMRHGDALMRFALLEGSTEDPRPCLVYTAHHAVYDGWSEASMFEEAETIYRQGLNALPAVAPYKKFIHYLSTIDSAASEEFWRSHLEGDLPAPFPPGSPDATTSLLTSRPNRSQFHSIRLPSLHSLPYTLPTVLKAAWALLLSRYTTSDDVIFGHVLSGRTVPLRGVSDMMGPTISTVPVRVRLNPDESVEALLRRIQTQAQDMTAFEQIGMQNIRRLLASPEAVDVGHLFFIQPPMEAGTTDLALEPVADADFDFDTYPLIVECQLDSDNGATLSVKYNDARISQTSMTWLLQHFENLVGQLYQSPRTAAISTLELTGSSDIQTLRGWIGAPVTPVQNTVHDEFRSRAFAHPERCAVQAWDGTLSYRELDVLSSQYARKLCSLGLSVGQAVGLIFDKSCWAAVAMLAVLKAGGCCVQLDAKHPSTRLVEIVEDTSLHHILAASSHVSLAKSLPVDHAIEVNHLSNSALQTSLDKASRLPVVDVMSPAYMTFTSGSTGKPKSVVINHQAIHTSISAFSSALCMNFKSRVLQFAAYTFDISYAETFAPLTLGATLCVLSEQDRLNDLAGAISRLGANWACLTPTVASLVEPASIKGLLKTLVLSGEAPTEENLRIWSGKVPNLINAYGPSEASVWCAAGSFKRPDDSCTNIGRPVGCHLVIAEPSDINRLTPVGCVGELIVCGPILSSGYLNNEKANSAAFHQNIAWREKLGIHAGCSRVYRTGDLARFLPDGSIEYLGRADTQVKIYGRRIEPREIEHHIHLELGDYLNMVDSVTLANRKNQKMLVAFIYQESAFVPNLDLATLARDLNPEIQSTLASLQAALRSRLPHWMIPTLFIPLRFMPTNAAGKTDRKLLARAVNLLTDDQLRDFALSGRTEKKPLTTYLQQQLADLWADVLTLDVQSIGADDTFFTLGGDSILAMKMASRARSAQISLSVADIFNYPVLADLASHLQALMPLTPGSETPTSDFHSKMALAPATDLVLLEALAQKAGVDAAAVEAVEHTTDFQDLALVGHLSKSRWMLNWFFFDGPGSGDAERLRKGCHDLVQQFDILRTVFVAHEGRFWQVVLNKLKPSFRVESTADFAGFTQSLYEDGLAQELNLSKPLVEFVLAVHPGGHSHRLLMRLSHAQYDGVSLPTLWDCLQRACHGEALPRISSFTQFLRATKPANLDATRSYWRSLLNGATETRFVAHSKPALRDEAHDRVVHVTRRQVPVVSLRQHGITPATVLRSAWAILLARLSASSDVTFGQTTANRSATTLPDIENVVGPCLNVVPVRASLKPGQTVLEFLLAQQAQQVSGLAHESLGFRQIIRDCTNWPSWTHFSSVVQHQNIEPDRDVPLGPNDADMYKPGFLGADLDLTDVSVLSTPTIDGYVDLDLLTSCKVMSPFAAELLVDQLSELLQLWAVVPLERFKVNERSMTTAMIPLVPADIGVPPVVKNSRRADIQDAWQTCLSKANSVVSLEDGDADFFRLGGDLVQMAQLASELHAKGIGRGVALETLVQHSTLDAMVQILS"

    test_seqs_long = [
        # ("test_seq_empty", ""), 1000, 998, 999
        ("test_seq_small", "MPEDKHNNPNLITMSDLQKAAKAANMSVEDAARNIADAVGLTCRKE"),
        ("test_seq_one_split", "MEMTRKEVVTENNSGRMDGQKVSADQRSVASHMNMESKNSLDLNQAASQWSTVFSLSPQPILITDGEFSILKGNEAFVDLSGISQEKLVGKKIQDFMISSQEGEGAREALTQRRRTTGTVTITFPAGVQTLEQYCIPVCEEGKQISTVVFIFKNITRRVRAEEETEKIKQKLLHDYGERVKEQKLFYATAALIQDDSLTPEEVLSEVVNLIPPGWQYPEVTAARITVGDIDVRTPHFQKTAWKQEASFAIKDGNRGTLEVVYLEDKPFEAEGPFLAEERNLINSLSDMLKTYLDRKSGEEHLAERIKEQEALLHDYGERVKEQTLFYSTATLIQDDLHTTAEVLSEIVELIPPGWQYPEVTAARITVGDVDVRTRNYRKTSWSQTAQFSVKGGKEGVIEVVYLEEKPAEVEGPFLAEERNLINSLSDMLKTYLDRKSGEEHLAERIKEQEALLHDYGERVKEQTLFYSTATLIQDDLHTTAEVLSEIVELIPPGWQYPEVTAARITVGDVDVRTRNYRKTSWSQTAQFSVKGGKEGVIEVVYLEEKPAEVEGPFLAEERNLINSLSDMLKTYLDRKSGDEHLAERIKEQEALLHNYGERVKEQTLFYSTATLIQDDLHTTAEVLSEIVELIPPGWQYPEVTAARITVGDVDVRTRNYRKTSWSQTAQFSVKGGKEGVIEVVYLEEKPAEAEGPFLAEERNLINSLSDMLKTYLDRKSGEEELVRHMTEIRELQHQTDTIVQENPMPIILLDQKFHIMVTNDAYVKLTGIEKERLLTMSATDLDVIEHSGEGLRELLQKKQRTYGELIVNFPAGRKTLEQHGIPVFTTAGELSRLLIVYNDVTEERQKMHQISQLKHRSETIVQENPMPILLTDAEFNIVVTNHAYVELTSIDRDRLQRMNARDFKILEQKGEGLRRVVREHLPATGEVTVEFPIGARTLEQYGIPILADDGSLVNILIVYNDVTTQRAQEQEIQVMMKESQQKADQLSRSCVDLDECMSLIAAKNLTHVVSIEDGDPLTGVKRDYNDAIAAIRDVIASIRGSMVQLNLTIEDSSRSTEEVARAVEQVAIATQKSSEAAKVQLDRIEGVSREIGDLSASIEEIASTSQTVRDLAARVAQEGNQAAGLGKDATQKMKVVEEISEQSVHEINQLNEQMHQITKIVNLITEIANQTNLLALNAAIEAARAGEHGRGFAVVAGEVKNLASESRKASQQIEDLIVSIQKNSDKTASSMQTSYNEIKVGIESVGKTIDSLNRITVEADKLVEGISEISRATGDQAEATNRVMEGIEESAGNVKENLGMMEDLAALAEETSASSEEISSAAGELTTMSDHVKGLIVQFQLE"),
        ("test_seq_full", long_seq),
        # ("test_seq_one_AA_overlap", long_seq[: (max_seq_len + 1)]),
    ]

    # TODO: set max_seq_len to exactly the same value which will be computed during prediction, as ProstT5 is very sensitive to changes here
    # split_lens = [MAX_SEQENCE_LENGTH - int(ceil(MIN_SPLIT_LEN / int(len(seq) / MAX_SEQENCE_LENGTH))) for _, seq in test_seqs_long]
    split_lens = [1000, 998, 999]

    test_seqs_short = [
        (seq_id + str(i), seq[i * max_seq_len : (i + 1) * max_seq_len])
        for (seq_id, seq), max_seq_len in zip(test_seqs_long, split_lens)
        for i in range(int(len(seq) / max_seq_len) + 1)
        if seq_id != "test_seq_one_AA_overlap"
    ]

    test_dir = Path("test")
    if not test_dir.exists():
        test_dir.mkdir()

    short_AA_file = test_dir / "short_AA.fasta"
    short_3Di_file = test_dir / short_AA_file.name.replace("_AA.fasta", "_3Di.fasta")
    long_AA_file = test_dir / "long_AA.fasta"
    long_3Di_file = test_dir / long_AA_file.name.replace("_AA.fasta", "_3Di.fasta")

    with open(short_AA_file, "w") as out_file_short:
        for seq_id, seq_aa in test_seqs_short:
            out_file_short.write(">" + seq_id + "\n")
            out_file_short.write(seq_aa + "\n")

    with open(long_AA_file, "w") as out_file_long:
        for seq_id, seq_aa in test_seqs_long:
            out_file_long.write(">" + seq_id + "\n")
            out_file_long.write(seq_aa + "\n")

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
        "python",
        "scripts/predict_3Di_encoderOnly.py",
        "--input",
        str(fasta_files[0]),
        "--output",
        str(fasta_files[2]),
        "--half",
        "1",
        "--model",
        "/home/mpjw/eggNOG-3Di/data/prostt5/model/",
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    # ProstT5 predict long sequence with auto splitting
    command = [
        "python",
        "scripts/predict_3Di_encoderOnly.py",
        "--input",
        str(fasta_files[1]),
        "--output",
        str(fasta_files[3]),
        "--half",
        "1",
        "--model",
        "/home/mpjw/eggNOG-3Di/data/prostt5/model/",
        "--split_long_seqs",
        "1000",
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    assert result.returncode == 0, "Script failed with error: {}".format(result.stderr)

    short_3Di_records = list(SeqIO.parse(fasta_files[2], "fasta"))
    long_3Di_records = list(SeqIO.parse(fasta_files[3], "fasta"))

    # get pairs of sequences for concatenated short sequences corresponding to a long sequence
    for long_rec in long_3Di_records:
        
        if str(long_rec.id) == "test_seq_one_AA_overlap":
            continue
        
        long_id = str(long_rec.id)
        long_seq = str(long_rec.seq)
        short_seq = ''.join([str(short_rec.seq) for short_rec in short_3Di_records if str(short_rec.id).startswith(long_id)])
        
        assert (
            len(short_seq) == len(long_seq)
        ), "3Di sequences did not match in length! {}!={}\nid: {}\nLong seq: {}\nShort seq:{}".format(
            len(long_seq), len(short_seq), long_id, long_seq, short_seq
        )

        assert (
            short_seq == long_seq
        ), "3Di sequences did not match! Sequence identity:{}\nid: {}\nLong seq: {}\nShort seq:{}".format(
            sum([short_seq[i] == long_seq[i] for i in range(len(long_seq))])
            / len(long_seq),
            long_id,
            long_seq,
            short_seq,
        )
