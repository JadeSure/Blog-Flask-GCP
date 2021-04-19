from google.cloud import datastore

datastore_client = datastore.Client()

# query = datastore_client.query(kind= 'user')
# key = datastore_client.key( 'subject','python', 'user', 's38039909')
# query.key_filter(key)
# kind1 = 'user'
# kind2 = 'subject'
#
# parent_key = datastore_client.key('user', 's38039909')
# my_query = datastore_client.query(ancestor = parent_key)
# # my_query.order = ['-timestamp']
#
# subject_set = set()
# for entity in list(my_query.fetch()):
#     if 'subject' in entity:
#         # print(entity['subject'])
#         subject_set.add(entity['subject'])
#
# # new_query = datastore_client.query(kind = list(subject_set), ancestor = parent_key)
# my_query.order = ['-timestamp']
#
#
# for entity in list(my_query.fetch()):
#     print(entity)


delete_key = datastore_client.key("message", 5731076903272448, 'user', '987654321')
datastore_client.delete(delete_key)