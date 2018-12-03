import pandas as pd


def construct_library(path):
    my_df = pd.read_csv(path)
    my_df.columns = ['datetime', 'name', "url", 'description', 'notes', 'category', 'gender', 'race_ethnicity', 'age',
                     'marital_status', 'employment', 'sexual_orient', 'beliefs', 'criminality', 'citizenship', 'time_period', 'new']
    list_of_records = my_df.to_dict(orient='records')

    headers_to_cleanse = ['category', 'gender', 'race_ethnicity', 'age', 'marital_status', 'employment',
                          'sexual_orient', 'beliefs', 'criminality', 'citizenship', 'time_period']

    library = {
        'Food': {'display': False, 'data': []},
        'Education': {'display': False, 'data': []},
        'Health': {'display': False, 'data': []},
        'Housing': {'display': False, 'data': []},
        'Other': {'display': False, 'data': []}
    }
    master_categories = ['Food', 'Education', 'Health', 'Housing']

    for d in list_of_records:
        # remove extra key(s)
        d.pop('datetime')

        # split lists
        for k, v in d.items():
            if k in headers_to_cleanse and ',' in str(v):
                d[k] = v.split(', ')

        # add display flag
        d['display'] = True

        # add review flag
        d['review'] = False

        # edit replacement flag
        if d['new'] == 'new':
            d['new'] = True
        else:
            d['new'] = False

        # bin resources
        my_cat = d['category']
        if type(my_cat) is not list:
            my_cat = [my_cat]

        # handle time_period
        if d['time_period'] not in ['long_term', 'short_term']:
            d['time_period'] = 'either'

        for i in range(len(my_cat)):
            temp = []
            if 'Food' in my_cat[i]:
                temp = library['Food']['data']
                temp.append(d)
                library['Food']['data'] = temp

            if 'Education' in my_cat[i]:
                temp = library['Education']['data']
                temp.append(d)
                library['Education']['data'] = temp

            if 'Health' in my_cat[i]:
                temp = library['Health']['data']
                temp.append(d)
                library['Health']['data'] = temp

            if 'Housing' in my_cat[i]:
                temp = library['Housing']['data']
                temp.append(d)
                library['Housing']['data'] = temp

            if my_cat[i] not in master_categories:
                temp = library['Other']['data']
                temp.append(d)
                library['Other']['data'] = temp

    return library


if __name__ == '__main__':
    print(construct_library())
