import handler
import hashlib
import logging
import models
import urllib
import webapp2

from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

def upload_url():
  return blobstore.create_upload_url('/post')

class IndexHandler(handler.BaseHandler):
  def get(self):
    self.render_text_template('index.txt', upload_url=upload_url())

class ClientHandler(handler.BaseHandler):
  def get(self):
    import hashlib
    m = hashlib.md5()
    with open('client/client.sh') as f:
      m.update(f.read())
    self.redirect(self.url_for_document(m.hexdigest()))

class CreateUrlHandler(handler.BaseHandler):
  def get(self):
    self.response.content_type = 'text/plain'
    self.response.write(upload_url())

class UploadHandler(
    blobstore_handlers.BlobstoreUploadHandler, handler.BaseHandler):
  def post(self):
    self.response.content_type = 'text/plain'
    upload = self.get_uploads('document')[0]

    m = hashlib.md5()
    m.update(upload.open().read())
    md5sum = m.hexdigest()

    sent_md5sum = self.request.get('md5sum', None)
    if sent_md5sum and md5sum != sent_md5sum:
      self.response.write('Provided md5sum does not match uploaded file.')
      return

    document = models.Document(content=upload, md5sum=md5sum)
    document.put()
    if self.request.get('redirect', None):
      self.redirect('/%s' % md5sum)
    else:
      self.response.write('%s\n' % self.url_for_document(md5sum))

class DownloadHandler(
    blobstore_handlers.BlobstoreDownloadHandler, handler.BaseHandler):
  def get(self, blobid):
    resource = str(urllib.unquote(blobid))
    results = models.Document.all().filter('md5sum =', resource).fetch(1)
    if results:
      self.send_blob(results[0].content, content_type='text/plain')
    else:
      logging.error('Could not find document for md5sum "%s"' % resource)
      self.error(404)

app = webapp2.WSGIApplication([
  ('/', IndexHandler),
  ('/client', ClientHandler),
  ('/url', CreateUrlHandler),
  ('/post', UploadHandler),
  ('/([^/]+)', DownloadHandler),
  ])
