'''
A class of different visualizers to
track the activities of the user
'''

class Visualizer:
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import json

    def __init__(self, csv_path='data/browsing_history.csv', theme='dark'):
        self.df = self.pd.read_csv(csv_path, error_bad_lines=False,parse_dates=['When'])
        self.sns.set_style(theme)
        self.plt.rcParams['figure.figsize'] = (15, 12)

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
                del data['Day of Week']
                interval = 'all time'
                if 'interval' in kwargs.keys():
                    interval = kwargs['interval']
                    defined_interval = {
                        'past day': 1,
                        'past week': 7,
                        'past two week': 14,
                        'past month': 30,
                        'past quarter': 91,
                        'past six month': 182,
                        'past year': 365,
                    }
                    if interval != 'all time':
                        end = defined_interval[interval]
                        if data.shape[0] < 2:
                            raise Exception('No available data or not enough data')
                        elif data.shape[0] < defined_interval[interval]:
                            end = data.shape[0]
                        data = data.loc[1:end]
                
                data = data.sum().sort_values() / 3600
                if 'purpose' not in kwargs.keys() and 'is_purpose' not in kwargs.keys():
                    data.plot.barh(title='Time spent on website for {}'.format(interval))
                    self.plt.axvline(data.mean(), color='red', linewidth=2)
                    self.plt.xlabel('Time spent')
                    self.plt.ylabel('Websites')
                    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                    summarization = 'Total: {} hours\nAverage: {} hours'.format(round(data.sum(), 2), round(data.mean(), 2))
                    self.plt.text(0, -.5, summarization, fontsize=14,
                        verticalalignment='top', bbox=props)
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
                        data_of_purpose = Visualizer.trim(data_of_purpose)
                        data_of_purpose.plot.barh(title='Time spent on websites for {} {}'.format(purpose, interval))
                        self.plt.axvline(data_of_purpose['Time spent'].mean(), color='red', linewidth=2)
                        self.plt.xlabel('Time spent')
                        self.plt.ylabel('Websites')
                        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                        summarization = 'Total: {} hours\nAverage: {} hours'.format(round(data_of_purpose['Time spent'].sum(), 2), round(data_of_purpose['Time spent'].mean(), 2))
                        self.plt.text(0, -.5, summarization, fontsize=14,
                            verticalalignment='top', bbox=props)

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
                        data_by_purpose = Visualizer.trim(data_by_purpose)
                        data_by_purpose.plot.pie(y='Time spent', wedgeprops = dict(width=.3), autopct='%.2f%%', title='Time spent on websites by purpose {}'.format(interval))
                        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
                        summarization = 'Total: {} hours\nAverage: {} hours'.format(round(data_by_purpose['Time spent'].sum(), 2), round(data_by_purpose['Time spent'].mean(), 2))
                        self.plt.text(0, -.5, summarization, fontsize=14,
                            verticalalignment='top', bbox=props)
                self.plt.show()
            except IOError as e:
                print(e)
            except KeyError as e:
                print(e)
            except Exception as e:
                print(e)
        else: 
            data = self.df.copy()
            del data['Day of Week']
            data = data.sum().sort_values() / 3600
            data.plot.barh(title="Time spent on websites all time")
            self.plt.axvline(data.mean(), color='red', linewidth=2)
            self.plt.xlabel('Time spent')
            self.plt.ylabel('Websites')
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            summarization = 'Total: {} hours\nAverage: {} hours'.format(round(data.sum(),1), round(data.mean(), 2))
            self.plt.text(0, -.5, summarization, fontsize=14,
                verticalalignment='top', bbox=props)
            self.plt.show()

    def by_basis(self, basis, activity):
        '''
        Plot the user's requested activity on a specific basis

        Parameters:
        ----------
        basis: the basis requested by the user
        activity: the activity to be plotted, can be a specific website or a purpose
        '''
        available_bases = {
            'daily': 'D',
            'weekly': 'W',
            'monthly': 'M',
            'quarterly': 'Q',
            'yearly': 'Y'
        }
        try:
            if basis not in available_bases.keys():
                raise Exception('Not a supported basis')
            websites = self.json.load(open('data/util_data.json', 'r'))['web store']
            websites_df = self.pd.DataFrame.from_dict(websites)
            if activity in websites_df[['title', 'purpose']]:
                raise Exception('Activity not found')
            data = self.df.copy()
            del data['Day of Week']
            data.set_index('When', inplace=True)
            if (websites_df['purpose'] == activity).any():
                activities = websites_df[websites_df['purpose'] == activity]['title'].tolist()
                data[activity] = data[activities].sum(axis=1)
            data = data[activity] / 3600 
            grouped = data.groupby(self.pd.Grouper(freq=available_bases[basis])).sum()
            grouped.plot.bar(title='Time spent on {} {}'.format(activity, basis))
            self.plt.axhline(grouped.mean(), color='red', linewidth=2)
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            summarization = 'Total: {} hours\nAverage: {} hours'.format(round(grouped.sum(), 2), round(grouped.mean(), 2))
            self.plt.text(0, -.5, summarization, fontsize=14,
                verticalalignment='top', bbox=props)
            self.plt.show()

        except Exception as e:
            print(e)

    def by_day_of_week(self, activity):
        '''
        Plot the user's requested activity on by day of week

        Parameters:
        ----------
        activity: the activity to be plotted, can be a specific website or a purpose
        '''
        try:
            websites = self.json.load(open('data/util_data.json', 'r'))['web store']
            websites_df = self.pd.DataFrame.from_dict(websites)
            if activity in websites_df[['title', 'purpose']]:
                raise Exception('Activity not found')
            data = self.df.copy()
            weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            data['Day of Week'] = self.pd.Categorical(data['Day of Week'], categories=weekdays, ordered=True)
            data = data.sort_values(by='Day of Week')  
            data.set_index('Day of Week', inplace=True)
            if (websites_df['purpose'] == activity).any():
                activities = websites_df[websites_df['purpose'] == activity]['title'].tolist()
                data[activity] = data[activities].sum(axis=1) 
            data = data[activity] / 3600
            self.plt.scatter(data.index, data)
            self.plt.title('Time spent on {} activity by day of week'.format(activity))
            self.plt.axhline(data.mean(), color='red', linewidth=2)
            self.plt.xlabel('Day of week')
            self.plt.ylabel('Time spent')
            props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
            summarization = 'Total: {} hours\nAverage: {} hours'.format(round(data.sum(), 2), round(data.mean(), 2))
            self.plt.text(0, data.min() - .2, summarization, fontsize=14,
                verticalalignment='top', bbox=props)
            self.plt.show()

        except Exception as e:
            print(e)

# testing
if __name__ == '__main__':
    v = Visualizer()
    v.by_requests()
    v.by_requests(interval='past day')
    v.by_requests(interval='yesterday')
    v.by_requests(purpose='social media')
    v.by_requests(purpose='socialize')
    v.by_requests(is_purpose=True)
    v.by_requests(interval='past day', purpose='social media')
    v.by_requests(interval='past day', is_purpose=True)
    v.by_basis('daily', 'social media')
    v.by_day_of_week('study')