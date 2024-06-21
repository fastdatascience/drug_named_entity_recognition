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
import pathlib
import re

this_path = pathlib.Path(__file__).parent.resolve()

drug_variant_to_canonical = {}
drug_canonical_to_data = {}

exclusions = {'&', 'ABATE', 'ACACIA', 'ACETAMIDE', 'ACETATE', 'ACETOPHENONE', 'ACETYLCHOLINE', 'ACETYLENE',
              'ACRIFLAVINE', 'ACT', 'ACTINIUM', 'ADENINE', 'ADENOSINE', 'ADRENALONE', 'ADVOCATE', 'AGMATINE', 'AGON',
              'AIM', 'AIR', 'ALANINE', 'ALEC', 'ALLANTOIN', 'ALLSPICE', 'ALMOND', 'ALOE', 'ALUMINIUM', 'AMBER',
              'AMBUSH', 'AMEN', 'AMETHYST', 'AMMONIA', 'AMT', 'AMYLAMINE', 'AMYLOPECTIN', 'AMYLOSE', 'ANETHOLE',
              'ANGELICA', 'ANILINE', 'ANTIMONY', 'ANTIPYRINE', 'AP', 'APIGENIN', 'APPLE', 'APRICOT', 'ARGININE',
              'ARTICHOKE', 'AS', 'ASA', 'ASPARAGINE', 'ASPARAGUS', 'AVOCADO', 'AX', 'BA', 'BAL', 'BALANCE', 'BANANA',
              'BARIUM', 'BARLEY', 'BASIL', 'BAYER', 'BD', 'BEAM', 'BEAN', 'BEEF', 'BEESWAX', 'BEET', 'BELLADONNA',
              'BENTONITE', 'BENZIMIDAZOLE', 'BENZOIN', 'BENZOPHENONE', 'BENZYLAMINE', 'BERBERINE', 'BERGAMOT',
              'BERKELIUM', 'BETAINE', 'BEZOAR', 'BILBERRY', 'BLACKBERRY', 'BLACKFISH', 'BLUEBERRY', 'BLUEFISH', 'BORAX',
              'BORNEOL', 'BORON', 'BROCCOLI', 'BROMOFORM', 'BT', 'BU', 'BUCKWHEAT', 'BUTYLAMINE', 'CABALETTA',
              'CABBAGE', 'CADAVERINE', 'CADMIUM', 'CAFFEINE', 'CALAMUS', 'CALCIUM', 'CAMPHANE', 'CAMPHENE', 'CAMPHOR',
              'CANTALOUPE', 'CAPSAICIN', 'CAPSICUM', 'CARAWAY', 'CARBAZOLE', 'CARBONATE', 'CARDAMOM', 'CARNOSINE',
              'CAROB', 'CARROT', 'CARVACROL', 'CASEIN', 'CASHEW', 'CATFISH', 'CAULIFLOWER', 'CD', 'CELERY',
              'CELLOBIOSE', 'CELLULOSE', 'CESIUM', 'CHERRY', 'CHICKEN', 'CHLORINE', 'CHOLECYSTOKININ', 'CHOLESTEROL',
              'CHOLINE', 'CHROMIUM', 'CHRYSIN', 'CHYMOTRYPSIN', 'CINCHOPHEN', 'CINNAMALDEHYDE', 'CINNAMON', 'CIT',
              'CLAM', 'CLIPPER', 'CLOVE', 'CO', 'COBALT', 'COCAINE', 'COCARBOXYLASE', 'COCOA', 'COCONUT', 'COD',
              'CODFISH', 'COP', 'COPPER', 'CORN', 'CORTICOSTERONE', 'COTTON', 'COUMARIN', 'CP', 'CRANBERRY', 'CREATINE',
              'CREATININE', 'CREOSOTE', 'CRESOL', 'CREST', 'CROCIN', 'CROTONALDEHYDE', 'CUCUMBER', 'CUMIDINE', 'CUMIN',
              'CURCUMIN', 'CUTTLEBONE', 'CYANAMIDE', 'CYCLOHEXANOL', 'CYCLOHEXANONE', 'CYCLOPROPANE', 'CYCLOPS',
              'CYSTEINE', 'CYSTINE', 'CYTISINE', 'D', 'DAP', 'DATE', 'DC', 'DEX', 'DEXTRAN', 'DEXTROSE', 'DIAMORPHINE',
              'DIANE', 'DICHROMATE', 'DIETHYLSTILBESTROL', 'DIGITOXIN', 'DIHYDROTACHYSTEROL', 'DILL', 'DIMENSION',
              'DINITROPHENOL', 'DIOSMIN', 'DIPHENYLGUANIDINE', 'DM', 'DUCK', 'DUMP', 'DUROQUINONE', 'E5', 'ECGONINE',
              'ECHINACEA', 'ECSTASY', 'EGG', 'EGGPLANT', 'ELLA', 'ELM', 'EMETINE', 'EMODIN', 'ENDURA', 'EOSIN',
              'EPHEDRINE', 'ERGOMETRINE', 'ERGOSTEROL', 'ERGOTAMINE', 'ERYTHRITOL', 'ESCULIN', 'ESTRADIOL', 'ESTRIOL',
              'ESTROGEN', 'ESTRONE', 'ETHANOL', 'ETHANOLAMINE', 'ETHER', 'EUCALYPTOL', 'EUGENOL', 'FANG', 'FARNESOL',
              'FENCHONE', 'FENNEL', 'FIBRIN', 'FIG', 'FISETIN', 'FLAVONE', 'FLEET', 'FLOUNDER', 'FLUORESCEIN',
              'FLUORESCIN', 'FLUORIDE', 'FLUORSPAR', 'FORMALDEHYDE', 'FOXY', 'FOY', 'FRANKINCENSE', 'FRUCTOSE',
              'FUCOSE', 'FUCOXANTHIN', 'GADOLINIUM', 'GALACTOSE', 'GARLIC', 'GELATIN', 'GENISTEIN', 'GERANIOL',
              'GINGER', 'GINSENG', 'GLUCOSAMINE', 'GLUTATHIONE', 'GLYCERIN', 'GLYCINE', 'GLYCOLIDE', 'GOLD',
              'GOLDENSEAL', 'GOOSE', 'GOSSYPOL', 'GRAPE', 'GRAPEFRUIT', 'GRAPHITE', 'GUAIACOL', 'GUANIDINE', 'GUANINE',
              'GUANOSINE', 'GUVACINE', 'HADDOCK', 'HAEM', 'HARMALINE', 'HARMINE', 'HAZELNUT', 'HEATHER', 'HELIUM',
              'HEMATIN', 'HEME', 'HEMIN', 'HEMOGLOBIN', 'HENNA', 'HEPARIN', 'HERRING', 'HESPERIDIN', 'HEXESTROL',
              'HISTAMINE', 'HISTIDINE', 'HONEY', 'HYALURONIDASE', 'HYDROGEN', 'HYDROTALCITE', 'HYOSCYAMINE',
              'HYPERICIN', 'HYPOCHLORITE', 'HYPOPHOSPHITE', 'HYPOXANTHINE', 'IDES', 'IMIDAZOLE', 'INDIGO', 'INDIRUBIN',
              'INDIUM', 'INDOLE', 'INO', 'INOSITOL', 'INSPIRE', 'INULIN', 'IODIDE', 'IODINE', 'IODOBENZENE', 'IODOFORM',
              'IPECAC', 'IRON', 'ISATIN', 'ISOEUGENOL', 'ISOFLAVONE', 'ISOLEUCINE', 'ISOPENTANE', 'ISOQUERCITRIN',
              'ISOQUINOLINE', 'JM', 'KALE', 'KAOLIN', 'KAVA', 'LA', 'LAC', 'LACTASE', 'LACTOSE', 'LAMB', 'LANOLIN',
              'LANTHANUM', 'LECITHIN', 'LEEK', 'LEMON', 'LENTIL', 'LETTUCE', 'LEUCINE', 'LH', 'LICORICE', 'LINDANE',
              'LITHIUM', 'LOBELINE', 'LOBSTER', 'LUPEOL', 'LUTEIN', 'LUTEOLIN', 'LYCOPENE', 'LYE', 'LYSINE', 'LYSOZYME',
              'M', 'MACKEREL', 'MAGNESIUM', 'MALTODEXTRIN', 'MALTOSE', 'MANGANESE', 'MANGO', 'MANNITOL', 'MANNOSE',
              'MAT', 'MATE', 'MENADIONE', 'MENT', 'MENTHOL', 'MENTHONE', 'MERLIN', 'METHANE', 'METHIONINE',
              'METHYLAMINE', 'METRIC', 'MILK', 'MOLYBDATE', 'MOLYBDENUM', 'MONITOR', 'MONO', 'MORPHOLINE', 'MUSE',
              'MUSHROOM', 'MUSKMELON', 'MYRICETIN', 'MYRRH', 'NAA', 'NARINGENIN', 'NECTARINE', 'NEODYMIUM', 'NEON',
              'NIACIN', 'NICOTINAMIDE', 'NICOTINE', 'NIKETHAMIDE', 'NIOBIUM', 'NITRATE', 'NITRITE', 'NITROGEN',
              'NITROGLYCERIN', 'NITROPRUSSIDE', 'NIX', 'NO', 'NOCTURNE', 'NORLEUCINE', 'NUTMEG', 'OAT', 'OE', 'OKRA',
              'OLEANDRIN', 'OLIVE', 'ONION', 'OPIUM', 'ORANGE', 'ORNITHINE', 'ORRIS', 'OTHER', 'OUABAIN', 'OXYGEN',
              'OXYTOCIN', 'OYSTER', 'OZONE', 'PAH', 'PAPAIN', 'PAPAVERINE', 'PAPAYA', 'PAPRIKA', 'PARALDEHYDE',
              'PARSLEY', 'PARSNIP', 'PAT', 'PATROL', 'PC', 'PEA', 'PEACH', 'PEANUT', 'PEAR', 'PEARL', 'PECAN', 'PECTIN',
              'PEG', 'PENTAERYTHRITOL', 'PEPPERMINT', 'PEPSIN', 'PERCH', 'PERCHLORATE', 'PETROLATUM', 'PG',
              'PHENACETIN', 'PHENOL', 'PHENOLPHTHALEIN', 'PHENOTHIAZINE', 'PHENYLACETALDEHYDE', 'PHENYLALANINE',
              'PHOSPHOCREATINE', 'PHOSPHORUS', 'PHTHALOCYANINE', 'PHYSOSTIGMINE', 'PINEAPPLE', 'PINITOL', 'PIPERAZINE',
              'PIPERINE', 'PISTACHIO', 'PLATINUM', 'PLUM', 'POMEGRANATE', 'PORK', 'POTASSIUM', 'POTATO', 'POULTRY',
              'PRECONCEIVE', 'PREDATE', 'PREP', 'PRIMUS', 'PROCAINE', 'PROFLAVINE', 'PROGESTERONE', 'PROLATE',
              'PROLINE', 'PROTAMINE', 'PROTHROMBIN', 'PROTOCATECHUALDEHYDE', 'PROTOPORPHYRIN', 'PS', 'PSEUDOEPHEDRINE',
              'PSEUDOTROPINE', 'PUMICE', 'PUMPKIN', 'PURSLANE', 'PUTRESCINE', 'PV', 'Q', 'QUAHOG', 'RABBIT', 'RADISH',
              'RAS', 'RASPBERRY', 'RECAP', 'RECEDE', 'REDUX', 'REPOSAL', 'RESORCINOL', 'RHAMNOSE', 'RHEIN', 'RHUBARB',
              'RIBOFLAVIN', 'RIBOSE', 'RICE', 'RID', 'ROSEMARY', 'ROSIN', 'ROTENONE', 'ROUNDUP', 'RUBIDIUM', 'RUTIN',
              'RYE', 'SA', 'SACCHARIN', 'SAFFLOWER', 'SAGE', 'SALICYLAMIDE', 'SALMON', 'SALOL', 'SAM', 'SAMARIUM',
              'SAME', 'SARCOSINE', 'SCALLOP', 'SCOPOLAMINE', 'SELENIUM', 'SENNA', 'SEQUEL', 'SERENADE', 'SERINE',
              'SHRIMP', 'SILICON', 'SILVER', 'SK', 'SKULLCAP', 'SMELT', 'SNAIL', 'SOMA', 'SONATA', 'SORBITOL',
              'SORGHUM', 'SOYBEAN', 'SPARTEINE', 'SPEARMINT', 'SPERMACETI', 'SPERMIDINE', 'SPERMINE', 'SPHINGOSINE',
              'SPINACH', 'SQUALENE', 'SQUASH', 'STRAWBERRY', 'SUCCINIMIDE', 'SUCROSE', 'SWORDFISH', 'T', 'T3', 'T4',
              'TABLOID', 'TAGATOSE', 'TALC', 'TANGERINE', 'TANTALUM', 'TANTUM', 'TAO', 'TARTRONATE', 'TAURINE',
              'TENUATE', 'TERPINEOL', 'TESTOSTERONE', 'TETRAMETHYLAMMONIUM', 'TG', 'THEOBROMINE', 'THEOPHYLLINE',
              'THIAMINE', 'THREONINE', 'THROMBIN', 'THYME', 'THYMINE', 'THYMOL', 'THYROID', 'TIMOTHY', 'TING', 'TIRADE',
              'TITANIUM', 'TOBACCO', 'TOCOPHEROL', 'TOLUENE', 'TOMATO', 'TRAGACANTH', 'TREHALOSE', 'TRIBUTYRIN',
              'TRIOLEIN', 'TROUT', 'TRP', 'TRYPSIN', 'TUBOCURARINE', 'TUNA', 'TURKEY', 'TURMERIC', 'TURNIP',
              'TURPENTINE', 'TYRAMINE', 'TYROSINASE', 'TYROSINE', 'URACIL', 'UREA', 'URETHANE', 'VA', 'VALERIAN',
              'VALINE', 'VANADIUM', 'VANILLA', 'VANQUISH', 'VEAL', 'VENISON', 'VERBENONE', 'VERSED', 'VINEGAR', 'VIP',
              'VITAMIN', 'VORTEX', 'W', 'WASABI', 'WATER', 'WATERMELON', 'WHEAT', 'WHEY', 'WHITEFISH', 'WIND',
              'WORMWOOD', 'XANTHINE', 'XENON', 'XYLITOL', 'XYLOSE', 'YAZYEAST', 'YEAST', 'YOHIMBINE', 'ZINC',
              'ZINGERONE', 'ZONAL'}

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


def add_variant(canonical_name, variant):
    if variant not in drug_variant_to_canonical:
        drug_variant_to_canonical[variant] = set()
    drug_variant_to_canonical[variant].add(canonical_name)


def add_drug(id, generic_names: list, synonyms: list):
    synonyms = [s.strip() for s in synonyms]

    for synonym_idx, synonym in enumerate(list(synonyms)):
        if synonym in drug_canonical_to_data:
            if synonym_idx > 0:
                synonyms = [synonym] + synonyms
            break

    if re.sub("[- ].+", "", synonyms[0].upper()) in exclusions:
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
    if "generic_names" not in drug_canonical_to_data[synonyms[0]]:
        drug_canonical_to_data[synonyms[0]]["generic_names"] = generic_names
    else:
        drug_canonical_to_data[synonyms[0]]["generic_names"] = list(
            set(drug_canonical_to_data[synonyms[0]]["generic_names"] + generic_names))
    for variant in set(generic_names + synonyms):
        if re.sub(" .+", "", variant.upper()) in exclusions:
            return
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

        add_drug(id, [name], [name] + synonyms)

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

        add_drug(id, [], [name] + synonyms)

with open(this_path.joinpath("drugs_dictionary_mesh.csv"), 'r', encoding="utf-8") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    headers = None
    for row in spamreader:
        if not headers:
            headers = row
            continue
        id = row[0]
        generic_names = row[1].split("|")
        name = row[2]
        synonyms = row[3].split("|")
        add_drug(id, generic_names, [name] + synonyms)

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
        add_drug(id, [name], [name] + synonyms)

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

        uc_name = name.upper()

        if uc_name in drug_variant_to_canonical and len(drug_variant_to_canonical[uc_name]) == 1 and \
                list(drug_variant_to_canonical[uc_name])[0].upper() != uc_name:
            synonyms = [name] + synonyms
            name = list(drug_variant_to_canonical[uc_name])[0]

        add_drug(id, [], [name] + synonyms)

for v in drug_canonical_to_data.values():
    v["synonyms"] = list(v["synonyms"])

# Make sure we don't have multiple mappings.
for variant, candidate_canonicals in drug_variant_to_canonical.items():
    if len(candidate_canonicals) > 1:
        combined_canonical = {}
        ranked_canonicals = sorted(candidate_canonicals, key=lambda candidate: len(drug_canonical_to_data[candidate]),
                                   reverse=True)
        best_canonical = ranked_canonicals[0]
        combined_canonical_data = drug_canonical_to_data[best_canonical]

        for other_canonical in ranked_canonicals[1:]:
            other_canonical_data = drug_canonical_to_data[other_canonical]
            if other_canonical_data["name"] == combined_canonical_data["name"].lower():
                combined_canonical_data["name"] = other_canonical_data["name"]

            combined_canonical_data['synonyms'].extend(other_canonical_data['synonyms'])

            combined_canonical_data['generic_names'].extend(other_canonical_data['generic_names'])

            if combined_canonical_data.get('nhs_url') is None and other_canonical_data.get('nhs_url') is not None:
                combined_canonical_data['nhs_url'] = other_canonical_data['nhs_url']

        drug_variant_to_canonical[variant] = [best_canonical]
        drug_canonical_to_data[best_canonical] = combined_canonical_data


def find_drugs(tokens: list, is_ignore_case: bool = True):
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
