#!/usr/bin/env python3
"""Deterministically generate evidence-bound DGAF/PDMAL research figures."""
from __future__ import annotations

import argparse, hashlib, importlib.util, json, math, re, sys
from pathlib import Path
from xml.sax.saxutils import escape

MANIFEST = Path("tools/research_figures/figure_manifest.json")
STATE = Path("docs/CURRENT_STATE.md")
OUTDIR = Path("docs/research_figures/generated")
IDS = tuple(f"FIG-{i:03d}" for i in range(1, 6))
TOPOLOGIES = ("ring", "pdmal", "random_regular", "small_world", "complete")
EDGES = {"ring": 20, "pdmal": 30, "random_regular": 30, "small_world": 40, "complete": 190}
FAILURES = (0, 1, 2, 3, 4, 5, 6, 8, 10)
REF_SEED = 20270201
STYLE = """text{font-family:Arial,Helvetica,sans-serif;fill:#111}.t{font-size:26px;font-weight:700}.s{font-size:14px}.l{font-size:14px;font-weight:600}.x{font-size:12px}.z{font-size:10px}.b{fill:#fff;stroke:#111;stroke-width:1.5}.m{fill:#f5f5f5;stroke:#555}.f{fill:#fff;stroke:#111;stroke-width:4}.e{stroke:#222;stroke-width:1;fill:none}.d{stroke:#555;stroke-dasharray:5 5;fill:none}.n{fill:#fff;stroke:#111;stroke-width:1}"""


class FigureGenerationError(RuntimeError):
    pass


def _path(root: Path, rel: str | Path) -> Path:
    root, p = root.resolve(), (root / rel).resolve()
    try: p.relative_to(root)
    except ValueError as exc: raise FigureGenerationError(f"path escapes repository root: {rel}") from exc
    return p


def load_manifest(repo_root: Path):
    p = _path(repo_root, MANIFEST)
    if not p.is_file(): raise FigureGenerationError(f"manifest missing: {MANIFEST}")
    try: data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc: raise FigureGenerationError(f"invalid manifest: {exc}") from exc
    if not isinstance(data, list): raise FigureGenerationError("manifest must be a list")
    seen, specs = set(), []
    for item in data:
        need = {"id","title","priority","epistemic_class","source_bindings","output"}
        if not isinstance(item, dict) or not need <= item.keys(): raise FigureGenerationError("invalid manifest entry")
        fid, output = str(item["id"]), Path(str(item["output"]))
        if not re.fullmatch(r"FIG-\d{3}", fid) or fid in seen: raise FigureGenerationError(f"invalid/duplicate id: {fid}")
        if output.is_absolute() or ".." in output.parts or output.parts[:3] != ("docs","research_figures","generated"):
            raise FigureGenerationError(f"unsafe output path for {fid}: {output}")
        bindings = item["source_bindings"]
        if not isinstance(bindings, list) or not bindings: raise FigureGenerationError(f"{fid} has no source bindings")
        for rel in bindings: _path(repo_root, str(rel))
        seen.add(fid); specs.append(item)
    if tuple(str(x["id"]) for x in specs) != IDS: raise FigureGenerationError("first-wave manifest IDs/order changed")
    class Spec(dict):
        __getattr__ = dict.__getitem__
        @property
        def figure_id(self): return self["id"]
    return [Spec(x) for x in specs]


def parse_frontmatter(text: str) -> dict[str,str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---": raise FigureGenerationError("CURRENT_STATE frontmatter missing")
    out = {}
    for line in lines[1:]:
        if line.strip() == "---": return out
        if not line.strip(): continue
        if ":" not in line: raise FigureGenerationError(f"malformed frontmatter: {line}")
        k,v = line.split(":",1); out[k.strip()] = v.strip()
    raise FigureGenerationError("CURRENT_STATE frontmatter not closed")


def parse_transition_chain(text: str) -> list[str]:
    marker = "The current governed order is:"
    if marker not in text: raise FigureGenerationError("governed order not found")
    out, started = [], False
    for line in text.split(marker,1)[1].splitlines():
        s=line.strip(); m=re.fullmatch(r"`(.+)`",s)
        if m:
            started=True; value=m.group(1); out.append(value[2:] if value.startswith("→ ") else value)
        elif started and s: break
    if len(out)<3: raise FigureGenerationError("transition chain too short")
    return out


def _digest(root: Path, bindings) -> str:
    h=hashlib.sha256()
    for rel in bindings:
        p=_path(root,rel)
        if not p.is_file(): raise FigureGenerationError(f"source missing: {rel}")
        h.update(str(rel).encode()+b"\0"+p.read_bytes()+b"\0")
    return "sha256:"+h.hexdigest()


def load_topologies(repo_root: Path, reference_seed: int = REF_SEED):
    d=_path(repo_root,"experiments/pdmal_topology"); hp=d/"graph_harness.py"
    if not hp.is_file() or not (d/"seeds.py").is_file(): raise FigureGenerationError("topology source missing")
    old=sys.modules.pop("seeds",None); sys.path.insert(0,str(d)); name="_rf_graph_harness"
    try:
        spec=importlib.util.spec_from_file_location(name,hp); mod=importlib.util.module_from_spec(spec); sys.modules[name]=mod; spec.loader.exec_module(mod)
        graphs=mod.build_topologies(reference_seed)
    except Exception as exc: raise FigureGenerationError(f"topology import failed: {exc}") from exc
    finally:
        sys.modules.pop(name,None); sys.path.pop(0)
        if old is not None: sys.modules["seeds"]=old
        else: sys.modules.pop("seeds",None)
    if tuple(graphs)!=TOPOLOGIES: raise FigureGenerationError("topology family changed")
    for n,g in graphs.items():
        if g.number_of_nodes()!=20 or g.number_of_edges()!=EDGES[n]: raise FigureGenerationError(f"{n} invariant changed")
    if {d for _,d in graphs["pdmal"].degree()}!={3}: raise FigureGenerationError("PDMAL degree invariant changed")
    return graphs


def T(x,y,s,c="x",a="start"): return f'<text x="{x:.1f}" y="{y:.1f}" class="{c}" text-anchor="{a}">{escape(str(s))}</text>'
def R(x,y,w,h,c="b",rx=8): return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" class="{c}"/>'
def L(x1,y1,x2,y2,c="e"): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{c}"/>'
def A(x1,y1,x2,y2):
    q=math.atan2(y2-y1,x2-x1); p=[(x2+8*math.cos(q+2.58),y2+8*math.sin(q+2.58)),(x2+8*math.cos(q-2.58),y2+8*math.sin(q-2.58))]
    return L(x1,y1,x2,y2)+f'<path d="M{x2:.1f},{y2:.1f} L{p[0][0]:.1f},{p[0][1]:.1f} L{p[1][0]:.1f},{p[1][1]:.1f}Z" fill="#111"/>'
def M(x,y,lines,c="x",a="start",dy=17): return f'<text x="{x}" y="{y}" class="{c}" text-anchor="{a}">' + "".join(f'<tspan x="{x}" dy="{0 if i==0 else dy}">{escape(str(v))}</tspan>' for i,v in enumerate(lines)) + '</text>'
def H(title,sub,w): return T(w/2,38,title,"t","middle")+T(w/2,64,sub,"s","middle")
def F(w,h,d): return T(24,h-20,"Generated from canonical repository sources; visualization does not create scientific state.","z")+T(w-24,h-20,d,"z","end")
def DOC(fid,klass,d,w,h,title,body): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" data-figure-id="{fid}" data-epistemic-class="{klass}" data-source-digest="{d}">\n<title>{escape(title)}</title>\n<style>{STYLE}</style>\n{body}\n</svg>\n'

def _human(v):
    return {"NOT_ESTABLISHED":"NOT ESTABLISHED","NOT_AUTHORIZED_NOT_RUN":"NOT AUTHORIZED / NOT RUN"}.get(v,v.replace("_"," "))


def fig1(spec,state,d):
    fm=parse_frontmatter(state); w,h=1200,720; lv=fm.get("last_verified","unknown")
    b=H(spec.title,f"Research lanes are separated by evidence and authorization boundaries · Source snapshot last_verified: {lv}",w)
    b+=R(60,95,1080,90,"m")+T(90,125,"DGAF governance / evidence control plane","l")
    b+=M(90,150,[f"High-Assurance: {fm.get('candidate_status','unknown')}",f"Canonical empirical N: {fm.get('canonical_high_assurance_empirical_n','?')} · efficacy: {_human(fm.get('canonical_dgaf_efficacy','unknown'))}"])
    boxes=[(70,235,325,145,"Track A Epoch 001",["Historical exact-scope boundary","Completed blinded collection is not transferable","Primary outcome status remains source-bound"]),(438,235,325,145,"Track A Epoch 002",["Controlling successor scientific lane","Collection: COMPLETE","50 paired seed units / 2,250 blinded observations",f"Primary analysis: {_human(fm.get('track_a_successor_primary_analysis','unknown'))}"]),(805,235,325,145,"Canonical High-Assurance",["Separate candidate / freeze / authorization lane","No state inheritance from Track A",f"N={fm.get('canonical_high_assurance_empirical_n','?')}"]),(150,445,390,125,"B1 / B2 / B3",["Standalone non-empirical lanes","Engineering/formal evidence only","No empirical efficacy transfer"]),(660,445,390,125,"Track C composition",["Integrated composition proposal lane","Execution/efficacy requires its own authority","Adjacency is not evidence transfer"])]
    for x,y,bw,bh,title,lines in boxes: b+=R(x,y,bw,bh)+T(x+18,y+30,title,"l")+M(x+18,y+58,lines)
    b+=A(600,185,600,225)+L(232,220,968,220,"d")+T(600,210,"shared governance discipline; evidence remains lane-scoped","z","middle")+L(600,380,600,430,"d")+T(600,418,"non-empirical lanes do not establish Track A or High-Assurance efficacy","z","middle")+F(w,h,d)
    return DOC(spec.figure_id,spec.epistemic_class,d,w,h,spec.title,b)


def _pos(n,cx,cy,r): return {i:(cx+r*math.cos(-math.pi/2+2*math.pi*i/n),cy+r*math.sin(-math.pi/2+2*math.pi*i/n)) for i in range(n)}
def _graph(g,cx,cy,r,dense=False):
    nodes=sorted(g.nodes()); p0=_pos(len(nodes),cx,cy,r); p={n:p0[i] for i,n in enumerate(nodes)}
    seg=' '.join(f'M{p[u][0]:.1f},{p[u][1]:.1f}L{p[v][0]:.1f},{p[v][1]:.1f}' for u,v in g.edges())
    out=f'<path d="{seg}" class="e"'+(' opacity="0.22"' if dense else '')+'/>'
    return out+''.join(f'<circle cx="{p[n][0]:.1f}" cy="{p[n][1]:.1f}" r="4" class="n"/>' for n in nodes)

def fig2(spec,graphs,d):
    w,h=1200,790; b=H(spec.title,f"Canonical 20-node generators · representative stochastic topology seed {REF_SEED} · structural illustration only",w)
    panels=[("ring",220,235),("pdmal",600,235),("random_regular",980,235),("small_world",410,555),("complete",790,555)]; pretty={"ring":"Ring","pdmal":"PDMAL / dodecahedral","random_regular":"Random 3-regular","small_world":"Watts–Strogatz small-world","complete":"Complete"}
    for name,cx,cy in panels:
        g=graphs[name]; deg=sorted({v for _,v in g.degree()}); dl=str(deg[0]) if len(deg)==1 else f"{deg[0]}–{deg[-1]}"
        b+=R(cx-165,cy-140,330,270)+T(cx,cy-108,pretty[name],"l","middle")+_graph(g,cx,cy,88,name=="complete")+T(cx,cy+112,f"V={g.number_of_nodes()} · E={g.number_of_edges()} · degree={dl}","x","middle")
    return DOC(spec.figure_id,spec.epistemic_class,d,w,h,spec.title,b+F(w,h,d))


def fig3(spec,state,d):
    req=["50 prospective seeds","5 topologies","9 failure counts","2,250 raw observations"]
    if any(x.lower() not in state.lower() for x in req): raise FigureGenerationError("Epoch 002 design constants missing")
    w,h=1220,690; left,top,cw,ch=210,140,98,72; rows=["ring","PDMAL","random-regular","small-world","complete"]
    b=H(spec.title,"Design only — no hidden condition mapping or outcome values are displayed",w)+T(left-160,top-52,"Topology","l")+T(left+cw*4.5,top-52,"Failure counts","l","middle")
    for c,f in enumerate(FAILURES): b+=T(left+c*cw+cw/2,top-20,f,"l","middle")
    for r,name in enumerate(rows):
        y=top+r*ch; b+=T(left-18,y+43,name,"l","end")
        for c in range(9):
            x=left+c*cw; b+=R(x,y,cw,ch,"b",0)+T(x+cw/2,y+33,"n=50","x","middle")+T(x+cw/2,y+51,"paired seeds","z","middle")
    b+=T(w/2,545,"5 topologies × 9 failure counts = 45 blinded cells per seed","l","middle")+T(w/2,572,"45 cells/seed × 50 paired seed units = 2,250 blinded cells","l","middle")+M(w/2,610,["This figure describes the prospective/locked matrix only.","It contains no effect estimates, condition decoding, efficacy statement, or primary-analysis result."],"x","middle")+F(w,h,d)
    return DOC(spec.figure_id,spec.epistemic_class,d,w,h,spec.title,b)


def fig4(spec,state,d):
    chain=parse_transition_chain(state); fm=parse_frontmatter(state); w=1200; bh,gap,top=52,20,110; h=top+len(chain)*(bh+gap)+100
    b=H(spec.title,f"Ordered chain parsed from docs/CURRENT_STATE.md · Source snapshot last_verified: {fm.get('last_verified','unknown')}",w)
    for i,item in enumerate(chain):
        y=top+i*(bh+gap); cls="f" if "CURRENT FRONTIER" in item else ("m" if " — " not in item else "b")
        b+=R(250,y,700,bh,cls)+T(600,y+32,item,"l" if cls=="f" else "x","middle")
        if i<len(chain)-1: b+=A(600,y+bh,600,y+bh+gap-5)
    b+=T(w/2,h-48,"A diagrammed transition is not an authorization event; each predecessor remains evidence-bound.","x","middle")+F(w,h,d)
    return DOC(spec.figure_id,spec.epistemic_class,d,w,h,spec.title,b)


def fig5(spec,d):
    w,h=1320,790; b=H(spec.title,"Claim strength is bounded by identity, provenance, authorization, and analysis lineage",w)
    nodes=[(80,135,250,78,"Protocol + source code","Defines intended mechanism"),(400,135,250,78,"Exact commit / candidate","Binds implementation identity"),(720,135,250,78,"CI / predicate evidence","Supports only tested predicates"),(1040,135,220,78,"Governance decision","Can authorize bounded next step"),(1040,320,220,78,"Authorized execution","Produces scoped observations"),(720,320,250,78,"Collected artifacts","Require provenance + custody"),(400,320,250,78,"Custody / lock receipts","Bind retained data state"),(80,320,250,78,"Materialization receipt","Binds controlled readable data"),(80,505,250,78,"Analysis authorization","Separate human-controlled gate"),(400,505,250,78,"Locked analysis output","Applies preregistered method"),(720,505,250,78,"Scoped research claim","May not exceed evidence")]
    centers=[]
    for x,y,bw,bh,title,sub in nodes: b+=R(x,y,bw,bh)+T(x+bw/2,y+30,title,"l","middle")+T(x+bw/2,y+55,sub,"z","middle"); centers.append((x+bw/2,y+bh/2))
    for a,c,label in [(0,1,"bound to"),(1,2,"tested at"),(2,3,"supports decision"),(3,4,"authorizes"),(4,5,"generates"),(5,6,"bound by"),(6,7,"permits controlled"),(7,8,"precedes"),(8,9,"authorizes"),(9,10,"supports")]:
        x1,y1=centers[a]; x2,y2=centers[c]; b+=A(x1,y1,x2,y2)+T((x1+x2)/2,(y1+y2)/2-7,label,"z","middle")
    b+=R(1010,505,250,105,"m")+T(1135,535,"Non-transfer rule","l","middle")+M(1135,560,["Historical or adjacent evidence","does not silently bind a new","candidate, epoch, or claim."],"z","middle",15)+L(970,545,1010,545,"d")+F(w,h,d)
    return DOC(spec.figure_id,spec.epistemic_class,d,w,h,spec.title,b)


def render_all(repo_root: Path, output_root: Path | None = None):
    root=repo_root.resolve(); specs=load_manifest(root); statep=_path(root,STATE)
    if not statep.is_file(): raise FigureGenerationError(f"source missing: {STATE}")
    state=statep.read_text(encoding="utf-8"); output=(output_root.resolve() if output_root else _path(root,OUTDIR)); output.mkdir(parents=True,exist_ok=True); graphs=None; paths=[]
    for spec in specs:
        d=_digest(root,spec.source_bindings)
        if spec.figure_id=="FIG-001": raw=fig1(spec,state,d)
        elif spec.figure_id=="FIG-002": graphs=graphs or load_topologies(root); raw=fig2(spec,graphs,d)
        elif spec.figure_id=="FIG-003": raw=fig3(spec,state,d)
        elif spec.figure_id=="FIG-004": raw=fig4(spec,state,d)
        else: raw=fig5(spec,d)
        p=output/Path(spec.output).name; tmp=p.with_suffix(".svg.tmp"); tmp.write_text(raw,encoding="utf-8",newline="\n"); tmp.replace(p); paths.append(p)
    return paths


def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--repo-root",type=Path,default=Path.cwd()); ap.add_argument("--output-dir",type=Path)
    a=ap.parse_args(argv)
    try: paths=render_all(a.repo_root,a.output_dir)
    except FigureGenerationError as exc: print(f"ERROR: {exc}",file=sys.stderr); return 2
    for p in paths: print(p)
    return 0

if __name__=="__main__": raise SystemExit(main())
