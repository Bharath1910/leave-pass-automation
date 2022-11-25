import firebase_admin, datetime
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('./firebase-adminsdk.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

docRef = db.collection(u'declined').document(u'22BEC7194')
docRef.set({
    u'regNo': u'22BEC7194',
    u'fromDate': datetime.datetime(2020, 5, 1),
    u'toDate': datetime.datetime(2022, 5, 1),
    u'reason': u'Festival',
    u'mentorRegNo': u'22ABC1234'
})

users_ref = db.collection(u'pending')
docs = users_ref.stream()

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')

