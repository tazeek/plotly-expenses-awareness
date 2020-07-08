import pandas as pd

def weeklyBankStats(file):

	# Open the CSV file
	data = pd.read_csv(file)

	# Get the week number and drop date column
	data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

	# Calculate the totals
	data['Total'] = data['Basic Savings'] + data['Current Account']

	# Find the difference in totals
	data['Difference'] = data['Total'].diff(1)

	# Fill the NaN valus
	data.fillna(0, inplace=True)

	return data

def maintenanceStats(file):

	# Open the CSV file
	data = pd.read_csv(file)

	# Sum up all common maintenance
	#data = data.groupby('name')[['cost']].sum().reset_index()

	return data

def groceryShoppingStats(file):

	# Open the CSV file
	data = pd.read_csv(file)

	# Sum up all common grocery stores
	data = data.groupby('name')[['cost']].sum().reset_index()

	# Find the percentage
	data['percentage'] = (data['cost']*100)/data['cost'].sum()
	data.percentage = data.percentage.round(2)

	# Final output: grocery shop, total spent, percentage
	data.rename(columns = {
			'cost':'total_spent',
			'name': 'grocery_shop'
		},
	inplace=True)

	return data

def weeklyStatsOutside(file):

	# Open the CSV file
	data = pd.read_csv(file)

	# Concatenate the description as: <where spent> - <how much>
	data['description'] = data['place'] + ' - ' + data['cost'].astype(str)

	# Iterate one row at a time

	# Enter week number for all dates

	# Sum up common week numbers, and keep the first start date

	# Final output (columns): week number, start date, total, description
	data.drop(columns=['place'], inplace=True)
	return data

weekly_bank_stats_df = weeklyBankStats('bank_balance.csv')
print("\n")

print (weekly_bank_stats_df)

print("\n")

grocery_stats_df = groceryShoppingStats('groceries.csv')
print(grocery_stats_df)

print("\n")

eat_out_df = weeklyStatsOutside('eat_out.csv')
print(eat_out_df)

print("\n")

maintenance_stats = maintenanceStats('maintenance.csv')
print(maintenance_stats)
