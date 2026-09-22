"""Post-process the Chrome tagged PDF: flatten NonStruct wrappers and set document metadata.

Usage: python pdf_postprocess.py IN.pdf [OUT.pdf]   (OUT defaults to IN; use OUT if IN is open in a viewer)

Chrome tags every <div>/<span> as NonStruct. NonStruct is structure-neutral by definition, but the
wrappers clutter the tree and some checkers flag them. This pass replaces each NonStruct element
with its own children (marked-content ids and child elements), repairs the /P parent links and
the ParentTree so every marked-content id still resolves to its structure element, then sets
/Lang, DisplayDocTitle and XMP title/description.
"""
import sys, collections
import pikepdf

TITLE = "WCAG 2.2 Success Criteria Map"
DESC = ("All 86 WCAG 2.2 success criteria by principle and guideline, with plain-language summaries "
        "and the Section 508 functional performance criteria each serves.")


def is_elem(x):
    return isinstance(x, pikepdf.Dictionary) and "/S" in x


def kids(elem):
    if "/K" not in elem:
        return []
    k = elem["/K"]
    return list(k) if isinstance(k, pikepdf.Array) else [k]


def flatten(elem, removed):
    """Return the new /K list for elem with NonStruct children replaced by their children."""
    out = []
    for k in kids(elem):
        if is_elem(k) and str(k["/S"]) == "/NonStruct":
            removed[k.objgen] = elem
            for g in flatten(k, removed):
                if is_elem(g):
                    g["/P"] = elem
                out.append(g)
        else:
            if is_elem(k):
                flatten_into(k, removed)
            out.append(k)
    return out


def flatten_into(elem, removed):
    new = flatten(elem, removed)
    elem["/K"] = pikepdf.Array(new) if len(new) != 1 else new[0]


def main(path, out=None):
    out = out or path
    pdf = pikepdf.open(path, allow_overwriting_input=True)
    root = pdf.Root
    st = root.StructTreeRoot
    removed = {}
    # top level: /K of StructTreeRoot is the Document element (or an array of them)
    for top in kids(st):
        if is_elem(top):
            flatten_into(top, removed)

    # ParentTree: mcid -> structure element. Re-point entries that referenced a removed NonStruct.
    fixed = 0
    if "/ParentTree" in st:
        nums = st.ParentTree.get("/Nums")
        if nums is not None:
            for i in range(1, len(nums), 2):
                arr = nums[i]
                if isinstance(arr, pikepdf.Array):
                    for j in range(len(arr)):
                        ref = arr[j]
                        if isinstance(ref, pikepdf.Dictionary) and ref.objgen in removed:
                            parent = removed[ref.objgen]
                            # walk up in case the parent itself was removed
                            while parent.objgen in removed:
                                parent = removed[parent.objgen]
                            arr[j] = parent
                            fixed += 1

    root.Lang = pikepdf.String("en-US")
    root.ViewerPreferences = pikepdf.Dictionary(DisplayDocTitle=True)
    with pdf.open_metadata() as m:
        m["dc:title"] = TITLE
        m["dc:language"] = ["en-US"]
        m["dc:description"] = DESC
    pdf.docinfo["/Title"] = TITLE
    pdf.save(out)

    # report
    pdf = pikepdf.open(out)
    cnt = collections.Counter()

    def walk(n):
        if isinstance(n, pikepdf.Array):
            for k in n:
                walk(k)
        elif is_elem(n):
            cnt[str(n["/S"])] += 1
            if "/K" in n:
                walk(n["/K"])

    walk(pdf.Root.StructTreeRoot.K)
    print(f"removed {len(removed)} NonStruct wrappers, re-pointed {fixed} ParentTree entries")
    print("tags:", dict(cnt.most_common()))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
