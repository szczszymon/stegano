from docx import Document
from docx.shared import Pt


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


def gather_text(doc):
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)

    return "\n\n".join(text), text


def embed(path):
    cover = Document(path)
    doc = Document()

    # Extraction of document data
    def_size = 12 # cover.paragraphs[0].style.font.size
    text, paragraphs = gather_text(cover)

    # Embedding Procedure
    secret = input("Provide a secret message: ")
    secret += EoS
    count = 0

    # TODO: Clear all paragraphs from doc and start writing data
    #   unchanged data should be written like before stego work
    #   changes have to be written as separate runs
    idx = 0
    x = secret[idx]
    s = CSM[x.upper()]
    txt = ""

    # Embedding Procedure
    for paragraph in paragraphs:
        p = doc.add_paragraph()
        for y in paragraph:
            if idx + 1 < len(secret):
                print(f"y1: {y}\n")
            if y.upper() in s:
                if txt != "":
                    r = p.add_run(txt)
                    r.style.font.size = Pt(def_size)
                    print(f"check: {r.style.font.size}")
                    txt = ""

                pos = s.index(y.upper())
                print(f"pos: {pos}")
                print(f"y: {y}")
                print(f"s: {s}\n")
                print(f"r: {r.style.font.size}")

                r = p.add_run(y)
                match pos:
                    case 0:
                        r.style.font.size = Pt(def_size - 1)
                    case 1:
                        r.style.font.size = Pt(def_size - 2)
                    case 2:
                        r.style.font.size = Pt(def_size - 3)
                    case 3:
                        r.style.font.size = Pt(def_size + 1)
                    case 4:
                        r.style.font.size = Pt(def_size + 2)
                    case 5:
                        r.style.font.size = Pt(def_size + 3)
                    case 6:
                        r.style.font.size = Pt(def_size + 4)

                print(f"r2: {r.style.font.size}")

                if x.lower() in group1:
                    for key in CSM.keys():
                        CSM[key] = CSM[key][1::] + CSM[key][0]  # Left Circular Shift
                else:
                    for key in CSM.keys():
                        CSM[key] = CSM[key][-1] + CSM[key][:-1:]  # Right Circular Shift

                if idx + 1 < len(secret):
                    idx += 1
                    x = secret[idx]
                    s = CSM[x.upper()]
                else:
                    break

            else:
                txt += y

        if txt != "":
            r = p.add_run(txt)
            r.style.font.size = Pt(def_size)
            txt = ""

        else:
            continue
        break


    doc.save("Stego_method3.docx")


def extract(path, def_size):
    doc = Document(path)

    # Extraction Procedure
    secret = ""
    end = False

    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            size = run.style.font.size
            if def_size != size:
                x = run.text
                if size == def_size - 1:
                    pos = 0
                elif size == def_size - 2:
                    pos = 1
                elif size == def_size -3:
                    pos = 2
                elif size == def_size + 1:
                    pos = 3
                elif size == def_size + 2:
                    pos = 4
                elif size == def_size + 3:
                    pos = 5
                elif size == def_size + 4:
                    pos = 6

                pos = "" # Decode from Font Size x CSM String Index
                for c in CSM.keys():
                    s = CSM[c]
                    if x.upper() not in s:
                        continue
                    if s.index(x.upper()) == pos:
                        secret += c
                        if c in group1:
                            for key in CSM.keys():
                                CSM[key] = CSM[key][1::] + CSM[key][0]  # Left Circular Shift
                        else:
                            for key in CSM.keys():
                                CSM[key] = CSM[key][-1] + CSM[key][:-1:]  # Right Circular Shift
                            #   verify below
                    if len(secret) >= 5:
                        if secret[-5::] == EoS:
                            end = True
                            break
                if end:
                    break
        if end:
            break

    return secret


embed("ref_m32.docx")
sec = extract("Stego_method3.docx", 12)
print(f"sec: {sec}")
