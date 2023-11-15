from flask import Flask, render_template, request, redirect, send_file
from extractors.rmt import extract_rmt_jobs
from extractors.wwr import extract_wwr_jobs
from file import save_to_file


app = Flask('JobScrapper')
app.config["TEMPLATES_AUTO_RELOAD"] = True

db = {}

@app.route("/")
def home():
  return render_template('home.html', name='hee')

@app.route('/search')
def search():
  keyword = request.args.get('keyword')
  if keyword == None :
    return redirect('/')
  if keyword in db:
    jobs = db[keyword]
  else :
    rmt = extract_rmt_jobs(keyword)
    wwr = extract_wwr_jobs(keyword)
    jobs = rmt + wwr
    db[keyword] = jobs
  c_jobs = len(jobs)  
  return render_template('search.html', keyword=keyword, jobs=jobs, c_jobs=c_jobs)

@app.route('/export')
def export():
  keyword = request.args.get('keyword')
  if keyword == None:
    return redirect('/')
  if keyword not in db :
    return redirect(f'/search?keyword={keyword}')
  save_to_file(keyword, db[keyword])
  return send_file(f'{keyword}.csv',as_attachment=True)


app.run("0.0.0.0")

