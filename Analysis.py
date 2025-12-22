import pandas as pd
import matplotlib.pyplot as plt
import os
# In analysis.py main runner, ADD:
from models import JobTracker
os.makedirs(r"C:\Users\hp\Documents\python\Jon tracker\reports", exist_ok=True)  # Auto-create reports folder

def Response_rate_per_source(df_source, typ):
    """Count rows matching status types or total if typ=None"""
    if typ:
        return df_source[df_source['status'].isin(typ)].shape[0]
    else:
        return df_source.shape[0]  # Total applications


def verify_division_by_zero(a, b):
    if b == 0: return 0
    else: return a / b

def create_empty_df(cat):
    df = pd.DataFrame(columns=[f'{cat}', 'big index', 'small index', 'pourcentage'])
    # 3. Specify and apply the desired data types using astype()
    df = df.astype({
        f'{cat}': str,
        'big index': int,
        'small index': int,
        'pourcentage': float })
    return df

def create_list():
    unique_source = ('applied', 'rejected', 'interview', 'offer')
    source_list = []
    a = ''
    while a!= 'q':
        print('Choose a statut to add to the calculation or type q to stop:')
        a= input(f''' 1 : {unique_source[0]}\n 2 : {unique_source[1]}\n 3 : {unique_source[2]}\n 4 : {unique_source[3]}
             ''')
        if a == '1': source_list.append(unique_source[0])
        if a == '2': source_list.append(unique_source[1])
        if a == '3': source_list.append(unique_source[2])
        if a == '4': source_list.append(unique_source[3])
    unique_tuple = tuple(set(source_list))
    return unique_tuple

class df_functions:
    def __init__(self, df):
        self.df = df

    def Response_rate_all_source(self, cat, typ, typ1= None):
        df = create_empty_df(cat)
        unique_source = self.df[cat].unique()
        stat = ', '.join(typ)
        for source in unique_source:
            df_source = self.df[self.df[cat] == source]
            df_with_index = Response_rate_per_source(df_source, typ)
            number_of_applications = Response_rate_per_source(df_source, typ1)
            pourcentage = verify_division_by_zero(df_with_index, number_of_applications) * 100
            # New row data as a dictionary wrapped in a list (to make it a DataFrame)
            new_row_df = pd.DataFrame([{f'{cat}': source, 'big index': number_of_applications, 'small index': df_with_index, 'pourcentage': pourcentage}])
            # Concatenate the original DataFrame and the new row DataFrame
            # df.append(new_row_df, ignore_index=True)
            df = pd.concat([df, new_row_df], ignore_index=True)
            df_sorted = df.sort_values(by='pourcentage', ascending=False).reset_index(drop=True)
        if typ1: stat1 = ', '.join(typ1)
        else: df = df.rename(columns={'big index': 'number_of_applications'})
        return df_sorted

    def best_country_to_apply(self):
        country_group = self.df.groupby('country')['id'].count()
        best_country = country_group.idxmax()
        best_count = country_group.max()
        print(f"The best country to apply is {best_country} with {best_count} applications.")
        return best_country, best_count

    def best_country_for_interviews(self, cat):
        data = self.Response_rate_all_source(f'{cat}', ('interview', 'offer'), )
        max = data['pourcentage'].idxmax()
        best_country = data.at[max, f'{cat}']
        best_count = data.at[max, 'small index']
        print(f"The best {cat} for interviews is {best_country} with {best_count} interviews.")
        return best_country, best_count

    def country_for_interviews(self, cat):
        data = self.Response_rate_all_source(f'{cat}', ('interview', 'offer'), )
        print(data[f'{cat}'])
        a = input("Choose the number of the source you want to see:")
        i = int(a)
        row = data.loc[i]
        print(f"{cat} : From {row[f'{cat}']}: {row['big index']} applications, {row['small index']} interviews => {row['pourcentage']:.2f}% interview rate.")

    def application_per_month(self):
        # ✅ BULLETPROOF - Works with ANY index type
        if isinstance(self.df.index, pd.DatetimeIndex):
            self.df['month'] = self.df.index.month_name()
        else:
            self.df['month'] = pd.to_datetime(self.df.index).month_name()

        applications_per_month = self.df.groupby('month')['id'].count()
        for month in applications_per_month.index:
            print(f"{month}: {applications_per_month[month]} applications")
        return applications_per_month

    def application_per_week(self):
        self.df['week']= self.df.index.to_period('W')
        applications_per_week = self.df.groupby('week')['id'].count()
        i = 1
        for week in applications_per_week.index:
            print(f"Week {i}: {applications_per_week[week]} applications")
            i += 1
        return applications_per_week

    def application_per_W_M(self):
        a = ''
        while a not in ['W', 'M']:
            a = input("Type W for week or M for month: ").capitalize()
        if a == 'W': self.application_per_week()
        elif a == 'M': self.application_per_month()

    def Response_rate_per_country(self):
        unique_country = self.df['country'].unique()
        for country in unique_country:
            df_country = self.df[self.df['country'] == country]
            df_without_index = df_country.loc[df_country['status'] != 'applied'].shape[0]
            number_of_applications = df_country.shape[0]
            pourcentage = (df_without_index / number_of_applications) * 100
            print(f"Country: {country} => {pourcentage:.2f}%")

    def calculate_total_days(self, df2, id_list = []):
        if id_list == []: id_list = self.df['id'].tolist()
        df1 = self.df.copy()
        df1['application_date'] = df1.index
        df1['application_date'] = pd.to_datetime(df1['application_date'])
        df1.set_index('id', inplace=True)
        df1['first_interaction'] = pd.NaT
        df1['first_interaction'] = pd.to_datetime(df1['first_interaction'])
        for app_id in df1.index:
            first_interaction = df2[df2['application_id'] == app_id]['date'].min()
            df1.loc[app_id, 'first_interaction'] = first_interaction
        df1['total_days'] = df1['first_interaction'] - df1['application_date']
        df1.drop(['notes', 'salary', 'status', 'tech_stack'], axis=1, inplace=True)
        return df1

    def calculate_average_days(self, df2, id_list = []):
        if id_list == []: id_list = self.df['id'].tolist()
        df1 = self.calculate_total_days(df2, id_list)
        T = df1['total_days'].dropna().shape[0]
        total_days = df1['total_days'].sum().days
        if T > 0:
            average_days = total_days / T
        return average_days

    def salary_per_role(self):
        grouping_key = 'Data ' + self.df['role'].str.split(' ').str[-1]
        df1 = self.df.copy()
        df1['role'] = grouping_key
        df1.set_index('role', inplace=True)
        salary = df1.groupby('role')['salary'].transform('count').to_frame()
        salary['min'] = df1.groupby('role')['salary'].transform('min')
        salary['max'] = df1.groupby('role')['salary'].transform('max')
        salary['mean'] = df1.groupby('role')['salary'].transform('mean')
        salary = salary.drop_duplicates()
        return salary

    def salary_per_source(self, cat):
        df1 = self.df.copy()
        df1.set_index(f'{cat}', inplace=True)
        salary = df1.groupby(f'{cat}')['salary'].transform('count').to_frame()
        salary['min'] = df1.groupby(f'{cat}')['salary'].transform('min')
        salary['max'] = df1.groupby(f'{cat}')['salary'].transform('max')
        salary['mean'] = df1.groupby(f'{cat}')['salary'].transform('mean')
        salary = salary.drop_duplicates()
        return salary

    def plot_conversion_funnel(self, cat='source'):
        """Plot conversion rates as bar chart"""
        data = self.Response_rate_all_source(cat, ['interview', 'offer'])
        plt.figure(figsize=(10, 6))
        plt.bar(data[cat], data['pourcentage'])
        plt.title(f'Interview/Offer Rate by {cat.capitalize()}')
        plt.ylabel('Percentage (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'reports/{cat}_conversion.png', dpi=300, bbox_inches='tight')
        plt.show()
        print(f"📊 Chart saved: reports/{cat}_conversion.png")


if __name__ == "__main__":
    tracker = JobTracker()
    df = pd.read_sql_query("SELECT * FROM applications", tracker.conn)
    df['date_applied'] = pd.to_datetime(df['date_applied'])
    df.set_index('date_applied', inplace=True)

    df2 = pd.read_sql_query("SELECT * FROM interactions", tracker.conn)
    df2['date'] = pd.to_datetime(df2['date'])

    analyzer = df_functions(df)
    print("=== 🚀 Job Tracker Analysis Dashboard 🚀 ===\n")

    print("1. 🔄 Conversion Funnel by Source:")
    funnel = analyzer.Response_rate_all_source('source', ['interview', 'offer'])
    print(funnel)

    print("\n2. 🗺️ Best Countries for Interviews:")
    analyzer.best_country_for_interviews('country')

    print("\n3. 📅 Monthly Application Trends:")
    monthly = analyzer.application_per_month()

    print("\n4. 💰 Salary Trends by Role:")
    salary_trends = analyzer.salary_per_role()
    print(salary_trends)

    print("\n5. 📈 Generating Charts...")
    analyzer.plot_conversion_funnel('source')
    analyzer.plot_conversion_funnel('country')

    print("\n✅ Analysis complete! Check 'reports/' folder for charts.")
    tracker.commit_close()
    print("🔌 Database connection closed.")















# def Response_rate_per_source(df_source, typ):
#     if typ :  pass
#     else: typ = ('applied', 'rejected', 'interview', 'offer')
#     df_with_index = 0
#     for pyt in typ:
#         df_with_index += df_source.loc[df_source['status'] == pyt].shape[0]
#     return df_with_index



# a = create_list()
# print(a)




# ty = ['rejected', 'interview', 'offer']
# df_func = df_functions(df1)
# a = df_func.Response_rate_all_source('source', ('interview', 'offer'), ('applied', ))
# print(a)

# # print(grouping_key)
# print(df2)

# print(df_func.Response_rate_all_source('source', ('interview', 'offer')))
# # df_func.best_country_for_interviews('country')
# # df_func.country_for_interviews('source')
# # df_func.best_country_for_interviews('source')
# # df_func.application_per_W_M()
# print(df_func.salary_per_role())
# print(df_func.salary_per_source('source'))
# print(df_func.salary_per_source('country'))
# print(df_func.calculate_average_days(df2))
# print(df_func.calculate_total_days(df2))
# # print(df1)
# # print(df2)

# # 4. Close the database connection
# # conn.close()
