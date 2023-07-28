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

import csv
import re
import pathlib
this_path = pathlib.Path(__file__).parent.resolve()

drug_variant_to_canonical = {}
drug_canonical_to_data = {}

exclusions = {'ACACIA',
              'ACETAMIDE',
              'ACETATE',
              'ACETOPHENONE',
              'ACETYLCHOLINE',
              'ACETYLENE',
              'ACRIFLAVINE',
              'ACT',
              'ACTINIUM',
              'ADENINE',
              'ADENOSINE',
              'ADRENALONE',
              'AGMATINE',
              'AIM',
              'ALANINE',
              'ALLANTOIN',
              'ALLSPICE',
              'ALMOND',
              'ALUMINIUM',
              'AMBER',
              'AMEN',
              'AMMONIA',
              'AMYLAMINE',
              'AMYLOPECTIN',
              'AMYLOSE',
              'ANETHOLE',
              'ANILINE',
              'ANTIMONY',
              'ANTIPYRINE',
              'APIGENIN',
              'APPLE',
              'APRICOT',
              'ARGININE',
              'ARTICHOKE',
              'ASPARAGINE',
              'ASPARAGUS',
              'AVOCADO',
              'BA',
              'BANANA',
              'BARIUM',
              'BARLEY',
              'BASIL',
              'BEAN',
              'BEEF',
              'BEESWAX',
              'BEET',
              'BELLADONNA',
              'BENTONITE',
              'BENZIMIDAZOLE',
              'BENZOIN',
              'BENZOPHENONE',
              'BENZYLAMINE',
              'BERBERINE',
              'BERKELIUM',
              'BETAINE',
              'BILBERRY',
              'BLACKBERRY',
              'BLUEBERRY',
              'BLUEFISH',
              'BORNEOL',
              'BORON',
              'BROCCOLI',
              'BROMOFORM',
              'BUCKWHEAT',
              'BUTYLAMINE',
              'CABALETTA',
              'CABBAGE',
              'CADAVERINE',
              'CADMIUM',
              'CAFFEINE',
              'CALCIUM',
              'CAMPHANE',
              'CAMPHENE',
              'CAMPHOR',
              'CANTALOUPE',
              'CAPSAICIN',
              'CAPSICUM',
              'CARAWAY',
              'CARBAZOLE',
              'CARBONATE',
              'CARDAMOM',
              'CARNOSINE',
              'CAROB',
              'CARROT',
              'CARVACROL',
              'CASEIN',
              'CASHEW',
              'CATFISH',
              'CAULIFLOWER',
              'CELERY',
              'CELLOBIOSE',
              'CESIUM',
              'CHERRY',
              'CHICKEN',
              'CHLORINE',
              'CHOLECYSTOKININ',
              'CHOLESTEROL',
              'CHOLINE',
              'CHROMIUM',
              'CHRYSIN',
              'CHYMOTRYPSIN',
              'CINCHOPHEN',
              'CINNAMALDEHYDE',
              'CINNAMON',
              'CLOVE',
              'COBALT',
              'COCAINE',
              'COCARBOXYLASE',
              'COCOA',
              'COCONUT',
              'COPPER',
              'CORN',
              'CORTICOSTERONE',
              'COTTON',
              'COUMARIN',
              'CRANBERRY',
              'CREATINE',
              'CREATININE',
              'CRESOL',
              'CREST',
              'CROCIN',
              'CROTONALDEHYDE',
              'CUCUMBER',
              'CUMIDINE',
              'CUMIN',
              'CURCUMIN',
              'CYANAMIDE',
              'CYCLOHEXANOL',
              'CYCLOHEXANONE',
              'CYCLOPROPANE',
              'CYSTEINE',
              'CYSTINE',
              'CYTISINE',
              'DATE',
              'DEXTRAN',
              'DIAMORPHINE',
              'DICHROMATE',
              'DIETHYLSTILBESTROL',
              'DIGITOXIN',
              'DIHYDROTACHYSTEROL',
              'DILL',
              'DINITROPHENOL',
              'DIOSMIN',
              'DIPHENYLGUANIDINE',
              'DUCK',
              'DUROQUINONE',
              'ECGONINE',
              'ECHINACEA',
              'EGG',
              'EGGPLANT',
              'ELM',
              'EMETINE',
              'EMODIN',
              'ENDURA',
              'EOSIN',
              'EPHEDRINE',
              'ERGOMETRINE',
              'ERGOSTEROL',
              'ERGOTAMINE',
              'ERYTHRITOL',
              'ESCULIN',
              'ESTRADIOL',
              'ESTRIOL',
              'ESTRONE',
              'ESTROGEN',
              'ETHANOL',
              'ETHANOLAMINE',
              'ETHER',
              'EUCALYPTOL',
              'EUGENOL',
              'FARNESOL',
              'FENCHONE',
              'FENNEL',
              'FIBRIN',
              'FIG',
              'FISETIN',
              'FLAVONE',
              'FLEET',
              'FLOUNDER',
              'FLUORESCEIN',
              'FLUORESCIN',
              'FLUORIDE',
              'FLUORSPAR',
              'FORMALDEHYDE',
              'FRANKINCENSE',
              'FRUCTOSE',
              'FUCOSE',
              'FUCOXANTHIN',
              'GADOLINIUM',
              'GALACTOSE',
              'GARLIC',
              'GELATIN',
              'GENISTEIN',
              'GERANIOL',
              'GINGER',
              'GINSENG',
              'GLUCOSAMINE',
              'GLUTATHIONE',
              'GLYCERIN',
              'GLYCINE',
              'GLYCOLIDE',
              'GOLD',
              'GOLDENSEAL',
              'GOOSE',
              'GOSSYPOL',
              'GRAPE',
              'GRAPEFRUIT',
              'GUAIACOL',
              'GUANIDINE',
              'GUANINE',
              'GUANOSINE',
              'GUVACINE',
              'HADDOCK',
              'HARMALINE',
              'HARMINE',
              'HAZELNUT',
              'HELIUM',
              'HEMATIN',
              'HEMIN',
              'HEMOGLOBIN',
              'HEPARIN',
              'HERRING',
              'HESPERIDIN',
              'HEXESTROL',
              'HISTAMINE',
              'HISTIDINE',
              'HONEY',
              'HYALURONIDASE',
              'HYDROGEN',
              'HYDROTALCITE',
              'HYOSCYAMINE',
              'HYPERICIN',
              'HYPOCHLORITE',
              'HYPOPHOSPHITE',
              'HYPOXANTHINE',
              'IMIDAZOLE',
              'INDIRUBIN',
              'INDIUM',
              'INDOLE',
              'INOSITOL',
              'INULIN',
              'IODIDE',
              'IODINE',
              'IODOBENZENE',
              'IODOFORM',
              'IPECAC',
              'IRON',
              'ISATIN',
              'ISOEUGENOL',
              'ISOFLAVONE',
              'ISOLEUCINE',
              'ISOPENTANE',
              'ISOQUERCITRIN',
              'ISOQUINOLINE',
              'KALE',
              'KAOLIN',
              'KAVA',
              'LACTOSE',
              'LAMB',
              'LANOLIN',
              'LANTHANUM',
              'LECITHIN',
              'LEEK',
              'LEMON',
              'LENTIL',
              'LETTUCE',
              'LEUCINE',
              'LICORICE',
              'LINDANE',
              'LITHIUM',
              'LOBELINE',
              'LOBSTER',
              'LUPEOL',
              'LUTEIN',
              'LUTEOLIN',
              'LYCOPENE',
              'LYSINE',
              'LYSOZYME',
              'MACKEREL',
              'MAGNESIUM',
              'MALTODEXTRIN',
              'MALTOSE',
              'MANGANESE',
              'MANGO',
              'MANNITOL',
              'MANNOSE',
              'MENADIONE',
              'MENTHOL',
              'MENTHONE',
              'METHANE',
              'METHIONINE',
              'METHYLAMINE',
              'MOLYBDATE',
              'MOLYBDENUM',
              'MORPHOLINE',
              'MUSKMELON',
              'MYRICETIN',
              'MYRRH',
              'NARINGENIN',
              'NECTARINE',
              'NEODYMIUM',
              'NEON',
              'NIACIN',
              'NICOTINAMIDE',
              'NICOTINE',
              'NIKETHAMIDE',
              'NIOBIUM',
              'NITRATE',
              'NITRITE',
              'NITROGEN',
              'NITROGLYCERIN',
              'NITROPRUSSIDE',
              'NORLEUCINE',
              'NUTMEG',
              'OAT',
              'OKRA',
              'OLEANDRIN',
              'ONION',
              'OPIUM',
              'ORANGE',
              'ORNITHINE',
              'ORRIS',
              'OUABAIN',
              'OXYGEN',
              'OXYTOCIN',
              'OYSTER',
              'OZONE',
              'PAPAIN',
              'PAPAVERINE',
              'PAPAYA',
              'PAPRIKA',
              'PARALDEHYDE',
              'PARSLEY',
              'PARSNIP',
              'PATROL',
              'PEA',
              'PEACH',
              'PEANUT',
              'PEAR',
              'PECAN',
              'PECTIN',
              'PENTAERYTHRITOL',
              'PEPPERMINT',
              'PEPSIN',
              'PERCH',
              'PERCHLORATE',
              'PETROLATUM',
              'PHENACETIN',
              'PHENOL',
              'PHENOLPHTHALEIN',
              'PHENOTHIAZINE',
              'PHENYLACETALDEHYDE',
              'PHENYLALANINE',
              'PHOSPHOCREATINE',
              'PHOSPHORUS',
              'PHTHALOCYANINE',
              'PHYSOSTIGMINE',
              'PINEAPPLE',
              'PINITOL',
              'PIPERAZINE',
              'PIPERINE',
              'PISTACHIO',
              'PLATINUM',
              'PLUM',
              'POMEGRANATE',
              'PORK',
              'POTASSIUM',
              'POTATO',
              'POULTRY',
              'PROCAINE',
              'PROFLAVINE',
              'PROGESTERONE',
              'PROLINE',
              'PROTAMINE',
              'PROTHROMBIN',
              'PROTOCATECHUALDEHYDE',
              'PROTOPORPHYRIN',
              'PSEUDOEPHEDRINE',
              'PSEUDOTROPINE',
              'PUMICE',
              'PUMPKIN',
              'PURSLANE',
              'PUTRESCINE',
              'RABBIT',
              'RADISH',
              'RASPBERRY',
              'REPOSAL',
              'RESORCINOL',
              'RHAMNOSE',
              'RHEIN',
              'RHUBARB',
              'RIBOFLAVIN',
              'RIBOSE',
              'RICE',
              'ROSEMARY',
              'ROSIN',
              'ROTENONE',
              'RUBIDIUM',
              'RUTIN',
              'RYE',
              'SACCHARIN',
              'SAFFLOWER',
              'SAGE',
              'SALICYLAMIDE',
              'SALOL',
              'SAMARIUM',
              'SARCOSINE',
              'SCALLOP',
              'SCOPOLAMINE',
              'SELENIUM',
              'SENNA',
              'SERINE',
              'SHRIMP',
              'SILICON',
              'SILVER',
              'SMELT',
              'SNAIL',
              'SONATA',
              'SORBITOL',
              'SOYBEAN',
              'SPARTEINE',
              'SPEARMINT',
              'SPERMACETI',
              'SPERMIDINE',
              'SPERMINE',
              'SPHINGOSINE',
              'SPINACH',
              'SQUALENE',
              'SQUASH',
              'STRAWBERRY',
              'SUCCINIMIDE',
              'SUCROSE',
              'SWORDFISH',
              'TABLOID',
              'TAGATOSE',
              'TALC',
              'TANGERINE',
              'TANTALUM',
              'TARTRONATE',
              'TAURINE',
              'TENUATE',
              'TERPINEOL',
              'TESTOSTERONE',
              'TETRAMETHYLAMMONIUM',
              'THEOBROMINE',
              'THEOPHYLLINE',
              'THIAMINE',
              'THREONINE',
              'THROMBIN',
              'THYME',
              'THYMINE',
              'THYMOL',
              'THYROID',
              'TING',
              'TITANIUM',
              'TOCOPHEROL',
              'TOLUENE',
              'TOMATO',
              'TRAGACANTH',
              'TREHALOSE',
              'TRIBUTYRIN',
              'TRIOLEIN',
              'TROUT',
              'TRYPSIN',
              'TUBOCURARINE',
              'TUNA',
              'TURKEY',
              'TURMERIC',
              'TURNIP',
              'TURPENTINE',
              'TYRAMINE',
              'TYROSINASE',
              'TYROSINE',
              'URACIL',
              'UREA',
              'URETHANE',
              'VALERIAN',
              'VALINE',
              'VANADIUM',
              'VANILLA',
              'VEAL',
              'VENISON',
              'VERBENONE',
              'VERSED',
              'VITAMIN',
              'VORTEX',
              'WATER',
              'WATERMELON',
              'WHEAT',
              'WORMWOOD',
              'XANTHINE',
              'XENON',
              'XYLITOL',
              'XYLOSE',
              'YEAST',
              'ZINC',
              'ZINGERONE'}

# Drug names which are sufficiently generic that they may occur lower case
words_to_allow_lower_case = {'amphetamine',
                             'andrographolide',
                             'apomorphine',
                             'arbutin',
                             'arecoline',
                             'aspirin',
                             'atropine',
                             'bacitracin',
                             'barbital',
                             'benzocaine',
                             'benzofuran',
                             'benzylpenicillin',
                             'biguanide',
                             'biotin',
                             'cannabinol',
                             'cantharidin',
                             'carbromal',
                             'cathine',
                             'chloramphenicol',
                             'chloroform',
                             'chloroquine',
                             'codeine',
                             'colchicine',
                             'cortisone',
                             'emend',
                             'epinephrine',
                             'estrogen',
                             'ethylenediamine',
                             'ethylmorphine',
                             'factive',
                             'fibrinolysin',
                             'hexylresorcinol',
                             'hydroquinine',
                             'hydroquinone',
                             'lustral',
                             'methadone',
                             'methenamine',
                             'morphine',
                             'oxyquinoline',
                             'paregoric',
                             'penicillin',
                             'pentobarbital',
                             'phenobarbital',
                             'picropodophyllin',
                             'picrotoxin',
                             'pilocarpine',
                             'podophyllin',
                             'psyllium',
                             'pyrazole',
                             'pyridoxine',
                             'pyruvaldehyde',
                             'quercetin',
                             'quinacrine',
                             'quinidine',
                             'quinine',
                             'streptomycin',
                             'strychnine',
                             'sulfadiazine',
                             'sulfaguanidine',
                             'sulfamerazine',
                             'sulfamethazine',
                             'sulfamethylthiazole',
                             'sulfanilamide',
                             'sulfapyridine',
                             'sulfaquinoxaline',
                             'sulfathiazole',
                             'thymoquinone',
                             'thyroglobulin',
                             'trichloroethylene',
                             'trinitrotoluene',
                             'tryptophan',
                             'yohimbine'}

variant_regex = re.compile(r'^[A-Za-z][a-z]+(?:[ -][A-Z])?$')


def add_variant(canonical_name, variant):
    if variant not in drug_variant_to_canonical:
        drug_variant_to_canonical[variant] = set()
    drug_variant_to_canonical[variant].add(canonical_name)


def add_drug(id, synonyms):
    synonyms = [s.strip() for s in synonyms]
    if re.sub("[- ].+", "", synonyms[0].upper()) in exclusions:
        return
    if not variant_regex.match(synonyms[0]):
        return
    if synonyms[0] not in drug_canonical_to_data:
        drug_canonical_to_data[synonyms[0]] = {"name": synonyms[0], "synonyms": set()}
    if id.startswith("a"):
        drug_canonical_to_data[synonyms[0]]["medline_plus_id"] = id
    elif id.startswith("https://www.nhs.uk"):
        drug_canonical_to_data[synonyms[0]]["nhs_url"] = id
    elif id.startswith("https://en.wikipedia"):
        drug_canonical_to_data[synonyms[0]]["wikipedia_url"] = id
    elif id.startswith("DB"):
        drug_canonical_to_data[synonyms[0]]["drugbank_id"] = id
    else:
        drug_canonical_to_data[synonyms[0]]["mesh_id"] = id
    for variant in synonyms:
        if re.sub(" .+", "", variant.upper()) in exclusions:
            return
        if variant_regex.match(variant):
            drug_canonical_to_data[synonyms[0]]["synonyms"].add(variant)
            add_variant(synonyms[0], variant)
            add_variant(synonyms[0], variant.upper())
            if variant.lower() in words_to_allow_lower_case:
                add_variant(synonyms[0], variant.lower())


with open(this_path.joinpath("drugs_dictionary_medlineplus.csv"), 'r', encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    headers = None
    for row in spamreader:
        if not headers:
            headers = row
            continue
        id = row[0]
        name = row[1]
        synonyms = row[2].split("|")

        name = re.sub(
            " (Injection|Oral Inhalation|Transdermal|Ophthalmic|Topical|Vaginal Cream|Nasal Spray|Transdermal Patch|Rectal)",
            "", name)

        add_drug(id, [name] + synonyms)

with open(this_path.joinpath("drugs_dictionary_nhs.csv"), 'r', encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    headers = None
    for row in spamreader:
        if not headers:
            headers = row
            continue
        id = row[0]
        name = row[1]
        synonyms = row[2].split("|")

        add_drug(id, [name] + synonyms)


with open(this_path.joinpath("drugs_dictionary_wikipedia.csv"), 'r', encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    headers = None
    for row in spamreader:
        if not headers:
            headers = row
            continue
        id = row[0]
        name = row[1]
        synonyms = row[2].split("|")

        add_drug(id, [name] + synonyms)
        
with open(this_path.joinpath("drugs_dictionary_mesh.csv"), 'r', encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    headers = None
    for row in spamreader:
        if not headers:
            headers = row
            continue
        id = row[0]
        name = row[1]
        synonyms = row[2].split("|")
        add_drug(id, [name] + synonyms)
        
with open(this_path.joinpath("drugbank vocabulary.csv"), 'r', encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    headers = None
    for row in spamreader:
        if not headers:
            headers = row
            continue
        id = row[0]
        name = row[2]
        synonyms = row[5].split("|")
        add_drug(id, [name] + synonyms)
        


def find_drugs(tokens: list, is_ignore_case: bool = False):
    drug_matches = []
    is_exclude = set()

    # Search for 2 token sequences
    for token_idx, token in enumerate(tokens[:-1]):
        cand = token + " " + tokens[token_idx + 1]
        if is_ignore_case:
            match = drug_variant_to_canonical.get(cand.upper(), None)
        else:
            match = drug_variant_to_canonical.get(cand, None)
        if match:
            for m in match:
                drug_matches.append((drug_canonical_to_data[m], token_idx, token_idx + 1))
                is_exclude.add(token_idx)
                is_exclude.add(token_idx + 1)

    for token_idx, token in enumerate(tokens):
        if token_idx in is_exclude:
            continue
        if is_ignore_case:
            match = drug_variant_to_canonical.get(token.upper(), None)
        else:
            match = drug_variant_to_canonical.get(token, None)
        if match:
            for m in match:
                drug_matches.append((drug_canonical_to_data[m], token_idx, token_idx))

    return drug_matches
