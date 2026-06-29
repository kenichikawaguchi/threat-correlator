"""
metadata_extractor.py
Simple metadata extractor for Threat Correlator.
"""

import re

KNOWN_VENDORS = {
    "Microsoft","Oracle","Cisco","Google","Apache","Mozilla","VMware",
    "Fortinet","WordPress","Fortra","Ricoh","KONICA MINOLTA","Canon",
    "HP","Zyxel","Sonatype","Datadog","GPAC","OpenSIPS","Bludit",
    "OpenCPN","GStreamer"
}

PRODUCT_VENDOR_MAP = {
    "Firefox":"Mozilla",
    "Firefox ESR":"Mozilla",
    "Thunderbird":"Mozilla",
    "NSS":"Mozilla",
    "Android":"Google",
}

def _base(v=None,p=None,c=0,m=None):
    return {
        "vendor":v,"product":p,
        "version_start":None,"version_start_inclusive":None,
        "version_end":None,"version_end_inclusive":None,
        "confidence":c,"method":m
    }

def extract_version(desc,res):
    pats=[
        (r"before\s+v?([\d.]+)",False),
        (r"prior to\s+v?([\d.]+)",False),
        (r"<=\s*v?([\d.]+)",True),
        (r"<\s*v?([\d.]+)",False),
        (r"through\s+v?([\d.]+)",True),
        (r"up to\s+v?([\d.]+)",True),
    ]
    for pat,inc in pats:
        m=re.search(pat,desc,re.I)
        if m:
            res["version_end"]=m.group(1)
            res["version_end_inclusive"]=inc
            break
    return res

def _extract_github_style(desc):
    for p in [
        r"^([A-Za-z0-9_.-]+)\s+([A-Z][A-Za-z0-9 ._\-/]+?)\s+(before|through|prior|contains|allows|is|has)",
        r"^([A-Za-z0-9_.-]+)\s+([a-z][A-Za-z0-9._-]+)\s+(before|through|prior|contains|allows|is|has)"
    ]:
        m=re.search(p,desc)
        if m:return _base(m.group(1),m.group(2).strip(),0.97,"github_style")
    return None

def _extract_wordpress(desc):
    m=re.search(r"(Subscriber|Contributor|Customer|Author|Editor|Administrator|Authenticated|Unauthenticated).*?\bin\s+(.+?)\s*(?:<=|<|versions?|version|before|prior|through)",desc,re.I)
    return _base("WordPress",m.group(2).strip(),0.99,"wordpress") if m else None

def _extract_cisa_style(desc):
    for p in [
        r"A vulnerability has been found in\s+(.+?)\s+(before|through|allow|contains|is)",
        r"A vulnerability was identified in\s+(.+?)\s+(before|through|allow|contains|is)",
        r"A weakness has been identified in\s+(.+?)\s+(before|through|allow|contains|is)",
        r"A security flaw has been discovered in\s+(.+?)\s+(before|through|allow|contains|is)",
    ]:
        m=re.search(p,desc,re.I)
        if m:return _base(None,m.group(1).strip(),0.85,"cisa_style")
    return None

def _extract_mozilla(desc):
    for p,v in PRODUCT_VENDOR_MAP.items():
        if v=="Mozilla" and p.lower() in desc.lower():
            return _base("Mozilla",p,1.0,"mozilla")
    return None

def _extract_android(desc):
    if not desc.startswith("In "): return None
    comps=["PackageInstaller","Telecomm","Contacts Provider","Contacts","System","Framework","Bluetooth","Media","Kernel"]
    for c in comps:
        if c.lower() in desc.lower():
            return _base("Google",f"Android ({c})",0.95,"android")
    if "android" in desc.lower():
        return _base("Google","Android",0.9,"android")
    return None

def _extract_vendor_dict(desc):
    for vendor in sorted(KNOWN_VENDORS,key=len,reverse=True):
        if vendor in desc:
            m=re.search(rf"{re.escape(vendor)}\s+([A-Za-z0-9.+_\-/ ]{{2,80}})",desc)
            prod=None
            if m:
                prod=re.split(r"\b(contains|allows?|before|prior|through|versions?|version|is|are|has|have|with|that|which|and)\b",m.group(1),1,re.I)[0]
                prod=re.sub(r"\bv?(\d+\.\d+.*)$","",prod,re.I).strip(" ,.-")
            return _base(vendor,prod or None,0.95,"vendor_dict")
    for prod,vendor in PRODUCT_VENDOR_MAP.items():
        if prod.lower() in desc.lower():
            return _base(vendor,prod,0.95,"product_map")
    return None

def _extract_general_regex(desc):
    pats=[
        r"([A-Z][A-Za-z0-9.+_-]+(?:\s+[A-Z][A-Za-z0-9.+_-]+){0,3})\s+v\d",
        r"([A-Z][A-Za-z0-9.+_-]+(?:\s+[A-Z][A-Za-z0-9.+_-]+){0,3})\s+versions?",
        r"([A-Z][A-Za-z0-9.+_-]+(?:\s+[A-Z][A-Za-z0-9.+_-]+){0,3})\s+before",
        r"in\s+([A-Z][A-Za-z0-9.+_\-/ ]+?)\s*(<=|<|versions?|version|prior|before)",
    ]
    for p in pats:
        m=re.search(p,desc)
        if m:return _base(None,m.group(1).strip(),0.7,"regex")
    return None

def extract_metadata_from_desc(description:str)->dict:
    if not description:
        return _base()
    for fn in (
        _extract_github_style,
        _extract_wordpress,
        _extract_cisa_style,
        _extract_mozilla,
        _extract_android,
        _extract_vendor_dict,
        _extract_general_regex,
    ):
        r=fn(description)
        if r:
            return extract_version(description,r)
    return _base()
