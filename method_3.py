from docx import Document


# Define the Character-String Mapping (CSM)
CSM = {
    'A': 'WRZFOIN', 'B': 'F CWQXP', 'C': 'JMFXY Z', 'D': 'XA.MNTU',
    'E': 'YCHIJOS', 'F': 'KUX ZJC', 'G': ' .BCPQX', 'H': 'BLOSWMI',
    'I': 'PJGALHO', 'J': 'NSVOBGH', 'K': 'UWY.TSL', 'L': 'DIREFCQ',
    'M': 'GHTR.WB', 'N': 'ZBADEFG', 'O': 'MNSLAB.', 'P': 'TVIZM.A',
    'Q': 'SGKPHEM', 'R': 'HEUVIYJ', 'S': 'IYLNUAK', 'T': 'OFJGCDE',
    'U': 'VDEHKLY', 'V': 'LONQSUR', 'W': 'QP KXRV', 'X': 'EZDYGPT',
    'Y': '.KQUVZ ', 'Z': 'AXMTRVD', ' ': 'RTWBDNF', '.': 'CQPJ KW'
}

# Group definitions
group1 = {' ', 'a', 's', 'n', 'r', 'u', 'm', 'f', 'b', 'c', 'v', 'z', 'x', 'q'}
group2 = {'e', 't', 'o', 'i', 'h', 'd', 'l', 'w', 'g', 'y', '.', 'k', 'p', 'j'}
EoS = ". . ."

# TODO: Declare Font Size Change Value By Pos in CSM String

def gather_text(doc):
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)

    return "\n\n".join(text)


def embed(path):
    doc = Document(path)

    # Extraction of document data
    def_size = doc.paragraphs[0].style.font.size
    full_text = gather_text(doc)

    # Embedding Procedure
    secret = input("Provide a secret message: ")
    secret += EoS
    count = 0

    # TODO: Clear all paragraphs from doc and start writing data
    #   unchanged data should be written like before stego work
    #   changes have to be written as separate runs

    for x in secret:
        s = CSM[x.upper()]
        while True:
            y = full_text[count]
            count += 1
            if y in s:
                pos = s.index(y)
                # TODO: hange Font Size of Y here, write as a seperate run
                break
        if x in group1:
            # TODO: Left Circular Shift on all the Strings in CSM
        else:
            # TODO: Same as above but Right

    # TODO: Export as a new doc


def extract(path, def_size):
    doc = Document(path)

    # Extraction Procedure
    secret = ""
    end = False

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if def_size != run.style.font.size:
                x = run.text
                pos = "" # Decode from Font Size x CSM String Index
                for c, s in CSM:
                    if s.index(x) == pos:
                        secret += c
                        if c in group1:
                            # TODO: Left Circular Shift on all strings in CSM
                        else:
                            # TODO: same as above, but right
                            #   verify below
                    if len(secret) >= 5:
                        if secret[-5::] == EoS:
                            end = True
                            break
                if end:
                    break
        if end:
            break

    # TODO: verify
    return secret

