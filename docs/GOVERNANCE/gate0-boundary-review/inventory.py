"""Read-only source inventory. Python 3.12 + PyYAML 6.0.3. Never executes workflow code."""
import hashlib,json,re,subprocess,sys
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[3]
BASE="1a95b94332dffb404c5a3ce026d70781a8c10b90"
def git(*args):
 return subprocess.check_output(["git","-C",str(ROOT),*args])
def source(path):
 return git("show",BASE+":"+path).decode("utf-8")
files=git("ls-tree","-r","--name-only",BASE).decode().splitlines()
workflows=[]; jobs=[]; errors=[]
for path in files:
 if not (path.startswith(".github/workflows/") and path.endswith((".yml",".yaml"))): continue
 raw=source(path)
 try: doc=yaml.safe_load(raw)
 except yaml.YAMLError as exc:
  errors.append({"path":path,"error":str(exc)}); continue
 workflows.append({"path":path,"sha256":hashlib.sha256(raw.encode()).hexdigest()})
 for job_id,job in (doc.get("jobs") or {}).items():
  if not isinstance(job,dict): continue
  steps=job.get("steps",[])
  uploads=[]
  for index,step in enumerate(steps):
   if not isinstance(step,dict): continue
   if "upload-artifact@" not in str(step.get("uses","")): continue
   uploads.append({"index":index,"name":step.get("name"),"uses":step["uses"],"if":step.get("if","success() [implicit]"),"with":step.get("with",{})})
  if not uploads: continue
  text=json.dumps(job)
  flags=[]
  if re.search(r"secrets\.[A-Za-z_]",text): flags.append("SECRET_REFERENCE_REVIEW")
  if any("blinding_key.txt" in str(u["with"].get("path","")) for u in uploads): flags.append("RECOVERABLE_BLINDING_KEY_CUSTODY")
  if any(re.search(r"[*]|/$",str(u["with"].get("path","")).strip()) for u in uploads): flags.append("BROAD_PATH_REVIEW")
  if any(u["if"]=="always()" for u in uploads): flags.append("FAILURE_PATH_UPLOAD_REVIEW")
  perms=job.get("permissions",doc.get("permissions"))
  if isinstance(perms,dict) and any(v=="write" for v in perms.values()): flags.append("WRITE_CAPABILITY_REVIEW")
  jobs.append({"workflow":path,"job":job_id,"triggers":doc.get("on",doc.get(True)),"job_if":job.get("if"),"environment":job.get("environment"),"effective_declared_permissions":perms,"workflow_secret_references":sorted(set(re.findall(r"secrets\.([A-Za-z_][A-Za-z_0-9]*)",raw))),"job_secret_references":sorted(set(re.findall(r"secrets\.([A-Za-z_][A-Za-z_0-9]*)",text))),"checkout":[s for s in steps if str(s.get("uses","")).startswith("actions/checkout@")],"uploads":uploads,"review_flags":flags,"disposition":"SOURCE_INVENTORIED_CONTENT_AND_RECIPIENT_ADMISSION_NOT_ESTABLISHED"})
routes=[]
for path in files:
 if path.startswith(("api/","pages/api/","app/api/")) and path.endswith((".py",".ts",".tsx",".js")):
  raw=source(path)
  routes.append({"path":path,"sha256":hashlib.sha256(raw.encode()).hexdigest(),"disposition":"SOURCE_ENTRYPOINT_DEPLOYED_REACHABILITY_NOT_ESTABLISHED"})
report={"baseline":BASE,"method":"static YAML job inventory; no workflow or route execution; flags are review signals, not vulnerability classifications","python":sys.version.split()[0],"pyyaml":yaml.__version__,"workflow_count":len(workflows),"parse_errors":errors,"upload_job_count":len(jobs),"upload_step_count":sum(len(j["uploads"]) for j in jobs),"api_file_count":len(routes),"workflows":workflows,"jobs":jobs,"api_files":routes,"limitations":["Not a complete transitive call-graph or network-egress audit.","No artifact payloads, credentials or empirical outcomes read.","No independent gate acceptance.","YAML safe_load uses YAML 1.1; on/True key normalized explicitly.","Runtime reachability, artifact ACLs and provider credential scopes remain unverified."]}
out=Path(__file__).with_name("source_inventory.json")
out.write_text(json.dumps(report,indent=2,sort_keys=True,default=str)+"\n",encoding="utf-8",newline="\n")
out.with_suffix(".json.sha256").write_text(hashlib.sha256(out.read_bytes()).hexdigest()+"  source_inventory.json\n",encoding="utf-8")
print(json.dumps({k:report[k] for k in ["baseline","workflow_count","parse_errors","upload_job_count","upload_step_count","api_file_count"]}))
print("report_sha256",hashlib.sha256(out.read_bytes()).hexdigest())
