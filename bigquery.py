import os

from google.cloud import bigquery

PATH = os.path.join(os.getcwd(), 'chengccassgn1-ce7fd57eac11.json')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = PATH


def bigquery_check(sql_clause):
    client = bigquery.Client(project='chengccassgn1')
    query_job = client.query(sql_clause)  # Make an API request.
    print("The query data:")
    # print(query_job)

    output = ''
    temp_list = []
    for row in query_job:
    # Row values can be accessed by field name or index.
        for step, _ in enumerate(row):
            output = output + " "+str(row[step])
        temp_list.append(output)
        # print("country_code={}".format(row[1]))
        output = ''

    output = '\n'.join(temp_list)

    return output

if __name__ == '__main__':

    sql_clause_test: str = """
SELECT time_ref, sum(value) as trade_value
from DatasetAss1.gsquarterlySeptember20
group by time_ref
order by trade_value DESC
limit 10;
    """
    print(bigquery_check(sql_clause_test))

#     a =''
#     temp_list = []
#     for i in range(5):
#         for k in range(5):
#             a = str(k)+' ' + a
#
#         temp_list.append(a)
#         a  = ''
#
#     a = '\n'.join(temp_list)
#     print(a)

