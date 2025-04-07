import fitz
from rapidfuzz.fuzz import ratio

# === CONFIG ===
PDF_PATH = "Solid State Physics Ashcroft - OCR.pdf"
OUTPUT_PATH = "Solid State Physics Ashcroft - OCR ToC.pdf"
OFFSET = 22  # diferença entre páginas impressas e reais

# ← Defina seu dicionário de seções aqui (com páginas impressas do sumário)
sections = {
    "1": ("The Drude Theory of Metals", 1),
    "2": ("The Sommerfeld Theory of Metals", 29),
    "3": ("Failures of the Free Electron Model", 57),
    "4": ("Crystal Lattices", 63),
    "5": ("The Reciprocal Lattice", 85),
    "6": ("Determination of Crystal Structures by X-Ray Diffraction", 95),
    "7": ("Classification of Bravais Lattices and Crystal Structures", 111),
    "8": ("Electron Levels in a Periodic Potential : General Properties", 131),
    "9": ("Electrons in a Weak Periodic Potential", 151),
    "10": ("The Tight-Binding Method", 175),
    "11": ("Other Methods for Calculating Band Structure", 191),
    "12": ("The Semiclassical Model of Electron Dynamics", 213),
    "13": ("The Semiclassical Theory of Conduction in Metals", 243),
    "14": ("Measuring the Fermi Surface", 263),
    "15": ("Band Structure of Selected Metals", 283),
    "16": ("Beyond the Relaxation-Time Approximation", 313),
    "17": ("Beyond the Independent Electron Approximation", 329),
    "18": ("Surface Effects", 353),
    "19": ("Classification of Solids", 373),
    "20": ("Cohesive Energy", 395),
    "21": ("Failures of the Static Lattice Model", 415),
    "22": ("Classical Theory of the Harmonic Crystal", 421),
    "23": ("Quantum Theory of the Harmonic Crystal", 451),
    "24": ("Measuring Phonon Dispersion Relations", 469),
    "25": ("Anharmonic Effects in Crystals", 487),
    "26": ("Phonons in Metals", 511),
    "27": ("Dielectric Properties of Insulators", 533),
    "28": ("Homogeneous Semiconductors", 561),
    "29": ("Inhomogeneous Semiconductors", 589),
    "30": ("Defects in Crystals", 615),
    "31": ("Diamagnetism and Paramagnetism", 643),
    "32": ("Electron Interactions and Magnetic Structure", 671),
    "33": ("Magnetic Ordering", 693),
    "34": ("Superconductivity", 725)
}


doc = fitz.open(PDF_PATH)
toc = []

section_list = list(sections.items())

for idx, (sec_num, (title, logical_page)) in enumerate(section_list):
    start = logical_page + OFFSET
    end = (
        section_list[idx + 1][1][1] + OFFSET
        if idx + 1 < len(section_list)
        else len(doc)
    )

    # Adiciona o título principal (nível 1)
    toc.append([1, f"{sec_num}. {title}", start])

    # Pega a lista de subtópicos da primeira página da seção
    first_page = doc[start-1]
    lines = [line.strip() for line in first_page.get_text("text").split("\n") if line.strip()]
    found_title = False
    subtopics = []
    for line in lines:
        if line.lower() in title.lower() or line.isdigit():
            found_title = True
            continue
        if found_title:
            if line == "":  # pulou linha? pode ser o fim da lista
                break
            elif line.lower() in title.lower():
                continue
            if line[0].isupper():  # começa com maiúscula?
                subtopics.append(line)
    # Agora procura a localização real de cada subtítulo
    for subtopic in subtopics:
        for i in range(start, end):
            page = doc[i]
            page_lines = [l.strip() for l in page.get_text("text").split("\n") if l.strip()]
            for line in page_lines:
                if ratio(line.lower(), subtopic.lower()) >= 80:
                    toc.append([2, subtopic, i+1])
                    break
            else:
                continue
            break  # break externo se achou

doc.set_toc(toc)
doc.save(OUTPUT_PATH)

print(f"✔ PDF salvo com TOC em: {OUTPUT_PATH}")
