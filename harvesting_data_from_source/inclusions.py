'''
MIT License

Copyright (c) 2023 Fast Data Science Ltd (https://fastdatascience.com)

Maintainer: Thomas Wood

Tutorial at https://fastdatascience.com/drug-named-entity-recognition-python-library/

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

drugs_to_exclude_under_all_variants = {
    "blood glucose"
}

common_english_words_to_include_in_drugs_dictionary = {
    "absinthium",
    "acetphenetidin",
    "acetylsalicylate",
    "acocantherin",
    "actinomycin",
    "adrenalone",
    "adrenergic",
    "aerosporin",
    "aloe",
    "amidopyrine",
    "aminopyrine",
    "amphetamine",
    "analeptic",
    "analgesic",
    "andrographolide",
    "anesthetic",
    "angelica",
    "anorectic",
    "antacid",
    "anthelmintic",
    "antiasthmatic",
    "antibiotic",
    "anticholinergic",
    "antidiabetic",
    "antiemetic",
    "antiepileptic",
    "antifibrinolysin",
    "antihemorrhagic",
    "antihistamine",
    "antimalarial",
    "antiparasitic",
    "antipruritic",
    "antipyretic",
    "antispasmodic",
    "apomorphine",
    "arbutin",
    "arecoline",
    "aspirin",
    "atebrin",
    "atropine",
    "aureomycin",
    "bacitracin",
    "barbital",
    "barbitone",
    "barosmin",
    "belladonna",
    "benzocaine",
    "benzofuran",
    "benzoin",
    "benzylpenicillin",
    "berbamine",
    "betulin",
    "bicarbonate",
    "biguanide",
    "bioral",
    "biotin",
    "bismuth",
    "boldo",
    "borneol",
    "bronchodilator",
    "butyrolactone",
    "calamus",
    "camphor",
    "cannabinol",
    "cantharidin",
    "carbamate",
    "carbostyril",
    "carbromal",
    "cardiotonic",
    "catechu",
    "cathine",
    "cevadine",
    "chelerythrine",
    "chinin",
    "chloral",
    "chloramphenicol",
    "chloroform",
    "chloroquine",
    "cholinergic",
    "cholinesterase",
    "cinchonidine",
    "cinchophen",
    "cineole",
    "cinnamaldehyde",
    "citrate",
    "clavacin",
    "cocaine",
    "codeine",
    "colchicine",
    "conquinine",
    "convulsant",
    "copal",
    "cortisone",
    "coumarin",
    "curare",
    "curcumin",
    "cycloplegic",
    "cymene",
    "cystamine",
    "diamorphine",
    "dicoumarin",
    "digitoxin",
    "ecstasy",
    "elecampane",
    "emend",
    "emetine",
    "ephedrine",
    "epinephrine",
    "epinine",
    "ergometrine",
    "ergonovine",
    "ergotamine",
    "ergotaminine",
    "erythrosin",
    "esculin",
    "estrogen",
    "ethylenediamine",
    "ethylmorphine",
    "eucaine",
    "eucalyptol",
    "eugenol",
    "excipient",
    "expectorant",
    "factive",
    "fenchone",
    "fibrinolysin",
    "flagroot",
    "flector",
    "forane",
    "gallotannin",
    "ginkgo",
    "ginseng",
    "glycyrrhizin",
    "goldenseal",
    "gonadotropin",
    "guaiac",
    "guanidine",
    "guvacine",
    "harmaline",
    "heparin",
    "heroin",
    "hexamethylenamine",
    "hexylresorcinol",
    "histamine",
    "hyaluronidase",
    "hydramine",
    "hydrochloride",
    "hydrogel",
    "hydroquinine",
    "hydroquinone",
    "hyoscine",
    "hyoscyamine",
    "hypericin",
    "hypoglycemic",
    "indazole",
    "indirubin",
    "insulin",
    "inula",
    "isatin",
    "isocodeine",
    "isomeride",
    "isorhodeose",
    "isoxazole",
    "karaya",
    "licorice",
    "lithium",
    "luminal",
    "lustral",
    "mannose",
    "marijuana",
    "methadone",
    "methemoglobin",
    "methenamine",
    "methylamine",
    "morphia",
    "morphine",
    "myrrh",
    "narcotic",
    "nikethamide",
    "nitroglycerin",
    "nitroprusside",
    "olibanum",
    "opium",
    "ouabain",
    "oxyquinoline",
    "oxytocic",
    "palladia",
    "paludrin",
    "paludrine",
    "papaverine",
    "paraderm",
    "paraldehyde",
    "parasiticide",
    "paregoric",
    "penicillin",
    "pentobarbital",
    "peppermint",
    "phenacetin",
    "phenazone",
    "phenetidine",
    "phenobarbital",
    "phenothiazine",
    "physostigmine",
    "picropodophyllin",
    "picrotoxin",
    "pilocarpine",
    "piperazine",
    "podophyllin",
    "propolis",
    "protamine",
    "pseudoephedrine",
    "pseudotropine",
    "psyllium",
    "pyrazole",
    "pyridoxine",
    "pyruvaldehyde",
    "quercetin",
    "quinacrine",
    "quinate",
    "quinazoline",
    "quinidine",
    "quinina",
    "quinine",
    "quinoxaline",
    "rattleroot",
    "rhein",
    "rotenone",
    "safrole",
    "salicylamide",
    "salix",
    "salol",
    "santonin",
    "scopolamine",
    "senega",
    "sinomenine",
    "snakeroot",
    "sparteine",
    "spasmolytic",
    "stilbestrol",
    "stilboestrol",
    "streptomycin",
    "strychnin",
    "strychnine",
    "sulfadiazine",
    "sulfaguanidine",
    "sulfamerazine",
    "sulfamethazine",
    "sulfamethylthiazole",
    "sulfanilamide",
    "sulfapyridine",
    "sulfaquinoxaline",
    "sulfathiazole",
    "sympatholytic",
    "sympathomimetic",
    "tenuate",
    "theophylline",
    "thiouracil",
    "thymol",
    "thymoquinone",
    "thyroglobulin",
    "tragacanth",
    "tramal",
    "trental",
    "trichloroethylene",
    "trinitrotoluene",
    "triterpene",
    "tryptophan",
    "tyramine",
    "usnea",
    "valerone",
    "vasoconstrictor",
    "vasodilator",
    "veratrine",
    "vermifuge",
    "wormwood",
    "xanthopterin",
    "yajeine",
    "yohimbine",
    "glycyrrhiza"
}

extra_terms_to_exclude_from_drugs_dictionary = {
    "black lead",
    "mineral carbon",
    "natural graphite",
    "whole blood",
    "oxygen therapy",
    "mandarin peel",
    "pomegranate fruit",
    "green tea",
    "gold leaf",
    "gold powder",
    "patent blue",
    "horse chestnut",
    "blue x",
    "dry ice",
    "macadamia nut",
    "brussels sprout",
    "beet sugar",
    "cane sugar",
    "table sugar",
    "white sugar",
    "kiwi fruit",
    "bilberry fruit",
    "bullhead fruit",
    "caltrop fruit",
    "tribulus fruit",
    "green tea",
    "pomegranate fruit",
    "schisandra fruit",
    "forsythia fruit",
    "garcinia fruit",
    "paraguay tea",
    "mace fruit",
    "nutmeg fruit",
    "cashew fruit",
    "java tea",
    "kidney tea",
    "g proteins",
    "johnson",
    "ligand",
    "ligands"
}

# Add pharma company names
extra_terms_to_exclude_from_drugs_dictionary = extra_terms_to_exclude_from_drugs_dictionary.union(
    {
        'abbott',
        'abbvie',
        'abiomed',
        'abivax',
        'acadia',
        'acceleron',
        'acg group',
        'aci limited',
        'acme laboratories',
        'acorda',
        'acura',
        'adcock ingram',
        'advanz',
        'advaxis',
        'aerie',
        'agios',
        'ajanta',
        'akbarieh',
        'alcon',
        'alembic',
        'alexion',
        'algeta',
        'alimera',
        'alk-abelló',
        'alkaloid',
        'alkem',
        'alkermes',
        'almirall',
        'alnylam',
        'alphapharm',
        'altana',
        'alvogen',
        'alzheon',
        'ameridose',
        'amgen',
        'amneal',
        'amphastar',
        'angelini',
        'annexin',
        'anthera',
        'antibiotice iași',
        'aplia',
        'apotex',
        'apricus',
        'arbutus',
        'arena',
        'array',
        'arrowhead',
        'aryogen',
        'aspen pharmacare',
        'assertio',
        'astellas',
        'astex',
        'astrazeneca',
        'aurobindo',
        'avella',
        'aventis',
        'b. braun',
        'barkat',
        'bausch & lomb',
        'bausch health',
        'bavarian nordic',
        'baxter',
        'bayer',
        'beacon',
        'behestan darou',
        'beigene',
        'benitec',
        'berlin chemie',
        'besins healthcare',
        'beximco',
        'bharat biotech',
        'bio farma',
        'biocon',
        'biocryst',
        'bioderma',
        'biogen',
        'bioinvent',
        'biolinerx',
        'biomarin',
        'biomérieux',
        'biondvax',
        'bioverativ',
        'biovista',
        'bliss',
        'bluepharma',
        'bosnalijek',
        'bracco',
        'cadila',
        'camurus',
        'cansinobio',
        'capsugel',
        'cassava sciences',
        'catalent',
        'catalyst',
        'cathay drug',
        'cederroth',
        'cel-sci',
        'celesio',
        'celgene',
        'celltrion',
        'cencora',
        'century',
        'ceragenix',
        'cerevel',
        'chemidex',
        'cheng fong',
        'chiesi',
        'chong kun dang',
        'chugai',
        'cinnagen',
        'cipla',
        'civica rx',
        'clovis oncology',
        'cobel darou',
        'combe',
        'compugen',
        'concord',
        'corcept',
        'creative biomart',
        'crookes healthcare',
        'csl behring',
        'cspc zhongrun',
        'curevac',
        'cyclacel',
        'cytokinetics',
        'cytrx',
        'daewoong',
        'daiichi sankyo',
        'danco',
        'darou pakhsh',
        'debiopharm',
        'dechra',
        'delix',
        'dentsply sirona',
        'dermapharm',
        'deurali-janta',
        'diamyd medical',
        'diffusion',
        "divi's laboratories",
        'douglas',
        'editas medicine',
        'eisai',
        'elder',
        'emcure',
        'emergent',
        'endocyte',
        'eskayef',
        'esperion',
        'esteve',
        'exelgyn',
        'fabre-kramer',
        'fareva',
        'faron',
        'fermentek',
        'ferring',
        'flavorx',
        'flexion',
        'fortress',
        'fortune pharmacal',
        'fosun',
        'fresenius',
        'fulhold',
        'g.d. searle',
        'galapagos nv',
        'galderma',
        'galenika',
        'gedeon richter',
        'genentech',
        'general',
        'genmab',
        'genset',
        'giaconda',
        'gilead',
        'glatt group',
        'glaxosmithkline',
        'glenmark',
        'granules india',
        'green cross',
        'grifols',
        'grindeks',
        'grünenthal',
        'guangzhou',
        'hal allergy group',
        'hanhong',
        'hanmi',
        'hansoh',
        'harbin',
        'harrow health',
        'help remedies',
        'herron',
        'hetero drugs',
        'hikma',
        'himispherx',
        'hisamitsu',
        'hospira',
        'hovid',
        'hovione',
        'huadong medicine',
        'hypera',
        'immuron',
        'incepta',
        'incyte',
        'intarcia',
        'intas',
        'ionis',
        'ipsen',
        'jaber ebne hayyan',
        'janssen',
        'jenapharm',
        'jiangsu hengrui',
        'johnson & johnson',
        'jointown',
        'jones',
        'julphar',
        'kadmon',
        'kalbe farma',
        'kamada',
        'kangmei',
        'kannalife',
        'kimia farma',
        'kinetic concepts',
        'kissei',
        'knight',
        'kunming',
        'kyowa kirin',
        'laurus labs',
        'lavipharm',
        'lawley',
        'leadiant',
        'lexicon',
        'lifse',
        'ligand',
        'lijun',
        'liminal',
        'locus',
        'loghman',
        'lundbeck',
        'lundbeck seattle',
        'lupin limited',
        'mallinckrodt',
        'mankind',
        'martin dow',
        'mcguff',
        'medac',
        'medherant',
        'medivir',
        'medochemie',
        'meiji seika',
        'melinta',
        'melior discovery',
        'menarini',
        'mentholatum',
        'merck & co.',
        'merck group',
        'merrimack',
        'microgen',
        'mindmed',
        'mitsubishi tanabe',
        'mochida',
        'moderna',
        'molecular partners',
        'mundipharma',
        'mustang',
        'myrexis',
        'myriad genetics',
        'naari',
        'nanjing ange',
        'natco',
        'nativita',
        'nector',
        'neilmed',
        'neimeth',
        'nektar',
        'neurolixis',
        'neuropathix',
        'nicox',
        'nippon kayaku',
        'nippon soda',
        'north china',
        'novabay',
        'novartis',
        'novavax',
        'novo nordisk',
        'novobiotic',
        'noxxon',
        'ocean biomedical',
        'octapharma',
        'olainfarm',
        'oncolytics',
        'oramed',
        'orchid',
        'orexigen',
        'orexo',
        'organon & co.',
        'orifarm',
        'orion',
        'ortho-mcneil',
        'otis clapp',
        'otsuka',
        'ovation',
        'oxford biomedica',
        'oystershell nv',
        'painceptor',
        'panacea biotec',
        'patheon',
        'perrigo',
        'pfizer',
        'pfizer uk',
        'pharma nord',
        'pharmacosmos',
        'pharmaniaga',
        'pharmascience',
        'pharmavite',
        'pharmstandard',
        'photocure',
        'piramal group',
        'pku healthcare',
        'pluri',
        'portola',
        'prasco',
        'precision',
        'procter & gamble',
        'promomed',
        'proqr',
        'protalix',
        'protein sciences',
        'protek',
        'proteon',
        'psivida',
        'quantum',
        'quark',
        'r-pharm',
        'ratiopharm',
        'reata',
        'reckitt',
        'recursion',
        'regeneron',
        'regulus',
        'renata',
        'repligen',
        'repros',
        'retrotope',
        'roche',
        'rohto',
        'romat',
        'rosepharma',
        'rowell',
        'rubicon research',
        'ryukakusan',
        'saidal',
        'salix',
        'salubris',
        'sangamo',
        'sanitas',
        'sankogan',
        'sanofi',
        'santen',
        'sarepta',
        'seagen',
        'seppic',
        'servier',
        'shanghai',
        'sheffield',
        'shenzhen kangtai',
        'shionogi',
        'sido muncul',
        'sihuan',
        'silence',
        'simcere',
        'sinopharm',
        'sinopharm group',
        'sinovac',
        'smnith',
        'solopharm',
        'solvay',
        'somnogen canada inc',
        'spark',
        'spectrum',
        'sphere fluidics',
        'square',
        'stada arzneimittel',
        'stallergenes greer',
        'stiefel',
        'strides',
        'stryker',
        'sumitomo',
        'sunovion',
        'sutro',
        'synthon',
        'taisho',
        'takeda',
        'tasly',
        'teijin',
        'temmler',
        'terapia ranbaxy',
        'teva canada',
        'theramex',
        'theraplix',
        'thornton & ross',
        'tilray',
        'tonix',
        'torque',
        'torrent',
        'transgene',
        'troikaa',
        'ttk group',
        'turing',
        'unichem',
        'unilab',
        'unilever',
        'veloxis',
        'veranova',
        'vernalis research',
        'vertex',
        'vianex',
        'viatris',
        'viiv healthcare',
        'viromed',
        'vivimed labs',
        'weifa',
        'wilson therapeutics',
        'wockhardt',
        'wuxi apptec',
        'wörwag',
        'xiangxue',
        'yangtze river',
        'yuhan',
        'yunnan baiyao group',
        'zambon',
        'zandu realty',
        'zealand',
        'zentiva',
        'zeria',
        'zoetis',
        'zydus',
        'zymeworks'
        'zymogenetics'}
)

extra_mappings = {"mounjaro": "tirzepatide"}
