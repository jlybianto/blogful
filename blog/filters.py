from blog import app

@app.template_filter()
# Jinja does not include date formatting by default
def dateformat(date, format):
  if not date:
    return None
  return date.strftime(format)