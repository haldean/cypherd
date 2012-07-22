from google.appengine.ext import blobstore
from google.appengine.ext import db

class Document(db.Model):
  content = blobstore.BlobReferenceProperty(required=True)
  md5sum = db.StringProperty(required=True, indexed=True)
