from typing import Dict, Optional

# Synthetic retrieval dictionary
# Sources: National Institutes of Health (NIH), Mayo Clinic, Radiopaedia (public reliable sources)
KNOWLEDGE_BASE = {
    # Radiology Terms
    "consolidation": {
        "definition": "A region of normally compressible lung tissue that has filled with liquid instead of air.",
        "source": "Radiopaedia",
        "url": "https://radiopaedia.org/articles/consolidation"
    },
    "pneumothorax": {
        "definition": "The presence of air or gas in the cavity between the lungs and the chest wall, causing collapse of the lung.",
        "source": "Mayo Clinic",
        "url": "https://www.mayoclinic.org/diseases-conditions/pneumothorax/symptoms-causes/syc-20350367"
    },
    "fracture": {
        "definition": "A complete or partial break in a bone.",
        "source": "MedlinePlus (NIH)",
        "url": "https://medlineplus.gov/fractures.html"
    },
    "atelectasis": {
        "definition": "Complete or partial collapse of the entire lung or area (lobe) of the lung.",
        "source": "Mayo Clinic",
        "url": "https://www.mayoclinic.org/diseases-conditions/atelectasis/symptoms-causes/syc-20369684"
    },
    "pleural effusion": {
        "definition": "A backup of fluid in the space between the lungs and the chest wall.",
        "source": "MedlinePlus (NIH)",
        "url": "https://medlineplus.gov/pleuraldisorders.html"
    },
    
    # Lab Parameters (Ranges are general approximations for adults)
    "hemoglobin": {
        "definition": "A protein in red blood cells that carries oxygen.",
        "normal_range": "Male: 13.5-17.5 g/dL, Female: 12.0-15.5 g/dL",
        "source": "Mayo Clinic",
        "url": "https://www.mayoclinic.org/tests-procedures/hemoglobin-test/about/pac-20385075"
    },
    "wbc": {
        "definition": "White Blood Cells, part of the immune system.",
        "normal_range": "4,500 to 11,000 cells per microliter",
        "source": "MedlinePlus (NIH)",
        "url": "https://medlineplus.gov/wbc.html"
    },
    "creatinine": {
        "definition": "A waste product pumped out of the blood by the kidneys.",
        "normal_range": "Male: 0.74-1.35 mg/dL, Female: 0.59-1.04 mg/dL",
        "source": "Mayo Clinic",
        "url": "https://www.mayoclinic.org/tests-procedures/creatinine-test/about/pac-20384646"
    },
    "glucose": {
        "definition": "Blood sugar.",
        "normal_range": "70-99 mg/dL (fasting)",
        "source": "MedlinePlus (NIH)",
        "url": "https://medlineplus.gov/bloodglucose.html"
    },
    "platelets": {
        "definition": "Blood cells that help your body form clots to stop bleeding.",
        "normal_range": "150,000 to 450,000 platelets/mcL",
        "source": "Johns Hopkins Medicine",
        "url": "https://www.hopkinsmedicine.org/health/conditions-and-diseases/what-are-platelets-and-why-are-they-important"
    }
}

def map_to_citations(term: str) -> Dict[str, str]:
    """
    Look up a term in the knowledge base.
    Returns the dictionary entry if found (partial match supported), else empty dict.
    """
    term_lower = term.lower().strip()
    
    # Direct match
    if term_lower in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[term_lower]
    
    # Partial match scan
    for key, data in KNOWLEDGE_BASE.items():
        if key in term_lower or term_lower in key:
            return data
            
    return {}
