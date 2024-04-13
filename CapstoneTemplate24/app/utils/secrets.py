import os

def getSecrets():
    secrets = {
        'MONGO_HOST':"mongodb+srv://admin:1234@cluster0.nmtjn5p.mongodb.net/CapstoneTemplate24?retryWrites=true&w=majority",
        'MONGO_DB_NAME':"CapstoneTemplate24",
        'GOOGLE_CLIENT_ID': "1009590438709-5i2qppbe0e9ld7lj1jb5q35kn0nrfp19.apps.googleusercontent.com",
        'GOOGLE_CLIENT_SECRET':"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",
        'GOOGLE_DISCOVERY_URL':"https://accounts.google.com/.well-known/openid-configuration",
        'MY_EMAIL_ADDRESS':""
        }
    return secrets