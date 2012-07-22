import logging
import webapp2
from webapp2_extras import jinja2

class BaseHandler(webapp2.RequestHandler):
  def url_for_document(self, md5sum):
    return '%s/%s' % (self.request.host_url, md5sum)

  @webapp2.cached_property
  def jinja2(self):
    return jinja2.get_jinja2(app=self.app)

  def render_text_template(self, template, **context):
    self.response.content_type = 'text/plain'
    self.response.write(self.jinja2.render_template(template, **context))

  def render_html_template(self, template, **context):
    self.response.write(self.jinja2.render_template(template, **context))
