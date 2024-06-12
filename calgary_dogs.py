# calgary_dogs.py
# Author: Daniel Ikponmwen
#
# A terminal-based application for computing and printing statistics based on given input.


import pandas as pd


def load_data(file_path):
    """
    Loads the dog breed data from an Excel file and sets a multi-index.
    
    Parameters:
    file_path (str): The path to the Excel file.
    
    Returns:
    pd.DataFrame: A multi-index DataFrame containing the dog breed data.
    """

    df = pd.read_excel(file_path)
    # Setting a multi-index on 'Year' and 'Month'
    df.set_index(['Year', 'Month'], inplace=True)
    return df



def get_valid_breed(df):
    """
    Prompts the user to enter a dog breed and validates it against the dataset.
    Continues prompting until a valid breed is entered.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the dog breeds data.
    
    Returns:
    str: A valid dog breed name.
    """
    while True:
        breed = input("Please enter a dog breed: ").strip().upper()
        if breed in df.Breed.values:
            return breed
        else:
            print("Dog breed not found in the data. Please try again.")



def find_years_for_breed(df, breed):
    """
    Finds all years where the selected breed was listed in the top breeds.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the dog breeds data.
    breed (str): The selected dog breed.

    Returns:
    list: A list of years.
    """
    breed_data = df[df['Breed'] == breed]
    return breed_data.index.get_level_values('Year').unique().tolist()



def total_registrations(df, breed):
    """
    Calculates the total number of registrations for the selected breed.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the dog breeds data.
    breed (str): The selected dog breed.

    Returns:
    int: The total number of registrations.
    """
    return df[df['Breed'] == breed]['Total'].sum()



# def calculate_percentages(df, breed):
    """
    Calculates the percentage of selected breed registrations out of the total for each year and for all years combined.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the dog breeds data.
    breed (str): The selected dog breed.

    Returns:
    dict: A dictionary with yearly percentages and a total percentage.
    """
    percentages = {}
    total_registrations_all_years = df['Total'].sum()
    
    for year in df['Year'].unique():
        yearly_total = df[df['Year'] == year]['Total'].sum()
        breed_yearly_total = df[(df['Breed'] == breed) & (df['Year'] == year)]['Total'].sum()
        percentages[year] = (breed_yearly_total / yearly_total) * 100
    
    breed_total = df[df['Breed'] == breed]['Total'].sum()
    percentages['total'] = (breed_total / total_registrations_all_years) * 100
    
    return percentages



def calculate_percentages(df, breed):
    """
    Calculates the percentage of selected breed registrations out of the total for each year and for all years combined.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the dog breeds data.
    breed (str): The selected dog breed.

    Returns:
    dict: A dictionary with yearly percentages and a total percentage.
    """
    percentages = {}
    total_registrations_all_years = df['Total'].sum()
    idx = pd.IndexSlice

    for year in df.index.get_level_values('Year').unique():
        # Filter DataFrame for the specified year
        yearly_data = df.loc[idx[year, :]]
        
        
        # Get total registrations for the year
        yearly_total = yearly_data['Total'].sum()
        
        # Apply mask to filter rows for the specified breed within the year
        breed_mask = yearly_data['Breed'] == breed
        
        
        # Sum the 'Total' column for the breed
        breed_yearly_total = yearly_data.loc[breed_mask, 'Total'].sum()
        
        
        # Calculate the percentage
        percentages[year] = (breed_yearly_total / yearly_total) * 100
        
    breed_total = df[df['Breed'] == breed]['Total'].sum()
    percentages['total'] = (breed_total / total_registrations_all_years) * 100
    return percentages


def find_popular_months(df, breed):
    """
    Finds the most popular months for the selected breed registrations.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the dog breeds data.
    breed (str): The selected dog breed.

    Returns:
    list: A list of most popular months.
    """
    breed_data = df[df['Breed'] == breed]
    monthly_data = breed_data.groupby('Month')['Total'].count()
    max_registrations = monthly_data.max()
    return monthly_data[monthly_data == max_registrations].index.tolist()



def main():

    # Load data with multi-index
    file_path = 'CalgaryDogBreeds.xlsx'
    df = load_data(file_path)
    
    print("ENSF 692 Dogs of Calgary")

    # Get valid breed
    breed = get_valid_breed(df)

    # Data anaylsis stage
    years = find_years_for_breed(df, breed)
    print(f"The {breed} was found in the top breeds for years: {' '.join(map(str, years))}")
    
    total_reg = total_registrations(df, breed)
    print(f"There have been {total_reg} {breed} dogs registered total.")
    
    percentages = calculate_percentages(df, breed)
    for year, pct in percentages.items():
        if year == 'total':
            print(f"The {breed} was {pct:.6f}% of top breeds across all years.")
        else:
            print(f"The {breed} was {pct:.6f}% of top breeds in {year}. ")
    
    popular_months = find_popular_months(df, breed)
    print(f"Most popular month(s) for {breed} dogs: {' '.join(popular_months)}")


if __name__ == '__main__':
    main()
