'''
A class of different visualizers to
track the activities of the user
'''

class Visualize:
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import json

    def __init__(self, csv_path='data/browsing_history.csv', theme='dark'):
        self.df = self.pd.read_csv(csv_path, error_bad_lines=False,parse_dates=['When'])
        self.sns.set_style(theme)

    def change_theme(self, new_theme):
        self.sns.set_style(new_theme)

    @staticmethod
    def trim(df):
        '''
        Trim a dataframe to erase any rows with all 0 entries
        '''
        df = df.loc[(df != 0).any(1)]
        return df

    def by_requests(self, **kwargs):
        '''
        Plot the activities of the user based on the requests

        Parameters
        ----------
        **kwargs: all requests to the user's activities
        '''
        available_keys = ('interval', 'is_purpose', 'purpose')
        available_queries = {
            # 'basis': ('daily', 'weekly', 'monthly', 'yearly'),
            'interval': ('past day', 'past week', 'past two weeks', 'past month', 'past quarter',
                'past six month', 'past year', 'all time'),
            'purpose': ('work', 'entertainment', 'study', 'shopping', 'search', 'social media'),
            'is_purpose': (True, False)
        }
        if kwargs:
            try:
                if kwargs.keys() >= {'is_purpose', 'purpose'}:
                    raise Exception('Bad query: cannot request data for with both "is_purpose" and "purpose"')
                for k,v in kwargs.items():
                    if v not in available_queries[k]:
                        raise Exception('Bad input: {} is not a valid value for "{}"'.format(v, k))             
                data = self.df.copy()
                interval = 'all time'
                if 'interval' in kwargs.keys():
                    interval = kwargs['interval']
                    defined_interval = {
                        'past day': 1,
                        'past week': 8,
                        'past two week': 15,
                        'past month': 31,
                        'past quarter': 92,
                        'past six month': 183,
                        'past year': 366,
                    }
                    if interval != 'all time':
                        end = defined_interval[interval]
                        if data.shape[0] < 2:
                            raise Exception('No available data or not enough data')
                        elif data.shape[0] < defined_interval[interval]:
                            end = data.shape[0]
                        data = data.loc[:end]
                
                data = data.sum().sort_values()
                if 'purpose' not in kwargs.keys() and 'is_purpose' not in kwargs.keys():
                    data.plot.barh(title='Time spent on website for {}'.format(interval))
                else:
                    if 'purpose' in kwargs.keys():
                        purpose = kwargs['purpose']
                        data_of_purpose = {}
                        websites = self.json.load(open('data/util_data.json', 'r'))['web store']
                        for website in websites:
                            if website['purpose'] == purpose:
                                title = website['title']
                                data_of_purpose[title] = [data.loc[title]]
                        data_of_purpose = self.pd.DataFrame.from_dict(data_of_purpose).transpose()
                        data_of_purpose.rename(columns={0: 'Time spent'}, inplace=True)
                        data_of_purpose = data_of_purpose.sort_values(by='Time spent')
                        data_of_purpose = Visualize.trim(data_of_purpose)
                        data_of_purpose.plot.barh(title='Time spent on websites for {} {}'.format(purpose, interval))

                    if 'is_purpose' in kwargs.keys():
                        websites = self.json.load(open('data/util_data.json', 'r'))['web store']
                        data_by_purpose = {}
                        for website in websites:
                            purpose = website['purpose']
                            title = website['title']
                            if purpose not in data_by_purpose.keys():
                                data_by_purpose[purpose] = [0]
                            data_by_purpose[purpose][0] += data.loc[title]
                        data_by_purpose = self.pd.DataFrame.from_dict(data_by_purpose).transpose()
                        data_by_purpose.rename(columns={0: 'Time spent'}, inplace=True)
                        data_by_purpose = Visualize.trim(data_by_purpose)
                        data_by_purpose.plot.pie(y='Time spent', autopct='%.2f%%', title='Time spent on websites by purpose {}'.format(interval))
            except IOError as e:
                print(e)
            except KeyError as e:
                print(e)
            except Exception as e:
                print(e)
        else: 
            self.df.sum().sort_values().plot.barh(title="Time spent on websites all time")
        self.plt.show()

    def by_basis(self, basis, activity):
        '''
        Plot the user's requested activity on a specific basis

        Parameters:
        ----------
        basis: the basis requested by the user
        activity: the activity to be plotted, can be a specific website or a purpose
        '''
        available_basis = {
            'daily': 'D',
            'weekly': 'W',
            'monthly': 'M',
            'quarterly': 'Q',
            'yearly': 'Y'
        }
        if basis not in available_basis.keys():
            raise Exception('Not supported basis')
        websites = self.json.load(open('data/util_data.json', 'r'))['web store']
        websites_df = self.pd.DataFrame.from_dict(websites)
        if activity in websites_df[['title', 'purpose']]:
            raise Exception('Activity not found')
        if (websites_df['purpose'] == activity).any():
            activities = websites_df[websites_df['purpose'] == activity]['title'].tolist()
            data = self.df.copy()
            data.set_index('When', inplace=True)
            data[activity] = data[activities].sum(axis=1)
        data = data[activity].copy()  
        grouped = data.groupby(self.pd.Grouper(freq=available_basis[basis]))
        grouped.sum().plot.bar(title='Time spent on {} {}'.format(activity, basis))
        self.plt.show()

# testing
if __name__ == '__main__':
    v = Visualize()
    v.by_requests()
    v.by_requests(interval='past day')
    v.by_requests(interval='yesterday')
    v.by_requests(purpose='social media')
    v.by_requests(purpose='socialize')
    v.by_requests(is_purpose=True)
    v.by_requests(interval='past day', purpose='social media')
    v.by_requests(interval='past day', is_purpose=True)
    v.by_basis('daily', 'social media')
    v.by_basis('monthly', 'facebook')
    v.by_basis('yearly', 'youtube')