class DevelopmentConfig(object):
    DATABASE_URI = "postgresql://hmaryam:thinkful@localhost:5432/blogful-test"
    DEBUG = True
    UPLOAD_FOLDER = "uploads"

class TestingConfig(object):
    DATABASE_URI = "postgresql://hmaryam:thinkful@localhost:5432/blogful-test"
    DEBUG = True
    UPLOAD_FOLDER = "test-uploads"
